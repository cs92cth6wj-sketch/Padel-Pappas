# Padel Pappas 11.3 – Dit valgte logo

Logoet i denne pakke er lavet direkte fra det JPEG-billede, du uploadede. Ingen ændringer i logo, tekst eller farver. Ikonerne er eksporteret til forskellige størrelser.

# Padel Pappas 11.2 – Logo og iPhone-ikon

## Upload til GitHub
Kopiér **alle** filerne og mapperne til roden af dit Padel-Pappas-repository:

- `streamlit_app.py` (erstatter den tidligere version)
- `app_icon.png`
- `.streamlit/config.toml`
- `static/apple-touch-icon.png`
- `static/icon-192.png`
- `static/icon-512.png`
- `static/manifest.json`

Hvis du allerede har `.streamlit/config.toml` med andre indstillinger, **flet** blot `[server] enableStaticServing = true` ind i den eksisterende fil. Slet ikke eksisterende konfiguration eller Secrets.

## Hvad virker
Streamlit anvender `app_icon.png` som sit browserfavicon via `st.set_page_config`. Static-serving og ikon/manifest-filerne bliver gjort tilgængelige for en fremtidig eller separat PWA-startside.

## Begrænsning på iPhone
Streamlit Cloud giver ikke en dokumenteret, pålidelig måde at tilføje egen `apple-touch-icon`/manifest-tag til hovedsidens HTML-head. Derfor er **det ikke garanteret**, at Safari bruger logoet som hjemmeskærmsikon alene med disse ændringer. Hvis Safari stadig viser et andet ikon, kræver en garanteret løsning en selvstændig webapp-startside på et domæne med fuld kontrol over `<head>` og manifest (eller et PWA-wrapper-site, f.eks. GitHub Pages).

Fjern tidligere hjemmeskærmsgenvej og tilføj igen via Safari → Del → Føj til hjemmeskærm → Åbn som webapp.

## Test
Python-syntaks, billede, JSON og ZIP er valideret. Ingen live-test af iPhone-ikon på Streamlit Cloud er gennemført.
