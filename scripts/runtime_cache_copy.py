"""Native display copy for verified runtime retention, separate from clinical drafts."""
KEYS = ('label', 'unchecked', 'checking', 'ready', 'partial')
VALUES = {
    'en': ('Engine files', 'Not checked', 'Checking saved files…', 'Files saved', 'Files incomplete'),
    'uk': ('Файли двигуна', 'Ще не перевірено', 'Перевіряю збережені файли…', 'Файли збережено', 'Не всі файли збережено'),
    'es': ('Archivos del motor', 'Sin comprobar', 'Comprobando archivos guardados…', 'Archivos guardados', 'Faltan archivos'),
    'pt': ('Ficheiros do motor', 'Por verificar', 'A verificar ficheiros guardados…', 'Ficheiros guardados', 'Faltam ficheiros'),
    'de': ('Programmdateien', 'Nicht geprüft', 'Gespeicherte Dateien werden geprüft…', 'Dateien gespeichert', 'Dateien fehlen'),
    'fr': ('Fichiers du moteur', 'Non vérifiés', 'Vérification des fichiers enregistrés…', 'Fichiers enregistrés', 'Fichiers manquants'),
    'it': ('File del motore', 'Non verificati', 'Verifica dei file salvati…', 'File salvati', 'File mancanti'),
    'da': ('Programfiler', 'Ikke kontrolleret', 'Kontrollerer gemte filer…', 'Filer gemt', 'Ikke alle filer er gemt'),
    'sv': ('Programfiler', 'Inte kontrollerade', 'Kontrollerar sparade filer…', 'Filer sparade', 'Alla filer är inte sparade'),
    'nb': ('Programfiler', 'Ikke kontrollert', 'Kontrollerer lagrede filer…', 'Filer lagret', 'Ikke alle filer er lagret'),
    'fi': ('Ohjelmatiedostot', 'Ei tarkistettu', 'Tarkistetaan tallennettuja tiedostoja…', 'Tiedostot tallennettu', 'Tiedostoja puuttuu'),
}
COPY = {locale: dict(zip(KEYS, values)) for locale, values in VALUES.items()}


def messages_for(locale):
    return dict(zip(VALUES['en'], VALUES[locale]))
