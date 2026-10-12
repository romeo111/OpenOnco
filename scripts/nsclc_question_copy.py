"""Display-only questionnaire drafts; never translate profile keys or values."""
LANGUAGES = ('uk', 'es', 'pt', 'de', 'fr', 'it', 'da', 'sv', 'nb', 'fi')
SOURCE = (
    'Confirmed NSCLC histology', 'Confirmed NSCLC stage',
    'Molecular assessment confirms no actionable driver',
    'Squamous NSCLC: selected taxane for clinician review',
    'Adenocarcinoma', 'Other confirmed non-squamous histology',
    'Squamous cell carcinoma', 'Unknown / pending pathology',
    'Stage IV / metastatic', 'Stage III', 'Unknown / pending staging',
    'Confirmed driver-negative', 'Not confirmed / actionable driver / results pending',
    'Not selected',
    'Use the pathology report. Do not infer histology from PD-L1 or a drug preference.',
    'Do not infer metastatic stage from drug preference.',
    'Missing molecular results do not establish driver-negative disease.',
    'Choose one taxane only. Relevant to the pembrolizumab/carboplatin squamous route; no default choice.',
)
COPY = {
 'uk': (
  'Підтверджена гістологія НМРЛ', 'Підтверджена стадія НМРЛ', 'Молекулярне дослідження підтверджує відсутність драйверних змін, на які можна спрямувати лікування', 'Плоскоклітинний НМРЛ: обраний таксан для перевірки лікарем',
  'Аденокарцинома', 'Інша підтверджена неплоскоклітинна гістологія', 'Плоскоклітинна карцинома', 'Невідомо / очікується висновок патології', 'Стадія IV / метастатична', 'Стадія III', 'Невідомо / стадію ще визначають', 'Відсутність драйверних змін підтверджена', 'Не підтверджено / є драйверна зміна / очікуються результати', 'Не обрано',
  'Використовуйте висновок патології. Не визначайте гістологію за PD-L1 або бажаним препаратом.', 'Не визначайте метастатичну стадію за бажаним препаратом.', 'Відсутність результатів молекулярного дослідження не підтверджує відсутності драйверних змін.', 'Оберіть лише один таксан. Це поле стосується плоскоклітинного маршруту пембролізумаб/карбоплатин; вибору за замовчуванням немає.',
 ),
 'es': (
  'Histología confirmada del NSCLC', 'Estadio confirmado del NSCLC', 'El estudio molecular confirma que no hay alteraciones conductoras tratables', 'NSCLC escamoso: taxano elegido para revisión médica',
  'Adenocarcinoma', 'Otra histología no escamosa confirmada', 'Carcinoma de células escamosas', 'Desconocida / pendiente de anatomía patológica', 'Estadio IV / metastásico', 'Estadio III', 'Desconocido / estadificación pendiente', 'Ausencia de alteraciones conductoras confirmada', 'No confirmado / alteración conductora tratable / resultados pendientes', 'Sin seleccionar',
  'Utilice el informe de anatomía patológica. No deduzca la histología a partir de PD-L1 ni del medicamento preferido.', 'No deduzca el estadio metastásico a partir del medicamento preferido.', 'La falta de resultados moleculares no confirma la ausencia de alteraciones conductoras.', 'Elija un solo taxano. Este campo corresponde a la ruta escamosa con pembrolizumab/carboplatino; no hay selección predeterminada.',
 ),
 'pt': (
  'Histologia confirmada do NSCLC', 'Estádio confirmado do NSCLC', 'O estudo molecular confirma a ausência de alterações driver com tratamento dirigido', 'NSCLC escamoso: taxano escolhido para revisão médica',
  'Adenocarcinoma', 'Outra histologia não escamosa confirmada', 'Carcinoma de células escamosas', 'Desconhecida / anatomia patológica pendente', 'Estádio IV / metastático', 'Estádio III', 'Desconhecido / estadiamento pendente', 'Ausência de alterações driver confirmada', 'Não confirmado / alteração driver com tratamento dirigido / resultados pendentes', 'Não selecionado',
  'Use o relatório de anatomia patológica. Não deduza a histologia a partir de PD-L1 ou do medicamento preferido.', 'Não deduza o estádio metastático a partir do medicamento preferido.', 'A ausência de resultados moleculares não confirma a ausência de alterações driver.', 'Escolha apenas um taxano. Este campo aplica-se à via escamosa com pembrolizumab/carboplatina; não há escolha predefinida.',
 ),
 'de': (
  'Bestätigte NSCLC-Histologie', 'Bestätigtes NSCLC-Stadium', 'Die molekulare Untersuchung bestätigt das Fehlen therapeutisch adressierbarer Treiberveränderungen', 'Plattenepithel-NSCLC: gewähltes Taxan zur ärztlichen Prüfung',
  'Adenokarzinom', 'Andere bestätigte nicht-plattenepitheliale Histologie', 'Plattenepithelkarzinom', 'Unbekannt / Pathologiebefund ausstehend', 'Stadium IV / metastasiert', 'Stadium III', 'Unbekannt / Stadienbestimmung ausstehend', 'Fehlen von Treiberveränderungen bestätigt', 'Nicht bestätigt / adressierbare Treiberveränderung / Ergebnisse ausstehend', 'Nicht gewählt',
  'Verwenden Sie den Pathologiebefund. Leiten Sie die Histologie nicht aus PD-L1 oder dem bevorzugten Medikament ab.', 'Leiten Sie das metastasierte Stadium nicht aus dem bevorzugten Medikament ab.', 'Fehlende molekulare Ergebnisse bestätigen nicht das Fehlen von Treiberveränderungen.', 'Wählen Sie nur ein Taxan. Dieses Feld gilt für den Plattenepithel-Pfad mit Pembrolizumab/Carboplatin; es gibt keine Vorauswahl.',
 ),
 'fr': (
  'Histologie du NSCLC confirmée', 'Stade du NSCLC confirmé', 'Le bilan moléculaire confirme l’absence d’altération oncogénique ciblable', 'NSCLC épidermoïde : taxane choisi pour vérification médicale',
  'Adénocarcinome', 'Autre histologie non épidermoïde confirmée', 'Carcinome épidermoïde', 'Inconnue / résultat anatomopathologique en attente', 'Stade IV / métastatique', 'Stade III', 'Inconnu / stadification en attente', 'Absence d’altération oncogénique ciblable confirmée', 'Non confirmé / altération oncogénique ciblable / résultats en attente', 'Non sélectionné',
  'Utilisez le compte rendu anatomopathologique. Ne déduisez pas l’histologie de PD-L1 ou du médicament préféré.', 'Ne déduisez pas le stade métastatique du médicament préféré.', 'L’absence de résultats moléculaires ne confirme pas l’absence d’altération oncogénique.', 'Choisissez un seul taxane. Ce champ concerne la voie épidermoïde avec pembrolizumab/carboplatine ; aucun choix par défaut.',
 ),
 'it': (
  'Istologia del NSCLC confermata', 'Stadio del NSCLC confermato', 'L’esame molecolare conferma l’assenza di alterazioni driver trattabili', 'NSCLC squamoso: taxano scelto per verifica medica',
  'Adenocarcinoma', 'Altra istologia non squamosa confermata', 'Carcinoma a cellule squamose', 'Sconosciuta / referto patologico in attesa', 'Stadio IV / metastatico', 'Stadio III', 'Sconosciuto / stadiazione in attesa', 'Assenza di alterazioni driver confermata', 'Non confermato / alterazione driver trattabile / risultati in attesa', 'Non selezionato',
  'Usare il referto patologico. Non dedurre l’istologia da PD-L1 o dal farmaco preferito.', 'Non dedurre lo stadio metastatico dal farmaco preferito.', 'La mancanza di risultati molecolari non conferma l’assenza di alterazioni driver.', 'Scegliere un solo taxano. Il campo riguarda il percorso squamoso con pembrolizumab/carboplatino; non esiste una scelta predefinita.',
 ),
 'da': (
  'Bekræftet NSCLC-histologi', 'Bekræftet NSCLC-stadium', 'Molekylær undersøgelse bekræfter fravær af behandlingsrelevante driverforandringer', 'Planocellulær NSCLC: valgt taxan til lægelig vurdering',
  'Adenokarcinom', 'Anden bekræftet ikke-planocellulær histologi', 'Planocellulært karcinom', 'Ukendt / patologisvar afventes', 'Stadium IV / metastatisk', 'Stadium III', 'Ukendt / stadieinddeling afventes', 'Fravær af driverforandringer bekræftet', 'Ikke bekræftet / behandlingsrelevant driverforandring / resultater afventes', 'Ikke valgt',
  'Brug patologisvaret. Udled ikke histologi fra PD-L1 eller det foretrukne lægemiddel.', 'Udled ikke metastatisk stadium fra det foretrukne lægemiddel.', 'Manglende molekylære resultater bekræfter ikke fravær af driverforandringer.', 'Vælg kun ét taxan. Feltet gælder den planocellulære behandlingsvej med pembrolizumab/carboplatin; intet valg er forudindstillet.',
 ),
 'sv': (
  'Bekräftad NSCLC-histologi', 'Bekräftat NSCLC-stadium', 'Molekylär undersökning bekräftar frånvaro av behandlingsbara driverförändringar', 'Skivepitel-NSCLC: valt taxan för läkarbedömning',
  'Adenokarcinom', 'Annan bekräftad icke-skivepitelhistologi', 'Skivepitelkarcinom', 'Okänd / patologisvar inväntas', 'Stadium IV / metastaserad', 'Stadium III', 'Okänt / stadieindelning inväntas', 'Frånvaro av driverförändringar bekräftad', 'Inte bekräftat / behandlingsbar driverförändring / resultat inväntas', 'Inte valt',
  'Använd patologisvaret. Härled inte histologi från PD-L1 eller det föredragna läkemedlet.', 'Härled inte metastaserat stadium från det föredragna läkemedlet.', 'Saknade molekylära resultat bekräftar inte frånvaro av driverförändringar.', 'Välj endast ett taxan. Fältet gäller skivepitelvägen med pembrolizumab/karboplatin; inget val är förinställt.',
 ),
 'nb': (
  'Bekreftet NSCLC-histologi', 'Bekreftet NSCLC-stadium', 'Molekylær undersøkelse bekrefter fravær av behandlingsrelevante driverforandringer', 'Plateepitel-NSCLC: valgt taksan til legevurdering',
  'Adenokarsinom', 'Annen bekreftet ikke-plateepitelhistologi', 'Plateepitelkarsinom', 'Ukjent / patologisvar avventes', 'Stadium IV / metastatisk', 'Stadium III', 'Ukjent / stadieinndeling avventes', 'Fravær av driverforandringer bekreftet', 'Ikke bekreftet / behandlingsrelevant driverforandring / resultater avventes', 'Ikke valgt',
  'Bruk patologisvaret. Ikke utled histologi fra PD-L1 eller det foretrukne legemidlet.', 'Ikke utled metastatisk stadium fra det foretrukne legemidlet.', 'Manglende molekylære resultater bekrefter ikke fravær av driverforandringer.', 'Velg bare ett taksan. Feltet gjelder plateepitelveien med pembrolizumab/karboplatin; ingen valg er forhåndsvalgt.',
 ),
 'fi': (
  'Varmistettu NSCLC:n histologia', 'Varmistettu NSCLC:n levinneisyysaste', 'Molekyylitutkimus vahvistaa, ettei kohdennettavissa olevia driver-muutoksia ole', 'Levyepiteelinen NSCLC: valittu taksaani lääkärin arvioitavaksi',
  'Adenokarsinooma', 'Muu varmistettu ei-levyepiteelinen histologia', 'Levyepiteelikarsinooma', 'Tuntematon / patologian vastausta odotetaan', 'Levinneisyysaste IV / metastasoitunut', 'Levinneisyysaste III', 'Tuntematon / levinneisyysselvitys kesken', 'Driver-muutosten puuttuminen varmistettu', 'Ei varmistettu / kohdennettava driver-muutos / tuloksia odotetaan', 'Ei valittu',
  'Käytä patologian lausuntoa. Älä päättele histologiaa PD-L1:n tai toivotun lääkkeen perusteella.', 'Älä päättele metastasoitunutta tautia toivotun lääkkeen perusteella.', 'Puuttuvat molekyylitulokset eivät vahvista driver-muutosten puuttumista.', 'Valitse vain yksi taksaani. Kenttä koskee levyepiteelisen taudin pembrolitsumabi/karboplatiini-hoitopolkua; oletusvalintaa ei ole.',
 ),
}


def messages_for(locale):
    if locale == 'en':
        return {}
    values = COPY[locale]
    if len(values) != len(SOURCE):
        raise ValueError('Incomplete NSCLC questionnaire display copy')
    return dict(zip(SOURCE, values))
