"""Padel Samlet 2.0 — independently implemented mobile-first tournament app."""
import html
import json
import secrets
import random
import re
import requests
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import zlib
import tempfile
from engine import make_round, make_fixed_pairs_round, table

# Den interaktive banes HTML er indbygget i denne fil.
# Streamlit kan derfor indlaese den uden ekstra mapper i GitHub.
_COURT_HTML_ZLIB_BASE64 = (
    'eNqtWf1u48YR/19PwZPro5SQNEl9WCJNX3tBil6RuwBxG7QI0mLJXUp7xw+VXNpWZAF9hz5D36H/5036JJ3ZJSlSls5pURiQyN3Z'
    '+Z7fzMo3r2geie2GaWuRJreDG/zSEpKtgiElw9ubNSP09iZlgmjRmhQlE8GwErG5GNarGUlZMLzn7GGTF2KoRXkmWAZUD5yKdUDZ'
    'PY+YKV8MnnHBSWKWEUlY4Fj28ApElmKbsNvBF7swfzRL/hPPVl6YF5QVJqzsUSMjzOl2l5JixTPP9kMSfVoVeZVRTxQkKzekAJF+'
    'DKLNmKQ82XrlthQsNStumGSzSZipFow7tsqZ9sd3RgnnzJIVPPajPMkL72HNBdtLQfk9K+Ikf/DWnFKW7QdWuWZJsuvITXjGSGGu'
    'CkI5yB450xllK+PCuZ5cTxh82+7MpWNfGeI5m0etzBNOtYvp9TVd2PWGieer0nMWm0d/QyhF4x0XqNXHbPMI0kW+2VFebhKy9eKE'
    'Pfofq1LweGvWzvbAA+DkkIkHxjKfJHyVmWBNWnoRbLOiZW1rDW/lLXA385wpvConXLBlHMYRyNxwNPiZ9jN3ES5Yy++64dY3Z2JL'
    'vaO8KsRuk5cQ9jzzCpYQwe+ZT8oNiwQQw7LnXjl+yjNzzfhqLTxnCWf9lDw2CxMHF2QCeY5tXzYunR2UmrOls5wfuxTVOoqk/5kI'
    'Lm0VwPksXDqafQmPyym5Jtp0aV3D2/XSjSYLbWZbE3hbzibuJNZQoXFjqReyOC/YromKrvut7SQEXSvBfJ5BDXmL1mWee7AjjuMl'
    'HOEYMpPdA4/Sy/KMgYCMdRzZMktYLLwZ+AQyBOsiFyJP4UFWBeiSqvoAt7M/jUwgHNeOnKH8gy8KtmEQjGxlHntF5JrialzES9Av'
    '1mwN0sW4mC8W9mKJzxokwdj/yeQZZY+ei9XCCqz6Ewqjnsp2qemijazbV+iCzeN5HNKo5esc+Fpo9k7a7swsd3a5b3cKTBm1tZha'
    '17A1sFJO0aoz2qD36kz7RTrU3J7pUNsxUVJbso5CKKlHNLDuy5eCKr+fR1MG01ARbbSb95QHAIom7okkmzmURdPjYrEPRTaZw2NT'
    'fPjcQM+q4NSHJ4CaHrh0kKQFlgd1fmHbiF+MpOeS4bLNhcY70+ml30M7/DApLwAz8DwgVZWeRLnPw2Ljp+mZEkMtrTCpmArXBKIo'
    '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'
    'A0DirzMOHOiqi/dRNW/fXKmb6JX6N99/AF+49fQ='
)
_court_html = zlib.decompress(base64.b64decode(_COURT_HTML_ZLIB_BASE64))
_component_dir = Path(tempfile.gettempdir()) / 'padel_pappas_court_v56'
_component_dir.mkdir(parents=True, exist_ok=True)
_component_file = _component_dir / 'index.html'
if not _component_file.exists() or _component_file.read_bytes() != _court_html:
    _component_file.write_bytes(_court_html)
st.set_page_config(page_title='Padel Samlet', page_icon='🎾', layout='centered', initial_sidebar_state='collapsed')

court_input = components.declare_component('padel_court_input_v56', path=str(_component_dir))
# Server-side Supabase credentials are read only from Streamlit Secrets.
DB_URL = str(st.secrets.get('SUPABASE_URL', '')).rstrip('/')
DB_KEY = str(st.secrets.get('SUPABASE_SECRET_KEY', ''))
DB_READY = bool(DB_URL and DB_KEY)
ID_PATTERN = re.compile(r'^[A-Z0-9][A-Z0-9_/-]{2,31}$')


def normalize_id(value):
    return str(value).strip().upper()


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
.score-inline-note{font-size:12px;color:#c6dcde;text-align:center;margin-top:-4px;margin-bottom:8px}
.score-on-court-left + div [data-testid="stNumberInput"],
.score-on-court-right + div [data-testid="stNumberInput"]{
  margin-top:-120px!important;position:relative;z-index:15;
}
.score-on-court-left + div [data-testid="stNumberInput"] input{
  background:rgba(255,255,255,.96)!important;border:2px solid #4ca2ff!important;color:#10202a!important;
  box-shadow:0 10px 24px rgba(7,23,28,.35)!important;
}
.score-on-court-right + div [data-testid="stNumberInput"] input{
  background:rgba(255,255,255,.96)!important;border:2px solid #ff6d75!important;color:#10202a!important;
  box-shadow:0 10px 24px rgba(7,23,28,.35)!important;
}
.score-auto-box{
  margin-top:-120px;background:rgba(12,27,34,.92);border:2px solid #ff6d75;border-radius:12px;
  min-height:56px;padding:10px 14px;display:flex;align-items:center;justify-content:center;
  color:#ffffff;font-size:22px;font-weight:850;box-shadow:0 10px 24px rgba(7,23,28,.35);position:relative;z-index:15;
}
.score-auto-box small{font-size:11px;font-weight:650;color:#ffe2e4;margin-left:6px}
.score-overlay-spacer{height:4px}
@media(max-width:500px){
  .score-on-court-left + div [data-testid="stNumberInput"],
  .score-on-court-right + div [data-testid="stNumberInput"],
  .score-auto-box{margin-top:-106px!important}
  .score-auto-box{font-size:20px;min-height:52px;padding:8px 10px}
}
.brand{font-size:12px;letter-spacing:2px;font-weight:900;color:#3cddbd}
.hero-title{font-size:clamp(28px,7vw,44px);font-weight:850;color:white;letter-spacing:-1.5px;line-height:1.15;margin:5px 0 7px}
.subtitle{color:#9ebdbb;font-size:14px;margin-bottom:20px}
.leader{background:#13292e;border:1px solid #365356;padding:12px 13px;border-radius:13px;display:grid;grid-template-columns:28px 1fr 55px 60px;gap:6px;align-items:center;margin:7px 0;font-size:15px}
.leader.first{background:#18413d;border-color:#35ac9b}
.leader-name{font-weight:760}.leader-stat{text-align:right;color:#b5cdc9;font-size:13px}.leader-pts{font-size:20px;text-align:right;font-weight:850;color:white}

/* Stilling 4.2: tydelige V/U/T-kolonner på alle skærmstørrelser */
.standing-heading,.standing-row {display:grid;grid-template-columns:24px minmax(66px,1fr) 26px 26px 26px 42px 43px;gap:5px;align-items:center;}
.standing-heading{padding:8px 9px;color:#d2e9e7;font-size:11px;font-weight:750;text-align:center;}
.standing-heading .standing-person{text-align:left}
.standing-row{background:#13292e;border:1px solid #365356;padding:11px 9px;border-radius:12px;margin:6px 0;color:#f7ffff;font-size:13px;}
.standing-row.top{background:#18413d;border-color:#35ac9b}
.standing-row .standing-person{font-weight:750;overflow-wrap:anywhere;min-width:0}
.standing-row .standing-value{text-align:center;font-variant-numeric:tabular-nums}
.standing-row .standing-points{font-weight:850;color:#fff}
.standing-row .standing-diff{color:#bfe2d8}
@media(max-width:370px){.standing-heading,.standing-row{grid-template-columns:18px minmax(54px,1fr) 22px 22px 22px 33px 35px;gap:3px;font-size:11px;padding-left:5px;padding-right:5px}}

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


/* Version 3.4: faner og rediger-hold. Hold alle tilstande læsbare på mobil. */
.stApp div[data-baseweb="tab-list"] [data-baseweb="tab"],
.stApp div[data-baseweb="tab-list"] [role="tab"],
.stApp .stTabs [data-baseweb="tab"] {
  color:#F4FAFA!important;
  -webkit-text-fill-color:#F4FAFA!important;
  background:#214248!important;
  opacity:1!important;
  filter:none!important;
  font-weight:750!important;
  text-shadow:none!important;
}
.stApp div[data-baseweb="tab-list"] [data-baseweb="tab"] *,
.stApp div[data-baseweb="tab-list"] [role="tab"] *,
.stApp .stTabs [data-baseweb="tab"] * {
  color:#F4FAFA!important;
  -webkit-text-fill-color:#F4FAFA!important;
  opacity:1!important;
  filter:none!important;
  font-weight:750!important;
}
.stApp div[data-baseweb="tab-list"] [aria-selected="true"],
.stApp .stTabs [aria-selected="true"] {
  background:#0C7869!important;
  color:white!important;
  -webkit-text-fill-color:white!important;
}
.stApp div[data-baseweb="tab-list"] [aria-selected="true"] *,
.stApp .stTabs [aria-selected="true"] * {
  color:white!important;
  -webkit-text-fill-color:white!important;
}
/* Popover-knappen "Rediger hold" må aldrig blive hvid med hvid skrift. */
.stApp [data-testid="stPopover"] > button,
.stApp [data-testid="stPopover"] button,
.stApp [data-testid="stPopoverButton"] button,
.stApp button[kind="secondary"] {
  background:#24434A!important;
  border:1px solid #62878E!important;
  color:#F8FCFD!important;
  -webkit-text-fill-color:#F8FCFD!important;
  opacity:1!important;
}
.stApp [data-testid="stPopover"] button *,
.stApp [data-testid="stPopoverButton"] button *,
.stApp button[kind="secondary"] * {
  color:#F8FCFD!important;
  -webkit-text-fill-color:#F8FCFD!important;
  opacity:1!important;
}
.stApp [data-testid="stPopover"] button:hover,
.stApp button[kind="secondary"]:hover {background:#31585F!important;border-color:#7DDACA!important;}
.stApp [data-testid="stPopover"] button:disabled,
.stApp button[kind="secondary"]:disabled {opacity:.58!important;}
@media (max-width:600px) {
  .stApp div[data-baseweb="tab-list"] [data-baseweb="tab"] {padding:10px 8px!important;font-size:14px!important;}
}

/* VERSION 3.5: Kontrast-sikker fanenavigation.
   Vi giver ikke-aktive faner en LYS flade, så også Streamlits
   mørke standardtekst er tydelig, hvis frameworkets theme vinder. */
.stApp [data-baseweb="tab-list"] button[role="tab"],
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"] {
  background-color:#E8F2F1!important;
  color:#10282C!important;
  -webkit-text-fill-color:#10282C!important;
  border:1px solid #BCD1CF!important;
  border-radius:11px!important;
  opacity:1!important;
  font-weight:750!important;
  text-shadow:none!important;
  box-shadow:none!important;
}
.stApp [data-baseweb="tab-list"] button[role="tab"] *,
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"] * {
  color:#10282C!important;
  -webkit-text-fill-color:#10282C!important;
  opacity:1!important;
  font-weight:750!important;
  text-shadow:none!important;
}
.stApp [data-baseweb="tab-list"] button[role="tab"][aria-selected="true"],
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"] {
  background-color:#0C7869!important;
  border-color:#22C9AC!important;
  color:#FFFFFF!important;
  -webkit-text-fill-color:#FFFFFF!important;
}
.stApp [data-baseweb="tab-list"] button[role="tab"][aria-selected="true"] *,
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"] * {
  color:#FFFFFF!important;
  -webkit-text-fill-color:#FFFFFF!important;
}
.stApp [data-baseweb="tab-list"] button[role="tab"]:hover:not([aria-selected="true"]) {
  background-color:#FFFFFF!important;
}


/* Padel Pappas 3.9: history controls readable in both desktop and iOS Safari */
.stApp [data-testid="stExpander"] details,
.stApp [data-testid="stExpander"] details > summary,
.stApp [data-testid="stExpander"] summary {
 background:#203D43!important;color:#F7FCFC!important;border-radius:10px!important;
 -webkit-text-fill-color:#F7FCFC!important;
}
.stApp [data-testid="stExpander"] summary *,
.stApp [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {
 color:#F7FCFC!important;-webkit-text-fill-color:#F7FCFC!important;opacity:1!important;
}
.stApp [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
 background:#112A2F!important;color:#F5FBFB!important;
}
.stApp [data-testid="stExpander"] [data-testid="stWidgetLabel"] *,
.stApp [data-testid="stExpander"] [data-testid="stMetricLabel"] *,
.stApp [data-testid="stExpander"] [data-testid="stMetricValue"] *,
.stApp [data-testid="stExpander"] [data-testid="stMetricValue"] {
 color:#F3FAFA!important;-webkit-text-fill-color:#F3FAFA!important;opacity:1!important;
}
.stApp [data-testid="stExpander"] [data-testid="stFormSubmitButton"] button,
.stApp [data-testid="stExpander"] [data-testid="stFormSubmitButton"] button[kind="secondary"] {
 background:#204148!important;border:1px solid #6EB6B0!important;color:#FFFFFF!important;
 -webkit-text-fill-color:#FFFFFF!important;
}
.stApp [data-testid="stExpander"] [data-testid="stFormSubmitButton"] button * {
 color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;opacity:1!important;
}
/* Redundant selectors intentionally cover Streamlit tab markup versions. */
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"]:not([aria-selected="true"]),
.stApp [data-baseweb="tab-list"] [role="tab"]:not([aria-selected="true"]) {
 background:#E7F1F0!important;color:#142C30!important;-webkit-text-fill-color:#142C30!important;
 opacity:1!important;border-radius:9px!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"]:not([aria-selected="true"]) *,
.stApp [data-baseweb="tab-list"] [role="tab"]:not([aria-selected="true"]) * {
 color:#142C30!important;-webkit-text-fill-color:#142C30!important;opacity:1!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"][aria-selected="true"],
.stApp [data-baseweb="tab-list"] [role="tab"][aria-selected="true"] {
 background:#097D6D!important;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"][aria-selected="true"] *,
.stApp [data-baseweb="tab-list"] [role="tab"][aria-selected="true"] * {
 color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;
}


/* 4.0: score inputs contrast: a light control must have dark text, including inside History expanders */
.stApp [data-testid="stNumberInput"] input,
.stApp [data-testid="stNumberInput"] input[type="number"],
.stApp [data-testid="stExpander"] [data-testid="stNumberInput"] input,
.stApp [data-testid="stForm"] [data-testid="stNumberInput"] input,
.stApp [data-baseweb="input"] input[type="number"] {
  background-color:#F1F4F8!important;
  color:#17252F!important;
  -webkit-text-fill-color:#17252F!important;
  opacity:1!important;
  caret-color:#17252F!important;
  font-weight:800!important;
}
.stApp [data-testid="stNumberInput"] [data-baseweb="input"],
.stApp [data-testid="stNumberInput"] [data-baseweb="base-input"] {
  background-color:#F1F4F8!important;
}
.stApp [data-testid="stNumberInput"] button,
.stApp [data-testid="stNumberInput"] button * {
  color:#28323F!important;
  -webkit-text-fill-color:#28323F!important;
  opacity:1!important;
}
/* Deliberately apply after the expander general label styles. */


/* 4.7: Vandret padelbane, korrekte linjer og score på hver sin halvdel. */
.padel-real-card{border:1px solid #427b7d;border-radius:18px;padding:10px;background:linear-gradient(145deg,#17363c,#0e252d);margin:12px 0 0}
.padel-real-top{display:flex;align-items:center;justify-content:space-between;color:#e8ffff;margin:0 2px 10px;gap:10px}
.padel-real-top .court-pill{white-space:nowrap}
.padel-real{width:100%;aspect-ratio:2/1;min-height:160px;max-height:245px;margin:0 auto;position:relative;border:5px solid #688e92;border-radius:9px;background:linear-gradient(to right,#14568b 0%,#174572 49.7%,#762b34 50.3%,#92303e 100%);box-shadow:inset 0 0 25px #09131c99,0 8px 22px #0005;overflow:hidden;isolation:isolate}
/* Net x=50%. Servelinjerne er 6,95 m fra nettet: x=15,25% og 84,75% på en 20 m bane. */
.padel-real:before{content:'';position:absolute;inset:6px;border:2px solid rgba(238,253,255,.7);z-index:1;pointer-events:none}
.padel-real:after{content:'';position:absolute;top:0;bottom:0;left:50%;width:5px;transform:translateX(-50%);background:repeating-linear-gradient(to bottom,#e5f5f5 0 4px,#56727b 4px 7px);border-inline:1px solid #f9ffff;z-index:3;pointer-events:none;box-shadow:0 0 6px #0009}
.padel-service{position:absolute;top:6px;bottom:6px;border-left:2px solid #eef8ffcf;z-index:2;pointer-events:none}
.padel-service.top{left:15.25%}.padel-service.bottom{left:84.75%}
.padel-center-upper,.padel-center-lower{position:absolute;top:50%;height:2px;transform:translateY(-50%);background:#f2fbffcf;z-index:2;pointer-events:none}
.padel-center-upper{left:15.25%;width:34.75%}.padel-center-lower{left:50%;width:34.75%}
/* Navne tæt ved bagvægge; scorefelter i separat bånd under banen. */
.padel-team{position:absolute;top:8%;bottom:8%;width:30%;display:flex;align-items:center;justify-content:space-between;flex-direction:column;gap:6px;z-index:4;color:#fff;font-weight:750;text-align:center;font-size:clamp(10px,2.7vw,16px)}
.padel-team.blue{left:2%}.padel-team.red{right:2%}
.padel-player{background:#071a2add;border-radius:7px;max-width:100%;padding:4px 5px;overflow-wrap:anywhere;text-shadow:0 1px 3px #000;line-height:1.15}
.padel-team.red .padel-player{background:#2d0f19db}
.padel-net-badge{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:5;border:2px solid #40dec2;border-radius:50%;background:#0c2e35;color:#fff;padding:6px;font-weight:850;font-size:12px}
/* 4.8: Responsive score controls in a dedicated strip, no overlapping negative margins. */
.padel-score-strip-header{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px;margin-bottom:1px}
.padel-score-strip-header span{font-weight:800;font-size:13px;text-align:center;color:#fff;padding:8px 4px;border-radius:8px 8px 0 0}
.padel-score-strip-header .blue{background:#14568b}.padel-score-strip-header .red{background:#842e3d}
[class*="st-key-on_court_score_"]{position:relative!important;margin:0!important;padding:8px!important;background:#102a30!important;border:1px solid #487b7e;border-radius:0 0 13px 13px!important;box-sizing:border-box!important}
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"]{gap:8px!important;align-items:center!important}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"]{min-width:0!important}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] input{background:#f0f5f8!important;color:#15252c!important;-webkit-text-fill-color:#15252c!important;font-size:20px!important;font-weight:900!important;border-radius:8px!important;min-width:0!important;text-align:center!important;padding:4px!important}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] button{min-width:24px!important;width:24px!important;padding:0!important}
.padel-auto-score{background:#f0f5f8;border:2px solid #f58b93;border-radius:8px;padding:7px 2px;color:#13252c;font-weight:900;text-align:center;font-size:20px;min-height:48px}
.padel-auto-score small{display:block;font-size:10px;color:#3a464c;font-weight:650}
.padel-score-foot{color:#d7eeee;font-size:12px;text-align:center;margin:5px 0 12px}
@media(max-width:550px){
 .padel-real{min-height:140px;max-height:none;aspect-ratio:2/1}
 .padel-real-card{padding:8px}.padel-player{font-size:11px;padding:3px}
 [class*="st-key-on_court_score_"]{padding:5px!important}
 [class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"]{gap:5px!important}
 [class*="st-key-on_court_score_"] [data-testid="stNumberInput"] input{font-size:17px!important}
}

/* VERSION 5.0: tydelige centrerede spillere og holdfarvede scorefelter.
   CSS er lagt sidst for at overstyre de ældre farver. */
.padel-team{
  top:3%!important;bottom:3%!important;width:45%!important;
  display:flex!important;flex-direction:row!important;gap:6px!important;white-space:nowrap!important;
  justify-content:space-evenly!important;align-items:center!important;
  gap:7px!important;text-align:center!important;
  font-size:clamp(14px,2.8vw,19px)!important;
  font-weight:850!important;
}
.padel-team.blue{left:2.5%!important}
.padel-team.red{right:2.5%!important}
.padel-player{
  display:block!important;max-width:96%!important;
  border-radius:9px!important;padding:6px 8px!important;
  line-height:1.18!important;color:#fff!important;
  text-shadow:0 1px 3px #000!important;
  overflow-wrap:anywhere!important;
}
/* Blå score: både selve tallet, inputrammen og plus/minus skal passe til den blå halvdel. */
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child [data-testid="stNumberInput"] input,
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child [data-testid="stNumberInput"] [data-baseweb="input"],
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child [data-testid="stNumberInput"] [data-baseweb="base-input"]{
  background:#14568b!important;color:#fff!important;
  -webkit-text-fill-color:#fff!important;
  border-color:#4aaefa!important;
}
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child [data-testid="stNumberInput"] input{
  font-size:22px!important;font-weight:900!important;
  text-align:center!important;caret-color:#fff!important;
}
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child [data-testid="stNumberInput"] input::placeholder{
  color:#e7f5ff!important;-webkit-text-fill-color:#e7f5ff!important;opacity:1!important;
}
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child [data-testid="stNumberInput"] button{
  background:#14568b!important;color:#fff!important;border-color:#4aaefa!important;
}
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child [data-testid="stNumberInput"] button *{
  color:#fff!important;stroke:#fff!important;fill:none!important;
}
/* Rød score beregnes automatisk ved fast pointantal. */
.padel-auto-score{
  background:#842e3d!important;color:#fff!important;
  border:2px solid #f28b98!important;border-radius:10px!important;
  font-size:22px!important;font-weight:900!important;min-height:52px!important;
  display:flex!important;flex-direction:row!important;gap:6px!important;white-space:nowrap!important;
  justify-content:center!important;align-items:center!important;
  padding:6px 4px!important;
}
.padel-auto-score small{display:inline!important;color:#fff!important;font-size:12px!important;font-weight:650!important;opacity:.92!important}
/* Ved frit pointformat er det andet input rødt. */
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stNumberInput"] input,
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stNumberInput"] [data-baseweb="input"],
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stNumberInput"] [data-baseweb="base-input"]{
  background:#842e3d!important;color:#fff!important;-webkit-text-fill-color:#fff!important;
  border-color:#f28b98!important;
}
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stNumberInput"] button{
  background:#842e3d!important;color:#fff!important;border-color:#f28b98!important;
}
[class*="st-key-on_court_score_"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stNumberInput"] button *{stroke:#fff!important;color:#fff!important;fill:none!important}
@media(max-width:550px){
 .padel-team{font-size:clamp(13px,3.5vw,16px)!important;gap:4px!important}
 .padel-player{padding:5px 6px!important}
 [class*="st-key-on_court_score_"] [data-testid="stNumberInput"] input{font-size:19px!important}
 .padel-auto-score{font-size:19px!important;min-height:48px!important}
}

/* 5.2: stabilt layout af score-felt, X og plus/minus i to kolonner.
   Slå native clear-kryds fra, og giv spin-knapperne deres naturlige plads. */
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] {
  width:100%!important;min-width:0!important;overflow:visible!important;
}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] [data-baseweb="input"],
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] [data-baseweb="base-input"] {
  width:100%!important;min-width:0!important;display:flex!important;
  align-items:stretch!important;overflow:hidden!important;border-radius:10px!important;
  box-sizing:border-box!important;
}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] input {
  width:100%!important;min-width:0!important;flex:1 1 0!important;
  padding:6px 2px!important;text-overflow:clip!important;
}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] button {
  flex:0 0 32px!important;width:32px!important;min-width:32px!important;
  height:auto!important;min-height:48px!important;padding:0!important;
  border-radius:0!important;display:flex!important;align-items:center!important;justify-content:center!important;
}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] [data-baseweb="clear-icon"],
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] [aria-label="Clear"],
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] [aria-label="Clear input"] {
  display:none!important;
}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] svg {
  width:16px!important;height:16px!important;stroke-width:2.5!important;
}
@media(max-width:550px){
 [class*="st-key-on_court_score_"] [data-testid="stNumberInput"] button {
   flex-basis:26px!important;width:26px!important;min-width:26px!important;min-height:46px!important;
 }
 [class*="st-key-on_court_score_"] [data-testid="stNumberInput"] input {font-size:17px!important;}
}
/* 5.3: Navne igen over/under hinanden, midt i hver banehalvdel. */
.padel-team{top:5%!important;bottom:5%!important;width:42%!important;
 display:flex!important;flex-direction:column!important;align-items:center!important;
 justify-content:space-around!important;gap:8px!important;white-space:normal!important}
.padel-team.blue{left:4%!important}.padel-team.red{right:4%!important}
.padel-player{max-width:94%!important;padding:5px 7px!important;
 font-size:clamp(12px,2.8vw,18px)!important;overflow-wrap:anywhere!important}
/* Score: simple text input without native plus, minus or clear buttons. */
[class*="st-key-on_court_score_"] [data-testid="stTextInput"] input{
 background:#14568b!important;color:#fff!important;-webkit-text-fill-color:#fff!important;
 caret-color:#fff!important;border:1px solid #51a7fa!important;
 text-align:center!important;font-size:22px!important;font-weight:850!important;
 border-radius:10px!important;min-height:50px!important;width:100%!important}
[class*="st-key-on_court_score_"] [data-testid="stTextInput"] input::placeholder{
 color:#d8ebff!important;-webkit-text-fill-color:#d8ebff!important;opacity:1!important}
[class*="st-key-on_court_score_"] [data-testid="stColumn"]:nth-child(2) [data-testid="stTextInput"] input{
 background:#842e3d!important;border-color:#f28b98!important}
@media(max-width:550px){.padel-team{gap:6px!important}.padel-player{font-size:clamp(12px,3.3vw,15px)!important}}
/* 5.4: blue and red score controls have exactly the same external height. */
[class*="st-key-on_court_score_"] [data-testid="stTextInput"] input{
  box-sizing:border-box!important;height:50px!important;min-height:50px!important;
  padding:0 8px!important;line-height:50px!important;
}
.padel-auto-score{
  box-sizing:border-box!important;height:50px!important;min-height:50px!important;
  padding:0 8px!important;margin:0!important;
  line-height:1!important;width:100%!important;
}
@media(max-width:550px){
 .padel-auto-score{height:50px!important;min-height:50px!important}
}

/* Version 6.0 — neutral sort baggrund. Baner og knapper bevarer holdfarverne. */
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"] {
  background: #08090c !important;
  background-image: none !important;
}
[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
  background: #111318 !important;
  background-image: none !important;
}
.stApp { color: #f4f7f8 !important; }
</style>
'''
st.markdown(STYLE, unsafe_allow_html=True)


def fresh():
    return {'title':'Søndagspadel','players':[],'format':'Mexicano','round_limit':7,'target':32,
            'round':0,'matches':[],'history':[],'byes':[],'partner_mode':'Skiftende makker','ranking_priority':'Point først','finale':None}


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


def standings(data):
    """Calculate all results normally, but apply the tournament's tie-break order."""
    rows = table(data['players'], all_matches(data))
    if data.get('ranking_priority', 'Point først') == 'Sejre først':
        return sorted(rows, key=lambda r: (-r['wins'], -r['points'], -r['diff'], r['name'].casefold()))
    return sorted(rows, key=lambda r: (-r['points'], -r['wins'], -r['diff'], r['name'].casefold()))


def sorted_players(data):
    return [r['name'] for r in standings(data)]


def new_round(data):
    if data['round'] >= data['round_limit']:
        return False
    if any(m['blue_score'] is None or m['red_score'] is None for m in data['matches']):
        return False
    if data['matches']:
        data['history'].append({'number':data['round'],'matches':data['matches']})
    order=sorted_players(data) if data['round'] and data['format']=='Mexicano' else list(data['players'])
    if data.get('partner_mode') == 'Fast makker':
        pairs = [data['players'][i:i+2] for i in range(0,len(data['players']),2)]
        generated,byes = make_fixed_pairs_round(pairs,data['format'],all_matches(data),round_number=data['round'])
    else:
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

    entered = st.text_input('Turnerings-ID',value='',placeholder='F.eks. PADEL1/11 eller P-AB12CD34')
    if st.button('Åbn eksisterende turnering',use_container_width=True):
        tid=normalize_id(entered)
        try:
            data=db_load(tid)
            st.session_state.tid=tid
            st.session_state.tourney=data
            st.query_params['id']=tid
            st.rerun()
        except (requests.RequestException,ValueError,RuntimeError) as exc:
            st.error(f'Kunne ikke åbne turneringen: {exc}')
    st.divider()
    st.subheader('Opret ny turnering')
    id_choice = st.radio('Turnerings-ID', ['Vælg selv', 'Generér automatisk'], horizontal=True,
                         help='Du kan f.eks. bruge Padel1/11. ID må indeholde bogstaver, tal, /, - og _.')
    custom_id = ''
    if id_choice == 'Vælg selv':
        custom_id = st.text_input('Dit nye turnerings-ID', placeholder='F.eks. Padel1/11',
                                  help='3-32 tegn. Gem ID-et, så du kan åbne turneringen igen.')
    if st.button('Opret ny turnering',type='primary',use_container_width=True):
        tid = normalize_id(custom_id) if id_choice == 'Vælg selv' else 'P-'+secrets.token_hex(5).upper()
        if not ID_PATTERN.fullmatch(tid):
            st.error('Indtast et gyldigt turnerings-ID på 3-32 tegn. Brug bogstaver, tal, /, - eller _.')
        else:
            try:
                data=fresh()
                db_save(tid,data,create=True)
                st.session_state.tid=tid
                st.session_state.tourney=data
                st.query_params['id']=tid
                st.rerun()
            except requests.HTTPError as exc:
                if exc.response is not None and exc.response.status_code == 409:
                    st.error('Dette turnerings-ID er allerede i brug. Vælg et andet, eller åbn den eksisterende turnering.')
                else:
                    st.error(f'Kunne ikke oprette turneringen: {exc}')
            except (requests.RequestException,ValueError,RuntimeError) as exc:
                st.error(f'Kunne ikke oprette turneringen: {exc}')

# A shared URL works even after Streamlit restarts. Reload on tournament change.
url_id=normalize_id(st.query_params.get('id',''))
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
            fmt=st.radio('Turneringsform', ['Mexicano', 'Americano'],
                         index=['Mexicano', 'Americano'].index(d['format']))
            partner_mode=st.radio('Makkertype', ['Skiftende makker', 'Fast makker'],
                                  index=1 if d.get('partner_mode')=='Fast makker' else 0,
                                  help='Fast makker: Skriv partnerne to og to i spillerlisten (linje 1+2, 3+4 osv.).')
            if partner_mode == 'Fast makker':
                st.caption('Faste par: 1. og 2. navn er et par; 3. og 4. navn er næste par osv. Parrene bliver sammen i alle runder.')
            ranking_priority=st.radio('Hvad afgør placeringen?', ['Point først', 'Sejre først'],
                                      index=1 if d.get('ranking_priority')=='Sejre først' else 0,
                                      help='Point først: flest scorede point, derefter flest sejre og pointforskel. Sejre først: flest vundne kampe, derefter scorede point og pointforskel.')
            rounds=st.number_input('Maksimalt antal runder',min_value=1,max_value=40,value=int(d['round_limit']))
            target=st.number_input('Point pr. kamp (0 = frit)',min_value=0,max_value=100,value=int(d['target']))
            submitted=st.form_submit_button('Gem opsætning',type='primary',use_container_width=True)
        if submitted:
            players=[p.strip() for p in raw.splitlines() if p.strip()]
            if len(players)<4 or len(players)!=len(set(players)):
                st.error('Skriv mindst fire forskellige spillernavne.')
            elif partner_mode == 'Fast makker' and len(players)%2:
                st.error('Faste makkere kræver et lige antal spillere. Skriv hvert par lige efter hinanden.')
            elif d['round'] and (players!=d['players'] or fmt!=d['format'] or partner_mode!=d.get('partner_mode','Skiftende makker')):
                st.error('En startet turnering kan ikke ændre spillere eller turneringsform. Nulstil først.')
            else:
                d.update(title=title,players=players,format=fmt,partner_mode=partner_mode,ranking_priority=ranking_priority,round_limit=int(rounds),target=int(target))
                save();st.success('Opsætning gemt')
        st.divider()
        if st.button('Nulstil turnering',use_container_width=True):
            st.session_state.confirm_reset=True
        if st.session_state.get('confirm_reset'):
            st.warning('Alle runder og resultater slettes i denne turnering.')
            if st.button('Bekræft nulstilling',type='primary'):
                st.session_state.tourney=fresh();d=st.session_state.tourney;save();st.session_state.confirm_reset=False;st.rerun()

st.caption(f"{d['title']} · {d['format']} · {d.get('partner_mode','Skiftende makker')} · {len(d['players'])} spillere")
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
        # Første runde kan fordeles på ny, inden noget resultat er gemt.
        # Gemte scorer og efterfølgende runder er altid beskyttet.
        can_reshuffle = (d['round'] == 1 and not d['history'] and
                         all(m.get('blue_score') is None and m.get('red_score') is None
                             for m in d['matches']))
        if can_reshuffle:
            st.caption('Ikke tilfreds med fordelingen? Bland første runde igen, inden du gemmer resultater.')
            if st.button('🔀 Bland hold igen', use_container_width=True,
                         key=f"reshuffle_first_{st.session_state.tid}"):
                previous_lineups = [
                    (tuple(sorted(m['blue'])), tuple(sorted(m['red'])))
                    for m in d['matches']
                ]
                # Prøv forskellige fordelinger, så knappen normalt giver en reel ændring.
                for _ in range(10):
                    if d.get('partner_mode') == 'Fast makker':
                        pairs = [d['players'][k:k+2] for k in range(0,len(d['players']),2)]
                        rng = random.Random(secrets.randbits(64))
                        rng.shuffle(pairs)
                        generated, byes = make_fixed_pairs_round(
                            pairs, d['format'], [], round_number=0)
                    else:
                        order = list(d['players'])
                        rng = random.Random(secrets.randbits(64))
                        rng.shuffle(order)
                        generated, byes = make_round(
                            order, d['format'], [], seed=secrets.randbits(64))
                    new_lineups = [
                        (tuple(sorted(m['blue'])), tuple(sorted(m['red'])))
                        for m in generated
                    ]
                    if new_lineups != previous_lineups:
                        break
                d['matches'] = generated
                d['byes'] = byes
                # Rundenummer, turnerings-ID og tidligere data ændres ikke.
                save()
                st.rerun()
            st.caption('Bemærk: Eventuelle indtastede, men ikke gemte scores går tabt ved ny blanding.')
        if d['byes']:
            st.info('Sidder over denne runde: '+', '.join(d['byes']))
        # Indtast alle kampresultater først. Hele runden gemmes i ét databasekald.
        resultater = []
        for i, m in enumerate(d['matches']):
            # Stable frontend component keeps both inputs ON the court.
            # The browser sends changes back to Python; "Gem runde" still saves
            # all results together through the existing Supabase logic.
            current_key = f"court_{st.session_state.tid}_{d['round']}_{i}_{'_'.join(m['blue'] + m['red'])}"
            component_scores = court_input(
                court=m['court'], round=d['round'],
                blue_players=m['blue'], red_players=m['red'],
                target=int(d['target']),
                blue_score=m['blue_score'], red_score=m['red_score'],
                default={'blue': m['blue_score'], 'red': m['red_score']},
                key=current_key,
            )
            component_scores = component_scores if isinstance(component_scores, dict) else {}
            def safe_score(value, upper):
                if type(value) is int and 0 <= value <= upper:
                    return value
                return None
            v1 = safe_score(component_scores.get('blue'), int(d['target']) if d['target'] else 200)
            if d['target']:
                v2 = int(d['target']) - v1 if v1 is not None else None
            else:
                v2 = safe_score(component_scores.get('red'), 200)
            if component_scores.get('blue') is not None and v1 is None:
                st.warning(f"Bane {m['court']}: Blå score er ugyldig.")
            if not d['target'] and component_scores.get('red') is not None and v2 is None:
                st.warning(f"Bane {m['court']}: Rød score er ugyldig.")
            resultater.append((v1, v2))
            if d.get('partner_mode') == 'Fast makker':
                st.caption('Faste makkerpar: Holdene kan ikke byttes enkeltvis under turneringen.')
            else:
                st.markdown('')
            if d.get('partner_mode') != 'Fast makker':
              with st.popover('Rediger hold', use_container_width=True):
                p = d['players']
                chosen = st.multiselect('Vælg fire spillere', p, default=m['blue'] + m['red'],
                                        key=f"edit_{d['round']}_{i}", max_selections=4)
                if len(chosen) == 4:
                    if st.button('Byt makkerpar', key=f"swap_{d['round']}_{i}"):
                        m['blue'] = [chosen[0], chosen[2]]
                        m['red'] = [chosen[1], chosen[3]]
                        m['blue_score'] = None
                        m['red_score'] = None
                        # Glem tidligere scores for netop denne kamp ved makkerskift.
                        for colour in ('blue', 'red'):
                            st.session_state.pop(f"{colour}_{d['round']}_{i}", None)
                        save()
                        st.rerun()

        st.divider()
        st.subheader('Gem hele runden')
        antal_klare = sum(
            blue is not None and red is not None and
            (not d['target'] or blue + red == d['target'])
            for blue, red in resultater
        )
        st.caption(f'{antal_klare} af {len(resultater)} kampe har gyldige scores. ' + ('Indtast kun blåt holds point – rødt beregnes automatisk.' if d['target'] else 'Frit pointformat: indtast begge holds point.'))
        if st.button('💾 Gem runde', type='primary', use_container_width=True,
                     key=f"save_round_{d['round']}"):
            fejl = []
            for i, (blue, red) in enumerate(resultater):
                bane = d['matches'][i]['court']
                if blue is None or red is None:
                    fejl.append(f'Bane {bane}: Der mangler et resultat.')
                elif d['target'] and blue + red != d['target']:
                    fejl.append(f"Bane {bane}: Scores skal tilsammen give {d['target']} point.")
            if fejl:
                for besked in fejl:
                    st.error(besked)
            else:
                # Først nu opdateres kampene; der sendes kun ét PATCH til Supabase.
                for m, (blue, red) in zip(d['matches'], resultater):
                    m['blue_score'] = int(blue)
                    m['red_score'] = int(red)
                save()
                st.success(f'Hele runde {d["round"]} er gemt ({len(resultater)} kampe).')
                st.rerun()

        done = all(m['blue_score'] is not None and m['red_score'] is not None
                   for m in d['matches'])
        # Nye rettelser i inputfelter kræver en ny samlet lagring, før næste runde.
        unchanged = done and all(
            (blue, red) == (m['blue_score'], m['red_score'])
            for m, (blue, red) in zip(d['matches'], resultater)
        )
        if d['round'] < d['round_limit']:
            if st.button('Næste runde →', type='primary', use_container_width=True,
                         disabled=not unchanged):
                new_round(d)
                save()
                st.rerun()
            if not unchanged:
                st.caption('Indtast alle scores og tryk Gem runde, før næste runde kan dannes.')
        elif unchanged:
            st.success('Alle ordinære runder er færdige! Se stillingen eller spil finalen herunder.')

        # Finale efter grundspillet. Holdes adskilt fra ordinære kampstatistikker.
        if d['round'] >= d['round_limit'] and unchanged:
            st.divider()
            st.subheader('🏆 Finale')
            finale = d.get('finale')
            if finale is None:
                ranking = standings(d)
                if len(ranking) >= 4:
                    top4 = [r['name'] for r in ranking[:4]]
                    st.caption('De fire bedst placerede i grundspillet kvalificerer sig. Nr. 1 + 3 møder nr. 2 + 4. Finalens resultat ændrer ikke grundspillets stilling.')
                    st.write(f'**Blåt hold:** {top4[0]} + {top4[2]}')
                    st.write(f'**Rødt hold:** {top4[1]} + {top4[3]}')
                    if st.button('Start finale', type='primary', use_container_width=True):
                        d['finale'] = {'blue':[top4[0],top4[2]], 'red':[top4[1],top4[3]], 'blue_score':None, 'red_score':None, 'court':1}
                        save(); st.rerun()
                else:
                    st.warning('Der kræves mindst fire spillere for at afvikle en finale.')
            else:
                st.write('**Blåt hold:** ' + ' + '.join(finale['blue']))
                st.write('**Rødt hold:** ' + ' + '.join(finale['red']))
                if finale['blue_score'] is not None and finale['red_score'] is not None:
                    st.metric('Finaleresultat', f"{finale['blue_score']} – {finale['red_score']}")
                    if finale['blue_score'] == finale['red_score']:
                        st.warning('Finalen står lige. Ret resultatet for at kåre en vinder.')
                    else:
                        winner = finale['blue'] if finale['blue_score'] > finale['red_score'] else finale['red']
                        st.success('🏆 Turneringsvindere: ' + ' & '.join(winner))
                    if st.button('Ret finaleresultat'):
                        finale['blue_score'] = None
                        finale['red_score'] = None
                        save(); st.rerun()
                else:
                    st.caption('Indtast finalens score og gem den. Ved fast pointantal beregnes rødt holds score automatisk.')
                    with st.form('finale_score_form'):
                        blue_f = st.number_input('Blåt hold – finale', min_value=0, max_value=int(d['target']) if d['target'] else 200, value=0, step=1)
                        if d['target']:
                            red_f = int(d['target']) - int(blue_f)
                            st.metric('Rødt hold – automatisk', red_f)
                        else:
                            red_f = st.number_input('Rødt hold – finale', min_value=0, max_value=200, value=0, step=1)
                        if st.form_submit_button('Gem finaleresultat', type='primary', use_container_width=True):
                            finale['blue_score'] = int(blue_f)
                            finale['red_score'] = int(red_f)
                            save(); st.rerun()


with tab_table:
    st.subheader('🏆 Aktuel stilling')
    st.caption(f"Sortering: {d.get('ranking_priority', 'Point først')} · derefter {'scorede point' if d.get('ranking_priority') == 'Sejre først' else 'sejre'}, pointforskel og navn")
    rows=standings(d)
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
        st.markdown('<div class="standing-heading"><span>#</span><span class="standing-person">Spiller</span><span>V</span><span>U</span><span>T</span><span>+/-</span><span>Point</span></div>',unsafe_allow_html=True)
        for i,r in enumerate(rows):
            diff=f'+{r["diff"]}' if r['diff']>0 else str(r['diff'])
            name=html.escape(r['name'])
            st.markdown(
                f'<div class="standing-row {"top" if i==0 else ""}">'
                f'<span>{i+1}.</span><span class="standing-person">{name}</span>'
                f'<span class="standing-value">{r["wins"]}</span>'
                f'<span class="standing-value">{r["draws"]}</span>'
                f'<span class="standing-value">{r["losses"]}</span>'
                f'<span class="standing-value standing-diff">{diff}</span>'
                f'<span class="standing-value standing-points">{r["points"]}</span>'
                '</div>',unsafe_allow_html=True)
        st.caption('V = Vundne · U = Uafgjorte · T = Tabte · +/- = Pointforskel')
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
                    newb=c1.number_input('Blå',min_value=0,
                                         max_value=int(d['target']) if d['target'] else 200,
                                         value=int(m['blue_score'] or 0))
                    if d['target']:
                        newr=int(d['target'])-newb
                        c2.metric('Rød (beregnet)',newr)
                        if m['blue_score'] is None:
                            st.caption('Foreløbig beregning – kampen er ikke gemt som afgjort.')
                    else:
                        newr=c2.number_input('Rød',min_value=0,max_value=200,
                                             value=int(m['red_score'] or 0))
                    if st.form_submit_button('Ret resultat'):
                        if d['target'] and newb+newr!=d['target']:
                            st.error(f'Kampens samlede point skal være {d["target"]}.')
                        else:
                            m['blue_score']=newb;m['red_score']=newr;save();st.success('Resultatet er rettet.');st.rerun()
