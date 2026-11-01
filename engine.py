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


def make_fixed_pairs_round(pairs, mode, previous, round_number=0):
    """Schedule fixed teams; never change partners. Balance repeat opponents and byes.

    Mexicano groups teams by aggregate player standings after the first round;
    Americano finds low-repeat opponents. Uneven team counts give whole-team byes.
    """
    if len(pairs) < 2 or any(len(p) != 2 for p in pairs):
        raise ValueError('Faste makkerpar kræver mindst to par med præcis to spillere hver.')
    appearances = defaultdict(int)
    meetings = defaultdict(int)
    for m in previous:
        a, b = team_key(m['blue']), team_key(m['red'])
        for p in (a,b): appearances[p] += 1
        meetings[tuple(sorted((a,b)))] += 1
    ranked = [tuple(p) for p in pairs]
    if mode == 'Mexicano' and previous:
        standings = {r['name']: r['points'] for r in table([x for p in pairs for x in p], previous)}
        ranked.sort(key=lambda pair: -sum(standings.get(x, 0) for x in pair))
    else:
        # Rotate byes fairly; keep teams intact.
        ranked.sort(key=lambda p: (appearances[team_key(p)], (pairs.index(list(p)) - round_number) % len(pairs)))
    if mode == 'Mexicano':
        playing = ranked[:(len(ranked)//2)*2]
        waiting = ranked[len(playing):]
        grouped = [(playing[i], playing[i+1]) for i in range(0,len(playing),2)]
    else:
        waiting = ranked[(len(ranked)//2)*2:]
        playing = ranked[:(len(ranked)//2)*2]
        # Greedy pairing avoids exponential work for large groups (e.g. 36 players).
        grouped = []
        remaining = list(playing)
        while len(remaining) >= 2:
            first = remaining.pop(0)
            opponent = min(remaining, key=lambda p: (
                meetings[tuple(sorted((team_key(first),team_key(p))))],
                abs(appearances[team_key(first)] - appearances[team_key(p)])))
            remaining.remove(opponent)
            grouped.append((first, opponent))
    matches=[{'court':i+1,'blue':list(a),'red':list(b),'blue_score':None,'red_score':None}
             for i,(a,b) in enumerate(grouped)]
    return matches, [name for pair in waiting for name in pair]
