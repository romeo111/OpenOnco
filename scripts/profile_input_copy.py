"""Localized structural JSON errors, separate from clinical decisions."""
KEYS = ('json', 'object', 'finite', 'section')
VALUES = {
 'en': ('Enter valid JSON.', 'The profile must be a JSON object.', 'The profile contains a non-finite number.', 'This profile section must be an object or null:'),
 'uk': ('Введіть коректний JSON.', 'Профіль має бути JSON-об’єктом.', 'Профіль містить нескінченне або нечислове значення.', 'Цей розділ профілю має бути об’єктом або null:'),
 'es': ('Introduzca JSON válido.', 'El perfil debe ser un objeto JSON.', 'El perfil contiene un número no finito.', 'Esta sección del perfil debe ser un objeto o null:'),
 'pt': ('Introduza JSON válido.', 'O perfil deve ser um objeto JSON.', 'O perfil contém um número não finito.', 'Esta secção do perfil deve ser um objeto ou null:'),
 'de': ('Geben Sie gültiges JSON ein.', 'Das Profil muss ein JSON-Objekt sein.', 'Das Profil enthält eine nicht endliche Zahl.', 'Dieser Profilabschnitt muss ein Objekt oder null sein:'),
 'fr': ('Saisissez un JSON valide.', 'Le profil doit être un objet JSON.', 'Le profil contient un nombre non fini.', 'Cette section du profil doit être un objet ou null :'),
 'it': ('Inserisci JSON valido.', 'Il profilo deve essere un oggetto JSON.', 'Il profilo contiene un numero non finito.', 'Questa sezione del profilo deve essere un oggetto o null:'),
 'da': ('Indtast gyldig JSON.', 'Profilen skal være et JSON-objekt.', 'Profilen indeholder et ikke-endeligt tal.', 'Dette profilafsnit skal være et objekt eller null:'),
 'sv': ('Ange giltig JSON.', 'Profilen måste vara ett JSON-objekt.', 'Profilen innehåller ett tal som inte är ändligt.', 'Detta profilavsnitt måste vara ett objekt eller null:'),
 'nb': ('Skriv inn gyldig JSON.', 'Profilen må være et JSON-objekt.', 'Profilen inneholder et ikke-endelig tall.', 'Denne profildelen må være et objekt eller null:'),
 'fi': ('Anna kelvollinen JSON.', 'Profiilin on oltava JSON-objekti.', 'Profiili sisältää luvun, joka ei ole äärellinen.', 'Tämän profiilin osan on oltava objekti tai null:'),
}
COPY = {locale: dict(zip(KEYS, values)) for locale, values in VALUES.items()}

TRANSFER = {
'en': 'Keep this profile in JSON mode: select the matching disease form and use values supported by its fields. Your JSON has been preserved.',
'uk': 'Залиште цей профіль у режимі JSON: виберіть анкету відповідної хвороби та значення, які підтримують її поля. Ваш JSON збережено.',
'es': 'Mantenga este perfil en modo JSON: seleccione el formulario de la enfermedad correspondiente y valores compatibles con sus campos. Su JSON se conserva.',
'pt': 'Mantenha este perfil no modo JSON: selecione o formulário da doença correspondente e valores compatíveis com os campos. O seu JSON foi preservado.',
'de': 'Belassen Sie dieses Profil im JSON-Modus: Wählen Sie das passende Krankheitsformular und unterstützte Feldwerte. Ihr JSON bleibt erhalten.',
'fr': 'Gardez ce profil en mode JSON : choisissez le formulaire de la maladie correspondante et des valeurs prises en charge. Votre JSON est conservé.',
'it': 'Mantieni questo profilo in modalità JSON: scegli il modulo della malattia corrispondente e valori supportati dai campi. Il JSON è conservato.',
'da': 'Behold profilen i JSON-tilstand: Vælg formularen for den rette sygdom og værdier, som felterne understøtter. Din JSON er bevaret.',
'sv': 'Behåll profilen i JSON-läge: Välj formuläret för rätt sjukdom och värden som fälten stöder. Din JSON har bevarats.',
'nb': 'Behold profilen i JSON-modus: Velg skjemaet for riktig sykdom og verdier som feltene støtter. Din JSON er bevart.',
'fi': 'Pidä profiili JSON-tilassa: valitse vastaavan sairauden lomake ja kenttien tukemat arvot. JSON on säilytetty.',
}
for locale, message in TRANSFER.items():
    COPY[locale]['transfer'] = message
