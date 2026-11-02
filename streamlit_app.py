""Padel Samlet 2.0 — independently implemented mobile-first tournament app."""
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
    'gCn+tOPCgba6eHfVs/nNlb61Xun/NPwfDZwSuA=='
)
_court_html = zlib.decompress(base64.b64decode(_COURT_HTML_ZLIB_BASE64))
_component_dir = Path(tempfile.gettempdir()) / 'padel_pappas_court_v80'
_component_dir.mkdir(parents=True, exist_ok=True)
_component_file = _component_dir / 'index.html'
if not _component_file.exists() or _component_file.read_bytes() != _court_html:
    _component_file.write_bytes(_court_html)
st.set_page_config(page_title='Padel Pappas', page_icon='🎾', layout='centered', initial_sidebar_state='collapsed')

court_input = components.declare_component('padel_court_input_v80', path=str(_component_dir))
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
st.markdown(
    '<div class="p7-hero"><div class="brand">● PADEL PAPPAS 7.1</div>'
    f'<div class="hero-title">{html.escape(d["title"])}</div>'
    f'<div class="subtitle">{html.escape(d["format"])} · {html.escape(d.get("partner_mode", "Skiftende makker"))} · {len(d["players"])} spillere</div>'
    + (f'<div class="p7-id">Turnerings-ID: {html.escape(st.session_state.tid)}</div>' if st.session_state.get('tid') else '')
    + '</div>', unsafe_allow_html=True)
if st.session_state.get('tid'):
    st.caption(f'Del turneringen: https://padel-pappas.streamlit.app/?id={st.session_state.tid}')
played_rounds = len(d.get('history', []))
if d.get('matches') and all(m.get('blue_score') is not None and m.get('red_score') is not None for m in d['matches']):
    played_rounds += 1
st.markdown(
    '<div class="p7-stats">'
    f'<div class="p7-stat"><strong>{d.get("round", 0)}/{d.get("round_limit", 7)}</strong><small>Runde</small></div>'
    f'<div class="p7-stat"><strong>{len(d.get("matches", []))}</strong><small>Baner i runden</small></div>'
    f'<div class="p7-stat"><strong>{d.get("target", 0) or "Fri"}</strong><small>Point pr. kamp</small></div>'
    '</div>', unsafe_allow_html=True)

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

tab_games,tab_table,tab_log=st.tabs(['🎾 Kampe','🏆 Stilling','📜 Historik'])
with tab_games:
    st.markdown(f'<div class="p71-section-title">Runde {d["round"] or "–"} <span>· Kampe</span></div>', unsafe_allow_html=True)
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
            st.caption('Ikke-gemte scores går tabt ved ny blanding.')
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
                pass
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
    st.subheader('🏆 Leaderboard')
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
    st.subheader('📜 Kamphistorik')
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
