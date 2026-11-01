"""Padel Samlet 2.0 — independently implemented mobile-first tournament app."""
import html
import json
import secrets
import re
import requests
import streamlit as st
from engine import make_round, table

st.set_page_config(page_title='Padel Samlet', page_icon='🎾', layout='centered', initial_sidebar_state='collapsed')
# Server-side Supabase credentials are read only from Streamlit Secrets.
DB_URL = str(st.secrets.get('SUPABASE_URL', '')).rstrip('/')
DB_KEY = str(st.secrets.get('SUPABASE_SECRET_KEY', ''))
DB_READY = bool(DB_URL and DB_KEY)
ID_PATTERN = re.compile(r'^[A-Z0-9_-]{8,32}$')


def db_request(method, tid, payload=None):
    if not DB_READY:
        raise RuntimeError('Supabase skal konfigureres i Streamlit Secrets.')
    if not ID_PATTERN.fullmatch(tid):
        raise ValueError('Ugyldigt turnerings-ID.')
    url = f"{DB_URL}/rest/v1/tournaments"
    headers = {'apikey': DB_KEY, 'Content-Type':'application/json',
               'Accept':'application/json'}
    if not DB_KEY.startswith('sb_secret_'):
        headers['Authorization'] = f'Bearer {DB_KEY}'  # legacy service_role JWT only
    if method == 'GET':
        response = requests.get(url,headers=headers,params={'id':f'eq.{tid}','select':'data'},timeout=12)
    elif method == 'POST':
        headers['Prefer']='return=representation'
        response = requests.post(url,headers=headers,json={'id':tid,'data':payload},timeout=12)
    elif method == 'PATCH':
        headers['Prefer']='return=representation'
        response = requests.patch(url,headers=headers,params={'id':f'eq.{tid}'},json={'data':payload},timeout=12)
    else:
        raise ValueError('Unknown method')
    response.raise_for_status()
    return response.json()


def db_load(tid):
    values = db_request('GET',tid)
    if not values:
        raise ValueError('Turneringen blev ikke fundet. Kontrollér turnerings-ID.')
    return fresh() | values[0]['data']


def db_save(tid, data, create=False):
    result = db_request('POST' if create else 'PATCH',tid,data)
    if not result:
        raise RuntimeError('Turneringen blev ikke gemt. Prøv igen.')


# Public editing is deliberately enabled: anybody who knows a tournament ID can edit it.
def admin_logged_in():
    return True


def require_admin():
    return None


STYLE = '''
<style>
:root{color-scheme:dark}
.stApp{background:radial-gradient(ellipse at top,#163b39 0,#0c191f 340px,#0a1318 100%);color:#edf5f6}
.block-container{padding-top:1.1rem;max-width:850px;padding-bottom:6rem}
h1,h2,h3{color:#f0f8f7!important;letter-spacing:-.04em}
[data-testid="stSidebar"]{background:#102328}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:#12252a;padding:5px;border-radius:16px}
.stTabs [data-baseweb="tab"]{color:#b8cfca;background:transparent;border-radius:12px;padding:10px 16px;font-weight:650}
.stTabs [aria-selected="true"]{background:#174f48!important;color:#ebfffa!important}
.stButton button[kind="primary"]{background:#10a98e;border:1px solid #35c9ad;color:white;border-radius:12px}
.stButton button{border-radius:12px;min-height:43px}
[data-testid="stNumberInput"] input{font-size:20px;font-weight:750;text-align:center}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:#365656!important;border-radius:18px!important;background:#10242a!important}
.court-card{border:1px solid #366f70;border-radius:20px;padding:14px 14px 17px;background:linear-gradient(160deg,#15383d,#10242b);margin:12px 0 8px;box-shadow:0 6px 25px #07171977}
.court-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;color:#d5eeeb}
.court-pill{border:1px solid #417b7b;background:#183d40;padding:6px 12px;border-radius:99px;font-size:13px}
.court{display:grid;grid-template-columns:1fr 1fr;position:relative;min-height:190px;border:5px solid #607f84;border-radius:9px;overflow:hidden;box-shadow:inset 0 0 25px #09151c,0 5px 20px #0006}
.court-side{position:relative;display:flex;flex-direction:column;justify-content:space-evenly;align-items:center;text-align:center;min-width:0;padding:16px 10px;color:white;font-weight:760;line-height:1.4;font-size:clamp(13px,3.5vw,18px);overflow-wrap:anywhere}
.court-blue{background:linear-gradient(130deg,#1c6090,#113d70)}
.court-red{background:linear-gradient(210deg,#8a3038,#51212b)}
.court-side:before{content:'';position:absolute;inset:13% 12%;border:2px solid #ffffff85;pointer-events:none}
.court-side:after{content:'';position:absolute;top:50%;left:12%;width:76%;border-top:2px solid #ffffff85;pointer-events:none}
.court-name{z-index:1;text-shadow:1px 2px 4px #0b1c29;background:#0b1b2959;padding:3px 5px;border-radius:6px}
.court-net{position:absolute;z-index:2;left:calc(50% - 3px);top:0;bottom:0;width:6px;background:repeating-linear-gradient(to bottom,#e3faf9 0 3px,#546f76 3px 6px);box-shadow:0 0 3px white}
.vs{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:3;background:#092129;border:2px solid #49d9c5;color:white;font-weight:850;font-size:13px;border-radius:50%;width:42px;height:42px;display:flex;align-items:center;justify-content:center}
.score-heading{font-weight:650;color:#d6e8e9;font-size:14px;margin-top:7px}
.score-blue{color:#64b6ff}.score-red{color:#ff8c92}
.brand{font-size:12px;letter-spacing:2px;font-weight:900;color:#3cddbd}
.hero-title{font-size:clamp(28px,7vw,44px);font-weight:850;color:white;letter-spacing:-1.5px;line-height:1.15;margin:5px 0 7px}
.subtitle{color:#9ebdbb;font-size:14px;margin-bottom:20px}
.leader{background:#13292e;border:1px solid #365356;padding:12px 13px;border-radius:13px;display:grid;grid-template-columns:28px 1fr 55px 60px;gap:6px;align-items:center;margin:7px 0;font-size:15px}
.leader.first{background:#18413d;border-color:#35ac9b}
.leader-name{font-weight:760}.leader-stat{text-align:right;color:#b5cdc9;font-size:13px}.leader-pts{font-size:20px;text-align:right;font-weight:850;color:white}
.podium{display:grid;grid-template-columns:1fr 1.12fr 1fr;align-items:end;gap:8px;margin:14px 0 22px}
.podium-card{padding:13px 5px;background:#183037;border:1px solid #35595c;border-radius:17px;text-align:center}
.podium-card.winner{background:#174c43;border:1px solid #3ac8aa;padding:23px 5px}
.podium-rank{font-size:25px}.podium-name{font-weight:800;font-size:14px;overflow-wrap:anywhere}.podium-score{font-size:23px;font-weight:900;color:#fff}.podium-label{font-size:11px;color:#b6cfca}
.small-note{font-size:12px;color:#9fbab8}
@media(max-width:500px){.block-container{padding-left:13px;padding-right:13px}.court{min-height:170px}.court-card{padding:10px}.stTabs [data-baseweb="tab"]{padding:9px 6px;font-size:13px}}

/* Padel Pappas 3.1 — forbedret kontrast for mobil og desktop */
.stTabs [data-baseweb="tab-list"] {background:#142b30!important;gap:6px!important;}
.stTabs button[data-baseweb="tab"] {
  color:#EAF4F5!important;opacity:1!important;
  font-weight:750!important;font-size:16px!important;
  text-shadow:none!important;
}
.stTabs button[data-baseweb="tab"] p,
.stTabs button[data-baseweb="tab"] span {
  color:inherit!important;opacity:1!important;font-weight:inherit!important;
}
.stTabs button[data-baseweb="tab"][aria-selected="true"] {
  background:#146C60!important;color:#FFFFFF!important;
  border-radius:10px 10px 0 0!important;
}
.stTabs button[data-baseweb="tab"][aria-selected="false"] {
  color:#E5F0F1!important;background:#1A343A!important;
}
.stTabs [data-baseweb="tab-highlight"] {background:#49E5C4!important;}
section[data-testid="stSidebar"] {color:#F4FAFA!important;}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
section[data-testid="stSidebar"] .stMarkdown p {
  color:#F0F7F7!important;opacity:1!important;
}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {color:#C8DEDF!important;opacity:1!important;}
[data-testid="stAlert"] p {color:#F3F9FA!important;opacity:1!important;}
[data-testid="stAlert"] {border-color:#4C8E9A!important;}
@media(max-width:500px){
  .stTabs button[data-baseweb="tab"]{font-size:14px!important;padding:10px 8px!important;}
  .stTabs [data-baseweb="tab-list"]{gap:3px!important;}
}


/* Padel Pappas 3.2: mobilkontrast / faner / knapper */
html, body, [data-testid="stAppViewContainer"] {overflow-x:hidden!important;}
.stApp .block-container {width:100%!important;min-width:0!important;box-sizing:border-box!important;}
.stApp .hero-title {font-size:clamp(1.7rem,6.7vw,2.65rem)!important;line-height:1.15!important;letter-spacing:-.03em!important;overflow-wrap:break-word!important;}
.stApp .subtitle {overflow-wrap:break-word!important;}
/* Streamlit/BaseWeb puts label color on nested elements. Set it on ALL tab descendants. */
.stApp [data-testid="stTabs"] [data-baseweb="tab-list"] {display:flex!important;gap:5px!important;width:100%!important;max-width:100%!important;overflow-x:auto!important;scrollbar-width:none!important;background:#122a30!important;}
.stApp [data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar {display:none!important;}
.stApp [data-testid="stTabs"] button[data-baseweb="tab"] {color:#f2f8f7!important;background:#203a40!important;opacity:1!important;min-width:0!important;flex:1 0 auto!important;padding:11px 12px!important;font-weight:750!important;white-space:nowrap!important;}
.stApp [data-testid="stTabs"] button[data-baseweb="tab"] *,
.stApp [data-testid="stTabs"] button[data-baseweb="tab"] p,
.stApp [data-testid="stTabs"] button[data-baseweb="tab"] div,
.stApp [data-testid="stTabs"] button[data-baseweb="tab"] span {color:#f2f8f7!important;-webkit-text-fill-color:#f2f8f7!important;opacity:1!important;font-weight:750!important;}
.stApp [data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {background:#096f63!important;color:#fff!important;}
.stApp [data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] * {color:#fff!important;-webkit-text-fill-color:#fff!important;}
/* Secondary actions: dark surface rather than white cards; primary buttons remain teal. */
.stApp [data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"],
.stApp [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button[kind="secondary"],
.stApp [data-testid="stSidebar"] [data-testid="stButton"] button:not([kind="primary"]),
.stApp [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:not([kind="primary"]) {
  background:#213d44!important;border:1px solid #55787d!important;color:#f7fbfb!important;
  box-shadow:none!important;border-radius:12px!important;
}
.stApp [data-testid="stSidebar"] [data-testid="stButton"] button:not([kind="primary"]) *,
.stApp [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:not([kind="primary"]) * {color:#f7fbfb!important;-webkit-text-fill-color:#f7fbfb!important;opacity:1!important;}
.stApp [data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {background:#0ea891!important;color:#fff!important;border-color:#18bca2!important;}
.stApp [data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] * {color:#fff!important;-webkit-text-fill-color:#fff!important;}
.stApp [data-testid="stSidebar"] [data-testid="stButton"] button:hover {border-color:#68d7c5!important;background:#28565b!important;}
.stApp [data-testid="stSidebar"] [data-testid="stTextInput"] input {background:#f7fafa!important;color:#14282c!important;-webkit-text-fill-color:#14282c!important;border-radius:10px!important;}
.stApp [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder {color:#60777c!important;opacity:1!important;}
.stApp [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
.stApp [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {color:#e5f4f4!important;-webkit-text-fill-color:#e5f4f4!important;opacity:1!important;}
/* Accessible info/error/notice text; avoid invisible blue lettering on deep blue. */
.stApp [data-testid="stAlert"] p, .stApp [data-testid="stAlert"] li,
.stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {color:#f3fbff!important;-webkit-text-fill-color:#f3fbff!important;opacity:1!important;}
@media(max-width:600px){
 .stApp .block-container {padding-left:14px!important;padding-right:14px!important;}
 .stApp [data-testid="stTabs"] button[data-baseweb="tab"]{font-size:14px!important;padding:10px 8px!important;}
 .stApp [data-testid="stTabs"] [data-baseweb="tab-list"]{gap:3px!important;}
}

/* 3.3: Sørg for læsbar tekst i spillerlisten på iPhone og desktop.
   BaseWeb kan bruge både textarea-element og indre wrapper. */
.stApp textarea,
.stApp textarea[data-baseweb="textarea"],
.stApp [data-testid="stTextArea"] textarea,
.stApp [data-baseweb="textarea"] textarea {
  background-color:#F7FAFA!important;
  color:#172C30!important;
  -webkit-text-fill-color:#172C30!important;
  caret-color:#172C30!important;
  opacity:1!important;
  font-weight:500!important;
}
.stApp [data-testid="stTextArea"] [data-baseweb="textarea"],
.stApp [data-testid="stTextArea"] [data-baseweb="base-input"],
.stApp [data-baseweb="textarea"] > div {
  background-color:#F7FAFA!important;
  border-color:#789397!important;
}
.stApp [data-testid="stTextArea"] textarea::placeholder,
.stApp [data-baseweb="textarea"] textarea::placeholder {
  color:#62787D!important;
  -webkit-text-fill-color:#62787D!important;
  opacity:1!important;
}
.stApp [data-testid="stTextArea"] textarea:focus {
  color:#172C30!important;
  -webkit-text-fill-color:#172C30!important;
  outline-color:#18B69E!important;
}

</style>
'''
st.markdown(STYLE, unsafe_allow_html=True)


def fresh():
    return {'title':'Søndagspadel','players':[],'format':'Mexicano','round_limit':7,'target':32,
            'round':0,'matches':[],'history':[],'byes':[]}


def save():
    require_admin()
    tid = st.session_state.get('tid')
    if not tid:
        st.error('Vælg eller opret en turnering først.')
        st.stop()
    try:
        db_save(tid,st.session_state.tourney)
    except (requests.RequestException,RuntimeError,ValueError) as exc:
        st.error(f'Kunne ikke gemme turneringen: {exc}')
        st.stop()


def all_matches(data):
    return [m for rd in data['history'] for m in rd['matches']] + data['matches']


def sorted_players(data):
    t=table(data['players'],all_matches(data))
    return [r['name'] for r in t]


def new_round(data):
    if data['round'] >= data['round_limit']:
        return False
    if any(m['blue_score'] is None or m['red_score'] is None for m in data['matches']):
        return False
    if data['matches']:
        data['history'].append({'number':data['round'],'matches':data['matches']})
    order=sorted_players(data) if data['round'] and data['format']=='Mexicano' else list(data['players'])
    generated,byes=make_round(order,data['format'],all_matches(data),seed=data['round']*87+37)
    data['round']+=1
    data['matches']=generated
    data['byes']=byes
    return True

if not DB_READY:
    st.error('Appen kræver Streamlit Secrets med SUPABASE_URL og SUPABASE_SECRET_KEY. Se README.md.')
    st.stop()

with st.sidebar:
    st.header('Åbn turnering')
    st.caption('Åben redigering: Alle med turnerings-ID kan ændre resultater og opsætning.')

    entered = st.text_input('Turnerings-ID',value='',placeholder='F.eks. P-AB12CD34')
    if st.button('Åbn eksisterende turnering',use_container_width=True):
        tid=entered.strip().upper()
        try:
            data=db_load(tid)
            st.session_state.tid=tid
            st.session_state.tourney=data
            st.query_params['id']=tid
            st.rerun()
        except (requests.RequestException,ValueError,RuntimeError) as exc:
            st.error(f'Kunne ikke åbne turneringen: {exc}')
    if st.button('Opret ny turnering',type='primary',use_container_width=True):
        tid='P-'+secrets.token_hex(5).upper()
        try:
            data=fresh()
            db_save(tid,data,create=True)
            st.session_state.tid=tid
            st.session_state.tourney=data
            st.query_params['id']=tid
            st.rerun()
        except (requests.RequestException,ValueError,RuntimeError) as exc:
            st.error(f'Kunne ikke oprette turneringen: {exc}')

# A shared URL works even after Streamlit restarts. Reload on tournament change.
url_id=str(st.query_params.get('id','')).strip().upper()
if url_id and url_id != st.session_state.get('tid'):
    try:
        st.session_state.tourney=db_load(url_id)
        st.session_state.tid=url_id
    except (requests.RequestException,ValueError,RuntimeError) as exc:
        st.error(f'Kunne ikke indlæse turnering fra link: {exc}')
if 'tourney' not in st.session_state:
    st.session_state.tourney=fresh()
d=st.session_state.tourney
st.markdown('<div class="brand">🎾 PADEL SAMLET</div><div class="hero-title">Turnering & resultater</div><div class="subtitle">Kampe, makkerskifte og stilling – samlet ét sted</div>',unsafe_allow_html=True)
if st.session_state.get('tid'):
    st.info(f'Turnerings-ID: **{st.session_state.tid}** · Link: https://padel-pappas.streamlit.app/?id={st.session_state.tid}')

if st.session_state.get('tid'):
    with st.sidebar:
        st.divider()
        st.header('Turneringsopsætning')
        with st.form('setup'):
            title=st.text_input('Turneringens navn',value=d['title'])
            raw=st.text_area('Spillere – én pr. linje',value='\n'.join(d['players']),height=170,placeholder='Jan\nTue\nMick\nJanus')
            fmt=st.selectbox('Turneringsform',['Mexicano','Americano'],index=['Mexicano','Americano'].index(d['format']))
            rounds=st.number_input('Maksimalt antal runder',min_value=1,max_value=40,value=int(d['round_limit']))
            target=st.number_input('Point pr. kamp (0 = frit)',min_value=0,max_value=100,value=int(d['target']))
            submitted=st.form_submit_button('Gem opsætning',type='primary',use_container_width=True)
        if submitted:
            players=[p.strip() for p in raw.splitlines() if p.strip()]
            if len(players)<4 or len(players)!=len(set(players)):
                st.error('Skriv mindst fire forskellige spillernavne.')
            elif d['round'] and (players!=d['players'] or fmt!=d['format']):
                st.error('En startet turnering kan ikke ændre spillere eller turneringsform. Nulstil først.')
            else:
                d.update(title=title,players=players,format=fmt,round_limit=int(rounds),target=int(target))
                save();st.success('Opsætning gemt')
        st.divider()
        if st.button('Nulstil turnering',use_container_width=True):
            st.session_state.confirm_reset=True
        if st.session_state.get('confirm_reset'):
            st.warning('Alle runder og resultater slettes i denne turnering.')
            if st.button('Bekræft nulstilling',type='primary'):
                st.session_state.tourney=fresh();d=st.session_state.tourney;save();st.session_state.confirm_reset=False;st.rerun()

st.caption(f"{d['title']} · {d['format']} · {len(d['players'])} spillere")
tab_games,tab_table,tab_log=st.tabs(['🎾 Kampe','🏆 Stilling','📜 Historik'])
with tab_games:
    st.subheader(f"Aktuel · Runde {d['round'] or '–'}")
    if not st.session_state.get('tid'):
        st.info('Opret en turnering eller åbn en eksisterende via ID i venstremenuen.')
    elif not d['players']:
        st.info('Åbn menuen i venstre side og opret en turnering med mindst fire spillere.')
    elif d['round']==0:
        st.write(f"Klar til {d['format']} med {len(d['players'])} spillere.")
        if st.button('Start turnering',type='primary',use_container_width=True):
            new_round(d);save();st.rerun()
    else:
        if d['byes']:
            st.info('Sidder over denne runde: '+', '.join(d['byes']))
        for i,m in enumerate(d['matches']):
            a=[html.escape(name) for name in m['blue']]
            b=[html.escape(name) for name in m['red']]
            card=f'''<div class="court-card"><div class="court-top"><span class="court-pill">📍 Bane {m['court']}</span><span>Runde {d['round']}</span></div><div class="court"><div class="court-side court-blue"><span class="court-name">{a[0]}</span><span class="court-name">{a[1]}</span></div><div class="court-side court-red"><span class="court-name">{b[0]}</span><span class="court-name">{b[1]}</span></div><div class="court-net"></div><div class="vs">VS</div></div></div>'''
            st.markdown(card,unsafe_allow_html=True)
            col1,col2=st.columns(2,gap='small')
            with col1:
                st.markdown('<div class="score-heading score-blue">🔵 Blå hold</div>',unsafe_allow_html=True)
                v1=st.number_input('Blå score',min_value=0,max_value=200,value=int(m['blue_score'] or 0),key=f"blue_{d['round']}_{i}",label_visibility='collapsed')
            with col2:
                st.markdown('<div class="score-heading score-red">🔴 Rødt hold</div>',unsafe_allow_html=True)
                v2=st.number_input('Rød score',min_value=0,max_value=200,value=int(m['red_score'] or 0),key=f"red_{d['round']}_{i}",label_visibility='collapsed')
            csave,cedit=st.columns([2,1])
            with csave:
                if st.button('Gem resultat',key=f"save_{d['round']}_{i}",type='primary',use_container_width=True):
                    if d['target'] and v1+v2!=d['target']:
                        st.error(f"Resultaterne skal tilsammen give {d['target']} point.")
                    else:
                        m['blue_score']=v1;m['red_score']=v2;save();st.success('Resultat gemt')
            with cedit:
                with st.popover('Rediger hold',use_container_width=True):
                    p=d['players']
                    chosen=st.multiselect('Vælg fire spillere',p,default=m['blue']+m['red'],key=f"edit_{d['round']}_{i}",max_selections=4)
                    if len(chosen)==4:
                        if st.button('Byt makkerpar',key=f"swap_{d['round']}_{i}"):
                            m['blue']=[chosen[0],chosen[2]];m['red']=[chosen[1],chosen[3]];m['blue_score']=None;m['red_score']=None;save();st.rerun()
            if m['blue_score'] is not None:
                st.caption(f"Gemt: {m['blue_score']} – {m['red_score']}")
        st.divider()
        done=all(m['blue_score'] is not None and m['red_score'] is not None for m in d['matches'])
        if d['round']<d['round_limit']:
            if st.button('Næste runde →',type='primary',use_container_width=True,disabled=not done):
                new_round(d);save();st.rerun()
            if not done:
                st.caption('Gem alle kampresultater, før næste runde kan dannes.')
        elif done:
            st.success('Turneringen er færdig! Se slutstillingen under Stilling.')

with tab_table:
    st.subheader('🏆 Aktuel stilling')
    rows=table(d['players'],all_matches(d))
    if not rows:
        st.info('Tilføj spillere for at se stillingen.')
    else:
        podium=rows[:3]
        view=[podium[i] if i<len(podium) else None for i in [1,0,2]]
        labels=['🥈','🥇','🥉']
        cards=[]
        for i,r in enumerate(view):
            if r:
                cards.append(f'<div class="podium-card {"winner" if i==1 else ""}"><div class="podium-rank">{labels[i]}</div><div class="podium-name">{html.escape(r["name"])}</div><div class="podium-score">{r["points"]}</div><div class="podium-label">point</div></div>')
            else:cards.append('<div></div>')
        st.markdown('<div class="podium">'+''.join(cards)+'</div>',unsafe_allow_html=True)
        st.caption('Placering · Spiller · Sejre · +/- · Point')
        for i,r in enumerate(rows):
            diff=f'+{r["diff"]}' if r['diff']>0 else str(r['diff'])
            st.markdown(f'<div class="leader {"first" if i==0 else ""}"><span>{i+1}.</span><span class="leader-name">{html.escape(r["name"])}</span><span class="leader-stat">{r["wins"]} V · {diff}</span><span class="leader-pts">{r["points"]}</span></div>',unsafe_allow_html=True)
        with st.expander('Se komplette statistikker'):
            st.dataframe([{'Spiller':r['name'],'KS':r['played'],'V':r['wins'],'U':r['draws'],'T':r['losses'],'Point':r['points'],'PF':r['diff']} for r in rows],hide_index=True,use_container_width=True)
        who=st.selectbox('Se spillerstatistik', [r['name'] for r in rows])
        r=next(r for r in rows if r['name']==who)
        c1,c2,c3=st.columns(3)
        c1.metric('Kampe',r['played']);c2.metric('Sejre',r['wins']);c3.metric('Pointforskel',r['diff'])
        partners=[]
        for m in all_matches(d):
            for team in (m['blue'],m['red']):
                if who in team:partners += [n for n in team if n!=who]
        st.caption('Makkere: '+(', '.join(partners) if partners else 'Ingen kampe endnu'))

with tab_log:
    st.subheader('📜 Kampoversigt og rettelser')
    rounds=d['history']+([{'number':d['round'],'matches':d['matches']}] if d['matches'] else [])
    if not rounds:st.info('Ingen runder spillet endnu.')
    for rd in reversed(rounds):
        with st.expander(f'Runde {rd["number"]}',expanded=rd['number']==d['round']):
            for j,m in enumerate(rd['matches']):
                st.write(f"**Bane {m['court']}** · {', '.join(m['blue'])} vs {', '.join(m['red'])}")
                if m['blue_score'] is None:st.caption('Ikke afgjort')
                else:st.caption(f"Resultat: {m['blue_score']} – {m['red_score']}")
                with st.form(f"fix_{rd['number']}_{j}"):
                    c1,c2=st.columns(2)
                    newb=c1.number_input('Blå',min_value=0,max_value=200,value=int(m['blue_score'] or 0))
                    newr=c2.number_input('Rød',min_value=0,max_value=200,value=int(m['red_score'] or 0))
                    if st.form_submit_button('Ret resultat'):
                        if d['target'] and newb+newr!=d['target']:
                            st.error(f'Kampens samlede point skal være {d["target"]}.')
                        else:
                            m['blue_score']=newb;m['red_score']=newr;save();st.success('Resultatet er rettet.');st.rerun()
