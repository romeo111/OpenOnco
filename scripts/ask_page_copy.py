"""Curated, interface-only copy for the oncology question page."""

LANGUAGES = ('es', 'pt', 'de', 'fr', 'it', 'da', 'sv', 'nb', 'fi')

COPY = {
    'OpenOnco · AI-assisted draft': (
        'OpenOnco · borrador asistido por IA',
        'OpenOnco · rascunho assistido por IA',
        'OpenOnco · KI-gestützter Entwurf',
        'OpenOnco · brouillon assisté par IA',
        'OpenOnco · bozza assistita dall’IA',
        'OpenOnco · AI-assisteret udkast',
        'OpenOnco · AI-stött utkast',
        'OpenOnco · KI-støttet utkast',
        'OpenOnco · tekoälyn avustama luonnos',
    ),
    'Ask an oncology question': (
        'Haga una pregunta sobre oncología',
        'Faça uma pergunta sobre oncologia',
        'Stellen Sie eine Frage zur Onkologie',
        'Posez une question en oncologie',
        'Fai una domanda sull’oncologia',
        'Stil et spørgsmål om kræftbehandling',
        'Ställ en fråga om cancervård',
        'Still et spørsmål om kreftbehandling',
        'Esitä syövän hoitoa koskeva kysymys',
    ),
    'Describe a de-identified case or ask about a treatment plan. A model structures the question; OpenOnco checks available rule-based evidence and flags details that still need clinical review.': (
        'Describa un caso sin datos identificativos o pregunte por un plan de tratamiento. Un modelo estructura la pregunta; OpenOnco contrasta la evidencia disponible con sus reglas y señala los detalles que aún requieren revisión clínica.',
        'Descreva um caso sem dados identificativos ou pergunte sobre um plano de tratamento. Um modelo estrutura a pergunta; o OpenOnco verifica a evidência disponível com base em regras e assinala os detalhes que ainda exigem avaliação clínica.',
        'Beschreiben Sie einen Fall ohne identifizierende Angaben oder stellen Sie eine Frage zu einem Behandlungsplan. Ein Modell strukturiert die Frage; OpenOnco prüft die verfügbaren regelbasierten Belege und kennzeichnet Angaben, die noch klinisch geprüft werden müssen.',
        'Décrivez un cas sans données identifiantes ou posez une question sur un plan de traitement. Un modèle structure la question ; OpenOnco vérifie les données disponibles selon ses règles et signale les éléments qui nécessitent encore un examen clinique.',
        'Descrivi un caso senza dati identificativi o poni una domanda su un piano terapeutico. Un modello struttura la domanda; OpenOnco verifica le evidenze disponibili secondo le sue regole e segnala i dettagli che richiedono ancora una valutazione clinica.',
        'Beskriv et tilfælde uden identificerende oplysninger, eller stil et spørgsmål om en behandlingsplan. En model strukturerer spørgsmålet; OpenOnco kontrollerer det tilgængelige regelbaserede grundlag og markerer oplysninger, der stadig kræver klinisk vurdering.',
        'Beskriv ett fall utan identifierande uppgifter eller fråga om en behandlingsplan. En modell strukturerar frågan; OpenOnco kontrollerar tillgängligt regelbaserat underlag och markerar uppgifter som fortfarande kräver klinisk bedömning.',
        'Beskriv et tilfelle uten identifiserende opplysninger, eller spør om en behandlingsplan. En modell strukturerer spørsmålet; OpenOnco kontrollerer tilgjengelig regelbasert grunnlag og markerer opplysninger som fortsatt krever klinisk vurdering.',
        'Kuvaa tapaus ilman tunnistetietoja tai kysy hoitosuunnitelmasta. Malli jäsentää kysymyksen; OpenOnco tarkistaa saatavilla olevan sääntöihin perustuvan näytön ja merkitsee tiedot, jotka vaativat vielä kliinistä arviointia.',
    ),
    'For clinicians': ('Para profesionales clínicos', 'Para profissionais de saúde', 'Für Behandelnde', 'Pour les professionnels de santé', 'Per i clinici', 'Til klinikere', 'För vårdpersonal', 'For klinikere', 'Ammattilaisille'),
    'Prepare a de-identified case for multidisciplinary discussion.': (
        'Prepare un caso sin datos identificativos para la discusión multidisciplinaria.',
        'Prepare um caso sem dados identificativos para discussão multidisciplinar.',
        'Bereiten Sie einen Fall ohne identifizierende Angaben für die interdisziplinäre Besprechung vor.',
        'Préparez un cas sans données identifiantes pour une discussion pluridisciplinaire.',
        'Prepara un caso senza dati identificativi per la discussione multidisciplinare.',
        'Forbered et tilfælde uden identificerende oplysninger til tværfaglig drøftelse.',
        'Förbered ett fall utan identifierande uppgifter för multidisciplinär diskussion.',
        'Forbered et tilfelle uten identifiserende opplysninger til tverrfaglig diskusjon.',
        'Valmistele tapaus ilman tunnistetietoja moniammatillista keskustelua varten.',
    ),
    'For patients': ('Para pacientes', 'Para pacientes', 'Für Patientinnen und Patienten', 'Pour les patients', 'Per i pazienti', 'Til patienter', 'För patienter', 'For pasienter', 'Potilaille'),
    "Understand your oncologist's plan in plain language and prepare questions for your next visit. This draft cannot decide whether the plan is right for you.": (
        'Comprenda el plan de su oncólogo en un lenguaje sencillo y prepare preguntas para la próxima consulta. Este borrador no puede determinar si el plan es adecuado para usted.',
        'Compreenda o plano do seu oncologista em linguagem simples e prepare perguntas para a próxima consulta. Este rascunho não pode determinar se o plano é adequado para si.',
        'Verstehen Sie den Plan Ihrer Onkologin oder Ihres Onkologen in einfachen Worten und bereiten Sie Fragen für den nächsten Termin vor. Dieser Entwurf kann nicht beurteilen, ob der Plan für Sie geeignet ist.',
        'Comprenez le plan de votre oncologue en termes simples et préparez vos questions pour le prochain rendez-vous. Ce brouillon ne peut pas déterminer si ce plan vous convient.',
        'Comprendi il piano del tuo oncologo in parole semplici e prepara le domande per la prossima visita. Questa bozza non può stabilire se il piano sia adatto a te.',
        'Forstå din onkologs plan i et enkelt sprog, og forbered spørgsmål til næste besøg. Dette udkast kan ikke afgøre, om planen er den rette for dig.',
        'Förstå din onkologs plan på ett enkelt sätt och förbered frågor inför nästa besök. Utkastet kan inte avgöra om planen är rätt för dig.',
        'Forstå planen fra onkologen din med enkle ord, og forbered spørsmål til neste time. Utkastet kan ikke avgjøre om planen er riktig for deg.',
        'Ymmärrä onkologisi suunnitelma selkokielellä ja valmistele kysymyksiä seuraavaa vastaanottoa varten. Luonnos ei voi ratkaista, sopiiko suunnitelma sinulle.',
    ),
    'Before you submit': ('Antes de enviar', 'Antes de enviar', 'Vor dem Absenden', 'Avant d’envoyer', 'Prima di inviare', 'Før du sender', 'Innan du skickar', 'Før du sender', 'Ennen lähettämistä'),
    'Care decisions stay with your clinician': (
        'Las decisiones sobre su atención corresponden a su médico',
        'As decisões sobre os seus cuidados cabem ao seu médico',
        'Behandlungsentscheidungen trifft Ihre Ärztin oder Ihr Arzt',
        'Les décisions de soins reviennent à votre médecin',
        'Le decisioni sulle cure spettano al medico curante',
        'Beslutninger om behandling træffes sammen med din læge',
        'Beslut om vård fattas tillsammans med din läkare',
        'Beslutninger om behandling tas sammen med legen din',
        'Hoitopäätökset tehdään hoitavan lääkärin kanssa',
    ),
    'Describe your question': ('Describa su pregunta', 'Descreva a sua pergunta', 'Beschreiben Sie Ihre Frage', 'Décrivez votre question', 'Descrivi la tua domanda', 'Beskriv dit spørgsmål', 'Beskriv din fråga', 'Beskriv spørsmålet ditt', 'Kuvaa kysymyksesi'),
    'Discussion draft': ('Borrador para la discusión', 'Rascunho para discussão', 'Entwurf für die Besprechung', 'Brouillon pour discussion', 'Bozza per la discussione', 'Udkast til drøftelse', 'Utkast för diskussion', 'Utkast til diskusjon', 'Keskusteluluonnos'),
    'Your draft will appear here after you submit a question.': (
        'Su borrador aparecerá aquí después de enviar la pregunta.',
        'O seu rascunho aparecerá aqui depois de enviar a pergunta.',
        'Ihr Entwurf erscheint hier, nachdem Sie eine Frage abgesendet haben.',
        'Votre brouillon apparaîtra ici après l’envoi de votre question.',
        'La bozza apparirà qui dopo l’invio della domanda.',
        'Dit udkast vises her, når du har sendt et spørgsmål.',
        'Ditt utkast visas här när du har skickat en fråga.',
        'Utkastet vises her etter at du har sendt et spørsmål.',
        'Luonnos näkyy tässä, kun olet lähettänyt kysymyksen.',
    ),
    'Advanced · API connection': ('Avanzado · conexión API', 'Avançado · ligação à API', 'Erweitert · API-Verbindung', 'Avancé · connexion API', 'Avanzate · connessione API', 'Avanceret · API-forbindelse', 'Avancerat · API-anslutning', 'Avansert · API-tilkobling', 'Lisäasetukset · API-yhteys'),
}


def messages_for(locale):
    index = LANGUAGES.index(locale)
    messages = {source: values[index] for source, values in COPY.items()}
    messages['OpenOnco · Ask an oncology question'] = 'OpenOnco · ' + messages['Ask an oncology question']
    return messages
