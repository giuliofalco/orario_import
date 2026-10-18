
from collections import Counter
from leggi_orario import lezioni

# Ogni docente deve avere una sola riga per ciascun giorno.
coppie = [
    (lezione["docente"], lezione["giorno"])
    for lezione in lezioni
]

conteggi = Counter(coppie)
duplicati = {
    coppia: numero
    for coppia, numero in conteggi.items()
    if numero > 1
}

# Numero di docenti distinti e righe che saranno create in orario.
docenti = {lezione["docente"] for lezione in lezioni}
righe_orario = len(docenti) * 5

print("\n--- ANTEPRIMA IMPORTAZIONE ---")
print(f"Assegnazioni Excel: {len(lezioni)}")
print(f"Docenti distinti: {len(docenti)}")
print(f"Righe previste in orario: {righe_orario}")
print(f"Coppie docente/giorno duplicate: {len(duplicati)}")

if duplicati:
    print("\nATTENZIONE: duplicati trovati")
    for coppia, numero in duplicati.items():
        print(f"{coppia}: {numero} occorrenze")
else:
    print("\nNessun duplicato docente/giorno.")

print("\nPrime 10 coppie docente/giorno:")
for coppia in list(dict.fromkeys(coppie))[:10]:
    print(f"{coppia[0]} - {coppia[1]}")

print("\nNessuna modifica al database è stata eseguita.")

from collections import defaultdict
from leggi_orario import lezioni

# Una riga per ogni docente e giorno.
orari = defaultdict(lambda: {str(ora): "" for ora in range(1, 8)})

conflitti = []

for lezione in lezioni:
    docente = lezione["docente"]
    giorno = lezione["giorno"]
    ora = str(lezione["ora"])
    classe = lezione["classe"]

    riga = orari[(docente, giorno)]

    if riga[ora] and riga[ora] != classe:
        conflitti.append(
            (docente, giorno, ora, riga[ora], classe)
        )
    else:
        riga[ora] = classe

print("\n--- ANTEPRIMA IMPORTAZIONE ---")
print(f"Assegnazioni Excel: {len(lezioni)}")
print(f"Docenti distinti: {len({d for d, g in orari})}")
print(f"Righe da creare in orario: {len(orari)}")
print(f"Conflitti sulla stessa ora: {len(conflitti)}")

if conflitti:
    print("\nATTENZIONE: conflitti trovati")
    for conflitto in conflitti[:20]:
        print(conflitto)
else:
    print("\nNessun conflitto sulla stessa ora.")

print("\nEsempio di orario ricostruito:")
for chiave, ore in list(orari.items())[:3]:
    print(chiave, ore)

print("\nNessuna modifica al database.")
