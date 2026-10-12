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

EXAMPLE_LOAD = {
'en': ('The selected example is unavailable or its profile does not match the selected disease.', 'Could not load the selected example. Your existing input and report have been retained. Try again.', 'The example profile is loaded, but its report is unavailable. You can generate a new report.', 'Example profile loaded. Review its data and sources before use.'),
'uk': ('Вибраний приклад недоступний або його профіль не відповідає вибраній хворобі.', 'Не вдалося завантажити вибраний приклад. Поточні дані та звіт збережено. Спробуйте ще раз.', 'Профіль прикладу завантажено, але його звіт недоступний. Можна створити новий звіт.', 'Профіль прикладу завантажено. Перевірте його дані та джерела перед використанням.'),
'es': ('El ejemplo seleccionado no está disponible o su perfil no corresponde a la enfermedad seleccionada.', 'No se pudo cargar el ejemplo. Se conservan los datos y el informe actuales. Inténtelo de nuevo.', 'El perfil del ejemplo está cargado, pero su informe no está disponible. Puede generar un informe nuevo.', 'Perfil de ejemplo cargado. Revise sus datos y fuentes antes de usarlo.'),
'pt': ('O exemplo selecionado está indisponível ou o seu perfil não corresponde à doença selecionada.', 'Não foi possível carregar o exemplo. Os dados e o relatório atuais foram preservados. Tente novamente.', 'O perfil do exemplo foi carregado, mas o relatório está indisponível. Pode gerar um novo relatório.', 'Perfil de exemplo carregado. Reveja os dados e as fontes antes de o utilizar.'),
'de': ('Das ausgewählte Beispiel ist nicht verfügbar oder sein Profil passt nicht zur ausgewählten Krankheit.', 'Das Beispiel konnte nicht geladen werden. Ihre bisherigen Daten und der Bericht bleiben erhalten. Versuchen Sie es erneut.', 'Das Beispielprofil ist geladen, aber der Bericht ist nicht verfügbar. Sie können einen neuen Bericht erstellen.', 'Beispielprofil geladen. Prüfen Sie Daten und Quellen vor der Verwendung.'),
'fr': ('L’exemple sélectionné est indisponible ou son profil ne correspond pas à la maladie sélectionnée.', 'Impossible de charger l’exemple. Vos données et le rapport actuels sont conservés. Réessayez.', 'Le profil de l’exemple est chargé, mais son rapport est indisponible. Vous pouvez générer un nouveau rapport.', 'Profil d’exemple chargé. Vérifiez ses données et ses sources avant utilisation.'),
'it': ('L’esempio selezionato non è disponibile o il suo profilo non corrisponde alla malattia selezionata.', 'Impossibile caricare l’esempio. I dati e il rapporto attuali sono conservati. Riprova.', 'Il profilo di esempio è caricato, ma il rapporto non è disponibile. Puoi generare un nuovo rapporto.', 'Profilo di esempio caricato. Controlla i dati e le fonti prima di usarlo.'),
'da': ('Det valgte eksempel er utilgængeligt, eller profilen passer ikke til den valgte sygdom.', 'Eksemplet kunne ikke indlæses. Dine nuværende data og rapport er bevaret. Prøv igen.', 'Eksempelprofilen er indlæst, men rapporten er utilgængelig. Du kan oprette en ny rapport.', 'Eksempelprofil indlæst. Kontrollér data og kilder før brug.'),
'sv': ('Det valda exemplet är inte tillgängligt eller dess profil motsvarar inte den valda sjukdomen.', 'Exemplet kunde inte läsas in. Dina nuvarande uppgifter och rapport har bevarats. Försök igen.', 'Exempelprofilen har lästs in, men rapporten är inte tillgänglig. Du kan skapa en ny rapport.', 'Exempelprofil inläst. Granska uppgifter och källor före användning.'),
'nb': ('Det valgte eksemplet er utilgjengelig, eller profilen passer ikke til den valgte sykdommen.', 'Eksemplet kunne ikke lastes inn. Dine nåværende data og rapport er bevart. Prøv igjen.', 'Eksempelprofilen er lastet inn, men rapporten er utilgjengelig. Du kan lage en ny rapport.', 'Eksempelprofil lastet inn. Kontroller data og kilder før bruk.'),
'fi': ('Valittu esimerkki ei ole saatavilla tai sen profiili ei vastaa valittua sairautta.', 'Esimerkkiä ei voitu ladata. Nykyiset tietosi ja raportti on säilytetty. Yritä uudelleen.', 'Esimerkkiprofiili on ladattu, mutta raportti ei ole saatavilla. Voit luoda uuden raportin.', 'Esimerkkiprofiili ladattu. Tarkista tiedot ja lähteet ennen käyttöä.'),
}
for locale, messages in EXAMPLE_LOAD.items():
    COPY[locale].update(zip(('exampleUnavailable', 'exampleFailed', 'exampleReportFailed', 'exampleLoaded'), messages))

REPORT_INVALID = {
'en': 'The loaded page is not a readable OpenOnco report. Try generating the report again.',
'uk': 'Завантажена сторінка не є доступним для читання звітом OpenOnco. Спробуйте створити звіт заново.',
'es': 'La página cargada no es un informe legible de OpenOnco. Intente generar el informe de nuevo.',
'pt': 'A página carregada não é um relatório legível do OpenOnco. Tente gerar o relatório novamente.',
'de': 'Die geladene Seite ist kein lesbarer OpenOnco-Bericht. Versuchen Sie, den Bericht erneut zu erstellen.',
'fr': 'La page chargée n’est pas un rapport OpenOnco lisible. Essayez de générer le rapport à nouveau.',
'it': 'La pagina caricata non è un rapporto OpenOnco leggibile. Prova a generare nuovamente il rapporto.',
'da': 'Den indlæste side er ikke en læsbar OpenOnco-rapport. Prøv at oprette rapporten igen.',
'sv': 'Den inlästa sidan är inte en läsbar OpenOnco-rapport. Försök skapa rapporten igen.',
'nb': 'Den innlastede siden er ikke en lesbar OpenOnco-rapport. Prøv å lage rapporten på nytt.',
'fi': 'Ladattu sivu ei ole luettava OpenOnco-raportti. Yritä luoda raportti uudelleen.',
}
for locale, message in REPORT_INVALID.items():
    COPY[locale]['reportInvalid'] = message
