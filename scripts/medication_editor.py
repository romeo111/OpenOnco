"""Local medication editor configuration; names come from exact catalog records."""

import json
from pathlib import Path

import yaml

KEYS = [
    "title",
    "status",
    "unknown",
    "partial",
    "complete",
    "drugs",
    "selectHelp",
    "apply",
    "notice",
    "unsupported",
    "invalid",
    "changed",
    "saved",
]
ROWS = {
    "en": [
        "Concomitant medicines · JSON editor",
        "List completeness",
        "Unknown",
        "Partial list",
        "Complete list (reported by you)",
        "Select active medicines",
        "Select or deselect medicines using your device’s multiple-selection controls.",
        "Apply to JSON",
        "This catalog is limited. If a medicine is missing, keep the list partial. Your completeness statement is not independently verified; this does not check all interactions. Historical treatment is separate.",
        "Unsupported medication fields are present. Correct them in JSON; this editor will not overwrite them.",
        "Check the JSON and medication fields. Known medicines require partial or complete status.",
        "The JSON changed. Close and reopen this editor before applying.",
        "Medication list saved to this local profile.",
    ],
    "uk": [
        "Супутні ліки · редактор JSON",
        "Повнота переліку",
        "Невідомо",
        "Частковий перелік",
        "Повний перелік (за вашими даними)",
        "Виберіть ліки, які приймаються зараз",
        "Вибирайте або знімайте вибір ліків засобами множинного вибору вашого пристрою.",
        "Застосувати до JSON",
        "Каталог обмежений. Якщо препарату немає, залиште перелік частковим. Заявлена вами повнота незалежно не перевірена; це не перевірка всіх взаємодій. Попереднє лікування вказується окремо.",
        "Є непідтримувані поля ліків. Виправте їх у JSON; редактор не перезаписуватиме їх.",
        "Перевірте JSON і поля ліків. Для відомих ліків потрібен частковий або повний статус.",
        "JSON змінився. Закрийте й знову відкрийте редактор перед застосуванням.",
        "Перелік ліків збережено в цьому локальному профілі.",
    ],
    "es": [
        "Medicamentos concomitantes · editor JSON",
        "Integridad de la lista",
        "Desconocida",
        "Lista parcial",
        "Lista completa (según usted)",
        "Seleccione los medicamentos actuales",
        "Seleccione o deseleccione medicamentos con los controles de selección múltiple de su dispositivo.",
        "Aplicar al JSON",
        "El catálogo es limitado. Si falta un medicamento, mantenga la lista parcial. Su declaración de integridad no se verifica de forma independiente; esto no comprueba todas las interacciones. Los tratamientos previos se registran por separado.",
        "Hay campos de medicación no admitidos. Corríjalos en JSON; el editor no los sobrescribirá.",
        "Revise el JSON y los campos de medicación. Los medicamentos conocidos requieren el estado parcial o completo.",
        "El JSON ha cambiado. Cierre y vuelva a abrir el editor antes de aplicar.",
        "Lista de medicamentos guardada en este perfil local.",
    ],
    "pt": [
        "Medicamentos concomitantes · editor JSON",
        "Completude da lista",
        "Desconhecida",
        "Lista parcial",
        "Lista completa (segundo o utilizador)",
        "Selecione os medicamentos atuais",
        "Selecione ou desmarque medicamentos com os controlos de seleção múltipla do dispositivo.",
        "Aplicar ao JSON",
        "O catálogo é limitado. Se faltar um medicamento, mantenha a lista parcial. A completude declarada não é verificada de forma independente; isto não verifica todas as interações. Os tratamentos anteriores são registados separadamente.",
        "Existem campos de medicação não suportados. Corrija-os no JSON; o editor não os substituirá.",
        "Verifique o JSON e os campos de medicação. Medicamentos conhecidos exigem o estado parcial ou completo.",
        "O JSON foi alterado. Feche e reabra o editor antes de aplicar.",
        "Lista de medicamentos guardada neste perfil local.",
    ],
    "de": [
        "Begleitmedikation · JSON-Editor",
        "Vollständigkeit der Liste",
        "Unbekannt",
        "Unvollständige Liste",
        "Vollständige Liste (laut Ihrer Angabe)",
        "Aktuelle Medikamente auswählen",
        "Nutzen Sie die Mehrfachauswahl Ihres Geräts, um Medikamente aus- oder abzuwählen.",
        "In JSON übernehmen",
        "Der Katalog ist begrenzt. Fehlt ein Medikament, belassen Sie die Liste als unvollständig. Ihre Vollständigkeitsangabe wird nicht unabhängig geprüft; dies prüft nicht alle Wechselwirkungen. Frühere Behandlungen werden getrennt erfasst.",
        "Nicht unterstützte Medikationsfelder vorhanden. Korrigieren Sie diese im JSON; der Editor überschreibt sie nicht.",
        "Prüfen Sie JSON und Medikationsfelder. Bekannte Medikamente erfordern den Status unvollständig oder vollständig.",
        "Das JSON wurde geändert. Schließen und öffnen Sie den Editor erneut, bevor Sie Änderungen übernehmen.",
        "Medikamentenliste in diesem lokalen Profil gespeichert.",
    ],
    "fr": [
        "Médicaments concomitants · éditeur JSON",
        "Exhaustivité de la liste",
        "Inconnue",
        "Liste partielle",
        "Liste complète (selon vous)",
        "Sélectionnez les médicaments actuels",
        "Sélectionnez ou désélectionnez les médicaments avec les commandes de sélection multiple de votre appareil.",
        "Appliquer au JSON",
        "Ce catalogue est limité. Si un médicament manque, gardez une liste partielle. Votre déclaration d’exhaustivité n’est pas vérifiée indépendamment ; ceci ne vérifie pas toutes les interactions. Les traitements antérieurs sont enregistrés séparément.",
        "Des champs de médicaments non pris en charge sont présents. Corrigez-les dans le JSON ; cet éditeur ne les écrasera pas.",
        "Vérifiez le JSON et les champs de médicaments. Des médicaments connus exigent le statut partiel ou complet.",
        "Le JSON a changé. Fermez puis rouvrez cet éditeur avant d’appliquer.",
        "Liste des médicaments enregistrée dans ce profil local.",
    ],
    "it": [
        "Farmaci concomitanti · editor JSON",
        "Completezza dell’elenco",
        "Sconosciuta",
        "Elenco parziale",
        "Elenco completo (secondo te)",
        "Seleziona i farmaci attuali",
        "Seleziona o deseleziona i farmaci con i comandi di selezione multipla del dispositivo.",
        "Applica al JSON",
        "Il catalogo è limitato. Se manca un farmaco, lascia l’elenco parziale. La completezza dichiarata non è verificata in modo indipendente; questo non controlla tutte le interazioni. Le terapie precedenti sono registrate separatamente.",
        "Sono presenti campi dei farmaci non supportati. Correggili nel JSON; l’editor non li sovrascriverà.",
        "Controlla il JSON e i campi dei farmaci. I farmaci noti richiedono lo stato parziale o completo.",
        "Il JSON è cambiato. Chiudi e riapri l’editor prima di applicare.",
        "Elenco dei farmaci salvato in questo profilo locale.",
    ],
    "da": [
        "Samtidig medicin · JSON-editor",
        "Listens fuldstændighed",
        "Ukendt",
        "Delvis liste",
        "Komplet liste (ifølge dig)",
        "Vælg den aktuelle medicin",
        "Vælg eller fravælg medicin med enhedens kontroller til flervalg.",
        "Anvend i JSON",
        "Kataloget er begrænset. Mangler et lægemiddel, skal listen forblive delvis. Din angivelse af fuldstændighed er ikke uafhængigt kontrolleret; dette kontrollerer ikke alle interaktioner. Tidligere behandling registreres separat.",
        "Der er medicinfelter, som ikke understøttes. Ret dem i JSON; editoren overskriver dem ikke.",
        "Kontrollér JSON og medicinfelterne. Kendt medicin kræver status delvis eller komplet.",
        "JSON er ændret. Luk og genåbn editoren, før du anvender ændringer.",
        "Medicinlisten er gemt i denne lokale profil.",
    ],
    "sv": [
        "Samtidiga läkemedel · JSON-redigerare",
        "Listans fullständighet",
        "Okänd",
        "Delvis lista",
        "Fullständig lista (enligt dig)",
        "Välj aktuella läkemedel",
        "Markera eller avmarkera läkemedel med enhetens kontroller för flerval.",
        "Tillämpa i JSON",
        "Katalogen är begränsad. Om ett läkemedel saknas ska listan förbli delvis. Din uppgift om fullständighet har inte kontrollerats oberoende; detta kontrollerar inte alla interaktioner. Tidigare behandling registreras separat.",
        "Läkemedelsfält som inte stöds finns. Korrigera dem i JSON; redigeraren skriver inte över dem.",
        "Kontrollera JSON och läkemedelsfälten. Kända läkemedel kräver status delvis eller fullständig.",
        "JSON har ändrats. Stäng och öppna redigeraren igen innan du tillämpar ändringar.",
        "Läkemedelslistan har sparats i denna lokala profil.",
    ],
    "nb": [
        "Samtidige legemidler · JSON-editor",
        "Listens fullstendighet",
        "Ukjent",
        "Delvis liste",
        "Fullstendig liste (ifølge deg)",
        "Velg aktuelle legemidler",
        "Velg eller fjern legemidler med enhetens kontroller for flervalg.",
        "Bruk i JSON",
        "Katalogen er begrenset. Hvis et legemiddel mangler, må listen forbli delvis. Din angivelse av fullstendighet er ikke uavhengig kontrollert; dette sjekker ikke alle interaksjoner. Tidligere behandling registreres separat.",
        "Det finnes legemiddelfelt som ikke støttes. Rett dem i JSON; editoren overskriver dem ikke.",
        "Kontroller JSON og legemiddelfeltene. Kjente legemidler krever status delvis eller fullstendig.",
        "JSON er endret. Lukk og åpne editoren igjen før du bruker endringene.",
        "Legemiddellisten er lagret i denne lokale profilen.",
    ],
    "fi": [
        "Samanaikaiset lääkkeet · JSON-editori",
        "Luettelon kattavuus",
        "Tuntematon",
        "Osittainen luettelo",
        "Täydellinen luettelo (ilmoituksesi mukaan)",
        "Valitse nykyiset lääkkeet",
        "Valitse lääkkeitä tai poista valintoja laitteesi monivalintatoiminnoilla.",
        "Käytä JSONissa",
        "Luettelo on rajallinen. Jos lääke puuttuu, pidä luettelo osittaisena. Ilmoittamaasi kattavuutta ei ole tarkistettu riippumattomasti; tämä ei tarkista kaikkia yhteisvaikutuksia. Aiemmat hoidot kirjataan erikseen.",
        "Profiilissa on lääkekenttiä, joita ei tueta. Korjaa ne JSONissa; editori ei korvaa niitä.",
        "Tarkista JSON ja lääkekentät. Tunnetut lääkkeet vaativat osittaisen tai täydellisen tilan.",
        "JSON on muuttunut. Sulje editori ja avaa se uudelleen ennen muutosten käyttöä.",
        "Lääkeluettelo tallennettu tähän paikalliseen profiiliin.",
    ],
}
COPY = {locale: dict(zip(KEYS, row)) for locale, row in ROWS.items()}


FORM_KEYS = ["formTitle", "formApply", "formChanged", "formInvalid", "formLocked", "formSaved"]
FORM_ROWS = {
    "en": [
        "Concomitant medicines",
        "Save medication list",
        "The form changed. Close and reopen this section before saving.",
        "Check the form values and medication list. Known medicines require partial or complete status.",
        "Personalise this example, then reopen this section to edit its medication list.",
        "Medication list saved in the form.",
    ],
    "uk": [
        "Супутні ліки",
        "Зберегти перелік ліків",
        "Форма змінилася. Закрийте й знову відкрийте цей розділ перед збереженням.",
        "Перевірте значення форми й перелік ліків. Для відомих ліків виберіть частковий або повний перелік.",
        "Персоналізуйте цей приклад, потім знову відкрийте розділ для редагування його ліків.",
        "Перелік ліків збережено у формі.",
    ],
    "es": [
        "Medicamentos concomitantes",
        "Guardar lista de medicamentos",
        "El formulario ha cambiado. Cierre y vuelva a abrir esta sección antes de guardar.",
        "Revise los valores del formulario y la lista de medicamentos. Los medicamentos conocidos requieren el estado parcial o completo.",
        "Personalice este ejemplo y vuelva a abrir esta sección para editar sus medicamentos.",
        "Lista de medicamentos guardada en el formulario.",
    ],
    "pt": [
        "Medicamentos concomitantes",
        "Guardar lista de medicamentos",
        "O formulário foi alterado. Feche e reabra esta secção antes de guardar.",
        "Verifique os valores do formulário e a lista de medicamentos. Medicamentos conhecidos exigem o estado parcial ou completo.",
        "Personalize este exemplo e reabra esta secção para editar os seus medicamentos.",
        "Lista de medicamentos guardada no formulário.",
    ],
    "de": [
        "Begleitmedikation",
        "Medikamentenliste speichern",
        "Das Formular wurde geändert. Schließen und öffnen Sie diesen Abschnitt vor dem Speichern erneut.",
        "Prüfen Sie Formularwerte und Medikamentenliste. Bekannte Medikamente erfordern den Status unvollständig oder vollständig.",
        "Passen Sie dieses Beispiel an und öffnen Sie diesen Abschnitt erneut, um seine Medikamente zu bearbeiten.",
        "Medikamentenliste im Formular gespeichert.",
    ],
    "fr": [
        "Médicaments concomitants",
        "Enregistrer la liste des médicaments",
        "Le formulaire a changé. Fermez puis rouvrez cette section avant d’enregistrer.",
        "Vérifiez les valeurs du formulaire et la liste des médicaments. Des médicaments connus exigent le statut partiel ou complet.",
        "Personnalisez cet exemple, puis rouvrez cette section pour modifier ses médicaments.",
        "Liste des médicaments enregistrée dans le formulaire.",
    ],
    "it": [
        "Farmaci concomitanti",
        "Salva elenco dei farmaci",
        "Il modulo è cambiato. Chiudi e riapri questa sezione prima di salvare.",
        "Controlla i valori del modulo e l’elenco dei farmaci. I farmaci noti richiedono lo stato parziale o completo.",
        "Personalizza questo esempio, poi riapri questa sezione per modificarne i farmaci.",
        "Elenco dei farmaci salvato nel modulo.",
    ],
    "da": [
        "Samtidig medicin",
        "Gem medicinlisten",
        "Formularen er ændret. Luk og genåbn dette afsnit, før du gemmer.",
        "Kontrollér formularværdierne og medicinlisten. Kendt medicin kræver status delvis eller komplet.",
        "Tilpas dette eksempel, og genåbn afsnittet for at redigere dets medicin.",
        "Medicinlisten er gemt i formularen.",
    ],
    "sv": [
        "Samtidiga läkemedel",
        "Spara läkemedelslistan",
        "Formuläret har ändrats. Stäng och öppna avsnittet igen innan du sparar.",
        "Kontrollera formulärvärdena och läkemedelslistan. Kända läkemedel kräver status delvis eller fullständig.",
        "Anpassa det här exemplet och öppna avsnittet igen för att redigera dess läkemedel.",
        "Läkemedelslistan har sparats i formuläret.",
    ],
    "nb": [
        "Samtidige legemidler",
        "Lagre legemiddellisten",
        "Skjemaet er endret. Lukk og åpne avsnittet igjen før du lagrer.",
        "Kontroller skjemaverdiene og legemiddellisten. Kjente legemidler krever status delvis eller fullstendig.",
        "Tilpass dette eksemplet, og åpne avsnittet igjen for å redigere legemidlene.",
        "Legemiddellisten er lagret i skjemaet.",
    ],
    "fi": [
        "Samanaikaiset lääkkeet",
        "Tallenna lääkeluettelo",
        "Lomake on muuttunut. Sulje tämä osio ja avaa se uudelleen ennen tallennusta.",
        "Tarkista lomakkeen arvot ja lääkeluettelo. Tunnetut lääkkeet vaativat osittaisen tai täydellisen tilan.",
        "Mukauta tätä esimerkkiä ja avaa osio uudelleen muokataksesi sen lääkkeitä.",
        "Lääkeluettelo tallennettu lomakkeeseen.",
    ],
}
for locale, row in FORM_ROWS.items():
    COPY[locale].update(zip(FORM_KEYS, row))


def render_medication_editor(locale):
    root = Path(__file__).resolve().parents[1]
    drugs = []
    for path in sorted((root / "knowledge_base/hosted/content/drugs").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        names = data["names"]
        name = names.get("ukrainian") if locale == "uk" else names.get("english")
        drugs.append({"id": data["id"], "name": name or names["preferred"]})
    assert drugs and len({drug["id"] for drug in drugs}) == len(drugs)
    config = {"copy": COPY[locale], "drugs": sorted(drugs, key=lambda drug: drug["id"])}
    # Escape HTML parser delimiters even though catalog/copy are repository-owned.
    encoded = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
    return (
        "const medicationEditorConfig = "
        + encoded
        + ";\n"
        + (root / "scripts/medication_editor.js").read_text(encoding="utf-8")
    )


def localized_editor_config(encoded, locale):
    """Localize UI copy without changing source catalog IDs, names or order."""
    config = json.loads(encoded)
    config["copy"] = COPY[locale]
    return json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
