"""Padel Samlet 2.0 — independently implemented mobile-first tournament app."""
import html
import json
import secrets
import re
import requests
import streamlit as st
from engine import make_round, make_fixed_pairs_round, table

st.set_page_config(page_title='Padel Samlet', page_icon='🎾', layout='centered', initial_sidebar_state='collapsed')
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


/* 4.5: Authentic overhead padel court, 20 x 10 proportions, net at midcourt. */
.padel-real-card {border:1px solid #427b7d;border-radius:20px;padding:12px;background:linear-gradient(145deg,#17363c,#0e252d);margin:12px 0 0}
.padel-real-top {display:flex;align-items:center;justify-content:space-between;color:#e8ffff;margin:0 2px 12px;gap:10px}
.padel-real-top .court-pill {white-space:nowrap}
.padel-real {width:min(100%,335px);aspect-ratio:1/1.84;margin:0 auto;position:relative;border:6px solid #688e92;border-radius:8px;background:linear-gradient(to bottom,#155a91 0%,#173e70 49.75%,#762b34 50.25%,#992f40 100%);box-shadow:inset 0 0 25px #09131c99,0 10px 30px #0005;overflow:hidden;isolation:isolate}
.padel-real:before {content:'';position:absolute;inset:6px;border:2px solid rgba(238,253,255,.75);z-index:1;pointer-events:none}
.padel-real:after {content:'';position:absolute;left:0;right:0;top:50%;height:5px;transform:translateY(-50%);background:repeating-linear-gradient(90deg,#e5f5f5 0 4px,#56727b 4px 7px);border-block:1px solid #f9ffff;z-index:3;pointer-events:none;box-shadow:0 0 6px #0009}
.padel-service {position:absolute;left:8px;right:8px;border-top:2px solid #eef8ffcf;z-index:2;pointer-events:none}
.padel-service.top {top:34.75%}.padel-service.bottom {top:65.25%}
.padel-center-upper,.padel-center-lower {position:absolute;left:50%;width:2px;transform:translateX(-50%);background:#f2fbffcf;z-index:2;pointer-events:none}
.padel-center-upper {top:34.75%;height:15.25%}.padel-center-lower {top:50%;height:15.25%}
.padel-team {position:absolute;left:5%;right:5%;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:8px;z-index:4;color:#fff;font-weight:750;text-align:center;font-size:clamp(12px,3.4vw,16px)}
.padel-team.blue {top:5%;height:22%}.padel-team.red {bottom:5%;height:22%}
.padel-player {background:#071a2ab8;border-radius:7px;max-width:100%;padding:5px 8px;overflow-wrap:anywhere;text-shadow:0 1px 3px #000}
.padel-team.red .padel-player {background:#2d0f19b8}
.padel-net-badge{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:5;border:2px solid #40dec2;border-radius:50%;background:#0c2e35;color:#fff;padding:7px;font-weight:850;font-size:12px}
/* Native Streamlit score controls are positioned over the court, not in an iframe. */
.padel-score-label{font-weight:760;color:#fff;font-size:13px;text-align:center;position:relative;z-index:20;text-shadow:0 1px 4px #000}
.padel-score-overlay {height:0;position:relative;z-index:20}
[class*="st-key-on_court_score_"] {position:relative!important;z-index:21!important;margin:-225px auto 166px!important;max-width:420px!important;padding:0 10px!important}
.padel-scores-below {display:none}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] input {background:#f0f5f8!important;color:#15252c!important;font-size:22px!important;font-weight:900!important;border-radius:10px!important}
[class*="st-key-on_court_score_"] [data-testid="stNumberInput"] button {min-width:28px!important}
.padel-auto-score{background:#f0f5f8;border:2px solid #f58b93;border-radius:10px;padding:12px 4px;color:#13252c;font-weight:900;text-align:center;font-size:22px;min-height:56px}
.padel-auto-score small{display:block;font-size:10px;color:#3a464c;font-weight:650}
.padel-score-foot{color:#d7eeee;font-size:12px;text-align:center;margin-top:4px}
@media(min-width:650px){[class*="st-key-on_court_score_"]{margin-top:-225px!important;margin-bottom:166px!important}}
@media(max-width:470px){.padel-real{width:min(100%,300px)}[class*="st-key-on_court_score_"]{margin-top:-205px!important;margin-bottom:144px!important}.padel-player{font-size:12px}.padel-real-card{padding:9px}}
</style>
'''
st.markdown(STYLE, unsafe_allow_html=True)


def fresh():
    return {'title':'Søndagspadel','players':[],'format':'Mexicano','round_limit':7,'target':32,
            'round':0,'matches':[],'history':[],'byes':[],'partner_mode':'Skiftende makker'}


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
                d.update(title=title,players=players,format=fmt,partner_mode=partner_mode,round_limit=int(rounds),target=int(target))
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
        if d['byes']:
            st.info('Sidder over denne runde: '+', '.join(d['byes']))
        # Indtast alle kampresultater først. Hele runden gemmes i ét databasekald.
        resultater = []
        for i, m in enumerate(d['matches']):
            a = [html.escape(name) for name in m['blue']]
            b = [html.escape(name) for name in m['red']]
            # Portrait, overhead court: both service lines are 6.95 m from
            # the net; centre service line exists ONLY between service lines
            # and net. Real scoring widgets float over the court image.
            court = f'''<div class="padel-real-card">
              <div class="padel-real-top"><span class="court-pill">Bane {m['court']}</span><span>Runde {d['round']}</span></div>
              <div class="padel-real">
                <div class="padel-service top"></div><div class="padel-service bottom"></div>
                <div class="padel-center-upper"></div><div class="padel-center-lower"></div>
                <div class="padel-team blue"><span class="padel-player">{a[0]}</span><span class="padel-player">{a[1]}</span></div>
                <div class="padel-team red"><span class="padel-player">{b[0]}</span><span class="padel-player">{b[1]}</span></div>
                <div class="padel-net-badge">VS</div>
              </div></div>'''
            st.markdown(court, unsafe_allow_html=True)
            st.markdown('<div class="padel-score-overlay"></div>',unsafe_allow_html=True)
            # Keep native Streamlit inputs for keyboard/phone usability.
            # Streamlit lays the two columns over the central court area.
            with st.container(key=f"on_court_score_{d['round']}_{i}"):
                col1, col2 = st.columns(2, gap='small')
                with col1:
                    st.markdown('<div class="padel-score-label">Blåt hold</div>',unsafe_allow_html=True)
                    v1 = st.number_input('Blå score',min_value=0,
                                         max_value=int(d['target']) if d['target'] else 200,
                                         value=m['blue_score'],key=f"blue_{d['round']}_{i}",
                                         placeholder='Score',label_visibility='collapsed')
                with col2:
                    st.markdown('<div class="padel-score-label">Rødt hold</div>',unsafe_allow_html=True)
                    if d['target']:
                        v2 = None if v1 is None else int(d['target']) - int(v1)
                        st.markdown(f'<div class="padel-auto-score">{"–" if v2 is None else v2}<small>automatisk</small></div>',unsafe_allow_html=True)
                    else:
                        v2 = st.number_input('Rød score',min_value=0,max_value=200,
                                             value=m['red_score'],key=f"red_{d['round']}_{i}",
                                             placeholder='Score',label_visibility='collapsed')
            st.markdown('<div class="padel-score-foot">Indtast scoren direkte på banen</div>',unsafe_allow_html=True)
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
