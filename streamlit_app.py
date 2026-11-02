# Padel Pappas 10.1 – Rundevalg med knapper
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
    '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'
    '66uLdVc3mVxfq1nqh/pj6XzZFcdU='
)
_court_html = zlib.decompress(base64.b64decode(_COURT_HTML_ZLIB_BASE64))
_component_dir = Path(tempfile.gettempdir()) / 'padel_pappas_court_v93'
_component_dir.mkdir(parents=True, exist_ok=True)
_component_file = _component_dir / 'index.html'
if not _component_file.exists() or _component_file.read_bytes() != _court_html:
    _component_file.write_bytes(_court_html)
st.set_page_config(page_title='Padel Pappas', page_icon='🎾', layout='centered', initial_sidebar_state='collapsed')

court_input = components.declare_component('padel_court_input_v93', path=str(_component_dir))
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
/* Legacy light inactive tabs removed in 6.2. */
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

/* Version 6.1: Alle navigationfaner er grønne med tydelig hvid tekst. */
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"],
.stApp [data-baseweb="tab-list"] [role="tab"],
.stApp .stTabs [data-baseweb="tab"] {
  background:#176458!important;
  color:#ffffff!important;
  -webkit-text-fill-color:#ffffff!important;
  border:1px solid #2f9c8d!important;
  border-radius:11px!important;
  opacity:1!important;
  box-shadow:none!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"] *,
.stApp [data-baseweb="tab-list"] [role="tab"] *,
.stApp .stTabs [data-baseweb="tab"] * {
  color:#ffffff!important;
  -webkit-text-fill-color:#ffffff!important;
  opacity:1!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"][aria-selected="true"],
.stApp [data-baseweb="tab-list"] [role="tab"][aria-selected="true"],
.stApp .stTabs [data-baseweb="tab"][aria-selected="true"] {
  background:#079b80!important;
  border-color:#67ead5!important;
  box-shadow:inset 0 -3px #f5df82!important;
}
.stApp [data-testid="stTabs"] [data-baseweb="tab-list"] {
  background:transparent!important;
}


/* 6.2: Use the same green styling for every tab state, regardless of BaseWeb markup. */
.stApp div[data-testid="stTabs"] div[role="tablist"] button[role="tab"]:not([aria-selected="true"]),
.stApp div[data-testid="stTabs"] div[data-baseweb="tab-list"] button[data-baseweb="tab"]:not([aria-selected="true"]),
.stApp div[data-baseweb="tab-list"] button[role="tab"][aria-selected="false"],
.stApp div[data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="false"] {
  background-color:#176458!important;background-image:none!important;
  border:1px solid #38a899!important;color:#ffffff!important;
  -webkit-text-fill-color:#ffffff!important;opacity:1!important;
}
.stApp div[data-testid="stTabs"] div[role="tablist"] button[role="tab"]:not([aria-selected="true"]) *,
.stApp div[data-testid="stTabs"] div[data-baseweb="tab-list"] button[data-baseweb="tab"]:not([aria-selected="true"]) *,
.stApp div[data-baseweb="tab-list"] button[role="tab"][aria-selected="false"] *,
.stApp div[data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="false"] * {
  color:#ffffff!important;-webkit-text-fill-color:#ffffff!important;opacity:1!important;
}
.stApp div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
.stApp div[data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] {
  background-color:#0b9b83!important;color:#ffffff!important;
  border-color:#65e6ce!important;
}


/* PADEL PAPPAS 7.1 · unified visual system (last stylesheet wins) */
:root{color-scheme:dark}
html,body,.stApp,[data-testid="stAppViewContainer"], [data-testid="stMain"]{
 background:#090d12!important;color:#eff7f7!important;
}
.stApp{background:radial-gradient(circle at 70% -150px,#173c3a 0,#090d12 520px)!important}
[data-testid="stHeader"]{background:transparent!important}
.block-container{max-width:860px!important;padding-top:1.6rem!important;padding-bottom:6rem!important}
[data-testid="stSidebar"], [data-testid="stSidebarContent"]{background:#101a20!important}
.stApp h1,.stApp h2,.stApp h3{color:#f5fbfa!important;letter-spacing:-.025em!important}
.brand{font-size:11px!important;letter-spacing:.18em!important;color:#3be5bd!important}
.hero-title{font-weight:850!important;font-size:clamp(28px,6vw,43px)!important;margin-top:6px!important;letter-spacing:-.035em!important}
.subtitle{color:#a3b6bd!important;font-size:14px!important}
.p7-hero{padding:19px 20px 12px;background:linear-gradient(145deg,#13282c,#10171d 80%);border:1px solid #29454b;border-radius:20px;margin:2px 0 16px}
.p7-id{display:inline-block;background:#142e2e;border:1px solid #326b60;border-radius:8px;padding:7px 10px;margin:6px 0 4px;font-size:12px;color:#bfefe6;overflow-wrap:anywhere}
.p7-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin:12px 0 20px}
.p7-stat{background:#141f27;border:1px solid #293c44;border-radius:14px;padding:12px 7px;text-align:center}
.p7-stat strong{font-size:24px;line-height:1.2;color:#fff;display:block;font-weight:850;font-variant-numeric:tabular-nums}
.p7-stat small{display:block;color:#9fb4bd;font-size:11px;margin-top:5px}
/* Tab buttons: neither white default widgets nor green text on green. */
.stApp [data-testid="stTabs"] div[role="tablist"], .stApp [data-baseweb="tab-list"]{background:transparent!important;gap:8px!important;padding:0!important;overflow-x:auto!important}
.stApp [data-testid="stTabs"] button[role="tab"],.stApp [data-baseweb="tab-list"] button[data-baseweb="tab"]{
 flex:1 0 auto!important;background:#17282b!important;border:1px solid #2b655e!important;border-radius:12px!important;
 color:#d6f2ed!important;-webkit-text-fill-color:#d6f2ed!important;padding:12px 10px!important;font-weight:750!important;opacity:1!important;
}
.stApp [data-testid="stTabs"] button[role="tab"] *, .stApp [data-baseweb="tab-list"] button[data-baseweb="tab"] *{
 color:inherit!important;-webkit-text-fill-color:inherit!important;font-weight:inherit!important;opacity:1!important;
}
.stApp [data-testid="stTabs"] button[role="tab"][aria-selected="true"],.stApp [data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"]{
 background:#0da98f!important;border-color:#4df1cb!important;color:#fff!important;-webkit-text-fill-color:#fff!important;box-shadow:0 4px 17px #04b18c22!important;
}
.stApp [data-testid="stTabs"] [data-baseweb="tab-highlight"],.stApp [data-testid="stTabs"] [data-baseweb="tab-border"]{display:none!important}
/* Court card preserved: enhanced framing only, no changes to interactive component */
.padel-real-card,.court-card{background:#141f27!important;border:1px solid #314c58!important;box-shadow:0 12px 28px #0004!important;border-radius:17px!important}
.padel-real-top,.court-top{font-weight:750!important;color:#f5fcfc!important}
.padel-score-foot{color:#a5b9bc!important}
.padel-player{font-weight:850!important;letter-spacing:-.012em!important;text-shadow:0 2px 4px #000!important}
/* Modern leader board and podium */
.podium{gap:10px!important;margin:18px 0 22px!important}
.podium-card{background:#18232b!important;border:1px solid #364450!important;border-radius:18px!important;box-shadow:0 8px 24px #0003!important;padding:16px 5px!important}
.podium-card.winner{background:linear-gradient(155deg,#164c44,#193029)!important;border-color:#42d4ac!important;padding:25px 5px!important}
.podium-name{color:#f6fbfc!important;font-size:clamp(12px,3.3vw,15px)!important}
.podium-score{font-size:clamp(22px,5.5vw,29px)!important}
.standing-heading{color:#b6cbd0!important;padding:11px 9px!important}
.standing-row{background:#141f26!important;border:1px solid #2d3e47!important;border-radius:13px!important;min-height:45px!important;box-shadow:0 2px 8px #0002}
.standing-row.top{background:#16433b!important;border-color:#37bb9f!important}
.standing-row .standing-person{color:#fff!important}
/* Forms and actions */
.stApp [data-testid="stButton"] button[kind="primary"],.stApp [data-testid="stFormSubmitButton"] button[kind="primary"]{
 background:#0dab90!important;color:#fff!important;border:1px solid #37dbc0!important;border-radius:12px!important;min-height:48px!important;font-weight:780!important;
}
.stApp [data-testid="stButton"] button[kind="secondary"],.stApp [data-testid="stFormSubmitButton"] button[kind="secondary"]{
 background:#1d2a33!important;color:#f1f8f8!important;border:1px solid #42606c!important;border-radius:12px!important;
}
.stApp [data-testid="stButton"] button *, .stApp [data-testid="stFormSubmitButton"] button *{
 color:inherit!important;-webkit-text-fill-color:inherit!important
}
[data-testid="stExpander"]{border:1px solid #354b53!important;border-radius:13px!important;background:#132027!important}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary *{color:#fff!important;-webkit-text-fill-color:#fff!important}
@media(max-width:520px){
 .block-container{padding-left:12px!important;padding-right:12px!important;padding-top:.8rem!important}
 .p7-hero{padding:15px 14px 12px;border-radius:16px}
 .p7-stats{gap:6px}.p7-stat{padding:11px 4px}.p7-stat strong{font-size:21px}
 .stApp [data-testid="stTabs"] button[role="tab"]{font-size:13px!important;padding:11px 8px!important}
 .standing-row{padding-left:6px!important;padding-right:6px!important}
}


/* PADEL PAPPAS 7.1 - MOBILE EDITION, final overrides */
[data-testid="stHeader"]{background:#090d12!important;min-height:54px!important;box-shadow:0 1px 0 #24333a!important;z-index:999!important}
[data-testid="stToolbar"]{background:#090d12!important}
[data-testid="stMainBlockContainer"],.block-container{padding-top:4.3rem!important}
.stApp [data-testid="stVerticalBlock"]{gap:.65rem}
.p7-hero{padding:14px 17px 12px!important;margin:0 0 8px!important}
.p7-hero .hero-title{font-size:clamp(27px,6vw,38px)!important;margin:3px 0 4px!important}
.p7-hero .subtitle{margin:0!important}
.p7-stats{margin:7px 0 8px!important}
.p7-stat{padding:9px 5px!important}
.p7-stat strong{font-size:22px!important}
.p7-stat small{margin-top:2px!important}
.p71-section-title{font-size:clamp(24px,6vw,32px);font-weight:850;color:#fff;line-height:1.2;letter-spacing:-.025em;margin:5px 0 4px}
.p71-section-title span{font-size:.57em;font-weight:600;color:#a8bfbe}
.stApp [data-testid="stTabs"] div[role="tablist"]{margin:0 0 4px!important}
.stApp [data-testid="stTabs"] button[role="tab"]{min-height:42px!important}
.stApp [data-testid="stCaptionContainer"]{margin-top:0!important;margin-bottom:0!important}
.stApp [data-testid="stPopover"]{margin-top:0!important;margin-bottom:5px!important}
.stApp [data-testid="stButton"] button{min-height:44px!important}
@media(max-width:520px){
 [data-testid="stMainBlockContainer"],.block-container{padding-top:4.5rem!important;padding-left:12px!important;padding-right:12px!important}
 .p7-hero{padding:12px 12px 10px!important;border-radius:15px!important}
 .p7-hero .hero-title{font-size:29px!important}
 .p7-hero .subtitle{font-size:12px!important;line-height:1.4!important}
 .p7-id{padding:5px 8px!important;font-size:11px!important;margin-top:5px!important}
 .p7-stat{border-radius:11px!important;padding:8px 2px!important}
 .p7-stat strong{font-size:20px!important}
 .p7-stat small{font-size:10px!important}
 .p7-stats{gap:6px!important}
 .stApp [data-testid="stTabs"] button[role="tab"]{padding:8px 5px!important;font-size:12px!important;min-height:39px!important}
 .p71-section-title{font-size:25px!important}
 .stApp [data-testid="stVerticalBlock"]{gap:.45rem!important}
}


/* PADEL PAPPAS 7.2 - tab navigation matching the three stat tiles */
.stApp [data-testid="stTabs"] [role="tablist"],
.stApp [data-baseweb="tab-list"] {
 display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;
 gap:9px!important;overflow:visible!important;width:100%!important;
 background:transparent!important;border:0!important;padding:0!important;
 margin:0 0 7px!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"],
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"]{
 box-sizing:border-box!important;display:flex!important;justify-content:center!important;align-items:center!important;
 min-width:0!important;width:100%!important;max-width:100%!important;
 min-height:68px!important;margin:0!important;padding:12px 3px!important;
 background:#141f27!important;border:1px solid #293c44!important;
 border-radius:14px!important;box-shadow:none!important;
 color:#e9f3f5!important;-webkit-text-fill-color:#e9f3f5!important;
 font-size:clamp(12px,3vw,16px)!important;font-weight:730!important;line-height:1.2!important;
 white-space:nowrap!important;text-align:center!important;opacity:1!important;
 transition:border-color .15s ease,background .15s ease!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"] *,
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"] * {
 color:inherit!important;-webkit-text-fill-color:inherit!important;
 font-weight:inherit!important;white-space:nowrap!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"][aria-selected="true"],
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]{
 background:#16292c!important;border:2px solid #31d7b6!important;
 color:#fff!important;-webkit-text-fill-color:#fff!important;
 box-shadow:inset 0 0 0 1px #31d7b61a!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"]:hover{
 border-color:#54a99a!important;
}
.stApp [data-testid="stTabs"] [data-baseweb="tab-highlight"],
.stApp [data-testid="stTabs"] [data-baseweb="tab-border"]{display:none!important;}
.stApp [data-baseweb="tab-highlight"],
.stApp [data-baseweb="tab-border"],
.stApp [data-testid="stTabs"] [role="tablist"]::before,
.stApp [data-testid="stTabs"] [role="tablist"]::after,
.stApp [data-testid="stTabs"] [role="tab"]::before,
.stApp [data-testid="stTabs"] [role="tab"]::after{display:none!important;content:none!important;height:0!important;border:0!important;background:none!important;}
.stApp [data-testid="stTabs"] [role="tablist"]{border-bottom:0!important;box-shadow:none!important;background-image:none!important;}
@media(max-width:520px){
 .stApp [data-testid="stTabs"] [role="tablist"],.stApp [data-baseweb="tab-list"]{gap:6px!important;}
 .stApp [data-testid="stTabs"] [role="tablist"] [role="tab"],
 .stApp [data-baseweb="tab-list"] [data-baseweb="tab"]{
  min-height:60px!important;padding:9px 1px!important;font-size:clamp(11px,3.05vw,14px)!important;
  border-radius:12px!important;
 }
}


/* 7.4: React-Aria / Streamlit tabs: remove the native accent indicator.
   The active card's turquoise border remains the only selection indicator. */
.stApp [data-testid="stTabs"] [role="tablist"],
.stApp [data-testid="stTabs"] [data-baseweb="tab-list"] {
  position:relative!important; border-bottom:0!important;
  box-shadow:none!important; background-image:none!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] > [data-baseweb="tab-highlight"],
.stApp [data-testid="stTabs"] [data-baseweb="tab-highlight"],
.stApp [data-testid="stTabs"] [data-baseweb="tab-border"],
.stApp [data-testid="stTabs"] [role="tablist"] [class*="highlight"],
.stApp [data-testid="stTabs"] [role="tablist"] [class*="indicator"],
.stApp [data-testid="stTabs"] [role="tablist"] [class*="Indicator"] {
  display:none!important; opacity:0!important; visibility:hidden!important;
  height:0!important; border:0!important; box-shadow:none!important;
}
/* Opaque masking strip below the cards also covers Streamlit's animated
   underline when a future release changes the indicator element again. */
.stApp [data-testid="stTabs"] [role="tablist"]::after,
.stApp [data-testid="stTabs"] [data-baseweb="tab-list"]::after {
  content:""!important; display:block!important; position:absolute!important;
  bottom:-8px!important; left:0!important; right:0!important; height:9px!important;
  background:#090d12!important; border:0!important; border-radius:0!important;
  pointer-events:none!important; z-index:50!important;
}


/* PADEL PAPPAS 8.0 · LIGHT EDITION · placed last to override legacy dark rules */
:root{color-scheme:light!important}
html,body,[data-testid="stAppViewContainer"],.stApp,[data-testid="stMain"],[data-testid="stMainBlockContainer"]{
 background:#FAFBFC!important;color:#182431!important;
}
[data-testid="stHeader"],[data-testid="stToolbar"]{background:#FAFBFC!important;box-shadow:0 1px 0 #E8EEF1!important}
[data-testid="stSidebar"],[data-testid="stSidebarContent"]{background:#F0F5F6!important;color:#172A2D!important}
.stApp p,.stApp li,.stApp label,.stApp span:not([class*="name"]):not(.podium-rank),
.stApp [data-testid="stMarkdownContainer"]{color:#26363D}
.stApp h1,.stApp h2,.stApp h3,.stApp h4{color:#17242E!important}
.stApp [data-testid="stCaptionContainer"],.stApp [data-testid="stCaptionContainer"] p{color:#64757E!important}
.stApp a{color:#117A78!important}
.stApp [data-testid="stMarkdownContainer"] hr,.stApp hr{border-color:#E5ECF0!important}
.p7-hero{background:linear-gradient(118deg,#FFFFFF 45%,#E6F7F5 100%)!important;border:1px solid #E0EBEE!important;border-radius:20px!important;box-shadow:0 7px 25px #1934440c!important}
.p7-hero .hero-title,.hero-title{color:#162631!important}
.p7-hero .subtitle,.subtitle{color:#6A7C85!important}
.brand{color:#147E75!important}
.p7-id{background:#E7F6F3!important;border:1px solid #B7DBD6!important;color:#17695E!important}
.p7-stat,.p7-stats .p7-stat{background:#FFFFFF!important;border:1px solid #DEE9ED!important;border-radius:16px!important;box-shadow:0 4px 18px #213d4a0d!important}
.p7-stat strong{color:#192B33!important}
.p7-stat small{color:#697D85!important}
.p71-section-title{color:#14252C!important}
.p71-section-title span{color:#69808A!important}
.stApp [data-testid="stTabs"] [role="tablist"],.stApp [data-baseweb="tab-list"]{border:0!important;background:transparent!important;box-shadow:none!important}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"],
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"]{
 background:#FFFFFF!important;border:1px solid #DCE8EA!important;color:#263B42!important;
 -webkit-text-fill-color:#263B42!important;border-radius:15px!important;box-shadow:0 4px 15px #10262f0b!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"][aria-selected="true"],
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]{
 background:#137F75!important;border:2px solid #137F75!important;
 color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;box-shadow:0 4px 14px #086f652b!important;
}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"] *,
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"] *{color:inherit!important;-webkit-text-fill-color:inherit!important}
.stApp [data-baseweb="tab-highlight"],.stApp [data-baseweb="tab-border"],
.stApp [data-testid="stTabs"] [class*="highlight"],.stApp [data-testid="stTabs"] [class*="indicator"]{display:none!important;height:0!important;opacity:0!important}
.padel-real-card,.court-card{background:#FFFFFF!important;border:1px solid #DFEAEE!important;border-radius:18px!important;box-shadow:0 8px 27px #1c384016!important}
.padel-real-top,.court-top{color:#18343A!important}
.padel-score-foot{color:#627781!important}
.standing-row{background:#FFFFFF!important;border:1px solid #E1EBED!important;color:#20323B!important;box-shadow:0 3px 12px #2439450c!important}
.standing-row.top{background:#EAF8F4!important;border-color:#9ED9CD!important}
.standing-row .standing-person{color:#172B34!important}
.standing-heading{color:#4A606A!important}
.podium-card{background:#FFFFFF!important;border:1px solid #DCE7EA!important;box-shadow:0 5px 18px #17292f12!important}
.podium-card.winner{background:linear-gradient(150deg,#DDF5ED,#F9FFFC)!important;border-color:#73C5B0!important}
.podium-name,.podium-score{color:#19313A!important}
.podium-label{color:#546B72!important}
[data-testid="stExpander"]{background:#FFFFFF!important;border:1px solid #DFE9ED!important;border-radius:15px!important}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *{color:#233840!important;-webkit-text-fill-color:#233840!important}
.stApp [data-testid="stButton"] button[kind="primary"],.stApp [data-testid="stFormSubmitButton"] button[kind="primary"]{
 background:#138377!important;color:#FFFFFF!important;border:1px solid #0F786E!important;box-shadow:0 3px 12px #07695c22!important;
}
.stApp [data-testid="stButton"] button[kind="secondary"],.stApp [data-testid="stFormSubmitButton"] button[kind="secondary"]{
 background:#ECF8F6!important;color:#17665D!important;border:1px solid #92C9C2!important;box-shadow:none!important;
}
.stApp [data-testid="stButton"] button[kind="secondary"] *,.stApp [data-testid="stFormSubmitButton"] button[kind="secondary"] *{color:#17665D!important;-webkit-text-fill-color:#17665D!important}
.stApp [data-testid="stButton"] button[kind="primary"] *,.stApp [data-testid="stFormSubmitButton"] button[kind="primary"] *{color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important}
.stApp [data-testid="stTextInput"] input,.stApp [data-testid="stNumberInput"] input,
.stApp [data-testid="stTextArea"] textarea,.stApp [data-baseweb="select"]>div{
 background:#FFFFFF!important;color:#172E36!important;-webkit-text-fill-color:#172E36!important;border-color:#D9E5E9!important;
}
.stApp [data-testid="stTextInput"] input::placeholder{color:#8B9BA2!important}
.stApp [data-baseweb="popover"],.stApp [data-baseweb="menu"],.stApp [role="listbox"]{background:#FFFFFF!important;color:#1D343A!important}
.stApp [data-testid="stDataFrame"],.stApp [data-testid="stTable"]{background:#FFFFFF!important;color:#1C3239!important}
.stApp [data-testid="stAlert"]{border-radius:12px!important}
@media(max-width:520px){
 .p7-hero{border-radius:15px!important}
 .p7-stat{border-radius:12px!important}
}


/* PADEL PAPPAS 8.2 — LÆSBARHED I LYS VERSION. Sidste CSS-regler vinder. */
.stApp section[data-testid="stSidebar"],
.stApp [data-testid="stSidebarContent"] {
  background:#F0F5F6!important;
  color:#182D35!important;
}
.stApp section[data-testid="stSidebar"] label,
.stApp section[data-testid="stSidebar"] label *,
.stApp section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
.stApp section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
.stApp section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
.stApp section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
.stApp section[data-testid="stSidebar"] .stMarkdown p,
.stApp section[data-testid="stSidebar"] .stRadio p,
.stApp section[data-testid="stSidebar"] .stRadio label,
.stApp section[data-testid="stSidebar"] div[role="radiogroup"] label *,
.stApp section[data-testid="stSidebar"] h1,
.stApp section[data-testid="stSidebar"] h2,
.stApp section[data-testid="stSidebar"] h3,
.stApp section[data-testid="stSidebar"] small {
  color:#243840!important;-webkit-text-fill-color:#243840!important;opacity:1!important;
}
.stApp section[data-testid="stSidebar"] [data-testid="stTextInput"] input,
.stApp section[data-testid="stSidebar"] [data-testid="stTextArea"] textarea,
.stApp section[data-testid="stSidebar"] [data-testid="stNumberInput"] input{
  background:#FFFFFF!important;color:#1C3038!important;
  -webkit-text-fill-color:#1C3038!important;opacity:1!important;
}
.stApp section[data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder,
.stApp section[data-testid="stSidebar"] [data-testid="stTextArea"] textarea::placeholder{
  color:#667983!important;-webkit-text-fill-color:#667983!important;opacity:1!important;
}
.stApp section[data-testid="stSidebar"] button[kind="secondary"],
.stApp section[data-testid="stSidebar"] button:not([kind="primary"]){
  background:#E7F4F2!important;color:#146A60!important;
  -webkit-text-fill-color:#146A60!important;border-color:#9ACCC4!important;
}
.stApp section[data-testid="stSidebar"] button[kind="secondary"] *,
.stApp section[data-testid="stSidebar"] button:not([kind="primary"]) *{
  color:#146A60!important;-webkit-text-fill-color:#146A60!important;
}
.stApp section[data-testid="stSidebar"] button[kind="primary"] *,
.stApp section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button[kind="primary"] *{
  color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;
}
.stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"] *,
.stApp [data-testid="stAlert"] p,
.stApp [data-testid="stNotification"] p {
  color:#243B45!important;-webkit-text-fill-color:#243B45!important;opacity:1!important;
}
.stApp [data-testid="stAlert"]{
  background:#E5F2FF!important;border:1px solid #BDD9F3!important;
}
.stApp [data-testid="stAlert"] svg{color:#23567C!important}
.stApp [data-testid="stTabs"] [role="tablist"]::after{
  background:#FAFBFC!important;
}
/* SVG, ikoner og text i rubrikker på den lyse hovedside. */
.stApp [data-testid="stExpander"] summary,
.stApp [data-testid="stExpander"] summary *{
  color:#223A43!important;-webkit-text-fill-color:#223A43!important;
}


/* Padel Pappas 9.0 - mobile light polish; appended last for reliable specificity */
.pp9-progress{background:#fff;border:1px solid #d7e5e9;border-radius:17px;padding:14px;margin:12px 0 10px;box-shadow:0 3px 14px #263b4c0b}
.pp9-progress-heading{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:10px;color:#213842;font-size:14px}
.pp9-progress-heading span{color:#138b7d;font-size:12px;font-weight:700}
.pp9-track{height:8px;background:#e1efed;border-radius:99px;overflow:hidden}
.pp9-fill{height:100%;background:#10a58e;border-radius:99px;transition:width .25s}
.pp9-history-mini{display:flex;align-items:start;gap:10px;margin:7px 0;padding:11px;background:white;border:1px solid #deeaec;border-radius:12px;color:#243940;font-size:13px}
.pp9-history-mini b{min-width:58px}.pp9-history-mini span{overflow-wrap:anywhere}
.pp9-history-mini strong{color:#0e8979}
.pp9-saved{display:inline-block;font-size:12px;font-weight:800;color:#0b8874;background:#e2f7f0;border:1px solid #a9dfd1;border-radius:999px;padding:3px 10px;margin:0 0 1px 4px}
.pp9-winners{text-align:center;background:linear-gradient(130deg,#edfaf5,#fff8df);border:2px solid #33b99d;border-radius:18px;padding:24px 14px;margin:12px 0;color:#144f48;box-shadow:0 10px 30px #236b5215}
.pp9-winners>div{font-size:13px;letter-spacing:.08em;font-weight:850}.pp9-winners strong{display:block;color:#163d3d;font-size:clamp(22px,5vw,35px);margin:12px 0}.pp9-winners small{color:#5c7977}
/* More compact court surroundings and side-by-side round/points widgets */
.stApp [data-testid="stPopover"]{margin:0!important}
.stApp [data-testid="stPopover"] button{min-height:37px!important;border-radius:11px!important}
.stApp [data-testid="stTabs"] [role="tablist"]{border-bottom:0!important}
.stApp [data-testid="stTabs"] [role="tablist"]:after{display:none!important}
.stApp .stTabs [data-baseweb="tab-highlight"],.stApp [data-baseweb="tab-border"]{display:none!important}
.stApp section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
.stApp section[data-testid="stSidebar"] div[role="radiogroup"] label *,
.stApp section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *{color:#243840!important;-webkit-text-fill-color:#243840!important}
@media(max-width:520px){.pp9-progress{padding:11px 12px;margin:7px 0 5px}.pp9-history-mini{font-size:12px}}

/* PADEL PAPPAS 9.1 – konsekvent afstand, tydelige medaljeplaceringer */
.p7-stats{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px!important;margin:14px 0 12px!important;align-items:stretch!important}
.p7-stat{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;min-height:104px!important;box-sizing:border-box!important;margin:0!important}
.pp9-progress{margin:0 0 12px!important}
.stApp [data-testid="stTabs"] [role="tablist"],
.stApp [data-baseweb="tab-list"]{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px!important;margin:0 0 12px!important;padding:0!important;align-items:stretch!important;border:0!important;background:transparent!important}
.stApp [data-testid="stTabs"] [role="tablist"] [role="tab"],
.stApp [data-baseweb="tab-list"] [data-baseweb="tab"]{min-height:104px!important;margin:0!important;box-sizing:border-box!important;display:flex!important;align-items:center!important;justify-content:center!important;border-radius:16px!important}
/* En medalje erstatter placeringstallet. Farvet kant på hele spillerens række. */
.standing-heading,.standing-row{grid-template-columns:38px minmax(67px,1fr) 26px 26px 26px 42px 43px!important}
.standing-row.gold{background:#FFF8E5!important;border:2px solid #D8AF45!important;box-shadow:0 4px 14px #C7962920!important}
.standing-row.silver{background:#F4F7FA!important;border:2px solid #AAB8C7!important;box-shadow:0 4px 14px #70829418!important}
.standing-row.bronze{background:#FFF1E7!important;border:2px solid #C78C66!important;box-shadow:0 4px 14px #B66B3818!important}
.standing-row.gold .standing-person,.standing-row.silver .standing-person,.standing-row.bronze .standing-person{color:#1A313A!important}
.standing-rank{font-size:21px!important;font-weight:850!important;text-align:center!important;line-height:1.2!important}
@media(max-width:520px){
 .p7-stats{gap:7px!important;margin:9px 0 7px!important}
 .p7-stat{min-height:76px!important}
 .pp9-progress{margin:0 0 7px!important}
 .stApp [data-testid="stTabs"] [role="tablist"],.stApp [data-baseweb="tab-list"]{gap:7px!important;margin:0 0 8px!important}
 .stApp [data-testid="stTabs"] [role="tablist"] [role="tab"],.stApp [data-baseweb="tab-list"] [data-baseweb="tab"]{min-height:76px!important}
 .standing-heading,.standing-row{grid-template-columns:30px minmax(58px,1fr) 22px 22px 22px 35px 37px!important;gap:3px!important}
 .standing-rank{font-size:18px!important}
}

/* 9.2 — diskret redigering under banekortet */
.stApp [class*="st-key-court_edit_actions_"] {
  display:flex!important;justify-content:flex-end!important;
  margin-top:-12px!important;margin-bottom:8px!important;
  padding-right:12px!important;position:relative!important;z-index:2!important;
}
.stApp [class*="st-key-court_edit_actions_"] [data-testid="stPopover"] button,
.stApp [class*="st-key-court_edit_actions_"] button {
  background:transparent!important;color:#537780!important;-webkit-text-fill-color:#537780!important;
  border:0!important;box-shadow:none!important;min-height:29px!important;
  padding:2px 7px!important;font-size:12px!important;font-weight:600!important;
}
.stApp [class*="st-key-court_edit_actions_"] button *{color:#537780!important;-webkit-text-fill-color:#537780!important}
.stApp [class*="st-key-court_edit_actions_"] button:hover{background:#edf7f5!important;color:#156f65!important}

/* 9.3: Rediger hold er en diskret del af kampkortets fod, ikke en bred handlingsknap. */
.stApp [class*="st-key-court_edit_actions_"] {
  display:flex!important;
  justify-content:flex-end!important;
  align-items:center!important;
  width:calc(100% - 20px)!important;
  box-sizing:border-box!important;
  padding:0 10px 0 0!important;
  margin:-34px 10px 14px!important;
  position:relative!important;
  z-index:5!important;
  background:transparent!important;
  border:0!important;
  box-shadow:none!important;
}
.stApp [class*="st-key-court_edit_actions_"] [data-testid="stPopover"] button,
.stApp [class*="st-key-court_edit_actions_"] button {
  min-height:26px!important;
  padding:3px 8px!important;
  border:1px solid transparent!important;
  border-radius:8px!important;
  background:#f4faf9!important;
  color:#42777d!important;
  -webkit-text-fill-color:#42777d!important;
  font-size:12px!important;
  font-weight:650!important;
  box-shadow:none!important;
}
.stApp [class*="st-key-court_edit_actions_"] button:hover{border-color:#d3e8e6!important;background:#e9f5f2!important}
@media(max-width:520px){
 .stApp [class*="st-key-court_edit_actions_"] {margin-top:-30px!important;margin-bottom:12px!important;padding-right:3px!important}
 .stApp [class*="st-key-court_edit_actions_"] button{font-size:11px!important}
}

/* 9.4: lyse, ensartede inputrammer i Streamlit-formularer.
   Bevar indbyggede scorefelter på banerne uændret. */
.stApp section[data-testid="stSidebar"] [data-testid="stTextInput"] [data-baseweb="input"],
.stApp section[data-testid="stSidebar"] [data-testid="stTextInput"] [data-baseweb="base-input"],
.stApp section[data-testid="stSidebar"] [data-testid="stTextArea"] [data-baseweb="textarea"],
.stApp section[data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"],
.stApp section[data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="base-input"],
.stApp section[data-testid="stSidebar"] [data-baseweb="select"] > div,
.stApp section[data-testid="stSidebar"] input,
.stApp section[data-testid="stSidebar"] textarea {
 background:#fff!important;
 color:#20343d!important;-webkit-text-fill-color:#20343d!important;
 border-color:#CFDEE1!important;
 outline:none!important;
 box-shadow:none!important;
}
.stApp section[data-testid="stSidebar"] [data-testid="stTextInput"] [data-baseweb="input"],
.stApp section[data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"],
.stApp section[data-testid="stSidebar"] [data-testid="stTextArea"] [data-baseweb="textarea"],
.stApp section[data-testid="stSidebar"] [data-baseweb="select"] > div {
 border:1px solid #CFDEE1!important;
 border-radius:13px!important;
 box-shadow:none!important;
 overflow:hidden!important;
}
.stApp section[data-testid="stSidebar"] [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
.stApp section[data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within,
.stApp section[data-testid="stSidebar"] [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within,
.stApp section[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
 border-color:#63B8A9!important;
 box-shadow:0 0 0 3px rgba(32,155,134,.16)!important;
 outline:none!important;
}
.stApp section[data-testid="stSidebar"] input:focus,
.stApp section[data-testid="stSidebar"] textarea:focus {
 outline:none!important;box-shadow:none!important;
}
.stApp section[data-testid="stSidebar"] input::placeholder,
.stApp section[data-testid="stSidebar"] textarea::placeholder {
 color:#778C94!important;-webkit-text-fill-color:#778C94!important;opacity:1!important;
}


/* PADEL PAPPAS 9.5: Historik i samme lyse tema som baner og stilling. */
.stApp [class*="st-key-pp95_history"] [data-testid="stExpander"],
.stApp [class*="st-key-pp95_history"] details,
.stApp [class*="st-key-pp95_history"] [data-testid="stVerticalBlockBorderWrapper"] {
  background:#FFFFFF!important;
  color:#20343D!important;
  border:1px solid #DBE7EB!important;
  border-radius:16px!important;
  box-shadow:0 4px 18px rgba(29,63,72,.06)!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stExpander"] details,
.stApp [class*="st-key-pp95_history"] [data-testid="stExpander"] [data-testid="stExpanderDetails"],
.stApp [class*="st-key-pp95_history"] [data-testid="stExpander"] [data-testid="stExpanderHeader"],
.stApp [class*="st-key-pp95_history"] [data-testid="stExpander"] summary,
.stApp [class*="st-key-pp95_history"] [data-testid="stExpander"] summary * {
  background:#FFFFFF!important;
  color:#20343D!important;
  -webkit-text-fill-color:#20343D!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stForm"],
.stApp [class*="st-key-pp95_history"] [data-testid="stForm"] > div,
.stApp [class*="st-key-pp95_history"] form {
  background:#F6FAFB!important;
  color:#20343D!important;
  border:1px solid #DFEAED!important;
  border-radius:13px!important;
  box-shadow:none!important;
}
.stApp [class*="st-key-pp95_history"] p,
.stApp [class*="st-key-pp95_history"] label,
.stApp [class*="st-key-pp95_history"] label *,
.stApp [class*="st-key-pp95_history"] [data-testid="stMarkdownContainer"] *,
.stApp [class*="st-key-pp95_history"] [data-testid="stCaptionContainer"] *,
.stApp [class*="st-key-pp95_history"] [data-testid="stMetric"] *,
.stApp [class*="st-key-pp95_history"] [data-testid="stMetricValue"] {
  color:#20343D!important;
  -webkit-text-fill-color:#20343D!important;
  opacity:1!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stNumberInput"] input,
.stApp [class*="st-key-pp95_history"] [data-testid="stNumberInput"] [data-baseweb="input"],
.stApp [class*="st-key-pp95_history"] [data-testid="stNumberInput"] [data-baseweb="base-input"] {
  background:#FFFFFF!important;
  color:#20343D!important;
  -webkit-text-fill-color:#20343D!important;
  border-color:#CFDEE1!important;
  box-shadow:none!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stNumberInput"] button{
  background:#EAF3F4!important;
  border-color:#D4E3E7!important;
  color:#21434C!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stNumberInput"] button svg{
  color:#21434C!important;
  stroke:#21434C!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stFormSubmitButton"] button{
  background:#E7F5F2!important;
  border:1px solid #96CCC3!important;
  color:#166B61!important;
  -webkit-text-fill-color:#166B61!important;
  border-radius:11px!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stFormSubmitButton"] button *{
  color:#166B61!important;-webkit-text-fill-color:#166B61!important;
}
.stApp [class*="st-key-pp95_history"] [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within{
  border-color:#62B8A8!important;box-shadow:0 0 0 3px rgba(32,155,134,.13)!important;
}


/* 9.6: Streamlit input har flere indlejrede rammer; fjern den sorte yderste
   kant fra ALLE lag i både sidebar og formularer, også ved fokus. */
.stApp [data-testid="stTextInput"] [data-testid="stTextInputRootElement"],
.stApp [data-testid="stTextInput"] [data-baseweb="input"],
.stApp [data-testid="stTextInput"] [data-baseweb="base-input"],
.stApp [data-testid="stTextInput"] [data-baseweb="input"] > div,
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stTextArea"] [data-baseweb="textarea"],
.stApp [data-testid="stTextArea"] textarea,
.stApp [data-testid="stNumberInput"] [data-baseweb="input"],
.stApp [data-testid="stNumberInput"] [data-baseweb="base-input"] {
 background:#FFFFFF!important;
 color:#20343D!important;-webkit-text-fill-color:#20343D!important;
 border-color:#CFDEE1!important;
 outline:0!important;
 box-shadow:none!important;
 -webkit-box-shadow:none!important;
}
/* Kun EN synlig ramme: input-containeren, ikke flere indlejrede lag. */
.stApp [data-testid="stTextInput"] [data-baseweb="input"],
.stApp [data-testid="stTextArea"] [data-baseweb="textarea"],
.stApp [data-testid="stNumberInput"] [data-baseweb="input"] {
 border:1px solid #CFDEE1!important;border-radius:13px!important;
 overflow:hidden!important;box-shadow:none!important;
}
.stApp [data-testid="stTextInput"] [data-baseweb="base-input"],
.stApp [data-testid="stTextInput"] [data-baseweb="base-input"] > div,
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stTextArea"] textarea,
.stApp [data-testid="stNumberInput"] input {
 border:0!important;outline:0!important;box-shadow:none!important;
}
.stApp [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
.stApp [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within,
.stApp [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
 border-color:#55B6A3!important;
 box-shadow:0 0 0 3px rgba(40,160,139,.14)!important;
}
/* Sidepanel i nyere Streamlit kan bruge section, aside eller div. */
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"],
[data-testid="stSidebarContent"] [data-testid="stTextInputRootElement"]{
 border:0!important;box-shadow:none!important;outline:0!important;
}


/* 9.7 HISTORIK: Samme blå/røde bane, samme kort og navnerytme som Kampe */
.pp97-card{background:#fff;border:1px solid #deeaed;border-radius:18px;padding:8px 9px 11px;margin:12px 0 3px;box-shadow:0 4px 18px #142e390b}
.pp97-top{display:flex;justify-content:space-between;align-items:center;margin:2px 3px 9px;color:#26444c;font-size:14px}
.pp97-pill{border:1px solid #aad8d0;background:#e9f7f4;color:#17655e;border-radius:30px;padding:6px 11px}
.pp97-badge{font-size:12px;font-weight:700;border-radius:12px;padding:5px 8px;background:#e3f5ef;color:#157363}
.pp97-badge.pending{background:#f4f6f7;color:#687c83}
.pp97-court{position:relative;aspect-ratio:2/1;min-height:138px;max-height:225px;width:100%;border:3px solid #a8bec3;border-radius:12px;overflow:hidden;background:linear-gradient(90deg,#165b91 0%,#194a7a 49.7%,#792c38 50.3%,#95323f 100%)}
.pp97-court::before{content:'';position:absolute;inset:8px;border:2px solid #fff9;pointer-events:none}
.pp97-net{position:absolute;left:50%;top:0;bottom:0;transform:translateX(-50%);width:5px;background:repeating-linear-gradient(to bottom,#f9ffff 0 4px,#688089 4px 7px);z-index:2}
.pp97-service{position:absolute;top:8px;bottom:8px;width:2px;background:#e6f6fbdc;z-index:1}
.pp97-service.left{left:15.25%}.pp97-service.right{left:84.75%}
.pp97-midline{position:absolute;top:50%;height:2px;background:#e6f6fbdc;z-index:1}
.pp97-midline.left{left:15.25%;width:34.75%}.pp97-midline.right{left:50%;width:34.75%}
.pp97-vs{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:6;background:#102c32;border:2px solid #51dec4;border-radius:100px;width:36px;height:36px;display:grid;place-items:center;font-size:12px;font-weight:800;color:white!important}
.pp97-team{position:absolute;top:14%;bottom:14%;width:43%;display:flex;flex-direction:column;align-items:center;justify-content:space-between;z-index:4;pointer-events:none}
.pp97-team.blue{left:0}.pp97-team.red{right:0}
.pp97-name{color:#fff!important;-webkit-text-fill-color:#fff!important;letter-spacing:-.02em;text-align:center;max-width:98%;border-radius:8px;background:#082239b5;padding:6px 8px;font-weight:800;line-height:1.15;font-size:clamp(15px,3.1vw,22px);overflow-wrap:anywhere;text-shadow:0 1px 2px #000}
.pp97-team.red .pp97-name{background:#401520b5}
.pp97-score{position:absolute;top:50%;transform:translateY(-50%);width:24%;max-width:145px;min-width:66px;z-index:5;border-radius:10px;height:46px;display:flex;align-items:center;justify-content:center;gap:4px;font-size:23px;font-weight:850;color:#fff!important;-webkit-text-fill-color:#fff!important;line-height:1;box-shadow:0 4px 13px #001b,0 0 0 2px #ffffff18}
.pp97-score.blue{left:3.8%;background:rgba(10,50,94,.94);border:3px solid #76c5ff}
.pp97-score.red{right:3.8%;background:rgba(121,32,49,.96);border:3px solid #ff9daa}
.pp97-score.pending{font-size:20px}
.pp97-foot{text-align:center;color:#617880;font-size:12px;margin:8px 0 2px}
.pp97-edit{display:flex;justify-content:flex-end;margin:-4px 5px 11px}
.pp97-edit [data-testid="stPopover"] button{font-size:13px!important;min-height:30px!important;padding:3px 10px!important;background:transparent!important;border:0!important;color:#526c77!important;box-shadow:none!important}
@media(max-width:500px){
 .pp97-court{min-height:135px;max-height:205px}
 .pp97-team{top:12%;bottom:12%}
 .pp97-name{padding:3px 4px;font-size:clamp(14px,3.45vw,18px)}
 .pp97-score{height:42px;font-size:19px;width:23%;min-width:60px}
}


/* PADEL PAPPAS 9.8 – historik: lys rundevælger med tilpasset fokus. */
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] > div,
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] [data-baseweb="select"] > div,
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] [data-baseweb="input"],
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] [data-baseweb="base-input"] {
 background:#FFFFFF!important;color:#213841!important;-webkit-text-fill-color:#213841!important;
 border:1px solid #D7E5E9!important;border-radius:13px!important;
 box-shadow:none!important;outline:none!important;
}
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] > div:focus-within {
 border-color:#41B8A2!important;box-shadow:0 0 0 3px rgba(27,154,132,.15)!important;
 outline:none!important;
}
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] input,
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] span,
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] div,
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] svg {
 color:#213841!important;-webkit-text-fill-color:#213841!important;fill:initial!important;
}
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] svg {fill:#516B73!important;}
.stApp [class*="st-key-pp98_round_selector"] [data-baseweb="select"] > div {min-height:48px!important;}


/* 9.9: Streamlit BaseWeb-rundevælgere i både Kampe og Historik. */
.stApp [data-testid="stSelectbox"] [data-baseweb="select"],
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="input"],
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] [data-baseweb="base-input"],
.stApp [data-testid="stSelectbox"] div[role="combobox"],
.stApp [data-testid="stSelectbox"] [aria-haspopup="listbox"] {
 background-color:#FFFFFF!important;background:#FFFFFF!important;
 color:#213841!important;-webkit-text-fill-color:#213841!important;
 border-color:#D7E5E9!important;box-shadow:none!important;outline-color:transparent!important;
}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,
.stApp [data-testid="stSelectbox"] [aria-haspopup="listbox"] {
 border:1px solid #D7E5E9!important;border-radius:13px!important;min-height:48px!important;
}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div,
.stApp [data-testid="stSelectbox"] [aria-haspopup="listbox"]:focus-visible{
 border-color:#41B8A2!important;box-shadow:0 0 0 3px rgba(27,154,132,.15)!important;
}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] *,
.stApp [data-testid="stSelectbox"] div[role="combobox"] *,
.stApp [data-testid="stSelectbox"] [aria-haspopup="listbox"] *{
 color:#213841!important;-webkit-text-fill-color:#213841!important;
}
.stApp [data-testid="stSelectbox"] svg{color:#516B73!important;fill:#516B73!important;}
/* Options popup er portal-renderet uden for fanen. */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"],
[role="listbox"]{
 background:#FFFFFF!important;color:#213841!important;-webkit-text-fill-color:#213841!important;
}
[role="option"] *,[role="listbox"] *{color:#213841!important;-webkit-text-fill-color:#213841!important;}


/* 10.0 – Ret HELE select-komponenten, inkl. mørkt BaseWeb-felt.
   Gælder begge rundevælgere i Kampe og Historik. */
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"],
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div > div,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"],
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] [aria-haspopup="listbox"],
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] [data-baseweb="input"],
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] [data-baseweb="base-input"]{
 background:#ffffff!important;
 background-color:#ffffff!important;
 background-image:none!important;
 color:#1d333b!important;
 -webkit-text-fill-color:#1d333b!important;
 box-shadow:none!important;
}
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"]{
 border:1px solid #d4e3e7!important;
 border-radius:12px!important;
 overflow:hidden!important;
}
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within > div:first-child,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"]:focus-within{
 border-color:#51aa99!important;
 box-shadow:0 0 0 3px #bfe8df85!important;
}
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] span,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] input,
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] [role="combobox"] *{
 color:#1d333b!important;
 -webkit-text-fill-color:#1d333b!important;
}
.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] svg{
 color:#55727b!important;fill:currentColor!important;
}
/* Streamlit kan gengive hele inputfeltet i en BaseWeb input-container. */
.stApp [data-testid="stSelectbox"] [data-baseweb="input"],
.stApp [data-testid="stSelectbox"] [data-baseweb="base-input"]{
 background:#ffffff!important;background-color:#ffffff!important;
}


/* 10.1: Rundevælgere bruger rigtige knapper og ingen mørke BaseWeb-selectfelter. */
.stApp [data-testid="stTabs"] [data-testid="stButton"] button {
  border-radius:12px!important;
  min-height:43px!important;
}
.stApp [data-testid="stTabs"] [data-testid="stButton"] button[kind="secondary"] {
  background:#FFFFFF!important;
  border:1px solid #D7E5E9!important;
  color:#203840!important;
  box-shadow:none!important;
}
.stApp [data-testid="stTabs"] [data-testid="stButton"] button[kind="secondary"] *{
  color:#203840!important;-webkit-text-fill-color:#203840!important;
}
.stApp [data-testid="stTabs"] [data-testid="stButton"] button[kind="primary"]{
  background:#137F75!important;border:1px solid #137F75!important;color:#FFFFFF!important;
}
.stApp [data-testid="stTabs"] [data-testid="stButton"] button[kind="primary"] *{
  color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;
}

/* 10.3: konsekvent lodret afstand mellem kort på telefoner */
.p7-stats{margin:14px 0 0!important;gap:12px!important}
.pp9-progress{margin:0!important}
.stApp [data-testid="stTabs"] [role="tablist"],
.stApp [data-baseweb="tab-list"]{margin:0 0 12px!important;gap:12px!important}
/* Streamlit elementer er søskende: det er mellem elementerne luft skal sættes. */
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stMarkdownContainer"] .p7-stats){margin-bottom:14px!important}
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stMarkdownContainer"] .pp9-progress){margin-bottom:14px!important}
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stMarkdownContainer"] .p7-stats) + [data-testid="stElementContainer"]{margin-top:0!important}
.stApp [data-testid="stTabs"]{margin-top:0!important}
@media(max-width:700px){
 .p7-stats{gap:10px!important;margin:10px 0 0!important}
 .p7-stat{min-height:86px!important;border-radius:14px!important}
 .stApp [data-testid="stElementContainer"]:has(.p7-stats){margin-bottom:12px!important}
 .stApp [data-testid="stElementContainer"]:has(.pp9-progress){margin-bottom:12px!important}
 .pp9-progress{padding:12px!important;border-radius:15px!important}
 .stApp [data-testid="stTabs"] [role="tablist"],
 .stApp [data-baseweb="tab-list"]{gap:10px!important;margin:0 0 16px!important}
 .stApp [data-testid="stTabs"] [role="tablist"] [role="tab"],
 .stApp [data-baseweb="tab-list"] [data-baseweb="tab"]{min-height:82px!important}
 /* Rundevalg: knapper på to kolonner i stedet for lodret én efter én. */
 .stApp [data-testid="stHorizontalBlock"]:has([class*="st-key-pp101_g_"]),
 .stApp [data-testid="stHorizontalBlock"]:has([class*="st-key-pp101_h_"]){
   display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;
   column-gap:10px!important;row-gap:10px!important;align-items:stretch!important;
 }
 .stApp [data-testid="stHorizontalBlock"]:has([class*="st-key-pp101_g_"]) > [data-testid="stColumn"],
 .stApp [data-testid="stHorizontalBlock"]:has([class*="st-key-pp101_h_"]) > [data-testid="stColumn"]{
   width:100%!important;min-width:0!important;max-width:none!important;flex:initial!important;
 }
 .stApp [class*="st-key-pp101_g_"] button,
 .stApp [class*="st-key-pp101_h_"] button{min-height:46px!important;border-radius:12px!important}
}


/* 10.4: Afstand løses inde i selve Streamlit-elementernes højde,
   frem for negative/sammenfaldende margins. Virker på pc og mobil. */
.p7-stats{margin:0!important;gap:12px!important;}
.pp9-progress{margin:0!important;}
.stApp [data-testid="stElementContainer"]:has(.p7-stats),
.stApp [data-testid="stElementContainer"]:has(.pp9-progress),
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stMarkdownContainer"] .p7-stats),
.stApp [data-testid="stElementContainer"]:has(> [data-testid="stMarkdownContainer"] .pp9-progress){
  padding-bottom:20px!important;
  margin:0!important;
  box-sizing:border-box!important;
}
.stApp [data-testid="stTabs"]{margin-top:0!important;}
.stApp [data-testid="stTabs"] [role="tablist"],
.stApp [data-baseweb="tab-list"]{margin:0 0 16px!important;gap:12px!important;}
@media(max-width:700px){
 .p7-stats{gap:9px!important;margin:0!important;}
 .stApp [data-testid="stElementContainer"]:has(.p7-stats),
 .stApp [data-testid="stElementContainer"]:has(.pp9-progress){padding-bottom:14px!important;margin:0!important;}
 .stApp [data-testid="stTabs"] [role="tablist"],
 .stApp [data-baseweb="tab-list"]{margin:0 0 14px!important;gap:9px!important;}
}

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

# Velkomstside vises kun, når ingen turnering er åbnet. Delte links springer den over.
if not st.session_state.get('tid'):
    st.markdown("""
    <style>
    .pp11-welcome{background:linear-gradient(125deg,#fff 30%,#eaf8f5 100%);border:1px solid #d9e8e9;border-radius:24px;padding:25px 22px;margin-bottom:22px}
    .pp11-brand{color:#147f73;font-weight:900;letter-spacing:.18em;font-size:12px}
    .pp11-welcome h1{font-size:clamp(29px,6vw,42px)!important;letter-spacing:-.04em!important;margin:8px 0;color:#18313a!important}
    .pp11-welcome p{color:#647b82!important;font-size:16px;margin:4px 0}
    .pp11-card{padding:20px 18px 12px;background:white;border:1px solid #dbe7e9;border-radius:22px;text-align:center;margin-bottom:16px}
    .pp11-card h3{color:#19343c!important;margin:8px 0!important}
    .pp11-card p{color:#607880!important;margin:0 0 17px}
    .pp11-caption{text-align:center;color:#738891;font-size:12px;margin:20px 0}
    .stApp [class*='st-key-pp11_new_btn'] button{background:#128578!important;color:white!important;border-color:#128578!important;min-height:54px!important;font-weight:750!important}
    .stApp [class*='st-key-pp11_new_btn'] button *{color:white!important;-webkit-text-fill-color:white!important}
    .stApp [class*='st-key-pp11_open_btn'] button{background:white!important;color:#14766b!important;border:1px solid #afd7d0!important;min-height:54px!important;font-weight:700!important}
    .stApp [class*='st-key-pp11_open_btn'] button *{color:#14766b!important;-webkit-text-fill-color:#14766b!important}
    </style>
    <div class="pp11-welcome"><div class="pp11-brand">PADEL PAPPAS</div>
    <h1>Velkommen til Padel Pappas</h1>
    <p>Din turnering. Dine kampe. Din stilling.</p></div>
    <div class="pp11-card"><h3>Klar til at spille padel?</h3>
    <p>Opret en Americano- eller Mexicano-turnering, eller fortsæt en eksisterende.</p></div>
    """,unsafe_allow_html=True)
    if 'pp11_landing_mode' not in st.session_state:
        st.session_state.pp11_landing_mode=None
    if st.session_state.pp11_landing_mode is None:
        if st.button('＋ Opret ny turnering',type='primary',use_container_width=True,key='pp11_new_btn'):
            st.session_state.pp11_landing_mode='new';st.rerun()
        if st.button('↗ Åbn eksisterende turnering',use_container_width=True,key='pp11_open_btn'):
            st.session_state.pp11_landing_mode='open';st.rerun()
    elif st.session_state.pp11_landing_mode == 'open':
        st.subheader('Åbn eksisterende turnering')
        with st.form('pp11_open_form'):
            entered_