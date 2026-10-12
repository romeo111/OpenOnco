"""Explicit tool-specific data-flow copy, without provider-retention guarantees."""
HOME = {
    'en': 'Plan Builder evaluates clinical rules in your browser. Tumor Board sends submitted text to a server and may use a configured model provider. Use synthetic cases without identifying details; individual care decisions require a qualified clinician.',
    'uk': 'Конструктор плану оцінює клінічні правила у браузері. Туморборд надсилає введений текст серверу й може використовувати налаштованого постачальника моделі. Використовуйте синтетичні випадки без ідентифікаційних даних; індивідуальні рішення щодо лікування потребують кваліфікованого лікаря.',
    'es': 'Plan Builder evalúa las reglas clínicas en su navegador. Tumor Board envía el texto introducido a un servidor y puede usar un proveedor de modelos configurado. Use casos sintéticos sin datos identificativos; las decisiones de atención individual requieren un profesional clínico cualificado.',
    'pt': 'Plan Builder avalia as regras clínicas no seu navegador. Tumor Board envia o texto introduzido para um servidor e pode utilizar um fornecedor de modelos configurado. Utilize casos sintéticos sem dados identificativos; as decisões de cuidados individuais exigem um profissional clínico qualificado.',
    'de': 'Plan Builder wertet klinische Regeln in Ihrem Browser aus. Tumor Board sendet eingegebenen Text an einen Server und kann einen konfigurierten Modellanbieter nutzen. Verwenden Sie synthetische Fälle ohne identifizierende Angaben; individuelle Behandlungsentscheidungen erfordern qualifiziertes medizinisches Fachpersonal.',
    'fr': 'Plan Builder évalue les règles cliniques dans votre navigateur. Tumor Board envoie le texte saisi à un serveur et peut utiliser un fournisseur de modèles configuré. Utilisez des cas synthétiques sans données identifiantes ; les décisions de soins individuelles nécessitent un professionnel clinique qualifié.',
    'it': 'Plan Builder valuta le regole cliniche nel browser. Tumor Board invia il testo inserito a un server e può usare un fornitore di modelli configurato. Usa casi sintetici senza dati identificativi; le decisioni di cura individuali richiedono un professionista clinico qualificato.',
    'da': 'Plan Builder vurderer kliniske regler i din browser. Tumor Board sender den indtastede tekst til en server og kan bruge en konfigureret modeludbyder. Brug syntetiske tilfælde uden identificerende oplysninger; individuelle behandlingsbeslutninger kræver en kvalificeret kliniker.',
    'sv': 'Plan Builder utvärderar kliniska regler i webbläsaren. Tumor Board skickar den inmatade texten till en server och kan använda en konfigurerad modellleverantör. Använd syntetiska fall utan identifierande uppgifter; individuella vårdbeslut kräver kvalificerad vårdpersonal.',
    'nb': 'Plan Builder vurderer kliniske regler i nettleseren. Tumor Board sender teksten til en server og kan bruke en konfigurert modellleverandør. Bruk syntetiske tilfeller uten identifiserende opplysninger; individuelle behandlingsbeslutninger krever kvalifisert helsepersonell.',
    'fi': 'Plan Builder arvioi kliiniset säännöt selaimessasi. Tumor Board lähettää syötetyn tekstin palvelimelle ja voi käyttää määritettyä mallipalveluntarjoajaa. Käytä synteettisiä tapauksia ilman tunnistetietoja; yksilölliset hoitopäätökset edellyttävät pätevää terveydenhuollon ammattilaista.',
}
LOCAL_TITLE = dict(zip(HOME, ('Local rule evaluation','Локальна оцінка правил','Evaluación local de reglas','Avaliação local das regras','Lokale Regelauswertung','Évaluation locale des règles','Valutazione locale delle regole','Lokal regelvurdering','Lokal regelutvärdering','Lokal regelvurdering','Paikallinen sääntöjen arviointi')))
LOCAL_BODY = {
    'en': 'Plan Builder downloads public engine and knowledge-base assets and evaluates clinical rules in your browser.',
    'uk': 'Конструктор плану завантажує публічні ресурси рушія та бази знань і оцінює клінічні правила у браузері.',
    'es': 'Plan Builder descarga recursos públicos del motor y de la base de conocimientos y evalúa las reglas clínicas en su navegador.',
    'pt': 'Plan Builder descarrega recursos públicos do motor e da base de conhecimentos e avalia as regras clínicas no navegador.',
    'de': 'Plan Builder lädt öffentliche Engine- und Wissensdaten und wertet klinische Regeln in Ihrem Browser aus.',
    'fr': 'Plan Builder télécharge les ressources publiques du moteur et de la base de connaissances et évalue les règles cliniques dans votre navigateur.',
    'it': 'Plan Builder scarica le risorse pubbliche del motore e della base di conoscenze e valuta le regole cliniche nel browser.',
    'da': 'Plan Builder henter offentlige motor- og vidensbaseressourcer og vurderer kliniske regler i din browser.',
    'sv': 'Plan Builder hämtar offentliga motor- och kunskapsbasresurser och utvärderar kliniska regler i webbläsaren.',
    'nb': 'Plan Builder laster ned offentlige motor- og kunnskapsbaseressurser og vurderer kliniske regler i nettleseren.',
    'fi': 'Plan Builder lataa julkiset moottorin ja tietopohjan resurssit ja arvioi kliiniset säännöt selaimessasi.',
}
TRANSFER_TITLE = dict(zip(HOME, ('Server and provider processing','Обробка сервером і постачальником','Procesamiento por el servidor y el proveedor','Processamento pelo servidor e fornecedor','Server- und Anbieter-Verarbeitung','Traitement par le serveur et le fournisseur','Elaborazione da parte del server e del fornitore','Behandling hos server og udbyder','Behandling hos server och leverantör','Behandling hos server og leverandør','Palvelimen ja palveluntarjoajan käsittely')))
TRANSFER_BODY = {
    'en': 'Tumor Board sends submitted text to the configured API server and may use a model provider. Check hosting and provider policies; do not submit identifying patient information.',
    'uk': 'Туморборд надсилає введений текст налаштованому API-серверу й може використовувати постачальника моделі. Перевірте політики хостингу та постачальника; не надсилайте дані, що ідентифікують пацієнта.',
    'es': 'Tumor Board envía el texto introducido al servidor API configurado y puede usar un proveedor de modelos. Consulte las políticas del alojamiento y del proveedor; no envíe datos que identifiquen a pacientes.',
    'pt': 'Tumor Board envia o texto introduzido para o servidor API configurado e pode usar um fornecedor de modelos. Consulte as políticas do alojamento e do fornecedor; não envie dados que identifiquem pacientes.',
    'de': 'Tumor Board sendet eingegebenen Text an den konfigurierten API-Server und kann einen Modellanbieter nutzen. Prüfen Sie die Richtlinien von Hosting und Anbieter; übermitteln Sie keine identifizierenden Patientendaten.',
    'fr': 'Tumor Board envoie le texte saisi au serveur API configuré et peut utiliser un fournisseur de modèles. Consultez les politiques de l’hébergement et du fournisseur ; n’envoyez pas de données permettant d’identifier un patient.',
    'it': 'Tumor Board invia il testo inserito al server API configurato e può usare un fornitore di modelli. Controlla le politiche di hosting e del fornitore; non inviare dati che identificano i pazienti.',
    'da': 'Tumor Board sender den indtastede tekst til den konfigurerede API-server og kan bruge en modeludbyder. Kontrollér hosting- og udbyderpolitikkerne; send ikke oplysninger, der identificerer patienter.',
    'sv': 'Tumor Board skickar texten till den konfigurerade API-servern och kan använda en modellleverantör. Kontrollera värd- och leverantörspolicyerna; skicka inte uppgifter som identifierar patienter.',
    'nb': 'Tumor Board sender teksten til den konfigurerte API-serveren og kan bruke en modellleverandør. Kontroller hosting- og leverandørpolicyene; ikke send opplysninger som identifiserer pasienter.',
    'fi': 'Tumor Board lähettää tekstin määritetylle API-palvelimelle ja voi käyttää mallipalveluntarjoajaa. Tarkista hosting- ja palveluntarjoajakäytännöt; älä lähetä potilaita yksilöiviä tietoja.',
}


def messages_for(locale):
    return {table['en']:table[locale] for table in (HOME,LOCAL_TITLE,LOCAL_BODY,TRANSFER_TITLE,TRANSFER_BODY)}
