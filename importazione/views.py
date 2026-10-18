
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .analizza_orario import (
    analizza_file,
    crea_righe_anteprima,
    controlla_conflitti,
    importa_lezioni,
)


@staff_member_required
def pagina_importazione(request):
    messaggio = None
    errore = False
    anteprima = None

    if request.method == "POST":
        azione = request.POST.get("azione")

        # Fase 1: conferma dell'importazione
        if azione == "conferma_importazione":
            lezioni = request.session.get("orario_import_lezioni")

            if not lezioni:
                messaggio = (
                    "Non ci sono dati da importare. "
                    "Carica nuovamente il file Excel."
                )
                errore = True

            else:
                conflitti = controlla_conflitti(lezioni)

                if conflitti:
                    messaggio = (
                        "Importazione annullata: "
                        f"rilevati {len(conflitti)} conflitti."
                    )
                    errore = True

                else:
                    try:
                        numero_righe = importa_lezioni(lezioni)

                        request.session.pop(
                            "orario_import_lezioni", None
                        )

                        messaggio = (
                            "Importazione completata correttamente. "
                            f"Righe inserite: {numero_righe}."
                        )

                    except Exception:
                        messaggio = (
                            "Importazione non completata. "
                            "La transazione è stata annullata. "
                            "Controlla i log del server."
                        )
                        errore = True

        # Fase 2: caricamento e analisi del file
        else:
            file_excel = request.FILES.get("file_excel")

            if not file_excel:
                messaggio = "Seleziona un file Excel."
                errore = True

            elif not file_excel.name.lower().endswith(".xlsx"):
                messaggio = (
                    "Il file deve essere in formato Excel .xlsx."
                )
                errore = True

            else:
                try:
                    anteprima = analizza_file(file_excel)
                    lezioni = anteprima["lezioni"]

                    anteprima["righe"] = crea_righe_anteprima(lezioni)
                    anteprima["conflitti"] = controlla_conflitti(lezioni)
                    anteprima["numero_conflitti"] = len(
                        anteprima["conflitti"]
                    )

                    if anteprima["numero_conflitti"] == 0:
                        request.session["orario_import_lezioni"] = lezioni
                        messaggio = (
                            f"Analisi completata: "
                            f"{anteprima['numero_docenti']} docenti e "
                            f"{anteprima['numero_lezioni']} assegnazioni."
                        )
                    else:
                        request.session.pop(
                            "orario_import_lezioni", None
                        )
                        messaggio = (
                            "Analisi completata, ma sono presenti "
                            "conflitti da correggere."
                        )
                        errore = True

                except Exception:
                    messaggio = (
                        "Errore durante la lettura del file Excel. "
                        "Verifica il formato e riprova."
                    )
                    errore = True

    return render(
        request,
        "importazione/carica_orario.html",
        {
            "messaggio": messaggio,
            "errore": errore,
            "anteprima": anteprima,
        },
    )


