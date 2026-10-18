import os
import django
from collections import defaultdict

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)
django.setup()

from django.db import connection, transaction
from leggi_orario import lezioni

# Ricostruisce una riga per ogni docente e giorno
orari = defaultdict(lambda: {
    str(ora): "" for ora in range(1, 8)
})

for lezione in lezioni:
    nome = lezione["docente"]
    giorno = lezione["giorno"]
    ora = str(lezione["ora"])
    classe = lezione["classe"]

    riga = orari[(nome, giorno)]

    if riga[ora] and riga[ora] != classe:
        raise ValueError(
            f"Conflitto: {nome}, {giorno}, ora {ora}: "
            f"{riga[ora]} / {classe}"
        )

    riga[ora] = classe

print(f"Righe da importare: {len(orari)}")

with transaction.atomic():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM public.orario")

        for (nome, giorno), ore in orari.items():
            cursor.execute("""
                INSERT INTO public.orario
                (nome, giorno, "1", "2", "3", "4", "5", "6", "7")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                nome,
                giorno,
                ore["1"],
                ore["2"],
                ore["3"],
                ore["4"],
                ore["5"],
                ore["6"],
                ore["7"],
            ])

print("Importazione completata.")
