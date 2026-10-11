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
    'Drugs': ('Medicamentos', 'Medicamentos', 'Arzneimittel', 'Médicaments'),
    'Drug records with machine-readable context.': (
        'Fichas de medicamentos con contexto legible por máquina.',
        'Registos de medicamentos com contexto legível por máquina.',
        'Arzneimitteleinträge mit maschinenlesbarem Kontext.',
        'Fiches de médicaments avec un contexte lisible par machine.',
    ),
    'per-disease drill-down.': (
        'desglose por enfermedad.',
        'detalhamento por doença.',
        'Aufschlüsselung nach Erkrankung.',
        'détail par maladie.',
    ),
    'Decision tree step by step. Trace records fired_red_flags at each node.': (
        'Árbol de decisión paso a paso. El registro documenta fired_red_flags en cada nodo.',
        'Árvore de decisão passo a passo. O registo documenta fired_red_flags em cada nó.',
        'Entscheidungsbaum Schritt für Schritt. Das Protokoll erfasst fired_red_flags an jedem Knoten.',
        'Arbre de décision étape par étape. La trace consigne fired_red_flags à chaque nœud.',
    ),
    'Doses come from the standard NCCN/ESMO. Adjustments only via explicit': (
        'Las dosis proceden de las guías NCCN/ESMO. Los ajustes solo se realizan mediante reglas explícitas',
        'As doses provêm das diretrizes NCCN/ESMO. Os ajustes só são feitos por regras explícitas',
        'Die Dosierungen stammen aus den NCCN/ESMO-Leitlinien. Anpassungen erfolgen nur nach ausdrücklichen Regeln',
        'Les doses proviennent des recommandations NCCN/ESMO. Les ajustements suivent uniquement des règles explicites',
    ),
    'FDA Criterion 4 fields: intended_use, patient_population_match, algorithm_summary, automation_bias_warning': (
        'Campos del criterio 4 de la FDA: intended_use, patient_population_match, algorithm_summary, automation_bias_warning',
        'Campos do critério 4 da FDA: intended_use, patient_population_match, algorithm_summary, automation_bias_warning',
        'Felder für FDA-Kriterium 4: intended_use, patient_population_match, algorithm_summary, automation_bias_warning',
        'Champs du critère 4 de la FDA : intended_use, patient_population_match, algorithm_summary, automation_bias_warning',
    ),
    'lowers workup match confidence; lineage_hint + tissue dominate': (
        'reduce la confianza en la correspondencia del estudio diagnóstico; predominan lineage_hint y el tejido',
        'reduz a confiança na correspondência da avaliação diagnóstica; predominam lineage_hint e o tecido',
        'senkt die Sicherheit der diagnostischen Zuordnung; lineage_hint und Gewebe sind ausschlaggebend',
        'réduit la confiance dans la correspondance du bilan diagnostique ; lineage_hint et le tissu sont déterminants',
    ),
    '. Stale-cost warning > 180 days.': (
        '. Aviso si la antigüedad de los datos de costes es > 180 días.',
        '. Aviso se a antiguidade dos dados de custos for > 180 dias.',
        '. Warnung, wenn die Kostendaten > 180 Tage alt sind.',
        '. Alerte si les données de coût datent de > 180 jours.',
    ),
}

TECHNICAL_LITERALS = (
    '/diseases.html', '/ukr', '.cap-panel',
    '.lang-switch a, a.lang-other, a.lang-current',
)


def messages_for(locale):
    index = ('es', 'pt', 'de', 'fr').index(locale)
    return {
        **{source: values[index] for source, values in COPY.items()},
        **{literal: literal for literal in TECHNICAL_LITERALS},
    }
