"""Checked-in public-site translations. No translation API runs on page visits."""

from pathlib import PurePosixPath

LOCALES = {
    "uk": ("ukr", "Українська", "UA"),
    "en": ("", "English", "EN"),
    "es": ("es", "Español", "ES"),
    "pt": ("pt", "Português", "PT"),
    "de": ("de", "Deutsch", "DE"),
    "fr": ("fr", "Français", "FR"),
}
PUBLIC_PAGES = {"index.html", "about.html", "kb.html", "handbook.html", "try.html", "ask.html", "prevent.html", "gallery.html", "diseases.html", "specs.html", "news.html"}


def split_locale(path: str) -> tuple[str, str]:
    path = path.replace("\\", "/").lstrip("/") or "index.html"
    for code, (prefix, _, _) in LOCALES.items():
        if prefix and path.startswith(prefix + "/"):
            return code, path[len(prefix) + 1:] or "index.html"
    return "en", path


def locale_path(path: str, locale: str) -> str:
    _, page = split_locale(path)
    prefix = LOCALES[locale][0]
    return str(PurePosixPath(prefix, page)) if prefix else page


def locale_href(path: str, locale: str) -> str:
    mapped = locale_path(path, locale)
    return "/" + mapped.removesuffix("index.html") if mapped.endswith("index.html") else "/" + mapped


# New languages localize the public interface. Clinical records, original
# source titles and engine output retain their declared source language.
COPY = {
    "es": {
        "home": "Inicio", "about": "El proyecto", "try_cta": "Crear un plan", "diseases": "Enfermedades", "ask": "Comité de tumores", "kb": "Onco Wiki", "prevent": "Prevención", "news": "Noticias", "handbook": "Manual", "capabilities": "Funciones", "menu": "Menú", "tools": "Herramientas", "brand": "ONCOLOGÍA ABIERTA", "open": "Código abierto", "language": "Idioma",
        "title": "Oncología abierta, con fuentes que puedes consultar.",
        "lead": "Explora la base de conocimientos, consulta las fuentes y prepara preguntas para tu equipo de oncología. OpenOnco genera borradores mediante reglas explícitas; cada resultado requiere la revisión de un profesional sanitario.",
        "kicker": "Gratuito · código abierto · sin registro",
        "search": "Buscar en Onco Wiki", "learn": "Explorar el manual", "scale": "Alcance de la base de conocimientos", "sources": "Fuentes", "regimens": "Esquemas de tratamiento", "biomarkers": "Biomarcadores",
        "status_title": "Qué está traducido", "status": "La navegación, la búsqueda y las páginas de presentación están disponibles en español. Los registros clínicos, los capítulos y los resultados del motor siguen en inglés o ucraniano. El idioma de cada destino se indica antes de abrirlo.",
        "about_title": "Un proyecto abierto para comprender y revisar la información oncológica",
        "about_body": "OpenOnco combina registros YAML, referencias bibliográficas, ejemplos sintéticos y herramientas Python. Los identificadores de fuente y el estado de revisión permiten rastrear cada registro. La cobertura de la base de datos no equivale a una validación clínica.",
        "privacy_title": "Datos y privacidad", "privacy": "El constructor de planes ejecuta el motor en tu navegador. El comité de tumores envía el texto introducido a un servidor para analizarlo. En las herramientas públicas, utiliza únicamente ejemplos sintéticos y no introduzcas información identificativa de pacientes.",
        "clinical_title": "Revisión clínica pendiente", "clinical": "Proyecto en desarrollo. Los borradores educativos y de planificación no sustituyen al equipo médico ni autorizan a iniciar, suspender o cambiar un tratamiento.",
        "contribute": "Contribuir en GitHub", "documentation": "Documentación técnica (inglés)", "english": "Abrir en inglés", "english_note": "Esta herramienta y sus resultados están disponibles en inglés. Esta página explica su función en español.",
        "try_body": "Introduce un perfil sintético estructurado para generar un borrador de plan con referencias y señales de riesgo. Comprueba los datos faltantes y consulta las fuentes antes de la revisión clínica.",
        "ask_body": "Prepara una discusión multidisciplinar a partir de un caso sintético. El texto se envía a un servidor; no incluyas datos personales ni documentos de pacientes.",
        "prevent_body": "Explora el módulo de prevención y sus referencias. Las decisiones de cribado dependen del contexto individual y de las guías aplicables.",
        "gallery": "Ejemplos sintéticos", "gallery_body": "Consulta ejemplos de perfiles y resultados generados. Son casos ficticios para explorar el funcionamiento y las limitaciones del proyecto.",
        "diseases_body": "Consulta las enfermedades representadas en la base y su cobertura. Un registro existente no garantiza un algoritmo completo ni una revisión clínica finalizada.",
        "specs": "Especificaciones", "specs_body": "Consulta las especificaciones, los contratos del motor y las reglas de revisión del proyecto.",
        "news_body": "Consulta las novedades del proyecto y sus fuentes. Las noticias originales conservan el idioma en que se publicaron.",
        "handbook_title": "Manual de aprendizaje en oncología", "handbook_body": "Nueve capítulos educativos con fuentes, casos sintéticos y preguntas de práctica. Los capítulos están disponibles en inglés y ucraniano; su estado de revisión clínica se conserva.",
        "chapter_en": "Capítulo en inglés", "chapter_uk": "Capítulo en ucraniano", "questions": "Preguntas", "draft": "Borrador", "footer": "Código abierto · Código: MIT · Contenido: CC BY 4.0",
    },
    "pt": {
        "home": "Início", "about": "O projeto", "try_cta": "Criar um plano", "diseases": "Doenças", "ask": "Reunião multidisciplinar", "kb": "Onco Wiki", "prevent": "Prevenção", "news": "Notícias", "handbook": "Manual", "capabilities": "Funcionalidades", "menu": "Menu", "tools": "Ferramentas", "brand": "ONCOLOGIA ABERTA", "open": "Código aberto", "language": "Idioma",
        "title": "Oncologia aberta, com fontes que pode consultar.",
        "lead": "Explore a base de conhecimentos, consulte as fontes e prepare perguntas para a sua equipa de oncologia. O OpenOnco gera rascunhos através de regras explícitas; cada resultado exige a revisão de um profissional de saúde.",
        "kicker": "Gratuito · código aberto · sem registo",
        "search": "Pesquisar na Onco Wiki", "learn": "Explorar o manual", "scale": "Dimensão da base de conhecimentos", "sources": "Fontes", "regimens": "Esquemas de tratamento", "biomarkers": "Biomarcadores",
        "status_title": "O que está traduzido", "status": "A navegação, a pesquisa e as páginas de apresentação estão disponíveis em português. Os registos clínicos, os capítulos e os resultados do motor continuam em inglês ou ucraniano. O idioma de cada destino é indicado antes de o abrir.",
        "about_title": "Um projeto aberto para compreender e rever a informação oncológica",
        "about_body": "O OpenOnco combina registos YAML, referências bibliográficas, exemplos sintéticos e ferramentas Python. Os identificadores das fontes e o estado de revisão permitem rastrear cada registo. A cobertura da base de dados não equivale a validação clínica.",
        "privacy_title": "Dados e privacidade", "privacy": "O construtor de planos executa o motor no seu navegador. A reunião multidisciplinar envia o texto introduzido para um servidor para análise. Nas ferramentas públicas, utilize apenas exemplos sintéticos e não introduza informações que identifiquem pacientes.",
        "clinical_title": "Revisão clínica pendente", "clinical": "Projeto em desenvolvimento. Os rascunhos educativos e de planeamento não substituem a equipa médica nem autorizam o início, a suspensão ou a alteração de um tratamento.",
        "contribute": "Contribuir no GitHub", "documentation": "Documentação técnica (inglês)", "english": "Abrir em inglês", "english_note": "Esta ferramenta e os seus resultados estão disponíveis em inglês. Esta página explica a sua função em português.",
        "try_body": "Introduza um perfil sintético estruturado para gerar um rascunho de plano com referências e sinais de risco. Verifique os dados em falta e consulte as fontes antes da revisão clínica.",
        "ask_body": "Prepare uma discussão multidisciplinar a partir de um caso sintético. O texto é enviado para um servidor; não inclua dados pessoais nem documentos de pacientes.",
        "prevent_body": "Explore o módulo de prevenção e as suas referências. As decisões de rastreio dependem do contexto individual e das orientações aplicáveis.",
        "gallery": "Exemplos sintéticos", "gallery_body": "Consulte exemplos de perfis e resultados gerados. São casos fictícios para explorar o funcionamento e as limitações do projeto.",
        "diseases_body": "Consulte as doenças representadas na base e a sua cobertura. A existência de um registo não garante um algoritmo completo nem uma revisão clínica concluída.",
        "specs": "Especificações", "specs_body": "Consulte as especificações, os contratos do motor e as regras de revisão do projeto.",
        "news_body": "Consulte as novidades do projeto e as respetivas fontes. As notícias originais mantêm o idioma em que foram publicadas.",
        "handbook_title": "Manual de aprendizagem em oncologia", "handbook_body": "Nove capítulos educativos com fontes, casos sintéticos e perguntas de treino. Os capítulos estão disponíveis em inglês e ucraniano; o seu estado de revisão clínica é preservado.",
        "chapter_en": "Capítulo em inglês", "chapter_uk": "Capítulo em ucraniano", "questions": "Perguntas", "draft": "Rascunho", "footer": "Código aberto · Código: MIT · Conteúdo: CC BY 4.0",
    },
    "de": {
        "home": "Start", "about": "Über das Projekt", "try_cta": "Plan erstellen", "diseases": "Erkrankungen", "ask": "Tumorboard", "kb": "Onco Wiki", "prevent": "Prävention", "news": "Neuigkeiten", "handbook": "Handbuch", "capabilities": "Funktionen", "menu": "Menü", "tools": "Werkzeuge", "brand": "OFFENE ONKOLOGIE", "open": "Open Source", "language": "Sprache",
        "title": "Offene Onkologie mit nachvollziehbaren Quellen.",
        "lead": "Erkunden Sie die Wissensbasis, prüfen Sie Quellen und bereiten Sie Fragen für Ihr Onkologieteam vor. OpenOnco erstellt Entwürfe anhand expliziter Regeln. Jedes Ergebnis muss von medizinischem Fachpersonal geprüft werden.",
        "kicker": "Kostenlos · Open Source · ohne Registrierung",
        "search": "Onco Wiki durchsuchen", "learn": "Handbuch erkunden", "scale": "Umfang der Wissensbasis", "sources": "Quellen", "regimens": "Therapieschemata", "biomarkers": "Biomarker",
        "status_title": "Umfang der Übersetzung", "status": "Navigation, Suche und Projektseiten sind auf Deutsch verfügbar. Klinische Datensätze, Kapitel und Ergebnisse der Engine bleiben auf Englisch oder Ukrainisch. Die Sprache des Ziels wird vor dem Öffnen angegeben.",
        "about_title": "Ein offenes Projekt zum Verständnis und zur Prüfung onkologischer Informationen",
        "about_body": "OpenOnco verbindet YAML-Datensätze, Literaturverweise, synthetische Beispiele und Python-Werkzeuge. Quellenkennungen und Prüfstatus machen Datensätze nachvollziehbar. Der Umfang der Datenbank entspricht keiner klinischen Validierung.",
        "privacy_title": "Daten und Datenschutz", "privacy": "Der Planer führt die Engine in Ihrem Browser aus. Das Tumorboard sendet den eingegebenen Text zur Analyse an einen Server. Verwenden Sie in den öffentlichen Werkzeugen ausschließlich synthetische Beispiele und keine identifizierenden Patientendaten.",
        "clinical_title": "Klinische Prüfung ausstehend", "clinical": "Das Projekt befindet sich in Entwicklung. Lernmaterialien und Planentwürfe ersetzen kein Behandlungsteam und sind keine Grundlage, eine Behandlung eigenständig zu beginnen, abzusetzen oder zu ändern.",
        "contribute": "Auf GitHub mitwirken", "documentation": "Technische Dokumentation (Englisch)", "english": "Auf Englisch öffnen", "english_note": "Dieses Werkzeug und seine Ergebnisse sind auf Englisch verfügbar. Diese Seite erläutert seine Funktion auf Deutsch.",
        "try_body": "Geben Sie ein strukturiertes synthetisches Profil ein, um einen Planentwurf mit Quellen und Risikohinweisen zu erstellen. Prüfen Sie fehlende Angaben und die Quellen vor der klinischen Prüfung.",
        "ask_body": "Bereiten Sie anhand eines synthetischen Falls eine multidisziplinäre Besprechung vor. Der Text wird an einen Server gesendet. Geben Sie keine personenbezogenen Daten oder Patientenunterlagen ein.",
        "prevent_body": "Erkunden Sie das Präventionsmodul und seine Quellen. Entscheidungen zur Früherkennung hängen vom individuellen Kontext und den geltenden Leitlinien ab.",
        "gallery": "Synthetische Beispiele", "gallery_body": "Sehen Sie sich Beispielprofile und generierte Ergebnisse an. Die fiktiven Fälle veranschaulichen die Funktionsweise und Grenzen des Projekts.",
        "diseases_body": "Prüfen Sie die in der Wissensbasis enthaltenen Erkrankungen und deren Abdeckung. Ein vorhandener Datensatz garantiert weder einen vollständigen Algorithmus noch eine abgeschlossene klinische Prüfung.",
        "specs": "Spezifikationen", "specs_body": "Lesen Sie die Spezifikationen, die Verträge der Engine und die Prüfregeln des Projekts.",
        "news_body": "Lesen Sie Projektneuigkeiten und die zugehörigen Quellen. Originalmeldungen bleiben in ihrer Veröffentlichungssprache.",
        "handbook_title": "Lernhandbuch zur Onkologie", "handbook_body": "Neun Lernkapitel mit Quellen, synthetischen Fällen und Übungsfragen. Die Kapitel sind auf Englisch und Ukrainisch verfügbar; ihr klinischer Prüfstatus bleibt erhalten.",
        "chapter_en": "Kapitel auf Englisch", "chapter_uk": "Kapitel auf Ukrainisch", "questions": "Fragen", "draft": "Entwurf", "footer": "Open Source · Code: MIT · Inhalte: CC BY 4.0",
    },
    "fr": {
        "home": "Accueil", "about": "Le projet", "try_cta": "Créer un plan", "diseases": "Maladies", "ask": "Réunion de concertation", "kb": "Onco Wiki", "prevent": "Prévention", "news": "Actualités", "handbook": "Manuel", "capabilities": "Fonctionnalités", "menu": "Menu", "tools": "Outils", "brand": "ONCOLOGIE OUVERTE", "open": "Code ouvert", "language": "Langue",
        "title": "Une oncologie ouverte, avec des sources consultables.",
        "lead": "Explorez la base de connaissances, consultez les sources et préparez vos questions pour votre équipe d’oncologie. OpenOnco produit des brouillons à partir de règles explicites. Chaque résultat nécessite une vérification par un professionnel de santé.",
        "kicker": "Gratuit · code ouvert · sans inscription",
        "search": "Rechercher dans Onco Wiki", "learn": "Explorer le manuel", "scale": "Étendue de la base de connaissances", "sources": "Sources", "regimens": "Protocoles de traitement", "biomarkers": "Biomarqueurs",
        "status_title": "Ce qui est traduit", "status": "La navigation, la recherche et les pages de présentation sont disponibles en français. Les fiches cliniques, les chapitres et les résultats du moteur restent en anglais ou en ukrainien. La langue de destination est indiquée avant l’ouverture.",
        "about_title": "Un projet ouvert pour comprendre et examiner l’information en oncologie",
        "about_body": "OpenOnco associe des fiches YAML, des références bibliographiques, des exemples synthétiques et des outils Python. Les identifiants des sources et le statut de révision permettent de retracer chaque fiche. L’étendue de la base ne constitue pas une validation clinique.",
        "privacy_title": "Données et confidentialité", "privacy": "Le constructeur de plans exécute le moteur dans votre navigateur. L’outil de concertation envoie le texte saisi à un serveur pour analyse. Utilisez uniquement des exemples synthétiques dans les outils publics et ne saisissez aucune donnée permettant d’identifier un patient.",
        "clinical_title": "Vérification clinique en attente", "clinical": "Projet en cours de développement. Les contenus pédagogiques et les brouillons de plans ne remplacent pas l’équipe médicale et n’autorisent pas à commencer, arrêter ou modifier un traitement.",
        "contribute": "Contribuer sur GitHub", "documentation": "Documentation technique (anglais)", "english": "Ouvrir en anglais", "english_note": "Cet outil et ses résultats sont disponibles en anglais. Cette page explique son rôle en français.",
        "try_body": "Saisissez un profil synthétique structuré pour produire un brouillon de plan avec des références et des signaux de risque. Vérifiez les données manquantes et consultez les sources avant la vérification clinique.",
        "ask_body": "Préparez une discussion multidisciplinaire à partir d’un cas synthétique. Le texte est envoyé à un serveur. N’incluez aucune donnée personnelle ni aucun document de patient.",
        "prevent_body": "Explorez le module de prévention et ses références. Les décisions de dépistage dépendent du contexte individuel et des recommandations applicables.",
        "gallery": "Exemples synthétiques", "gallery_body": "Consultez des exemples de profils et de résultats générés. Ces cas fictifs illustrent le fonctionnement et les limites du projet.",
        "diseases_body": "Consultez les maladies représentées dans la base et leur couverture. Une fiche existante ne garantit ni un algorithme complet ni une vérification clinique achevée.",
        "specs": "Spécifications", "specs_body": "Consultez les spécifications, les contrats du moteur et les règles de révision du projet.",
        "news_body": "Consultez les actualités du projet et leurs sources. Les nouvelles originales conservent leur langue de publication.",
        "handbook_title": "Manuel d’apprentissage en oncologie", "handbook_body": "Neuf chapitres pédagogiques avec des sources, des cas synthétiques et des questions d’entraînement. Les chapitres sont disponibles en anglais et en ukrainien ; leur statut de vérification clinique est conservé.",
        "chapter_en": "Chapitre en anglais", "chapter_uk": "Chapitre en ukrainien", "questions": "Questions", "draft": "Brouillon", "footer": "Code ouvert · Code : MIT · Contenu : CC BY 4.0",
    },
}
