# Padel Pappas 12.2 – Grafiske finalebaner med guld/sølv
import html
import json
import secrets
import random
import math
from collections import Counter
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
)
_court_html = zlib.decompress(base64.b64decode(_COURT_HTML_ZLIB_BASE64))
_component_dir = Path(tempfile.gettempdir()) / 'padel_pappas_court_v122'
_component_dir.mkdir(parents=True, exist_ok=True)
_component_file = _component_dir / 'index.html'
if not _component_file.exists() or _component_file.read_bytes() != _court_html:
    _component_file.write_bytes(_court_html)
# Officielt Padel Pappas-logo som Streamlit favicon / browserikon.
# Dette er ikke en garanti for iOS-hjemmeskaermsikon paa Streamlit Cloud.
from PIL import Image
_APP_ICON_PATH = Path(__file__).parent / 'app_icon.png'
_APP_ICON = Image.open(_APP_ICON_PATH) if _APP_ICON_PATH.exists() else '🎾'
st.set_page_config(page_title='Padel Pappas', page_icon=_APP_ICON, layout='centered', initial_sidebar_state='collapsed')

court_input = components.declare_component('padel_court_input_v122', path=str(_component_dir))
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


/* 11.6 – samme diskrete handlingsdesign som Rediger hold */
.stApp [class*="st-key-pp116_share_actions"],
.stApp [class*="st-key-pp116_history_edit_"] {
  display:flex!important; justify-content:flex-start!important;
  width:100%!important; margin:4px 0 10px!important;
  padding:0!important; background:transparent!important;
  border:0!important; box-shadow:none!important;
}
.stApp [class*="st-key-pp116_share_actions"] [data-testid="stPopover"] button,
.stApp [class*="st-key-pp116_history_edit_"] [data-testid="stPopover"] button {
  min-height:33px!important; padding:5px 11px!important;
  border:1px solid #dcebe9!important; border-radius:9px!important;
  background:#f4faf9!important;
  color:#42777d!important; -webkit-text-fill-color:#42777d!important;
  font-size:13px!important; font-weight:650!important;
  box-shadow:none!important;
}
.stApp [class*="st-key-pp116_share_actions"] [data-testid="stPopover"] button *,
.stApp [class*="st-key-pp116_history_edit_"] [data-testid="stPopover"] button * {
  color:#42777d!important; -webkit-text-fill-color:#42777d!important;
}
.stApp [class*="st-key-pp116_share_actions"] [data-testid="stPopover"] button:hover,
.stApp [class*="st-key-pp116_history_edit_"] [data-testid="stPopover"] button:hover {
  background:#e9f5f2!important; border-color:#b9d9d4!important;
}
@media(max-width:520px){
 .stApp [class*="st-key-pp116_share_actions"] [data-testid="stPopover"] button,
 .stApp [class*="st-key-pp116_history_edit_"] [data-testid="stPopover"] button {font-size:12px!important;min-height:30px!important;padding:4px 9px!important}
}
</style>
'''
st.markdown(STYLE, unsafe_allow_html=True)


def fresh():
    return {'title':'Søndagspadel','players':[],'format':'Mexicano','round_limit':7,'target':32,
            'round':0,'matches':[],'history':[],'byes':[],'partner_mode':'Skiftende makker','ranking_priority':'Point først','finale':None,'finales':None,'americano_schedule':[]}


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


def planned_americano(data):
    """Plan all ordinary Americano rounds before play, separately from the final."""
    players = list(data['players'])
    limit = int(data['round_limit'])
    previous = []
    plan = []
    if data.get('partner_mode') == 'Fast makker':
        pairs = [players[i:i + 2] for i in range(0, len(players), 2)]
        for r in range(limit):
            games, byes = make_fixed_pairs_round(pairs, 'Americano', previous, round_number=r)
            plan.append({'matches': games, 'byes': byes})
            previous.extend(games)
        return plan

    # A circle pairing guarantees distinct partners for the first N-1 rounds.
    # A separate global search decides WHICH pairs play against each other:
    # this changes no partners, only opponents and court assignments.
    if len(players) % 4 == 0:
        rng = random.Random(secrets.randbits(64))
        rng.shuffle(players)
        ring = list(players)
        pair_rounds = []
        for round_idx in range(limit):
            pairs = [tuple(sorted((ring[i], ring[-1-i])))
                     for i in range(len(ring)//2)]
            rng.shuffle(pairs)
            pair_rounds.append(pairs)
            ring = [ring[0], ring[-1], *ring[1:-1]]

        # Each match is two fixed pairs. Optimise the arrangements across
        # *all* rounds, not greedily one round at a time.
        def opponent_edges(p, q):
            return [tuple(sorted((a, b))) for a in p for b in q]

        def quality(counts):
            # Repeated opponents are inevitable when 2*rounds > N-1.
            # Penalise concentrated repeats, particularly 3+ meetings.
            return sum(8 * max(0, c-1)**2 + 18 * max(0, c-2)**2
                       for c in counts.values())

        def build_counts(groups):
            result = Counter()
            for round_groups in groups:
                for p, q in round_groups:
                    result.update(opponent_edges(p, q))
            return result

        best_groups, best_quality = None, float('inf')
        # Small bounded search; no costly optimisation when opening an
        # existing tournament (the saved schedule is reused).
        for restart in range(3):
            groups = []
            for pairs in pair_rounds:
                shuffled = list(pairs)
                rng.shuffle(shuffled)
                groups.append([[shuffled[i], shuffled[i+1]]
                               for i in range(0, len(shuffled), 2)])
            counts = build_counts(groups)
            current = quality(counts)
            if current < best_quality:
                best_quality = current
                best_groups = [[(tuple(p), tuple(q)) for p, q in round_groups]
                               for round_groups in groups]
            steps = max(2500, min(7500, 120000 // max(1, limit)))
            for step in range(steps):
                rr = rng.randrange(limit)
                if len(groups[rr]) < 2:
                    break
                i, j = rng.sample(range(len(groups[rr])), 2)
                a, b = groups[rr][i], groups[rr][j]
                side_a, side_b = rng.randrange(2), rng.randrange(2)
                old_edges = opponent_edges(a[0], a[1]) + opponent_edges(b[0], b[1])
                a[side_a], b[side_b] = b[side_b], a[side_a]
                new_edges = opponent_edges(a[0], a[1]) + opponent_edges(b[0], b[1])
                counts.subtract(old_edges)
                counts.update(new_edges)
                candidate = quality(counts)
                # Simulated annealing permits improvements that require
                # temporarily moving through a less favourable arrangement.
                heat = max(0.35, 5.0 * (1.0-step/steps))
                accept = candidate <= current or rng.random() < math.exp((current-candidate)/heat)
                if accept:
                    current = candidate
                else:
                    counts.subtract(new_edges)
                    counts.update(old_edges)
                    a[side_a], b[side_b] = b[side_b], a[side_a]
                if current < best_quality:
                    best_quality = current
                    best_groups = [[(tuple(pair1), tuple(pair2))
                                    for pair1, pair2 in round_groups]
                                   for round_groups in groups]

        for round_groups in best_groups:
            matches = []
            for court, (blue, red) in enumerate(round_groups, 1):
                matches.append({'court': court, 'blue': list(blue),
                                'red': list(red), 'blue_score': None,
                                'red_score': None})
            plan.append({'matches': matches, 'byes': []})
        return plan

    # Other group sizes require byes; optimise over the entire schedule.
    # Several full candidates are compared for partner repetition and byes.
    best_score = None
    best_plan = None
    for attempt in range(12):
        schedule = []
        matches_so_far = []
        byes_count = {name:0 for name in players}
        for r in range(limit):
            # Prioritise people with fewer previous games to balance byes.
            ordered = sorted(players, key=lambda name:(byes_count[name],
                                 random.Random(attempt * 307 + r * 71 + players.index(name)).random()))
            generated, byes = make_round(ordered, 'Americano', matches_so_far,
                                        seed=(attempt+1)*100003 + r*71)
            for name in byes: byes_count[name] += 1
            schedule.append({'matches':generated, 'byes':byes})
            matches_so_far.extend(generated)
        pair_counts = {}
        for m in matches_so_far:
            for team in (m['blue'],m['red']):
                key=tuple(sorted(team))
                pair_counts[key] = pair_counts.get(key,0)+1
        repeat = sum(max(0, c-1) for c in pair_counts.values())
        score = (repeat, max(byes_count.values())-min(byes_count.values()))
        if best_score is None or score < best_score:
            best_score, best_plan = score, schedule
            if score == (0,0): break
    return best_plan


def new_round(data):
    if data['round'] >= data['round_limit']:
        return False
    if any(m['blue_score'] is None or m['red_score'] is None for m in data['matches']):
        return False
    if data['matches']:
        data['history'].append({'number':data['round'],'matches':data['matches']})
    if data['format'] == 'Americano':
        if len(data.get('americano_schedule', [])) != int(data['round_limit']):
            # Existing tournaments without a saved plan: preserve completed
            # rounds and generate a complete remaining schedule only once.
            remaining = int(data['round_limit']) - int(data['round'])
            if data['round'] == 0:
                data['americano_schedule'] = planned_americano(data)
            else:
                temp = dict(data)
                temp['round_limit'] = remaining
                temp_plan = planned_americano(temp)
                data['americano_schedule'] = ([None] * int(data['round'])) + temp_plan
        entry = data['americano_schedule'][data['round']]
        generated = [dict(m) for m in entry['matches']]
        byes = list(entry['byes'])
    else:
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
    /* Ingen tom sidepanel-drawer, før brugeren åbner eller opretter en turnering. */
    [data-testid="stSidebar"]{display:none!important}
    [data-testid="stSidebarCollapsedControl"]{display:none!important}
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
            welcome_open_id = st.text_input('Turnerings-ID', placeholder='F.eks. PADEL1/11', key='pp111_open_id')
            welcome_open_clicked = st.form_submit_button('Åbn turnering', type='primary', use_container_width=True)
        if welcome_open_clicked:
            welcome_tid = normalize_id(welcome_open_id)
            if not ID_PATTERN.fullmatch(welcome_tid):
                st.error('Indtast et gyldigt turnerings-ID (3-32 tegn).')
            else:
                try:
                    welcome_data = db_load(welcome_tid)
                    st.session_state['tid'] = welcome_tid
                    st.session_state['tourney'] = welcome_data
                    st.query_params['id'] = welcome_tid
                    st.rerun()
                except (requests.RequestException, ValueError, RuntimeError) as exc:
                    st.error(f'Kunne ikke åbne turneringen: {exc}')
        if st.button('← Tilbage',key='pp11_open_back'):
            st.session_state.pp11_landing_mode=None;st.rerun()
    else:
        st.subheader('Opret ny turnering')
        with st.form('pp11_new_form'):
            id_choice=st.radio('Turnerings-ID',['Vælg selv','Generér automatisk'],horizontal=True)
            chosen_id=st.text_input('Dit turnerings-ID',placeholder='F.eks. PADEL1/11',help='3-32 tegn; kun bogstaver, tal, /, - og _.')
            title=st.text_input('Turneringens navn',value='Søndagspadel')
            raw=st.text_area('Spillere – én pr. linje',height=170,placeholder='Jan\nTue\nLasse\nMia')
            fmt=st.radio('Turneringsform',['Mexicano','Americano'],horizontal=True)
            partner=st.radio('Makkertype',['Skiftende makker','Fast makker'],horizontal=True,
                            help='Ved fast makker skrives parrene to og to i spillerlisten.')
            ranking=st.radio('Hvad afgør placeringen?',['Point først','Sejre først'],horizontal=True)
            rounds=st.number_input('Maksimalt antal runder',min_value=1,max_value=40,value=7)
            target=st.number_input('Point pr. kamp (0 = frit)',min_value=0,max_value=100,value=32)
            create_clicked=st.form_submit_button('Opret turnering',type='primary',use_container_width=True)
        if create_clicked:
            players=[p.strip() for p in raw.splitlines() if p.strip()]
            tid=normalize_id(chosen_id) if id_choice=='Vælg selv' else 'P-'+secrets.token_hex(5).upper()
            if not ID_PATTERN.fullmatch(tid):
                st.error('Brug et turnerings-ID på 3-32 tegn med bogstaver, tal, /, - eller _.')
            elif len(players)<4 or len(players)!=len(set(players)):
                st.error('Skriv mindst fire forskellige spillernavne.')
            elif partner=='Fast makker' and len(players)%2:
                st.error('Faste makkere kræver et lige antal spillere.')
            else:
                data=fresh()
                data.update(title=title.strip() or 'Padelturnering',players=players,format=fmt,
                            partner_mode=partner,ranking_priority=ranking,round_limit=int(rounds),target=int(target))
                try:
                    db_save(tid,data,create=True)
                    st.session_state.tid=tid
                    st.session_state.tourney=data
                    st.query_params['id']=tid
                    st.rerun()
                except requests.HTTPError as exc:
                    if exc.response is not None and exc.response.status_code == 409:
                        st.error('Turnerings-ID er allerede i brug. Vælg et andet.')
                    else:
                        st.error(f'Kunne ikke oprette turneringen: {exc}')
                except (requests.RequestException,ValueError,RuntimeError) as exc:
                    st.error(f'Kunne ikke oprette turneringen: {exc}')
        if st.button('← Tilbage',key='pp11_new_back'):
            st.session_state.pp11_landing_mode=None;st.rerun()
    st.markdown('<div class="pp11-caption">Ingen konto nødvendig · Del turneringen med et link</div>',unsafe_allow_html=True)
    st.stop()

# Den oprindelige sidepanel-menu vises kun i en åben turnering.
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


st.markdown(
    '<div class="p7-hero"><div class="brand">● PADEL PAPPAS 11.8</div>'
    f'<div class="hero-title">{html.escape(d["title"])}</div>'
    f'<div class="subtitle">{html.escape(d["format"])} · {html.escape(d.get("partner_mode", "Skiftende makker"))} · {len(d["players"])} spillere</div>'
    + (f'<div class="p7-id">Turnerings-ID: {html.escape(st.session_state.tid)}</div>' if st.session_state.get('tid') else '')
    + '</div>', unsafe_allow_html=True)
if st.session_state.get('tid'):
    with st.container(key='pp116_share_actions'):
        with st.popover('↗ Del turnering', use_container_width=False):
            st.caption('Kopiér dette link og send det til deltagerne:')
            st.code(f'https://padel-pappas.streamlit.app/?id={st.session_state.tid}', language=None)
            st.caption('Alle med turnerings-ID kan redigere resultaterne.')
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
                if not d['round'] and (players != d['players'] or fmt != d['format'] or partner_mode != d.get('partner_mode') or int(rounds) != int(d['round_limit'])):
                    d['americano_schedule'] = []
                if d['round'] and int(rounds) != int(d['round_limit']) and d['format'] == 'Americano':
                    st.error('Antal runder kan ikke ændres efter Americano er startet, fordi programmet er fastlagt.')
                    st.stop()
                d.update(title=title,players=players,format=fmt,partner_mode=partner_mode,ranking_priority=ranking_priority,round_limit=int(rounds),target=int(target))
                save();st.success('Opsætning gemt')
        st.divider()
        if st.button('Nulstil turnering',use_container_width=True):
            st.session_state.confirm_reset=True
        if st.session_state.get('confirm_reset'):
            st.warning('Alle runder og resultater slettes i denne turnering.')
            if st.button('Bekræft nulstilling',type='primary'):
                st.session_state.tourney=fresh();d=st.session_state.tourney;save();st.session_state.confirm_reset=False;st.rerun()

# Tour progress is visual only, based on completed and persisted round scores.
completed_rounds = min(int(d.get('round_limit', 7)), played_rounds)
round_total = max(1, int(d.get('round_limit', 7)))
percent = round(100 * completed_rounds / round_total)
if st.session_state.get('tid') and d.get('round', 0) > 0:
    st.markdown(
        '<div class="pp9-progress"><div class="pp9-progress-heading">'
        f'<strong>Runde {d["round"]} af {round_total}</strong><span>{percent}% gennemført</span>'
        '</div><div class="pp9-track"><div class="pp9-fill" style="width:'
        f'{percent}%"></div></div></div>', unsafe_allow_html=True)

tab_games,tab_table,tab_log=st.tabs(['🎾 Kampe','🏆 Stilling','📜 Historik'])
with tab_games:
    completed_history = d.get('history', [])
    current_number = int(d.get('round') or 0)
    current_round_label = f'Runde {current_number}' if current_number > 0 else 'Aktuel runde'
    schedule = d.get('americano_schedule') or []
    show_all_americano = (d.get('format') == 'Americano' and current_number > 0
                         and len(schedule) == int(d.get('round_limit') or 0))
    # Alle ordinære Americano-runder vises straks efter turneringsstart.
    # Fremtidige runder vises kun som låst program, uden scorefelter.
    if show_all_americano:
        choices = [f'Runde {n}' for n in range(1, int(d['round_limit']) + 1)]
        st.caption('Hele Americano-programmet er planlagt. Kommende runder er kun til visning.')
    elif completed_history:
        choices = [f'✓ Runde {r["number"]}' for r in sorted(completed_history, key=lambda r: r['number'])] + [current_round_label]
        st.caption('Se tidligere runder (resultater kan rettes under Historik)')
    else:
        choices = []
    game_view_key = f'pp101_game_round_{st.session_state.get("tid", "")}'
    # Opdater valget til den netop startede runde, når appen går videre.
    if st.session_state.get(game_view_key) not in choices:
        st.session_state[game_view_key] = current_round_label
    if choices:
        for start in range(0, len(choices), 4):
            columns = st.columns(min(4, len(choices) - start), gap='small')
            for column, choice in zip(columns, choices[start:start + 4]):
                with column:
                    if st.button(choice, key=f'pp119_g_{start}_{choice}',
                                 type='primary' if st.session_state[game_view_key] == choice else 'secondary',
                                 use_container_width=True):
                        st.session_state[game_view_key] = choice
                        st.rerun()
    viewing = st.session_state.get(game_view_key, current_round_label)
    preview_only = bool(choices) and viewing != current_round_label
    if preview_only:
        preview_num = int(viewing.split()[-1])
        if preview_num < current_number:
            previous = next((x for x in completed_history if x['number'] == preview_num), None)
            if previous:
                st.markdown(f'### Runde {preview_num} · Resultater')
                for pm in previous['matches']:
                    score = 'Afventer' if pm['blue_score'] is None else f'{pm["blue_score"]} – {pm["red_score"]}'
                    st.markdown('<div class="pp9-history-mini"><b>Bane '+str(pm['court'])+'</b><span>'+
                                html.escape(' & '.join(pm['blue']))+' <strong>'+score+'</strong> '+
                                html.escape(' & '.join(pm['red']))+'</span></div>', unsafe_allow_html=True)
                st.caption('Resultater kan rettes under Historik.')
        elif show_all_americano and preview_num > current_number:
            planned = schedule[preview_num - 1]
            if planned:
                st.markdown(f'### Runde {preview_num} · Kommende kampe')
                st.caption('Programmet er fastlagt. Resultater kan først indtastes, når runden er aktuel.')
                for pm in planned['matches']:
                    st.markdown('<div class="pp9-history-mini"><b>Bane '+str(pm['court'])+'</b><span>'+
                                html.escape(' & '.join(pm['blue']))+' <strong>mod</strong> '+
                                html.escape(' & '.join(pm['red']))+'</span></div>', unsafe_allow_html=True)
                if planned.get('byes'):
                    st.info('Sidder over: ' + ', '.join(planned['byes']))
            else:
                st.info('Denne runde blev oprettet før forudplanlægningen og kan ikke forhåndsvises.')
    if not preview_only:
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
            if can_reshuffle and d['format'] != 'Americano':
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
                if m.get('blue_score') is not None and m.get('red_score') is not None:
                    st.markdown('<div class="pp9-saved">✓ Bane '+str(m['court'])+' · Gemt</div>', unsafe_allow_html=True)
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
                    # Diskret redigeringslink direkte under banevisningen.
                    with st.container(key=f"court_edit_actions_{d['round']}_{i}"):
                        with st.popover('✎ Rediger hold', use_container_width=False):
                            p = d['players']
                            chosen = st.multiselect('Vælg fire spillere', p, default=m['blue'] + m['red'],
                                                    key=f"edit_{d['round']}_{i}", max_selections=4)
                            if len(chosen) == 4:
                                if st.button('Byt makkerpar', key=f"swap_{d['round']}_{i}"):
                                    m['blue'] = [chosen[0], chosen[2]]
                                    m['red'] = [chosen[1], chosen[3]]
                                    m['blue_score'] = None
                                    m['red_score'] = None
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
                    st.session_state[game_view_key] = f'Runde {d["round"]}'
                    save()
                    st.rerun()
                if not unchanged:
                    st.caption('Indtast alle scores og tryk Gem runde, før næste runde kan dannes.')
            elif unchanged:
                st.success('Alle ordinære runder er færdige! Se stillingen eller spil finalen herunder.')

            # Placeringsfinaler efter grundspillet – én kamp pr. fire spillere.
            # Grundspillets rangliste fryses ved oprettelsen og ændres ikke af finaleresultater.
            if d['round'] >= d['round_limit'] and unchanged:
                st.divider()
                st.subheader('🏆 Placeringsfinaler')
                finales = d.get('finales')
                ranking = standings(d)
                if finales is None:
                    st.caption('Alle spillere får en ekstra placeringsfinale efter grundspillet: 1 + 3 mod 2 + 4, 5 + 7 mod 6 + 8 osv. Finalerne tæller ikke med i grundspillets stilling.')
                    for offset in range(0, len(ranking) - 3, 4):
                        group = ranking[offset:offset + 4]
                        st.write(f'**Bane {offset // 4 + 1} · Placering {offset + 1}–{offset + 4}:** '
                                 + html.escape(group[0]['name']) + ' + ' + html.escape(group[2]['name'])
                                 + ' mod ' + html.escape(group[1]['name']) + ' + ' + html.escape(group[3]['name']))
                    remaining = len(ranking) % 4
                    if remaining:
                        st.warning(f'{remaining} spiller(e) kan ikke indgå i en 2-mod-2-placeringsfinale. De øvrige kan stadig spille.')
                    if len(ranking) >= 4 and st.button('Start placeringsfinaler', type='primary', use_container_width=True):
                        built = []
                        for offset in range(0, len(ranking) - 3, 4):
                            group = ranking[offset:offset + 4]
                            built.append({'blue': [group[0]['name'], group[2]['name']],
                                          'red': [group[1]['name'], group[3]['name']],
                                          'blue_score': None, 'red_score': None,
                                          'court': offset // 4 + 1, 'rank_start': offset + 1})
                        # Bevar evt. allerede gemt resultat fra den ældre enkeltfinale.
                        old = d.get('finale')
                        if isinstance(old, dict) and built and old.get('blue') == built[0]['blue'] and old.get('red') == built[0]['red']:
                            built[0]['blue_score'] = old.get('blue_score')
                            built[0]['red_score'] = old.get('red_score')
                        d['finales'] = built
                        save()
                        st.rerun()
                    elif len(ranking) < 4:
                        st.warning('Der kræves mindst fire spillere for at afvikle placeringsfinaler.')
                else:
                    st.caption('Én ekstra kamp pr. fire spillere. Finaleresultaterne påvirker ikke grundspillets stilling.')
                    # Saml alle scorefelter, så finalerunden kan gemmes med én knap.
                    final_results = []
                    for index, match in enumerate(finales):
                        court = match.get('court', index + 1)
                        rank_start = match.get('rank_start', 4 * index + 1)
                        is_championship = index == 0
                        label = 'Mesterskabsfinale' if is_championship else f'Placering {rank_start}–{rank_start + 3}'
                        st.markdown(f'#### Bane {court} · {label}')
                        scored = match.get('blue_score') is not None and match.get('red_score') is not None
                        edit_key = f'pp122_edit_final_{st.session_state.tid}_{index}'
                        editing = st.session_state.get(edit_key, False)
                        final_key = f'pp122_court_final_{st.session_state.tid}_{index}_{int(editing)}_{int(scored)}'
                        final_value = court_input(
                            court=court, round='Finale', final_label=label,
                            championship=is_championship,
                            blue_players=match['blue'], red_players=match['red'],
                            target=int(d['target']),
                            blue_score=match.get('blue_score'), red_score=match.get('red_score'),
                            default={'blue': match.get('blue_score'), 'red': match.get('red_score')},
                            key=final_key,
                        )
                        final_value = final_value if isinstance(final_value, dict) else {}
                        if scored and not editing:
                            # Uændrede, allerede gemte resultater tages med ved samlet lagring.
                            final_results.append((match['blue_score'], match['red_score']))
                            st.caption('✓ Resultat gemt · ' + str(match['blue_score']) + ' – ' + str(match['red_score']))
                            if match['blue_score'] == match['red_score']:
                                st.warning('Kampen står lige. Ret resultatet for at kåre et vinderhold.')
                            else:
                                winner = match['blue'] if match['blue_score'] > match['red_score'] else match['red']
                                if is_championship:
                                    st.markdown('<div class="pp9-winners"><div>🏆 TURNERINGSVINDERE</div><strong>' + html.escape(' & '.join(winner)) + '</strong><small>Finalen er afsluttet</small></div>', unsafe_allow_html=True)
                                else:
                                    st.success('Vinder: ' + ' & '.join(winner))
                            if st.button('✎ Ret resultat', key=f'edit_placement_final_{index}'):
                                st.session_state[edit_key] = True
                                st.rerun()
                        else:
                            upper = int(d['target']) if d['target'] else 200
                            blue_value = final_value.get('blue')
                            blue_valid = type(blue_value) is int and 0 <= blue_value <= upper
                            if d['target']:
                                red_value = int(d['target']) - blue_value if blue_valid else None
                            else:
                                red_value = final_value.get('red')
                            red_valid = type(red_value) is int and 0 <= red_value <= (upper if d['target'] else 200)
                            final_results.append((int(blue_value), int(red_value)) if blue_valid and red_valid else (None, None))
                            if editing and st.button('Annuller rettelse', key=f'cancel_placement_final_{index}'):
                                st.session_state[edit_key] = False
                                st.rerun()
                        if index < len(finales) - 1:
                            st.divider()

                    st.divider()
                    st.subheader('Gem hele finalerunden')
                    antal_klare = sum(b is not None and r is not None for b, r in final_results)
                    st.caption(f'{antal_klare} af {len(finales)} finalekampe har gyldige scores.')
                    if st.button('💾 Gem finalerunde', type='primary', use_container_width=True,
                                 key=f'pp123_save_all_finales_{st.session_state.tid}'):
                        fejl = []
                        for match, (blue, red) in zip(finales, final_results):
                            bane = match.get('court', '?')
                            if blue is None or red is None:
                                fejl.append(f'Bane {bane}: Der mangler et gyldigt resultat.')
                            elif d['target'] and blue + red != int(d['target']):
                                fejl.append(f'Bane {bane}: Scores skal tilsammen give {d["target"]} point.')
                        if fejl:
                            for besked in fejl:
                                st.error(besked)
                        else:
                            for index, (match, (blue, red)) in enumerate(zip(finales, final_results)):
                                match['blue_score'] = int(blue)
                                match['red_score'] = int(red)
                                st.session_state[f'pp122_edit_final_{st.session_state.tid}_{index}'] = False
                            save()  # Én fælles gemning til Supabase.
                            st.success(f'Hele finalerunden er gemt ({len(finales)} kampe).')
                            st.rerun()
                    if finales and all(m.get('blue_score') is not None and m.get('red_score') is not None for m in finales):
                        st.success('Alle placeringsfinaler er afviklet!')



# 12.5 – Eksport af komplet stilling som PNG med Padel Pappas 8362-logo.
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps

_PP125_LOGO = (
    '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'
)

def pp125_standing_png(data, standings_rows):
    """Render every player into a standalone, share-ready PNG. No database changes."""
    W, margin, row_h = 1080, 60, 83
    header_h, footer_h = 420, 112
    total_h = header_h + len(standings_rows)*row_h + footer_h
    canvas = Image.new('RGB', (W,total_h), '#F7FAFA')
    dr = ImageDraw.Draw(canvas)
    regular = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    def font(sz, is_bold=False):
        try: return ImageFont.truetype(bold if is_bold else regular, sz)
        except OSError: return ImageFont.load_default()
    def fitted(value, max_w, sz=27, minimum=15):
        value=str(value)
        while dr.textbbox((0,0),value,font=font(sz,True))[2]>max_w and sz>minimum:
            sz-=1
        if dr.textbbox((0,0),value,font=font(sz,True))[2]>max_w:
            while value and dr.textbbox((0,0),value+'…',font=font(sz,True))[2]>max_w:
                value=value[:-1]
            value+='…'
        return value,font(sz,True)
    # Brand hero. The supplied official image is used unchanged, only resized.
    dr.rounded_rectangle((margin,35,W-margin,270),radius=28,fill='#FFFFFF',outline='#DCEBE8',width=3)
    try:
        raw = zlib.decompress(base64.b64decode(_PP125_LOGO))
        logo = Image.open(BytesIO(raw)).convert('RGB')
        logo.thumbnail((395,215), Image.Resampling.LANCZOS)
        canvas.paste(logo,(margin+26,45+(215-logo.height)//2))
    except Exception:
        dr.text((margin+28,110),'PADEL PAPPAS 8362',font=font(38,True),fill='#064D43')
    dr.text((480,86),'STILLING',font=font(50,True),fill='#193239')
    tournament = str(data.get('title','Turnering'))
    name_text,name_font = fitted(tournament,490,32,19)
    dr.text((484,153),name_text,font=name_font,fill='#168378')
    meta=f"{data.get('format','Padel')}  ·  {len(standings_rows)} spillere"
    dr.text((484,207),meta,font=font(20),fill='#62777B')
    dr.text((margin,310),'SLUTSTILLING' if data.get('finals_complete') else 'TURNERINGSSTILLING',font=font(30,True),fill='#24383E')
    # Column positions fit 1080px including long Danish names.
    cols=[margin+24,margin+95,645,712,779,854,942]
    labels=['#','Spiller','V','U','T','+/-','Point']
    for x,label in zip(cols,labels):
        dr.text((x,373),label,font=font(20,True),fill='#52686D')
    for i,r in enumerate(standings_rows):
        y=header_h+i*row_h
        fills=['#FFF7DC','#EFF3F7','#FFF0E7']
        borders=['#D8AB32','#A6B5C3','#C58C69']
        bg=fills[i] if i<3 else '#FFFFFF'
        border=borders[i] if i<3 else '#DCE7EA'
        dr.rounded_rectangle((margin,y+5,W-margin,y+row_h-6),radius=18,fill=bg,outline=border,width=4 if i<3 else 2)
        rank=f'{i+1}.'
        dr.text((cols[0],y+23),rank,font=font(25,True),fill='#173239')
        name,nfont=fitted(r['name'],520,27,17)
        dr.text((cols[1],y+24),name,font=nfont,fill='#20353B')
        diff=int(r['diff']); nums=[r['wins'],r['draws'],r['losses'],f'{diff:+d}',r['points']]
        for x,val in zip(cols[2:],nums):
            dr.text((x,y+26),str(val),font=font(22,True) if x==cols[-1] else font(21),fill='#20353B')
    bottom=header_h+len(standings_rows)*row_h
    dr.text((margin,bottom+27),'V = Vundne   ·   U = Uafgjorte   ·   T = Tabte   ·   +/- = Pointforskel',font=font(18),fill='#60767B')
    dr.text((margin,bottom+65),f'Padel Pappas 8362  ·  {datetime.now().strftime("%d.%m.%Y")}',font=font(18),fill='#168378')
    buf=BytesIO();canvas.save(buf,format='PNG',optimize=True);return buf.getvalue()

with tab_table:
    st.subheader('🏆 Leaderboard')
    st.caption(f"Sortering: {d.get('ranking_priority', 'Point først')} · derefter {'scorede point' if d.get('ranking_priority') == 'Sejre først' else 'sejre'}, pointforskel og navn")
    rows=standings(d)
    if not rows:
        st.info('Tilføj spillere for at se stillingen.')
    else:
        st.markdown('<div class="standing-heading"><span>#</span><span class="standing-person">Spiller</span><span>V</span><span>U</span><span>T</span><span>+/-</span><span>Point</span></div>',unsafe_allow_html=True)
        for i,r in enumerate(rows):
            diff=f'+{r["diff"]}' if r['diff']>0 else str(r['diff'])
            name=html.escape(r['name'])
            award = ('gold', 'silver', 'bronze')[i] if i < 3 else ''
            rank = ('🥇', '🥈', '🥉')[i] if i < 3 else f'{i+1}.'
            st.markdown(
                f'<div class="standing-row {award}">'
                f'<span class="standing-rank">{rank}</span><span class="standing-person">{name}</span>' 
                f'<span class="standing-value">{r["wins"]}</span>'
                f'<span class="standing-value">{r["draws"]}</span>'
                f'<span class="standing-value">{r["losses"]}</span>'
                f'<span class="standing-value standing-diff">{diff}</span>'
                f'<span class="standing-value standing-points">{r["points"]}</span>'
                '</div>',unsafe_allow_html=True)
        st.caption('V = Vundne · U = Uafgjorte · T = Tabte · +/- = Pointforskel')
        try:
            pp125_image = pp125_standing_png(d, rows)
            st.download_button(
                '📷 Download hele stillingen som PNG',
                data=pp125_image,
                file_name=f'Padel-Pappas-8362-Stilling-{re.sub(r"[^A-Za-z0-9_-]", "-", d.get("title", "Turnering"))}.png',
                mime='image/png',
                use_container_width=True,
                key='pp125_download_standing_png',
            )
        except Exception as pp125_exc:
            st.warning(f'Kunne ikke generere stillingsbilledet: {pp125_exc}')

        with st.expander('Se komplette statistikker'):
            st.dataframe([{'Spiller':r['name'],'KS':r['played'],'V':r['wins'],'U':r['draws'],'T':r['losses'],'Point':r['points'],'PF':r['diff']} for r in rows],hide_index=True,use_container_width=True)


def pp97_history_court(match, round_number):
    """En låst HTML-bane, med samme layout som den interaktive kampbane."""
    def esc(value):
        return html.escape(str(value), quote=True)
    saved = match.get('blue_score') is not None and match.get('red_score') is not None
    blue_score = esc(match['blue_score']) if saved else '–'
    red_score = esc(match['red_score']) if saved else '–'
    badge = '✓ Gemt' if saved else 'Afventer'
    status_class = '' if saved else ' pending'
    names = []
    for team in ('blue','red'):
        for name in match[team]:
            names.append(f'<span class="pp97-name">{esc(name)}</span>')
        # Supports shorter teams without breaking the court alignment.
        while len(names) < (2 if team == 'blue' else 4):
            names.append('<span class="pp97-name"></span>')
    foot = 'Resultatet er gemt' if saved else 'Kampen er endnu ikke gemt som afgjort'
    return (
        '<div class="pp97-card"><div class="pp97-top">'
        f'<span class="pp97-pill">Bane {esc(match["court"])}</span>'
        f'<span class="pp97-badge{status_class}">{badge}</span>'
        '</div><div class="pp97-court">'
        '<div class="pp97-service left"></div><div class="pp97-service right"></div>'
        '<div class="pp97-midline left"></div><div class="pp97-midline right"></div>'
        '<div class="pp97-net"></div>'
        f'<div class="pp97-team blue">{names[0]}{names[1]}</div>'
        f'<div class="pp97-team red">{names[2]}{names[3]}</div>'
        '<div class="pp97-vs">VS</div>'
        f'<div class="pp97-score blue{status_class}">{blue_score}</div>'
        f'<div class="pp97-score red{status_class}">{red_score}</div>'
        '</div>'
        f'<div class="pp97-foot">{foot}</div></div>'
    )

with tab_log:
    st.subheader('📜 Kamphistorik')
    rounds = d['history'] + ([{'number':d['round'],'matches':d['matches']}] if d['matches'] else [])
    if not rounds:
        st.info('Ingen runder spillet endnu.')
    else:
        round_numbers = sorted({r['number'] for r in rounds})
        st.caption('Vælg runde')
        history_view_key = f'pp101_history_round_{st.session_state.get("tid", "")}'
        if st.session_state.get(history_view_key) not in round_numbers:
            st.session_state[history_view_key] = round_numbers[-1]
        for start in range(0, len(round_numbers), 4):
            columns = st.columns(min(4, len(round_numbers) - start), gap='small')
            for column, number in zip(columns, round_numbers[start:start + 4]):
                with column:
                    if st.button(f'Runde {number}', key=f'pp101_h_{start}_{number}',
                                 type='primary' if st.session_state[history_view_key] == number else 'secondary',
                                 use_container_width=True):
                        st.session_state[history_view_key] = number
        selected_round = st.session_state[history_view_key]
        selected = next(r for r in rounds if r['number'] == selected_round)
        st.caption('Vælg en runde for at se resultater. Tryk på Ret resultat for at ændre.')
        for j, m in enumerate(selected['matches']):
            st.markdown(pp97_history_court(m, selected_round), unsafe_allow_html=True)
            with st.container(key=f'pp116_history_edit_{selected_round}_{j}'):
                with st.popover('✎ Ret resultat', use_container_width=False):
                    st.write(f'**Runde {selected_round} · Bane {m["court"]}**')
                    st.caption('Ændringer gemmes først, når du trykker Gem rettelse.')
                    with st.form(f"pp97_fix_{selected_round}_{j}"):
                        c1,c2=st.columns(2)
                        newb=c1.number_input('Blåt hold',min_value=0,
                                             max_value=int(d['target']) if d['target'] else 200,
                                             value=int(m['blue_score'] or 0),key=f'pp97_b_{selected_round}_{j}')
                        if d['target']:
                            newr=int(d['target'])-newb
                            c2.metric('Rødt hold',newr)
                        else:
                            newr=c2.number_input('Rødt hold',min_value=0,max_value=200,
                                                 value=int(m['red_score'] or 0),key=f'pp97_r_{selected_round}_{j}')
                        if st.form_submit_button('Gem rettelse', type='primary'):
                            if d['target'] and newb+newr != d['target']:
                                st.error(f'Scorerne skal tilsammen være {d["target"]} point.')
                            else:
                                m['blue_score']=int(newb)
                                m['red_score']=int(newr)
                                save()
                                st.success('Resultatet er gemt.')
                                st.rerun()
