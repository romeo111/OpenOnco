"""Non-clinical validation copy for the guided numeric controls."""
KEYS = ('number', 'integer', 'range', 'summary')
VALUES = {
    'en': ('Enter a valid number.', 'Enter a whole number.', 'Use a value within these limits:', 'Fix the highlighted numeric fields before generating or opening JSON.'),
    'uk': ('Введіть коректне число.', 'Введіть ціле число.', 'Введіть значення в цих межах:', 'Виправте виділені числові поля перед генерацією або відкриттям JSON.'),
    'es': ('Introduzca un número válido.', 'Introduzca un número entero.', 'Use un valor dentro de estos límites:', 'Corrija los campos numéricos resaltados antes de generar o abrir JSON.'),
    'pt': ('Introduza um número válido.', 'Introduza um número inteiro.', 'Use um valor dentro destes limites:', 'Corrija os campos numéricos destacados antes de gerar ou abrir JSON.'),
    'de': ('Geben Sie eine gültige Zahl ein.', 'Geben Sie eine ganze Zahl ein.', 'Verwenden Sie einen Wert innerhalb dieser Grenzen:', 'Korrigieren Sie die markierten Zahlenfelder, bevor Sie den Plan erstellen oder JSON öffnen.'),
    'fr': ('Saisissez un nombre valide.', 'Saisissez un nombre entier.', 'Utilisez une valeur dans ces limites :', 'Corrigez les champs numériques signalés avant de générer le plan ou d’ouvrir JSON.'),
    'it': ('Inserisci un numero valido.', 'Inserisci un numero intero.', 'Usa un valore entro questi limiti:', 'Correggi i campi numerici evidenziati prima di generare il piano o aprire JSON.'),
    'da': ('Indtast et gyldigt tal.', 'Indtast et helt tal.', 'Brug en værdi inden for disse grænser:', 'Ret de markerede talfelter, før du genererer planen eller åbner JSON.'),
    'sv': ('Ange ett giltigt tal.', 'Ange ett heltal.', 'Ange ett värde inom dessa gränser:', 'Rätta de markerade talfälten innan du skapar planen eller öppnar JSON.'),
    'nb': ('Skriv inn et gyldig tall.', 'Skriv inn et helt tall.', 'Bruk en verdi innenfor disse grensene:', 'Rett de markerte tallfeltene før du genererer planen eller åpner JSON.'),
    'fi': ('Anna kelvollinen luku.', 'Anna kokonaisluku.', 'Anna arvo näiden rajojen sisällä:', 'Korjaa korostetut numerokentät ennen suunnitelman luomista tai JSONin avaamista.'),
}
COPY = {locale: dict(zip(KEYS, values)) for locale, values in VALUES.items()}

SYNC = {
    'en': 'Re-enter this number to confirm it.',
    'uk': 'Введіть це число повторно, щоб підтвердити його.',
    'es': 'Vuelva a introducir este número para confirmarlo.',
    'pt': 'Introduza novamente este número para o confirmar.',
    'de': 'Geben Sie diese Zahl zur Bestätigung erneut ein.',
    'fr': 'Saisissez à nouveau ce nombre pour le confirmer.',
    'it': 'Inserisci di nuovo questo numero per confermarlo.',
    'da': 'Indtast dette tal igen for at bekræfte det.',
    'sv': 'Ange detta tal igen för att bekräfta det.',
    'nb': 'Skriv inn dette tallet på nytt for å bekrefte det.',
    'fi': 'Vahvista tämä luku kirjoittamalla se uudelleen.',
}
for locale, text in SYNC.items():
    COPY[locale]['sync'] = text
