# Padel Samlet 3.0 – turnerings-ID og Supabase

Opdateret fra Padel Samlet 2.0 med permanent database, administratorlogin og delbart turneringslink.

## Opsætning
1. Supabase: opret gratis projekt, gå til SQL Editor, indsæt alt fra `supabase_setup.sql`, vælg Run.
2. Supabase: under Project Settings/Connect/API Keys find Project URL og server-side secret key (`sb_secret_...` eller den ældre service_role JWT). **Brug ikke anon/publishable key**.
3. Streamlit Community Cloud > My apps > din app > Settings > Secrets:

```toml
SUPABASE_URL = "https://DIT_PROJEKT.supabase.co"
SUPABASE_SECRET_KEY = "DIN_SERVER_SIDE_SECRET_KEY"
ADMIN_PASSWORD = "EN_LANG_UNIK_ADMIN_KODE"
```

4. GitHub: upload/erstat `streamlit_app.py`, `engine.py`, `requirements.txt`, `supabase_setup.sql`, `README.md`. **Upload aldrig rigtige nøgler til GitHub**.
5. Når Streamlit starter, log ind med administratorkoden via venstremenuen. Opret turnering, indtast spillere, og del turnerings-ID eller link. Spillere kan læse resultater via link uden administratorkoden.

## Vigtigt
- Den offentlige webadresse giver læseadgang til turneringen for alle, der har turnerings-ID/link. Brug derfor ikke følsomme personoplysninger.
- Kun administrator kan oprette, ændre, nulstille turneringer og registrere resultater.
- Supabase gratisprojekt kan sættes på pause ved inaktivitet. Der kan også være usage limits.
- Simultane administratorændringer fra flere faner kan overskrive hinanden. Brug én administrator under turneringen.
- Dette er en ny funktionel kodeversion. Test med en prøveturnering, før den bruges til en vigtig turnering.
