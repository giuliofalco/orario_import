import os
import django
from collections import defaultdict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import connection

# Legge i nominativi già presenti nel database.
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT id, nome, cognome
        FROM docenti
        ORDER BY cognome, nome
    """)
    docenti_db = cursor.fetchall()

# Ricostruisce i nominativi presenti nell'Excel.
# Riutilizziamo la stessa funzione di lettura già verificata.
from leggi_orario import lezioni

docenti_excel = sorted({x["docente"] for x in lezioni})

def normalizza(testo):
    return " ".join((testo or "").upper().split())

# Indice dei docenti per cognome.
per_cognome = defaultdict(list)

for id_docente, nome, cognome in docenti_db:
    cognome_norm = normalizza(cognome)
    if cognome_norm:
        per_cognome[cognome_norm].append(
            (id_docente, normalizza(nome), cognome_norm)
        )

print("\n--- CONFRONTO NOMINATIVI ---")

for nominativo in docenti_excel:
    parti = normalizza(nominativo).split()

    if len(parti) == 1:
        cognome = parti[0]
        candidati = per_cognome.get(cognome, [])
    else:
        cognome = parti[0] if parti[0] in per_cognome else parti[-1]
        candidati = per_cognome.get(cognome, [])

    if len(candidati) == 1:
        id_docente, nome, cognome_db = candidati[0]
        print(f"DA VERIFICARE: {nominativo:30} -> {id_docente} {nome} {cognome_db}")
    elif len(candidati) > 1:
        print(f"AMBIGUO:      {nominativo:30} -> {candidati}")
    else:
        print(f"N NON TROVATO: {nominativo}")
