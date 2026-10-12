"""Reviewed display wording for browser storage; never translate JS options."""

LOCALES = ('it', 'da', 'sv', 'nb', 'fi')

COPY = {
    'Cache': ('Cache', 'Cache', 'Cache', 'Mellomlager', 'Välimuisti'),
    'Cache failed': ('Salvataggio nella cache non riuscito', 'Lagring i cache mislykkedes', 'Lagring i cache misslyckades', 'Lagring i mellomlager mislyktes', 'Tallennus välimuistiin epäonnistui'),
    'Cache unavailable': ('Cache non disponibile', 'Cache er ikke tilgængelig', 'Cache är inte tillgänglig', 'Mellomlager er ikke tilgjengelig', 'Välimuisti ei ole käytettävissä'),
    'Cached with some failed modules': ('Alcuni moduli non sono stati salvati nella cache', 'Nogle moduler blev ikke gemt i cache', 'Vissa moduler kunde inte sparas i cache', 'Noen moduler kunne ikke lagres i mellomlager', 'Joitakin moduuleja ei voitu tallentaa välimuistiin'),
    'Offline - cached bundles only': ('Offline: solo pacchetti salvati nella cache', 'Offline: kun pakker gemt i cache', 'Offline: endast paket sparade i cache', 'Frakoblet: bare pakker lagret i mellomlager', 'Ei verkkoyhteyttä: vain välimuistiin tallennetut paketit'),
    'Offline cache not started': ('Salvataggio nella cache per uso offline non avviato', 'Lagring i cache til offlinebrug er ikke startet', 'Lagring i cache för användning offline har inte startat', 'Lagring i mellomlager for frakoblet bruk er ikke startet', 'Tallennusta välimuistiin offline-käyttöä varten ei ole aloitettu'),
    'All modules cached for offline use': ('Tutti i moduli sono salvati nella cache per uso offline', 'Alle moduler er gemt i cache til offlinebrug', 'Alla moduler är sparade i cache för användning offline', 'Alle moduler er lagret i mellomlager for frakoblet bruk', 'Kaikki moduulit on tallennettu välimuistiin offline-käyttöä varten'),
    'Partial cache': ('Cache parziale', 'Delvis cache', 'Delvis cache', 'Delvis mellomlager', 'Osittainen välimuisti'),
    'Browser cache pending': ('Cache del browser in attesa', 'Browserens cache afventer', 'Webbläsarens cache väntar', 'Nettleserens mellomlager venter', 'Selainvälimuisti odottaa'),
}


def messages_for(locale):
    if locale not in LOCALES:
        return {}
    index = LOCALES.index(locale)
    return {source: values[index] for source, values in COPY.items()}
