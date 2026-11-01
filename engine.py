"""Independent match scheduling and standings logic for Padel Samlet."""
from collections import defaultdict
from itertools import combinations
import random


def team_key(players):
    return tuple(sorted(players))


def group_matchups(four):
    a, b, c, d = four
    return [((a, c), (b, d)), ((a, d), (b, c)), ((a, b), (c, d))]


def make_round(players, mode, previous, seed=None):
    """Return list of match dictionaries and byes, favouring new partners.

    For Mexicano input players are already ordered by standings. Groups of four
    are adjacent. In each group 1+3 vs 2+4 is the first choice.
    """
    rng = random.Random(seed)
    if len(players) < 4:
        raise ValueError('Mindst fire spillere kræves')
    seen_pairs = defaultdict(int)
    seen_opponents = defaultdict(int)
    for match in previous:
        a, b = match['blue'], match['red']
        for side in (a,b):
            seen_pairs[team_key(side)] += 1
        for x in a:
            for y in b:
                seen_opponents[team_key((x,y))] += 1

    n_courts = len(players)//4
    if mode == 'Mexicano':
        groups = [players[i*4:i*4+4] for i in range(n_courts)]
        byes = players[n_courts*4:]
    else:
        # Randomized search for groups/lineups that minimize repeat partners/opponents.
        best = None
        for _ in range(400):
            pool = list(players)
            rng.shuffle(pool)
            candidates = [pool[i*4:i*4+4] for i in range(n_courts)]
            trial = []
            score = 0
            for group in candidates:
                variants = group_matchups(group)
                choice = min(variants, key=lambda x: (
                    7*sum(seen_pairs[team_key(t)] for t in x) +
                    sum(seen_opponents[team_key((a,b))] for a in x[0] for b in x[1]),
                    rng.random()))
                score += 7*sum(seen_pairs[team_key(t)] for t in choice)
                score += sum(seen_opponents[team_key((a,b))] for a in choice[0] for b in choice[1])
                trial.append(choice)
            if best is None or score < best[0]:
                best = (score, trial, pool[n_courts*4:])
                if score == 0:
                    break
        return [{'court':i+1,'blue':list(a),'red':list(b),'blue_score':None,'red_score':None} for i,(a,b) in enumerate(best[1])],best[2]

    result = []
    for i, group in enumerate(groups):
        # Preserve 1+3 first where unused; prefer alternatives only on repeated lineups.
        variants = group_matchups(group)
        def cost(v):
            repeated = sum(seen_pairs[team_key(t)] for t in v)
            return (repeated, sum(seen_opponents[team_key((a,b))] for a in v[0] for b in v[1]), variants.index(v))
        blue, red = min(variants, key=cost)
        result.append({'court':i+1,'blue':list(blue),'red':list(red),'blue_score':None,'red_score':None})
    return result, byes


def table(players, completed):
    records = {name:{'name':name,'played':0,'wins':0,'draws':0,'losses':0,'points':0,'against':0,'diff':0} for name in players}
    for m in completed:
        x,y=m.get('blue_score'),m.get('red_score')
        if x is None or y is None:
            continue
        for side, pts, conceded in [('blue',x,y),('red',y,x)]:
            for name in m[side]:
                if name not in records:
                    continue
                r=records[name]
                r['played']+=1
                r['wins']+=int(pts>conceded)
                r['draws']+=int(pts==conceded)
                r['losses']+=int(pts<conceded)
                r['points']+=pts
                r['against']+=conceded
                r['diff']+=pts-conceded
    return sorted(records.values(), key=lambda r:(-r['points'],-r['wins'],-r['diff'],r['name'].casefold()))
