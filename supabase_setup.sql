-- Kør i Supabase SQL Editor. Tabellen kan kun læses/ændres via serverens secret key.
create table if not exists public.tournaments (
 id text primary key,
 data jsonb not null,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now()
);
alter table public.tournaments enable row level security;
-- Ingen policies for anon/authenticated. Service role omgår RLS.
create or replace function public.tournaments_set_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end;
$$;
drop trigger if exists trg_tournaments_updated_at on public.tournaments;
create trigger trg_tournaments_updated_at before update on public.tournaments
for each row execute function public.tournaments_set_updated_at();
