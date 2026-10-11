"""Curated display wording for the shared public-page components."""
COPY = {
    'A second opinion on cancer treatment — free, cited, and open.': (
        'Una segunda opinión sobre el tratamiento del cáncer: gratuita, con fuentes y abierta.',
        'Uma segunda opinião sobre o tratamento do cancro — gratuita, com fontes e aberta.',
        'Eine zweite Meinung zur Krebsbehandlung — kostenlos, mit Quellen und offen.',
        'Un second avis sur le traitement du cancer — gratuit, avec des sources et ouvert.',
    ),
    'Capabilities': ('Funcionalidades', 'Funcionalidades', 'Funktionen', 'Fonctionnalités'),
    'Specifications': ('Especificaciones', 'Especificações', 'Technische Spezifikationen', 'Spécifications'),
    'Try the plan builder': ('Probar el generador de planes', 'Experimentar o gerador de planos', 'Planer ausprobieren', 'Essayer le générateur de plans'),
    'About OpenOnco': ('Acerca de OpenOnco', 'Sobre o OpenOnco', 'Über OpenOnco', 'À propos d’OpenOnco'),
    'About the project': ('Acerca del proyecto', 'Sobre o projeto', 'Über das Projekt', 'À propos du projet'),
    'Project news': ('Noticias del proyecto', 'Notícias do projeto', 'Projektneuigkeiten', 'Actualités du projet'),
    'Participate in OpenOnco': ('Participar en OpenOnco', 'Participar no OpenOnco', 'Bei OpenOnco mitwirken', 'Participer à OpenOnco'),
    'Our purpose': ('Nuestro objetivo', 'O nosso objetivo', 'Unser Ziel', 'Notre objectif'),
    'Our approach': ('Nuestro enfoque', 'A nossa abordagem', 'Unser Vorgehen', 'Notre démarche'),
    'Next step': ('Siguiente paso', 'Próximo passo', 'Nächster Schritt', 'Prochaine étape'),
    'Open the plan builder': ('Abrir el generador de planes', 'Abrir o gerador de planos', 'Planer öffnen', 'Ouvrir le générateur de plans'),
    'Explore examples': ('Ver ejemplos', 'Explorar exemplos', 'Beispiele ansehen', 'Consulter les exemples'),
}


def messages_for(locale):
    index = ('es', 'pt', 'de', 'fr').index(locale)
    return {source: values[index] for source, values in COPY.items()}
