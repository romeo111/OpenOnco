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
