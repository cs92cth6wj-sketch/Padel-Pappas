# Padel Samlet 2.0 – selvstændig prototype

Ny og selvstændigt implementeret Streamlit-app til Americano og Mexicano.

## Start lokalt

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Åbn sidepanelet og indsæt mindst fire spillere. Vælg turnering, point og runder. Kampene vises på en stiliseret padelbane, resultater indtastes og stillingen opdateres.

## Vigtige begrænsninger

- **Prototype, ikke klar til offentlig gruppebrug.** Data gemmes i `tournament_local.json` på serveren. Streamlit Community Cloud giver ikke vedvarende fillagring, og filen kan forsvinde ved genstart. For rigtig drift skal appen kobles på en varig database (eksempelvis Supabase) og have brugerstyring.
- Ingen login, individuel tilmelding eller MobilePay-integration endnu.
- Ved antal spillere som ikke er deleligt med fire, sidder de resterende over. I Americano vælges de tilfældigt, uden endnu at sikre lige mange pauser over tid.
- Mexicano prioriterer 1+3 mod 2+4 inden for hver gruppe af fire, men skifter opstilling, når det reducerer gentagne makkere.
- Denne selvstændige kode er **ikke** en 1:1 kopi af et tredjepartsprojekt. Funktioner kan afvige fra den oprindelige app; test med din gruppe.
- `tournament_local.json` skal ikke deles offentligt. Den er udelukket i `.gitignore`.
