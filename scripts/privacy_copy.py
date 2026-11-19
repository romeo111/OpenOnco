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


_LOCAL_STORAGE = dict(zip(HOME, (
    ' Drafts persist in this browser until you clear the form or site data. Downloaded exports remain on your device. Loading the site and its public assets still makes network requests. Use synthetic cases.',
    ' Чернетки зберігаються в цьому браузері до очищення форми або даних сайту. Завантажені експорти залишаються на пристрої. Завантаження сайту й публічних ресурсів усе одно потребує мережевих запитів. Використовуйте синтетичні випадки.',
    ' Los borradores permanecen en este navegador hasta borrar el formulario o los datos del sitio. Los archivos exportados permanecen en el dispositivo. Cargar el sitio y sus recursos públicos requiere solicitudes de red. Use casos sintéticos.',
    ' Os rascunhos ficam neste navegador até limpar o formulário ou os dados do site. Os ficheiros exportados permanecem no dispositivo. Carregar o site e os recursos públicos requer pedidos de rede. Utilize casos sintéticos.',
    ' Entwürfe bleiben in diesem Browser, bis Sie das Formular oder die Websitedaten löschen. Exportierte Dateien bleiben auf Ihrem Gerät. Das Laden der Website und öffentlicher Ressourcen erfordert Netzwerkzugriffe. Verwenden Sie synthetische Fälle.',
    ' Les brouillons restent dans ce navigateur jusqu’à l’effacement du formulaire ou des données du site. Les fichiers exportés restent sur votre appareil. Le chargement du site et des ressources publiques nécessite des requêtes réseau. Utilisez des cas synthétiques.',
    ' Le bozze restano in questo browser finché non cancelli il modulo o i dati del sito. I file esportati restano sul dispositivo. Il caricamento del sito e delle risorse pubbliche richiede richieste di rete. Usa casi sintetici.',
    ' Udkast gemmes i denne browser, indtil du rydder formularen eller webstedets data. Eksporterede filer bliver på enheden. Indlæsning af webstedet og offentlige ressourcer kræver netværksanmodninger. Brug syntetiske tilfælde.',
    ' Utkast sparas i denna webbläsare tills du rensar formuläret eller webbplatsdata. Exporterade filer finns kvar på enheten. Laddning av webbplatsen och offentliga resurser kräver nätverksanrop. Använd syntetiska fall.',
    ' Utkast lagres i denne nettleseren til du tømmer skjemaet eller nettstedsdata. Eksporterte filer blir på enheten. Lasting av nettstedet og offentlige ressurser krever nettverksforespørsler. Bruk syntetiske tilfeller.',
    ' Luonnokset säilyvät tässä selaimessa, kunnes tyhjennät lomakkeen tai sivuston tiedot. Viedyt tiedostot jäävät laitteellesi. Sivuston ja julkisten resurssien lataaminen edellyttää verkkopyyntöjä. Käytä synteettisiä tapauksia.',
)))
_SERVER_RETENTION = dict(zip(HOME, (
    ' Retention and deletion depend on the hosting and model provider; this page does not establish their policies. Clearing the form does not delete text already submitted to them. Use synthetic cases.',
    ' Зберігання й видалення залежать від хостингу та постачальника моделі; ця сторінка не встановлює їхніх політик. Очищення форми не видаляє вже надісланий їм текст. Використовуйте синтетичні випадки.',
    ' La conservación y eliminación dependen del alojamiento y del proveedor del modelo; esta página no establece sus políticas. Borrar el formulario no elimina el texto ya enviado. Use casos sintéticos.',
    ' A conservação e eliminação dependem do alojamento e do fornecedor do modelo; esta página não estabelece essas políticas. Limpar o formulário não elimina o texto já enviado. Utilize casos sintéticos.',
    ' Aufbewahrung und Löschung hängen vom Hosting- und Modellanbieter ab; diese Seite legt deren Richtlinien nicht fest. Das Leeren des Formulars löscht bereits übermittelte Texte nicht. Verwenden Sie synthetische Fälle.',
    ' La conservation et la suppression dépendent de l’hébergeur et du fournisseur du modèle ; cette page ne définit pas leurs politiques. Effacer le formulaire ne supprime pas le texte déjà transmis. Utilisez des cas synthétiques.',
    ' Conservazione e cancellazione dipendono da hosting e fornitore del modello; questa pagina non ne stabilisce le politiche. Cancellare il modulo non elimina il testo già inviato. Usa casi sintetici.',
    ' Opbevaring og sletning afhænger af hosting- og modeludbyderen; denne side fastlægger ikke deres politikker. Rydning af formularen sletter ikke allerede indsendt tekst. Brug syntetiske tilfælde.',
    ' Lagring och radering beror på värd- och modellleverantören; denna sida fastställer inte deras policyer. Att rensa formuläret raderar inte redan inskickad text. Använd syntetiska fall.',
    ' Lagring og sletting avhenger av hosting- og modellleverandøren; denne siden fastsetter ikke deres retningslinjer. Å tømme skjemaet sletter ikke tekst som allerede er sendt. Bruk syntetiske tilfeller.',
    ' Säilytys ja poistaminen riippuvat hosting- ja mallipalveluntarjoajasta; tämä sivu ei määritä niiden käytäntöjä. Lomakkeen tyhjentäminen ei poista jo lähetettyä tekstiä. Käytä synteettisiä tapauksia.',
)))
for _locale in HOME:
    LOCAL_BODY[_locale] += _LOCAL_STORAGE[_locale]
    TRANSFER_BODY[_locale] += _SERVER_RETENTION[_locale]


def messages_for(locale):
    return {table['en']:table[locale] for table in (HOME,LOCAL_TITLE,LOCAL_BODY,TRANSFER_TITLE,TRANSFER_BODY)}
