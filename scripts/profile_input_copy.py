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

RESTORE = {
'en': ('JSON draft restored. Review it before generating a report.', 'JSON draft restored; its questionnaire could not be loaded. You can continue in JSON mode.'),
'uk': ('Чернетку JSON відновлено. Перевірте її перед створенням звіту.', 'Чернетку JSON відновлено; анкету завантажити не вдалося. Можна продовжити в режимі JSON.'),
'es': ('Borrador JSON restaurado. Revíselo antes de generar un informe.', 'Borrador JSON restaurado; no se pudo cargar su cuestionario. Puede continuar en modo JSON.'),
'pt': ('Rascunho JSON restaurado. Reveja-o antes de gerar um relatório.', 'Rascunho JSON restaurado; não foi possível carregar o questionário. Pode continuar no modo JSON.'),
'de': ('JSON-Entwurf wiederhergestellt. Prüfen Sie ihn vor dem Erstellen eines Berichts.', 'JSON-Entwurf wiederhergestellt; der Fragebogen konnte nicht geladen werden. Sie können im JSON-Modus fortfahren.'),
'fr': ('Brouillon JSON restauré. Vérifiez-le avant de générer un rapport.', 'Brouillon JSON restauré ; le questionnaire n’a pas pu être chargé. Vous pouvez continuer en mode JSON.'),
'it': ('Bozza JSON ripristinata. Controllala prima di generare un rapporto.', 'Bozza JSON ripristinata; impossibile caricare il questionario. Puoi continuare in modalità JSON.'),
'da': ('JSON-kladde gendannet. Kontrollér den, før du opretter en rapport.', 'JSON-kladde gendannet; spørgeskemaet kunne ikke indlæses. Du kan fortsætte i JSON-tilstand.'),
'sv': ('JSON-utkast återställt. Granska det innan du skapar en rapport.', 'JSON-utkast återställt; frågeformuläret kunde inte läsas in. Du kan fortsätta i JSON-läge.'),
'nb': ('JSON-utkast gjenopprettet. Kontroller det før du lager en rapport.', 'JSON-utkast gjenopprettet; spørreskjemaet kunne ikke lastes inn. Du kan fortsette i JSON-modus.'),
'fi': ('JSON-luonnos palautettu. Tarkista se ennen raportin luomista.', 'JSON-luonnos palautettu; kyselylomaketta ei voitu ladata. Voit jatkaa JSON-tilassa.'),
}
for locale, messages in RESTORE.items():
    COPY[locale]['restored'], COPY[locale]['restoreLimited'] = messages

QUESTIONNAIRE_LOAD = {
'en': ('The selected questionnaire is unavailable or does not match this disease.', 'Could not load the selected disease form. Your previous form, answers and report have been retained. Try again.'),
'uk': ('Вибрана анкета недоступна або не відповідає цій хворобі.', 'Не вдалося завантажити анкету вибраної хвороби. Попередню анкету, відповіді та звіт збережено. Спробуйте ще раз.'),
'es': ('El cuestionario seleccionado no está disponible o no corresponde a esta enfermedad.', 'No se pudo cargar el formulario seleccionado. Se conservan el formulario, las respuestas y el informe anteriores. Inténtelo de nuevo.'),
'pt': ('O questionário selecionado está indisponível ou não corresponde a esta doença.', 'Não foi possível carregar o formulário selecionado. O formulário, as respostas e o relatório anteriores foram preservados. Tente novamente.'),
'de': ('Der ausgewählte Fragebogen ist nicht verfügbar oder passt nicht zu dieser Krankheit.', 'Das ausgewählte Formular konnte nicht geladen werden. Das bisherige Formular, die Antworten und der Bericht bleiben erhalten. Versuchen Sie es erneut.'),
'fr': ('Le questionnaire sélectionné est indisponible ou ne correspond pas à cette maladie.', 'Impossible de charger le formulaire sélectionné. Le formulaire, les réponses et le rapport précédents sont conservés. Réessayez.'),
'it': ('Il questionario selezionato non è disponibile o non corrisponde a questa malattia.', 'Impossibile caricare il modulo selezionato. Il modulo, le risposte e il rapporto precedenti sono conservati. Riprova.'),
'da': ('Det valgte spørgeskema er utilgængeligt eller passer ikke til denne sygdom.', 'Den valgte formular kunne ikke indlæses. Din tidligere formular, svar og rapport er bevaret. Prøv igen.'),
'sv': ('Det valda frågeformuläret är inte tillgängligt eller motsvarar inte denna sjukdom.', 'Det valda formuläret kunde inte läsas in. Ditt tidigare formulär, svar och rapport har bevarats. Försök igen.'),
'nb': ('Det valgte spørreskjemaet er utilgjengelig eller passer ikke til denne sykdommen.', 'Det valgte skjemaet kunne ikke lastes inn. Ditt tidligere skjema, svar og rapport er bevart. Prøv igjen.'),
'fi': ('Valittu kyselylomake ei ole saatavilla tai ei vastaa tätä sairautta.', 'Valittua lomaketta ei voitu ladata. Aiempi lomake, vastaukset ja raportti on säilytetty. Yritä uudelleen.'),
}
for locale, messages in QUESTIONNAIRE_LOAD.items():
    COPY[locale]['questionnaireUnavailable'], COPY[locale]['switchFailed'] = messages
