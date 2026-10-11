"""Native navigation and source copy for additional checked-in language drafts."""
ADDITIONAL_LANGUAGES = ('it', 'da', 'sv', 'nb', 'fi')

ENGLISH_COPY = {
    'home': 'Home', 'about': 'About', 'try_cta': 'Plan Builder', 'diseases': 'Diseases',
    'ask': 'Tumor Board', 'kb': 'Onco Wiki', 'prevent': 'Prevention', 'news': 'News',
    'handbook': 'Handbook', 'capabilities': 'Capabilities', 'menu': 'Menu',
    'tools': 'Tools', 'brand': 'OPEN ONCOLOGY', 'open': 'Open source', 'language': 'Language',
    'title': 'Open oncology, with sources you can inspect.',
    'lead': 'Explore the knowledge base, inspect original sources and prepare questions for your oncology team. OpenOnco creates informational drafts through explicit rules. Technical checks do not approve individual treatment.',
    'kicker': 'Free · open source · no registration',
    'search': 'Search Onco Wiki', 'learn': 'Explore the handbook',
    'scale': 'Knowledge-base coverage', 'sources': 'Sources', 'regimens': 'Treatment regimens',
    'biomarkers': 'Biomarkers', 'status_title': 'Translation status',
    'status': 'This edition contains draft translations. Original English or Ukrainian passages may be retained for verification. Identifiers, doses and engine values stay unchanged. Language and clinical review status are recorded separately.',
    'about_title': 'A solo project for source-linked oncology information',
    'about_body': 'One maintainer develops OpenOnco with automated checks and source traceability. External clinical review is optional and recorded separately; it is not a development or publication quota. Coverage and technical tests are not clinical validation.',
    'privacy_title': 'Data and privacy',
    'privacy': 'The browser Plan Builder processes profiles locally. Tumor Board sends submitted text to a server. Use synthetic examples for public demonstrations; do not submit identifiable patient information.',
    'clinical_title': 'Informational drafts',
    'clinical': 'Educational and planning drafts do not replace your care team or authorize starting, stopping or changing treatment. Discuss individual decisions with your treating clinician.',
    'contribute': 'Contribute on GitHub', 'documentation': 'Technical documentation (English)',
    'english': 'Open the English original', 'english_note': 'The original English edition remains available for verification.',
    'try_body': 'Use a synthetic structured profile to create a draft with references and risk signals. Check missing data and original sources before discussing the result with a clinician.',
    'ask_body': 'Prepare a multidisciplinary discussion using a synthetic case. Submitted text is sent to a server; do not include personal information or patient documents.',
    'prevent_body': 'Explore the prevention tool and its sources. Screening decisions depend on individual context and applicable guidance.',
    'gallery': 'Synthetic examples', 'gallery_body': 'Explore fictional profiles and generated outputs to understand the tools and their limitations.',
    'diseases_body': 'Explore disease coverage. An existing record does not establish a complete algorithm or clinical validation.',
    'specs': 'Specifications', 'specs_body': 'Explore the project specifications, engine contracts and solo-maintainer delivery workflow.',
    'news_body': 'Read project updates and their sources. Original news articles retain their publication language.',
    'handbook_title': 'Oncology learning handbook',
    'handbook_body': 'Nine educational chapters with sources, synthetic examples and practice questions. Translations are drafts; original passages and actual review status are preserved.',
    'chapter_en': 'Chapter in English', 'chapter_uk': 'Chapter in Ukrainian',
    'questions': 'Questions', 'draft': 'Draft', 'footer': 'Open source · Code: MIT · Content: CC BY 4.0',
}

NAVIGATION = {
    'it': ('Home', 'Il progetto', 'Crea un piano', 'Malattie', 'Gruppo multidisciplinare', 'Onco Wiki', 'Prevenzione', 'Notizie', 'Manuale', 'Funzionalità', 'Menu', 'Strumenti', 'ONCOLOGIA APERTA', 'Codice aperto', 'Lingua'),
    'da': ('Forside', 'Om projektet', 'Opret en plan', 'Sygdomme', 'Tværfaglig konference', 'Onco Wiki', 'Forebyggelse', 'Nyheder', 'Håndbog', 'Funktioner', 'Menu', 'Værktøjer', 'ÅBEN ONKOLOGI', 'Åben kildekode', 'Sprog'),
    'sv': ('Hem', 'Om projektet', 'Skapa en plan', 'Sjukdomar', 'Multidisciplinär konferens', 'Onco Wiki', 'Förebyggande', 'Nyheter', 'Handbok', 'Funktioner', 'Meny', 'Verktyg', 'ÖPPEN ONKOLOGI', 'Öppen källkod', 'Språk'),
    'nb': ('Hjem', 'Om prosjektet', 'Lag en plan', 'Sykdommer', 'Tverrfaglig møte', 'Onco Wiki', 'Forebygging', 'Nyheter', 'Håndbok', 'Funksjoner', 'Meny', 'Verktøy', 'ÅPEN ONKOLOGI', 'Åpen kildekode', 'Språk'),
    'fi': ('Etusivu', 'Tietoa hankkeesta', 'Luo suunnitelma', 'Sairaudet', 'Moniammatillinen kokous', 'Onco Wiki', 'Ehkäisy', 'Uutiset', 'Käsikirja', 'Toiminnot', 'Valikko', 'Työkalut', 'AVOIN ONKOLOGIA', 'Avoin lähdekoodi', 'Kieli'),
}
NAVIGATION_KEYS = tuple(ENGLISH_COPY)[:15]

NOTICES = {
    'it': ('Traduzione preliminare: revisione clinica in attesa.', 'Consulta l’originale in inglese', 'Testo originale conservato per la verifica', 'Consulta l’originale in ucraino', 'Consulta la versione originale'),
    'da': ('Foreløbig oversættelse: klinisk gennemgang afventer.', 'Se den engelske original', 'Originaltekst bevaret til kontrol', 'Se den ukrainske original', 'Se originalversionen'),
    'sv': ('Preliminär översättning: klinisk granskning väntar.', 'Visa det engelska originalet', 'Originaltext bevarad för kontroll', 'Visa det ukrainska originalet', 'Visa originalversionen'),
    'nb': ('Foreløpig oversettelse: klinisk gjennomgang gjenstår.', 'Se den engelske originalen', 'Originaltekst bevart for kontroll', 'Se den ukrainske originalen', 'Se originalversjonen'),
    'fi': ('Alustava käännös: kliininen tarkistus on kesken.', 'Näytä englanninkielinen alkuperäisteksti', 'Alkuperäisteksti säilytetty tarkistusta varten', 'Näytä ukrainankielinen alkuperäisteksti', 'Näytä alkuperäinen versio'),
}

# Curated interface copy corrects literal model output. These are language
# drafts describing existing software, not reviews of clinical recommendations.
CURATED_SITE_FIELDS = {
    'it': {
        'title': 'Oncologia aperta, con fonti consultabili.',
        'kicker': 'Gratuito · codice aperto · senza registrazione',
        'lead': 'Esplora la base di conoscenze, consulta le fonti originali e prepara domande per il tuo team oncologico. OpenOnco genera bozze informative mediante regole esplicite. Le verifiche tecniche non costituiscono un’approvazione del trattamento individuale.',
        'about_body': 'Una sola persona sviluppa OpenOnco con verifiche automatiche e fonti tracciabili. La revisione clinica esterna è facoltativa e viene registrata separatamente; non è un requisito per lo sviluppo o la pubblicazione. La copertura dei dati e i test tecnici non sono una validazione clinica.',
        'privacy': 'Plan Builder elabora i profili localmente nel browser. Tumor Board invia il testo inserito a un server. Usa esempi sintetici nelle dimostrazioni pubbliche e non inserire informazioni che consentano di identificare un paziente.',
        'clinical': 'Le bozze educative e di pianificazione non sostituiscono il team curante e non autorizzano a iniziare, interrompere o modificare un trattamento. Discuti le decisioni individuali con il tuo medico curante.',
    },
    'da': {
        'title': 'Åben onkologi med kilder, du kan gennemgå.',
        'kicker': 'Gratis · åben kildekode · uden registrering',
        'lead': 'Udforsk vidensbasen, gennemgå de oprindelige kilder, og forbered spørgsmål til dit onkologiske team. OpenOnco udarbejder informationsudkast ud fra eksplicitte regler. Tekniske kontroller er ikke en godkendelse af den enkelte patients behandling.',
        'about_body': 'Én person udvikler OpenOnco med automatiserede kontroller og sporbare kilder. Ekstern klinisk gennemgang er valgfri og registreres særskilt; den er ikke et krav for udvikling eller offentliggørelse. Datadækning og tekniske test er ikke klinisk validering.',
        'privacy': 'Plan Builder behandler profiler lokalt i browseren. Tumor Board sender den indtastede tekst til en server. Brug syntetiske eksempler ved offentlige demonstrationer, og indtast ikke oplysninger, der kan identificere patienter.',
        'clinical': 'Udkast til undervisning og planlægning erstatter ikke dit behandlingsteam og giver ikke tilladelse til at starte, stoppe eller ændre en behandling. Drøft individuelle beslutninger med din behandlende læge.',
    },
    'sv': {
        'title': 'Öppen onkologi med källor som du kan granska.',
        'kicker': 'Gratis · öppen källkod · utan registrering',
        'lead': 'Utforska kunskapsbasen, granska originalkällorna och förbered frågor till ditt onkologiska team. OpenOnco skapar informationsutkast med uttryckliga regler. Tekniska kontroller innebär inte att en enskild patients behandling har godkänts.',
        'about_body': 'En person utvecklar OpenOnco med automatiserade kontroller och spårbara källor. Extern klinisk granskning är valfri och dokumenteras separat; den är inte ett krav för utveckling eller publicering. Datatäckning och tekniska tester är inte klinisk validering.',
        'privacy': 'Plan Builder behandlar profiler lokalt i webbläsaren. Tumor Board skickar den inmatade texten till en server. Använd syntetiska exempel vid offentliga demonstrationer och ange inte uppgifter som kan identifiera patienter.',
        'clinical': 'Utkast för utbildning och planering ersätter inte ditt vårdteam och ger inte tillåtelse att påbörja, avsluta eller ändra en behandling. Diskutera individuella beslut med din behandlande läkare.',
    },
    'nb': {
        'title': 'Åpen onkologi med kilder du kan undersøke.',
        'kicker': 'Gratis · åpen kildekode · uten registrering',
        'lead': 'Utforsk kunnskapsbasen, undersøk originalkildene og forbered spørsmål til ditt onkologiske team. OpenOnco lager informasjonsutkast med eksplisitte regler. Tekniske kontroller innebærer ikke at en enkelt pasients behandling er godkjent.',
        'about_body': 'Én person utvikler OpenOnco med automatiserte kontroller og sporbare kilder. Ekstern klinisk gjennomgang er valgfri og registreres separat; den er ikke et krav for utvikling eller publisering. Datadekning og tekniske tester er ikke klinisk validering.',
        'privacy': 'Plan Builder behandler profiler lokalt i nettleseren. Tumor Board sender teksten som er skrevet inn, til en server. Bruk syntetiske eksempler i offentlige demonstrasjoner, og ikke oppgi informasjon som kan identifisere pasienter.',
        'clinical': 'Utkast til opplæring og planlegging erstatter ikke behandlingsteamet ditt og gir ikke tillatelse til å starte, stoppe eller endre en behandling. Diskuter individuelle beslutninger med legen som behandler deg.',
    },
    'fi': {
        'title': 'Avointa onkologiaa ja tarkistettavia lähteitä.',
        'kicker': 'Maksuton · avoin lähdekoodi · ei rekisteröitymistä',
        'lead': 'Tutustu tietopohjaan, tarkista alkuperäiset lähteet ja valmistele kysymyksiä syövänhoitotiimillesi. OpenOnco tuottaa tietoluonnoksia selkeiden sääntöjen avulla. Tekniset tarkistukset eivät tarkoita yksittäisen potilaan hoidon hyväksymistä.',
        'about_body': 'Yksi henkilö kehittää OpenOncoa automaattisten tarkistusten ja jäljitettävien lähteiden avulla. Ulkopuolinen kliininen arvio on vapaaehtoinen ja kirjataan erikseen; se ei ole kehittämisen tai julkaisemisen edellytys. Tietopohjan kattavuus ja tekniset testit eivät ole kliinistä validointia.',
        'privacy': 'Plan Builder käsittelee profiileja paikallisesti selaimessa. Tumor Board lähettää syötetyn tekstin palvelimelle. Käytä julkisissa esittelyissä synteettisiä esimerkkejä äläkä syötä tietoja, joista potilaan voi tunnistaa.',
        'clinical': 'Opetukseen ja suunnitteluun tarkoitetut luonnokset eivät korvaa hoitotiimiäsi eivätkä anna lupaa aloittaa, lopettaa tai muuttaa hoitoa. Keskustele yksilöllisistä päätöksistä hoitavan lääkärisi kanssa.',
    },
}
