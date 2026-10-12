"""Explicit display terminology; source disease codes remain unchanged."""
import re

AVAILABILITY_LABELS = {
    'es': '✗ No registrado en Ucrania', 'pt': '✗ Não registado na Ucrânia',
    'de': '✗ Nicht in der Ukraine registriert', 'fr': '✗ Non enregistré en Ukraine',
    'it': '✗ Non registrato in Ucraina', 'da': '✗ Ikke registreret i Ukraine',
    'sv': '✗ Inte registrerat i Ukraina', 'nb': '✗ Ikke registrert i Ukraina',
    'fi': '✗ Ei rekisteröity Ukrainassa',
}

STAGING_LABELS = {
    'it': {'Stage': 'Stadio', 'Staging': 'Stadiazione'},
    'da': {'Stage': 'Stadium', 'Staging': 'Stadieinddeling'},
    'sv': {'Stage': 'Stadium', 'Staging': 'Stadieindelning'},
    'nb': {'Stage': 'Stadium', 'Staging': 'Stadieinndeling'},
    'fi': {'Stage': 'Levinneisyysaste', 'Staging': 'Levinneisyysluokitus'},
}


def diagnostic_display(source, locale):
    """Translate only the label of an exact technical code list, never clinical prose."""
    match = re.fullmatch(r'Unevaluated RedFlags: (RF-[A-Z0-9_-]+(?:, RF-[A-Z0-9_-]+)*)', source)
    if not match:
        return None
    label = {
        'es': 'Alertas no evaluadas: ',
        'pt': 'Alertas não avaliados: ',
        'de': 'Nicht ausgewertete Warnhinweise: ',
        'fr': 'Alertes non évaluées : ',
        'it': 'Segnali di allarme non valutati: ',
        'da': 'Ikke-vurderede advarselstegn: ',
        'sv': 'Ej bedömda varningssignaler: ',
        'nb': 'Ikke-vurderte varselsignaler: ',
        'fi': 'Arvioimattomat varoitusmerkit: ',
    }[locale]
    return label + match[1]

# Classification prefixes are not conditional negations. Keep these names
# explicit rather than weakening the negation check for treatment prose.
NSCLC = {
    'es': 'Cáncer de pulmón de células no pequeñas',
    'pt': 'Cancro do pulmão de não pequenas células',
    'de': 'Nicht-kleinzelliges Lungenkarzinom',
    'fr': 'Cancer bronchique non à petites cellules',
}
TERMINOLOGY_SOURCES = {
    'es': 'https://www.cancer.gov/espanol/tipos',
    'pt': 'https://www.dgs.pt/documentos-e-publicacoes/recomendacoes-nacionais-para-diagnostico-e-tratamento-do-cancro-do-pulmao-pdf.aspx',
    'de': 'https://www.krebsinformationsdienst.de/lungenkrebs/behandlung-nicht-kleinzelliges-bronchialkarzinom',
    'fr': 'https://www.cancer.fr/personnes-malades/les-cancers/poumon/comprendre-la-maladie/l-essentiel',
}

# Safety notices are compared sentence by sentence with their English source.
# They remain labeled pending clinical review on localized pages.
SAFETY_NOTICES = {
    'This report contains no molecular-target interpretation linked to treatment. This does not establish that molecular test results are negative or that no targets exist. Ask your doctor to review the original results and whether further testing is appropriate.': (
        'Este informe no contiene una interpretación de las dianas moleculares vinculada al tratamiento. Esto no demuestra que los resultados de las pruebas moleculares sean negativos ni que no existan dianas. Pida a su médico que revise los resultados originales y valore si son adecuadas otras pruebas.',
        'Este relatório não contém uma interpretação de alvos moleculares relacionada com o tratamento. Isto não demonstra que os resultados dos testes moleculares sejam negativos ou que não existam alvos. Peça ao seu médico que reveja os resultados originais e avalie se são apropriados testes adicionais.',
        'Dieser Bericht enthält keine Interpretation molekularer Zielstrukturen im Hinblick auf die Behandlung. Daraus lässt sich nicht ableiten, dass molekulare Testergebnisse negativ sind oder keine Zielstrukturen vorhanden sind. Bitten Sie Ihre Ärztin oder Ihren Arzt, die Originalbefunde zu prüfen und zu beurteilen, ob weitere Tests sinnvoll sind.',
        'Ce rapport ne présente pas d’interprétation des cibles moléculaires en lien avec le traitement. Cela ne permet pas de conclure que les résultats des analyses moléculaires sont négatifs ou qu’il n’existe pas de cible. Demandez à votre médecin d’examiner les résultats originaux et de déterminer si des analyses supplémentaires sont appropriées.',
    ),
    'Outpatient oncology treatment planning to support tumor-board discussion. Not a medical device; not for autonomous clinical decision-making.': (
        'Planificación del tratamiento oncológico ambulatorio para apoyar la deliberación del comité de tumores. No es un dispositivo médico; no está destinado a tomar decisiones clínicas de forma autónoma.',
        'Planeamento do tratamento oncológico em ambulatório para apoiar a discussão na reunião multidisciplinar de oncologia. Não é um dispositivo médico; não se destina à tomada autónoma de decisões clínicas.',
        'Planung ambulanter onkologischer Behandlungen zur Unterstützung der Tumorkonferenz. Kein Medizinprodukt; nicht für autonome klinische Entscheidungen bestimmt.',
        'Planification des traitements oncologiques ambulatoires pour soutenir la discussion en réunion de concertation pluridisciplinaire. Ce n’est pas un dispositif médical ; il n’est pas destiné à prendre des décisions cliniques de manière autonome.',
    ),
    'Diagnostic-phase MDT support: structure the workup, identify the team, surface unresolved questions. Not a medical device; not a treatment plan.': (
        'Apoyo al equipo multidisciplinar durante la fase diagnóstica: estructurar el estudio, identificar al equipo y señalar las cuestiones pendientes. No es un dispositivo médico; no es un plan de tratamiento.',
        'Apoio à equipa multidisciplinar na fase de diagnóstico: estruturar a avaliação, identificar a equipa e assinalar as questões por resolver. Não é um dispositivo médico; não é um plano de tratamento.',
        'Unterstützung des multidisziplinären Teams in der Diagnostikphase: Abklärung strukturieren, Team benennen und offene Fragen aufzeigen. Kein Medizinprodukt; kein Behandlungsplan.',
        'Soutien à l’équipe pluridisciplinaire pendant la phase diagnostique : structurer le bilan, identifier l’équipe et signaler les questions en suspens. Ce n’est pas un dispositif médical ; ce n’est pas un plan de traitement.',
    ),
    'Synthetic educational example. Do not self-treat: a qualified treating physician must verify the sources, patient data, contraindications, and final plan.': (
        'Ejemplo educativo sintético. No se trate por su cuenta: un médico tratante cualificado debe verificar las fuentes, los datos del paciente, las contraindicaciones y el plan final.',
        'Exemplo educativo sintético. Não se trate por conta própria: um médico assistente qualificado deve verificar as fontes, os dados do doente, as contraindicações e o plano final.',
        'Synthetisches Lehrbeispiel. Nicht selbst behandeln: Eine qualifizierte behandelnde Ärztin oder ein qualifizierter behandelnder Arzt muss die Quellen, Patientendaten, Gegenanzeigen und den endgültigen Plan prüfen.',
        'Exemple pédagogique synthétique. Ne vous traitez pas vous-même : un médecin traitant qualifié doit vérifier les sources, les données du patient, les contre-indications et le plan final.',
    ),
    'Informational tool, not a medical device. All recommendations must be verified by a qualified oncologist. Clinical content is provisional until two-reviewer sign-off.': (
        'Herramienta informativa, no un dispositivo médico. Un oncólogo cualificado debe verificar todas las recomendaciones. El contenido clínico es provisional hasta que lo aprueben dos revisores.',
        'Ferramenta informativa, não um dispositivo médico. Todas as recomendações devem ser verificadas por um oncologista qualificado. O conteúdo clínico é provisório até à aprovação por dois revisores.',
        'Informationsangebot, kein Medizinprodukt. Alle Empfehlungen müssen von einer qualifizierten Onkologin oder einem qualifizierten Onkologen geprüft werden. Die klinischen Inhalte bleiben bis zur Freigabe durch zwei Prüfende vorläufig.',
        'Outil d’information, pas un dispositif médical. Toutes les recommandations doivent être vérifiées par un oncologue qualifié. Le contenu clinique reste provisoire jusqu’à sa validation par deux évaluateurs.',
    ),
    'This document is an informational resource supporting tumor-board discussion (per CHARTER §11). It is not a system that makes clinical decisions. Every recommendation must be verified by the treating physician.': (
        'Este documento es un recurso informativo para apoyar la deliberación del comité de tumores (según CHARTER §11). No es un sistema que tome decisiones clínicas. El médico tratante debe verificar todas las recomendaciones.',
        'Este documento é um recurso informativo para apoiar a discussão na reunião multidisciplinar de oncologia (conforme CHARTER §11). Não é um sistema que toma decisões clínicas. O médico assistente deve verificar todas as recomendações.',
        'Dieses Dokument ist eine Informationsquelle zur Unterstützung der Tumorkonferenz (gemäß CHARTER §11). Es ist kein System, das klinische Entscheidungen trifft. Jede Empfehlung muss von der behandelnden Ärztin oder dem behandelnden Arzt überprüft werden.',
        'Ce document est une ressource d’information destinée à soutenir la discussion en réunion de concertation pluridisciplinaire (conformément à CHARTER §11). Ce n’est pas un système qui prend des décisions cliniques. Chaque recommandation doit être vérifiée par le médecin traitant.',
    ),
    'HCP-mediated prevention / early-diagnosis counseling for at-risk asymptomatic individuals (CHARTER §3 amendment 2026-05-18, Path A). Not a medical device; not for autonomous clinical decision-making; not for patient-direct deployment.': (
        'Orientación sobre prevención y diagnóstico precoz, mediada por profesionales sanitarios (HCP), para personas asintomáticas en riesgo (enmienda de CHARTER §3 del 2026-05-18, vía A). No es un dispositivo médico; no está destinada a tomar decisiones clínicas de forma autónoma; no está destinada a su uso directo por pacientes.',
        'Aconselhamento em prevenção e diagnóstico precoce, mediado por profissionais de saúde (HCP), para pessoas assintomáticas em risco (adenda à CHARTER §3 de 2026-05-18, Via A). Não é um dispositivo médico; não se destina à tomada autónoma de decisões clínicas; não se destina à disponibilização direta aos doentes.',
        'Durch medizinisches Fachpersonal (HCP) vermittelte Beratung zu Prävention und Früherkennung für asymptomatische Risikopersonen (Änderung von CHARTER §3 vom 2026-05-18, Pfad A). Kein Medizinprodukt; nicht für autonome klinische Entscheidungen bestimmt; nicht zur direkten Bereitstellung an Patientinnen und Patienten bestimmt.',
        'Conseil en prévention et diagnostic précoce assuré par un professionnel de santé (HCP) pour les personnes asymptomatiques à risque (amendement à CHARTER §3 du 2026-05-18, voie A). Ce n’est pas un dispositif médical ; il n’est pas destiné à la prise de décisions cliniques autonomes ; il n’est pas destiné à un déploiement direct auprès des patients.',
    ),
}


def safety_notices_for(locale):
    if locale in ('it', 'da', 'sv', 'nb', 'fi'):
        catalog = messages_for(locale)
        return {source: catalog.get(source, source) for source in SAFETY_NOTICES}
    index = ('es', 'pt', 'de', 'fr').index(locale)
    return {source: translations[index] for source, translations in SAFETY_NOTICES.items()}

UI_MESSAGES = {
    'Solo project. One maintainer delivers updates with automated checks and source traceability. External clinical review is optional and is recorded separately.': (
        'Proyecto individual. Una persona responsable publica las actualizaciones con comprobaciones automáticas y trazabilidad de las fuentes. La revisión clínica externa es opcional y se registra por separado.',
        'Projeto individual. Uma pessoa responsável publica as atualizações com verificações automáticas e rastreabilidade das fontes. A revisão clínica externa é opcional e registada separadamente.',
        'Einzelprojekt. Eine verantwortliche Person veröffentlicht Aktualisierungen mit automatisierten Prüfungen und nachvollziehbaren Quellen. Externe klinische Prüfungen sind optional und werden gesondert dokumentiert.',
        'Projet individuel. Une personne responsable publie les mises à jour avec des contrôles automatisés et des sources traçables. La relecture clinique externe est facultative et consignée séparément.',
    ),
    'Clinical content is informational; technical checks are not treatment approval.': (
        'El contenido clínico es informativo; las comprobaciones técnicas no constituyen una aprobación del tratamiento.',
        'O conteúdo clínico é informativo; as verificações técnicas não constituem uma aprovação do tratamento.',
        'Klinische Inhalte dienen der Information; technische Prüfungen sind keine Freigabe einer Behandlung.',
        'Le contenu clinique est informatif ; les contrôles techniques ne constituent pas une approbation du traitement.',
    ),
    "Only current independent content reviews by authorized reviewers are counted; this is not approval of a patient's treatment.": (
        'Solo se cuentan las revisiones actuales e independientes del contenido realizadas por revisores autorizados; esto no constituye la aprobación del tratamiento de un paciente.',
        'Só são contabilizadas as revisões atuais e independentes do conteúdo por revisores autorizados; isto não constitui a aprovação do tratamento de um doente.',
        'Gezählt werden nur aktuelle, unabhängige Inhaltsprüfungen durch autorisierte Prüfende; dies ist keine Freigabe der Behandlung eines Patienten.',
        'Seules les relectures actuelles et indépendantes du contenu par des relecteurs autorisés sont comptées ; cela ne constitue pas une approbation du traitement d’un patient.',
    ),
    'Clinical content review pending': ('Revisión del contenido clínico pendiente', 'Revisão do conteúdo clínico pendente', 'Prüfung des klinischen Inhalts ausstehend', 'Vérification du contenu clinique en attente'),
    'Clinical content review pending (1 of 2 eligible reviews recorded)': ('Revisión del contenido clínico pendiente (1 de 2 revisiones admisibles registrada)', 'Revisão do conteúdo clínico pendente (1 de 2 revisões admissíveis registada)', 'Prüfung des klinischen Inhalts ausstehend (1 von 2 zulässigen Prüfungen dokumentiert)', 'Vérification du contenu clinique en attente (1 des 2 relectures recevables enregistrée)'),
    'Required clinical-content reviews recorded': ('Revisiones requeridas del contenido clínico registradas', 'Revisões necessárias do conteúdo clínico registadas', 'Erforderliche Prüfungen des klinischen Inhalts dokumentiert', 'Relectures requises du contenu clinique enregistrées'),
    'This status describes reviews of the knowledge-base content, not approval of a plan for you.': ('Este estado describe revisiones del contenido de la base de conocimientos, no la aprobación de un plan para usted.', 'Este estado descreve revisões do conteúdo da base de conhecimento, não a aprovação de um plano para si.', 'Dieser Status beschreibt Prüfungen des Inhalts der Wissensbasis, keine Freigabe eines Plans für Sie.', 'Ce statut décrit les relectures du contenu de la base de connaissances, pas l’approbation d’un plan pour vous.'),
    'Required biomarker information is missing from the profile. Review of the main option in this report is incomplete.': ('Falta información necesaria sobre biomarcadores en el perfil. La revisión de la opción principal en este informe está incompleta.', 'Falta informação necessária sobre biomarcadores no perfil. A análise da opção principal neste relatório está incompleta.', 'Im Profil fehlen erforderliche Informationen zu Biomarkern. Die Beurteilung der Hauptoption in diesem Bericht ist unvollständig.', 'Des informations nécessaires sur les biomarqueurs manquent dans le profil. L’examen de l’option principale dans ce rapport est incomplet.'),
    'Biomarker gaps for the main option in this report': ('Datos de biomarcadores que faltan para la opción principal en este informe', 'Dados de biomarcadores em falta para a opção principal neste relatório', 'Fehlende Biomarker-Daten für die Hauptoption in diesem Bericht', 'Données de biomarqueurs manquantes pour l’option principale dans ce rapport'),
    'Option in this report': ('Opción en este informe', 'Opção neste relatório', 'Option in diesem Bericht', 'Option dans ce rapport'),
    'A) Main option in this report': ('A) Opción principal en este informe', 'A) Opção principal neste relatório', 'A) Hauptoption in diesem Bericht', 'A) Option principale dans ce rapport'),
    'B) Main option in this report': ('B) Opción principal en este informe', 'B) Opção principal neste relatório', 'B) Hauptoption in diesem Bericht', 'B) Option principale dans ce rapport'),
    'A) Alternative option in this report': ('A) Opción alternativa en este informe', 'A) Opção alternativa neste relatório', 'A) Alternative Option in diesem Bericht', 'A) Autre option dans ce rapport'),
    'B) Alternative option in this report': ('B) Opción alternativa en este informe', 'B) Opção alternativa neste relatório', 'B) Alternative Option in diesem Bericht', 'B) Autre option dans ce rapport'),
    'Signals recorded in this report — not reasons for selecting every option.': (
        'Señales registradas en este informe; no son motivos para seleccionar todas las opciones.',
        'Sinais registados neste relatório; não são motivos para selecionar todas as opções.',
        'In diesem Bericht aufgezeichnete Signale; keine Gründe für die Auswahl jeder Option.',
        'Signaux enregistrés dans ce rapport ; ce ne sont pas des motifs de sélection de chaque option.',
    ),
    'Recorded signal (original source text):': (
        'Señal registrada (texto original de la fuente):',
        'Sinal registado (texto original da fonte):',
        'Aufgezeichnetes Signal (Originaltext der Quelle):',
        'Signal enregistré (texte original de la source) :',
    ),
    'A signal was recorded, but its explanation is unavailable. See the technical report.': (
        'Se registró una señal, pero su explicación no está disponible. Consulte el informe técnico.',
        'Foi registado um sinal, mas a sua explicação não está disponível. Consulte o relatório técnico.',
        'Ein Signal wurde aufgezeichnet, aber seine Erklärung ist nicht verfügbar. Siehe den technischen Bericht.',
        'Un signal a été enregistré, mais son explication est indisponible. Consultez le rapport technique.',
    ),
    'Report-wide finding — not a reason for selecting an option.': (
        'Hallazgo general del informe; no es un motivo para seleccionar una opción.',
        'Achado geral do relatório; não é um motivo para selecionar uma opção.',
        'Befund des gesamten Berichts; kein Grund für die Auswahl einer Option.',
        'Constat général du rapport ; ce n’est pas un motif de sélection d’une option.',
    ),
    'This report does not record an algorithm path selecting this option. Ask your doctor to review the technical report and its suitability for you.': (
        'Este informe no registra una ruta del algoritmo que seleccione esta opción. Pida a su médico que revise el informe técnico y si esta opción es adecuada para usted.',
        'Este relatório não regista um percurso do algoritmo que selecione esta opção. Peça ao seu médico que reveja o relatório técnico e se esta opção é adequada para si.',
        'Dieser Bericht enthält keinen aufgezeichneten Algorithmuspfad, der diese Option auswählt. Bitten Sie Ihre Ärztin oder Ihren Arzt, den technischen Bericht zu prüfen und zu beurteilen, ob diese Option für Sie geeignet ist.',
        'Ce rapport ne contient pas de parcours enregistré de l’algorithme sélectionnant cette option. Demandez à votre médecin d’examiner le rapport technique et si cette option vous convient.',
    ),
    'The recorded algorithm path selected this option. This does not establish its suitability for you.': (
        'La ruta registrada del algoritmo seleccionó esta opción. Esto no demuestra que sea adecuada para usted.',
        'O percurso registado do algoritmo selecionou esta opção. Isto não demonstra que seja adequada para si.',
        'Der aufgezeichnete Algorithmuspfad hat diese Option ausgewählt. Dies bestätigt nicht, dass sie für Sie geeignet ist.',
        'Le parcours enregistré de l’algorithme a sélectionné cette option. Cela ne confirme pas qu’elle vous convient.',
    ),
    'No red flags were recorded as triggered on that path. This does not rule out risks or replace assessment by your doctor.': (
        'No se registraron señales de alarma activadas en esa ruta. Esto no descarta riesgos ni sustituye la evaluación de su médico.',
        'Não foram registados sinais de alerta ativados nesse percurso. Isto não exclui riscos nem substitui a avaliação pelo seu médico.',
        'Auf diesem Pfad wurden keine ausgelösten Warnsignale aufgezeichnet. Dies schließt Risiken nicht aus und ersetzt keine ärztliche Beurteilung.',
        'Aucun signal d’alerte déclenché n’a été enregistré sur ce parcours. Cela n’exclut pas les risques et ne remplace pas l’évaluation par votre médecin.',
    ),
    'Clinical review of this biomarker record is pending.': (
        'La revisión clínica de este registro de biomarcador está pendiente.',
        'A revisão clínica deste registo de biomarcador está pendente.',
        'Die klinische Prüfung dieses Biomarker-Eintrags steht noch aus.',
        'La vérification clinique de cette entrée de biomarqueur est en attente.',
    ),
    'Original Ukrainian explanation; translation unavailable:': ('Explicación original en ucraniano; traducción no disponible:', 'Explicação original em ucraniano; tradução indisponível:', 'Ukrainische Originalerläuterung; Übersetzung nicht verfügbar:', 'Explication originale en ukrainien ; traduction indisponible :'),
    'Original source explanation; translation unavailable:': ('Explicación de la fuente original; traducción no disponible:', 'Explicação da fonte original; tradução indisponível:', 'Erläuterung aus der Originalquelle; Übersetzung nicht verfügbar:', 'Explication de la source originale ; traduction indisponible :'),
    'Original Ukrainian text; translation unavailable:': ('Texto original en ucraniano; traducción no disponible:', 'Texto original em ucraniano; tradução indisponível:', 'Ukrainischer Originaltext; Übersetzung nicht verfügbar:', 'Texte original en ukrainien ; traduction indisponible :'),
    '🚨 Original Ukrainian text; translation unavailable:': ('🚨 Texto original en ucraniano; traducción no disponible:', '🚨 Texto original em ucraniano; tradução indisponível:', '🚨 Ukrainischer Originaltext; Übersetzung nicht verfügbar:', '🚨 Texte original en ukrainien ; traduction indisponible :'),
    'The algorithm recorded (original Ukrainian text; translation unavailable):': ('El algoritmo registró (texto original en ucraniano; traducción no disponible):', 'O algoritmo registou (texto original em ucraniano; tradução indisponível):', 'Der Algorithmus hat erfasst (ukrainischer Originaltext; Übersetzung nicht verfügbar):', 'L’algorithme a enregistré (texte original en ukrainien ; traduction indisponible) :'),
    'Duration (original source text):': ('Duración (texto de la fuente original):', 'Duração (texto da fonte original):', 'Dauer (Text aus der Originalquelle):', 'Durée (texte de la source originale) :'),
    'Information to clarify with your doctor': ('Información que debe aclarar con su médico', 'Informação a esclarecer com o seu médico', 'Informationen, die Sie mit Ihrer Ärztin oder Ihrem Arzt klären sollten', 'Informations à clarifier avec votre médecin'),
    'The recorded data checks are complete. This does not mean that treatment has been approved.': ('Las comprobaciones de los datos registrados están completas. Esto no significa que el tratamiento haya sido aprobado.', 'As verificações dos dados registados estão concluídas. Isto não significa que o tratamento tenha sido aprovado.', 'Die Prüfungen der erfassten Daten sind abgeschlossen. Das bedeutet nicht, dass die Behandlung genehmigt wurde.', 'Les vérifications des données enregistrées sont terminées. Cela ne signifie pas que le traitement a été approuvé.'),
    'Some data or checks need clarification before your doctor reviews this report.': ('Algunos datos o comprobaciones necesitan aclaración antes de que su médico revise este informe.', 'Alguns dados ou verificações precisam de esclarecimento antes de o seu médico analisar este relatório.', 'Einige Daten oder Prüfungen müssen geklärt werden, bevor Ihre Ärztin oder Ihr Arzt diesen Bericht beurteilt.', 'Certaines données ou vérifications doivent être clarifiées avant que votre médecin examine ce rapport.'),
    'Important information is missing from the profile. Your doctor needs to clarify it when reviewing this report.': ('Falta información importante en el perfil. Su médico debe aclararla al revisar este informe.', 'Falta informação importante no perfil. O seu médico deve esclarecê-la ao analisar este relatório.', 'Im Profil fehlen wichtige Informationen. Ihre Ärztin oder Ihr Arzt muss diese bei der Beurteilung dieses Berichts klären.', 'Des informations importantes manquent dans le profil. Votre médecin doit les clarifier lors de l’examen de ce rapport.'),
    'Required biomarker information is missing from the profile. Review of the standard option is incomplete.': ('Falta información necesaria sobre biomarcadores en el perfil. La revisión de la opción estándar está incompleta.', 'Falta informação necessária sobre biomarcadores no perfil. A análise da opção padrão está incompleta.', 'Im Profil fehlen erforderliche Informationen zu Biomarkern. Die Beurteilung der Standardoption ist unvollständig.', 'Des informations nécessaires sur les biomarqueurs manquent dans le profil. L’examen de l’option standard est incomplet.'),
    'Data completeness has not been assessed in this report.': ('La integridad de los datos no se ha evaluado en este informe.', 'A completude dos dados não foi avaliada neste relatório.', 'Die Vollständigkeit der Daten wurde in diesem Bericht nicht beurteilt.', 'L’exhaustivité des données n’a pas été évaluée dans ce rapport.'),
    'Missing from the profile does not mean a test was not performed. Ask your doctor which results to add or verify. Do not change treatment based only on this report.': ('Que un dato falte en el perfil no significa que la prueba no se haya realizado. Pregunte a su médico qué resultados debe añadir o verificar. No cambie el tratamiento basándose únicamente en este informe.', 'A ausência de dados no perfil não significa que um exame não tenha sido realizado. Pergunte ao seu médico quais os resultados a acrescentar ou verificar. Não altere o tratamento apenas com base neste relatório.', 'Fehlende Angaben im Profil bedeuten nicht, dass eine Untersuchung nicht durchgeführt wurde. Fragen Sie Ihre Ärztin oder Ihren Arzt, welche Ergebnisse ergänzt oder überprüft werden sollten. Ändern Sie die Behandlung nicht allein aufgrund dieses Berichts.', 'L’absence de données dans le profil ne signifie pas qu’un examen n’a pas été réalisé. Demandez à votre médecin quels résultats ajouter ou vérifier. Ne modifiez pas le traitement sur la seule base de ce rapport.'),
    'Important clinical information missing': ('Información clínica importante que falta', 'Informação clínica importante em falta', 'Fehlende wichtige klinische Informationen', 'Informations cliniques importantes manquantes'),
    'Additional information to clarify': ('Información adicional que debe aclararse', 'Informação adicional a esclarecer', 'Weitere zu klärende Informationen', 'Informations supplémentaires à clarifier'),
    'Conditions the system could not evaluate': ('Condiciones que el sistema no pudo evaluar', 'Condições que o sistema não conseguiu avaliar', 'Bedingungen, die das System nicht beurteilen konnte', 'Conditions que le système n’a pas pu évaluer'),
    'Required biomarker results missing': ('Resultados necesarios de biomarcadores que faltan', 'Resultados necessários de biomarcadores em falta', 'Fehlende erforderliche Biomarker-Ergebnisse', 'Résultats nécessaires de biomarqueurs manquants'),
    'Biomarker gaps for the standard option': ('Datos de biomarcadores que faltan para la opción estándar', 'Dados de biomarcadores em falta para a opção padrão', 'Fehlende Biomarker-Daten für die Standardoption', 'Données de biomarqueurs manquantes pour l’option standard'),
    'Missing information recorded in the profile': ('Información que consta como ausente en el perfil', 'Informação assinalada como ausente no perfil', 'Im Profil als fehlend erfasste Informationen', 'Informations indiquées comme manquantes dans le profil'),
    'Your oncology plan': ('Su plan oncológico', 'O seu plano oncológico', 'Ihr onkologischer Plan', 'Votre plan oncologique'),
    'What was found': ('Qué se ha encontrado', 'O que foi encontrado', 'Was festgestellt wurde', 'Ce qui a été trouvé'),
    'What this means for treatment': ('Qué significa esto para el tratamiento', 'O que isto significa para o tratamento', 'Was dies für die Behandlung bedeutet', 'Ce que cela signifie pour le traitement'),
    'Technical version for your doctor →': ('Versión técnica para su médico →', 'Versão técnica para o seu médico →', 'Fachliche Version für Ihre Ärztin oder Ihren Arzt →', 'Version technique pour votre médecin →'),
    'English translation draft — incomplete and awaiting clinical/language review. Some explanations remain in their original language and are marked. Consult the original report and your doctor.': (
        'Borrador de traducción al inglés: incompleto y pendiente de revisión clínica y lingüística. Algunas explicaciones se conservan en su idioma original y están marcadas. Consulte el informe original y a su médico.',
        'Tradução preliminar para inglês: incompleta e a aguardar revisão clínica e linguística. Algumas explicações permanecem no idioma original e estão assinaladas. Consulte o relatório original e o seu médico.',
        'Englischer Übersetzungsentwurf: unvollständig und noch klinisch und sprachlich zu prüfen. Einige Erläuterungen bleiben in ihrer Originalsprache und sind gekennzeichnet. Lesen Sie den Originalbericht und sprechen Sie mit Ihrer Ärztin oder Ihrem Arzt.',
        'Traduction provisoire en anglais : incomplète et en attente de vérification clinique et linguistique. Certaines explications restent dans leur langue d’origine et sont signalées. Consultez le rapport original et votre médecin.',
    ),
    'Interpretation requires clinical review': (
        'La interpretación requiere revisión clínica',
        'A interpretação requer revisão clínica',
        'Die Interpretation erfordert eine klinische Prüfung',
        'L’interprétation nécessite une vérification clinique',
    ),
    'Regimen': ('Esquema terapéutico', 'Esquema terapêutico', 'Therapieschema', 'Protocole thérapeutique'),
    'Regimens': ('Esquemas terapéuticos', 'Esquemas terapêuticos', 'Therapieschemata', 'Protocoles thérapeutiques'),
    'Red flag': ('Señal de alerta', 'Sinal de alerta', 'Warnhinweis', 'Signal d’alerte'),
    'Red flags': ('Señales de alerta', 'Sinais de alerta', 'Warnhinweise', 'Signaux d’alerte'),
    'Drug': ('Fármaco', 'Fármaco', 'Arzneimittel', 'Médicament'),
    'Drugs': ('Fármacos', 'Fármacos', 'Arzneimittel', 'Médicaments'),
    'Disease': ('Enfermedad', 'Doença', 'Erkrankung', 'Maladie'),
    'Diseases': ('Enfermedades', 'Doenças', 'Erkrankungen', 'Maladies'),
    'Biomarker': ('Biomarcador', 'Biomarcador', 'Biomarker', 'Biomarqueur'),
    'Actionability': ('Relevancia terapéutica', 'Relevância terapêutica', 'Therapeutische Relevanz', 'Pertinence thérapeutique'),
    'Male': ('Masculino', 'Masculino', 'Männlich', 'Masculin'),
    'Female': ('Femenino', 'Feminino', 'Weiblich', 'Féminin'),
    'Evidence': ('Evidencia', 'Evidência', 'Evidenz', 'Données probantes'),
    'Pregnancy': ('Embarazo', 'Gravidez', 'Schwangerschaft', 'Grossesse'),
    'Histology': ('Histología', 'Histologia', 'Histologie', 'Histologie'),
    'Biomarkers': ('Biomarcadores', 'Biomarcadores', 'Biomarker', 'Biomarqueurs'),
    'Model answer revealed': ('Respuesta orientativa mostrada', 'Resposta modelo apresentada', 'Musterantwort angezeigt', 'Réponse type affichée'),
    '✗ Not yet — see explanation': ('✗ Todavía no — consulte la explicación', '✗ Ainda não — consulte a explicação', '✗ Noch nicht — siehe Erklärung', '✗ Pas encore — voir l’explication'),
    '(no matching diseases)': ('(sin enfermedades coincidentes)', '(sem doenças correspondentes)', '(keine passenden Erkrankungen)', '(aucune maladie correspondante)'),
    '(no examples for this disease yet)': ('(aún no hay ejemplos para esta enfermedad)', '(ainda não há exemplos para esta doença)', '(noch keine Beispiele für diese Erkrankung)', '(aucun exemple pour cette maladie actuellement)'),
    'Options:': ('Opciones:', 'Opções:', 'Optionen:', 'Options :'),
    'Rationale:': ('Justificación:', 'Fundamentação:', 'Begründung:', 'Justification :'),
    'Clarifying questions:': ('Preguntas aclaratorias:', 'Perguntas de esclarecimento:', 'Rückfragen:', 'Questions de clarification :'),
    'Engine limitations:': ('Limitaciones del motor:', 'Limitações do motor:', 'Einschränkungen der Engine:', 'Limites du moteur :'),
    'OpenOnco': ('OpenOnco', 'OpenOnco', 'OpenOnco', 'OpenOnco'),
    'Plan Builder': ('Generador de planes', 'Gerador de planos', 'Plan erstellen', 'Générateur de plans'),
    'OpenOnco · Plan Builder': ('OpenOnco · Generador de planes', 'OpenOnco · Gerador de planos', 'OpenOnco · Plan erstellen', 'OpenOnco · Générateur de plans'),
    'Filter diseases': ('Filtrar enfermedades', 'Filtrar doenças', 'Erkrankungen filtern', 'Filtrer les maladies'),
    'Filter examples': ('Filtrar ejemplos', 'Filtrar exemplos', 'Beispiele filtern', 'Filtrer les exemples'),
    '— select —': ('— seleccionar —', '— selecionar —', '— auswählen —', '— sélectionner —'),
    '— select an example —': ('— seleccionar un ejemplo —', '— selecionar um exemplo —', '— Beispiel auswählen —', '— sélectionner un exemple —'),
    '— select an example for this disease —': ('— seleccionar un ejemplo para esta enfermedad —', '— selecionar um exemplo para esta doença —', '— Beispiel für diese Erkrankung auswählen —', '— sélectionner un exemple pour cette maladie —'),
    'first line': ('primera línea', 'primeira linha', 'Erstlinie', 'première ligne'),
    'newly diagnosed (1L)': ('diagnóstico reciente (1L)', 'diagnóstico recente (1L)', 'neu diagnostiziert (1L)', 'nouvellement diagnostiqué (1L)'),
    'Curated showcase': ('Ejemplo seleccionado', 'Exemplo selecionado', 'Ausgewähltes Beispiel', 'Exemple sélectionné'),
    'Curated plan': ('Plan seleccionado', 'Plano selecionado', 'Ausgewählter Plan', 'Plan sélectionné'),
    'Diagnostic brief': ('Resumen diagnóstico', 'Resumo diagnóstico', 'Diagnostische Übersicht', 'Résumé diagnostique'),
    'Molecular decision example': ('Ejemplo de razonamiento molecular', 'Exemplo de raciocínio molecular', 'Beispiel zur molekularen Entscheidungsfindung', 'Exemple de raisonnement moléculaire'),
    'JSON profile': ('Perfil JSON', 'Perfil JSON', 'JSON-Profil', 'Profil JSON'),
    'Raw JSON (advanced)': ('JSON sin procesar (avanzado)', 'JSON em bruto (avançado)', 'Rohes JSON (erweitert)', 'JSON brut (avancé)'),
    'QUESTIONNAIRE READINESS': ('ESTADO DEL CUESTIONARIO', 'ESTADO DO QUESTIONÁRIO', 'STATUS DES FRAGEBOGENS', 'ÉTAT DU QUESTIONNAIRE'),
    'Questionnaire readiness': ('Estado del cuestionario', 'Estado do questionário', 'Status des Fragebogens', 'État du questionnaire'),
    'Pick a disease to start.': ('Seleccione una enfermedad para empezar.', 'Selecione uma doença para começar.', 'Wählen Sie zunächst eine Erkrankung aus.', 'Choisissez une maladie pour commencer.'),
    'Pick a disease from the list above to start the questionnaire.': ('Seleccione una enfermedad en la lista para iniciar el cuestionario.', 'Selecione uma doença na lista para iniciar o questionário.', 'Wählen Sie eine Erkrankung aus der Liste, um den Fragebogen zu starten.', 'Choisissez une maladie dans la liste pour commencer le questionnaire.'),
    'Pick a disease from the list to start.': ('Seleccione una enfermedad en la lista para empezar.', 'Selecione uma doença na lista para começar.', 'Wählen Sie zunächst eine Erkrankung aus der Liste.', 'Choisissez une maladie dans la liste pour commencer.'),
    'Personalise this example': ('Personalizar este ejemplo', 'Personalizar este exemplo', 'Beispiel anpassen', 'Personnaliser cet exemple'),
    'Show plan': ('Mostrar el plan', 'Mostrar o plano', 'Plan anzeigen', 'Afficher le plan'),
    'Share with your doctor · PDF': ('Compartir con su médico · PDF', 'Partilhar com o seu médico · PDF', 'Mit Ihrer Ärztin oder Ihrem Arzt teilen · PDF', 'Partager avec votre médecin · PDF'),
    'Save as PDF via your browser print dialog': ('Guardar como PDF mediante la impresión del navegador', 'Guardar como PDF através da impressão do navegador', 'Über den Druckdialog des Browsers als PDF speichern', 'Enregistrer en PDF avec la fonction d’impression du navigateur'),
    'No real patient data.': ('No incluya datos reales de pacientes.', 'Não inclua dados reais de doentes.', 'Keine echten Patientendaten eingeben.', 'N’incluez aucune donnée réelle de patient.'),
    'Drafts are stored in your browser localStorage.': ('Los borradores se guardan en este navegador.', 'Os rascunhos são guardados neste navegador.', 'Entwürfe werden in diesem Browser gespeichert.', 'Les brouillons sont enregistrés dans ce navigateur.'),
    'Online': ('En línea', 'Com ligação', 'Online', 'En ligne'),
    'Offline': ('Sin conexión', 'Sem ligação', 'Offline', 'Hors ligne'),
    'Service worker active': ('Caché del navegador activa', 'Cache do navegador ativa', 'Browser-Cache aktiv', 'Cache du navigateur actif'),
    'Clinician': ('Profesional sanitario', 'Profissional de saúde', 'Fachpersonal', 'Professionnel de santé'),
    'Build': ('Versión del motor', 'Versão do motor', 'Engine-Version', 'Version du moteur'),
    'BROWSER': ('NAVEGADOR', 'NAVEGADOR', 'BROWSER', 'NAVIGATEUR'),
    'OFFLINE': ('SIN CONEXIÓN', 'SEM LIGAÇÃO', 'OFFLINE', 'HORS LIGNE'),
    'Ready offline': ('Disponible sin conexión', 'Disponível sem ligação', 'Offline verfügbar', 'Disponible hors ligne'),
    'Open an issue': ('Informar de un problema', 'Comunicar um problema', 'Problem melden', 'Signaler un problème'),
    'Something not working?': ('¿Algo no funciona?', 'Algo não funciona?', 'Funktioniert etwas nicht?', 'Un problème ?'),
    'Stage': ('Estadio', 'Estádio', 'Stadium', 'Stade'),
    'Staging': ('Estadificación', 'Estadiamento', 'Stadieneinteilung', 'Stadification'),
    'Performance status': ('Estado funcional', 'Estado funcional', 'Allgemeinzustand', 'État général'),
    'Build a cited treatment-plan draft from a virtual patient profile. The in-browser engine shows which diagnosis, staging, biomarker and safety fields change the plan.': (
        'Prepare un borrador de plan de tratamiento con referencias a partir del perfil de un paciente virtual. El motor del navegador muestra qué campos del diagnóstico, estadificación, biomarcadores y seguridad modifican el plan.',
        'Crie um rascunho de plano de tratamento com referências a partir do perfil de um doente virtual. O motor no navegador mostra quais os campos de diagnóstico, estadiamento, biomarcadores e segurança que alteram o plano.',
        'Erstellen Sie anhand eines virtuellen Patientenprofils einen mit Quellen belegten Entwurf eines Behandlungsplans. Die Engine im Browser zeigt, welche Angaben zu Diagnose, Stadieneinteilung, Biomarkern und Sicherheit den Plan verändern.',
        'Préparez un brouillon de plan de traitement référencé à partir du profil d’un patient virtuel. Le moteur dans le navigateur montre quels champs de diagnostic, de stadification, de biomarqueurs et de sécurité modifient le plan.',
    ),
}

DISEASE_TITLES = {
    'Small cell lung cancer': ('Cáncer de pulmón de células pequeñas', 'Cancro do pulmão de pequenas células', 'Kleinzelliges Lungenkarzinom', 'Cancer bronchique à petites cellules'),
    'Diffuse Large B-Cell Lymphoma, Not Otherwise Specified': ('Linfoma difuso de células B grandes, sin otra especificación', 'Linfoma difuso de grandes células B, sem outra especificação', 'Diffuses großzelliges B-Zell-Lymphom, nicht näher spezifiziert', 'Lymphome diffus à grandes cellules B, sans autre précision'),
    'Adult T-Cell Leukemia/Lymphoma': ('Leucemia/linfoma de células T del adulto', 'Leucemia/linfoma de células T do adulto', 'Adulte T-Zell-Leukämie/Lymphom', 'Leucémie/lymphome T de l’adulte'),
    'Chondrosarcoma': ('Condrosarcoma', 'Condrossarcoma', 'Chondrosarkom', 'Chondrosarcome'),
    'Lymphangioleiomyomatosis': ('Linfangioleiomiomatosis', 'Linfangioleiomiomatose', 'Lymphangioleiomyomatose', 'Lymphangioléiomyomatose'),
    'Gastrointestinal stromal tumor': ('Tumor del estroma gastrointestinal', 'Tumor do estroma gastrointestinal', 'Gastrointestinaler Stromatumor', 'Tumeur stromale gastro-intestinale'),
    'High-Grade B-Cell Lymphoma, Double-Hit / Triple-Hit': ('Linfoma de células B de alto grado, double-hit / triple-hit', 'Linfoma de células B de alto grau, double-hit / triple-hit', 'Hochgradiges B-Zell-Lymphom, Double-Hit / Triple-Hit', 'Lymphome B de haut grade, double-hit / triple-hit'),
    'Low-grade glioma': ('Glioma de bajo grado', 'Glioma de baixo grau', 'Niedriggradiges Gliom', 'Gliome de bas grade'),
    'Invasive breast cancer': ('Cáncer de mama invasivo', 'Cancro da mama invasivo', 'Invasives Mammakarzinom', 'Cancer du sein invasif'),
    'Prostate adenocarcinoma': ('Adenocarcinoma de próstata', 'Adenocarcinoma da próstata', 'Adenokarzinom der Prostata', 'Adénocarcinome de la prostate'),
    'Pancreatic ductal adenocarcinoma': ('Adenocarcinoma ductal de páncreas', 'Adenocarcinoma ductal do pâncreas', 'Duktales Adenokarzinom des Pankreas', 'Adénocarcinome canalaire du pancréas'),
    'Ovarian carcinoma': ('Carcinoma de ovario', 'Carcinoma do ovário', 'Ovarialkarzinom', 'Carcinome ovarien'),
}

SHOWCASE_TITLES = {
    'AML - FLT3-ITD - heme actionability and risk': ('AML - FLT3-ITD - relevancia terapéutica y riesgo hematológicos', 'AML - FLT3-ITD - relevância terapêutica e risco hematológicos', 'AML - FLT3-ITD - hämatologische therapeutische Relevanz und Risiko', 'AML - FLT3-ITD - pertinence thérapeutique et risque hématologiques'),
    'BCC - locally advanced - hedgehog inhibitor 1L': ('BCC - localmente avanzado - inhibidor de Hedgehog 1L', 'BCC - localmente avançado - inibidor de Hedgehog 1L', 'BCC - lokal fortgeschritten - Hedgehog-Inhibitor 1L', 'BCC - localement avancé - inhibiteur de Hedgehog 1L'),
    'Breast HR+/HER2- - PIK3CA H1047R - post-CDK4/6i': ('Mama HR+/HER2- - PIK3CA H1047R - después de CDK4/6i', 'Mama HR+/HER2- - PIK3CA H1047R - após CDK4/6i', 'Brust HR+/HER2- - PIK3CA H1047R - nach CDK4/6i', 'Sein HR+/HER2- - PIK3CA H1047R - après CDK4/6i'),
    'Cervical · Locally Advanced (CCRT + Pembrolizumab)': ('Cuello uterino · Localmente avanzado (CCRT + Pembrolizumab)', 'Colo do útero · Localmente avançado (CCRT + Pembrolizumab)', 'Zervix · Lokal fortgeschritten (CCRT + Pembrolizumab)', 'Col de l’utérus · Localement avancé (CCRT + Pembrolizumab)'),
    'Cholangiocarcinoma - IDH1 R132 - 2L molecular option': ('Colangiocarcinoma - IDH1 R132 - opción molecular 2L', 'Colangiocarcinoma - IDH1 R132 - opção molecular 2L', 'Cholangiokarzinom - IDH1 R132 - molekulare Option 2L', 'Cholangiocarcinome - IDH1 R132 - option moléculaire 2L'),
    'Endometrial - dMMR/MSH2 - immunotherapy evidence': ('Endometrio - dMMR/MSH2 - evidencia de inmunoterapia', 'Endométrio - dMMR/MSH2 - evidência de imunoterapia', 'Endometrium - dMMR/MSH2 - Evidenz zur Immuntherapie', 'Endomètre - dMMR/MSH2 - données sur l’immunothérapie'),
    'Gastric/GEJ - HER2 amplification - IHC/ISH actionability': ('Gástrico/GEJ - amplificación de HER2 - relevancia terapéutica IHC/ISH', 'Gástrico/GEJ - amplificação de HER2 - relevância terapêutica IHC/ISH', 'Magen/GEJ - HER2-Amplifikation - therapeutische Relevanz IHC/ISH', 'Gastrique/GEJ - amplification de HER2 - pertinence thérapeutique IHC/ISH'),
    'GIST - KIT exon 11 - genotype sets TKI dose': ('GIST - KIT exón 11 - el genotipo determina la dosis de TKI', 'GIST - KIT exão 11 - o genótipo determina a dose de TKI', 'GIST - KIT Exon 11 - Genotyp bestimmt TKI-Dosis', 'GIST - KIT exon 11 - le génotype détermine la dose de TKI'),
    'Infantile fibrosarcoma - NTRK fusion - rare tumor target': ('Fibrosarcoma infantil - fusión NTRK - diana en tumor raro', 'Fibrossarcoma infantil - fusão NTRK - alvo em tumor raro', 'Infantiles Fibrosarkom - NTRK-Fusion - Zielstruktur bei seltenem Tumor', 'Fibrosarcome infantile - fusion NTRK - cible dans une tumeur rare'),
    'mCRC - BRAF V600E - tumor-specific actionability': ('mCRC - BRAF V600E - relevancia terapéutica específica del tumor', 'mCRC - BRAF V600E - relevância terapêutica específica do tumor', 'mCRC - BRAF V600E - tumorspezifische therapeutische Relevanz', 'mCRC - BRAF V600E - pertinence thérapeutique spécifique de la tumeur'),
    'Melanoma - BRAF V600E - targeted vs immunotherapy context': ('Melanoma - BRAF V600E - contexto de terapia dirigida frente a inmunoterapia', 'Melanoma - BRAF V600E - contexto de terapêutica dirigida versus imunoterapia', 'Melanom - BRAF V600E - zielgerichtete Therapie versus Immuntherapie', 'Mélanome - BRAF V600E - contexte thérapie ciblée versus immunothérapie'),
    'NSCLC - acquired EGFR T790M - resistance-aware review': ('NSCLC - EGFR T790M adquirida - revisión que considera la resistencia', 'NSCLC - EGFR T790M adquirida - revisão que considera a resistência', 'NSCLC - erworbene EGFR T790M - Prüfung unter Berücksichtigung der Resistenz', 'NSCLC - EGFR T790M acquise - évaluation tenant compte de la résistance'),
    'NSCLC - ALK fusion - ESCAT IA / CIViC evidence': ('NSCLC - fusión ALK - evidencia ESCAT IA / CIViC', 'NSCLC - fusão ALK - evidência ESCAT IA / CIViC', 'NSCLC - ALK-Fusion - Evidenz ESCAT IA / CIViC', 'NSCLC - fusion ALK - données ESCAT IA / CIViC'),
    'Ovarian - germline BRCA1 - PARPi maintenance': ('Ovario - BRCA1 germinal - mantenimiento con PARPi', 'Ovário - BRCA1 germinal - manutenção com PARPi', 'Ovar - BRCA1-Keimbahn - PARPi-Erhaltung', 'Ovaire - BRCA1 germinale - entretien par PARPi'),
    'mCRPC - germline BRCA2 - PARP/HRR context': ('mCRPC - BRCA2 germinal - contexto PARP/HRR', 'mCRPC - BRCA2 germinal - contexto PARP/HRR', 'mCRPC - BRCA2-Keimbahn - PARP/HRR-Kontext', 'mCRPC - BRCA2 germinale - contexte PARP/HRR'),
    'Papillary thyroid - RET fusion - RAI-refractory target': ('Tiroides papilar - fusión RET - diana refractaria a RAI', 'Tiroide papilar - fusão RET - alvo refratário a RAI', 'Papilläre Schilddrüse - RET-Fusion - Zielstruktur bei RAI-refraktärer Erkrankung', 'Thyroïde papillaire - fusion RET - cible réfractaire à RAI'),
}


def messages_for(locale):
    from scripts.privacy_copy import messages_for as privacy_messages
    if locale in ('it', 'da', 'sv', 'nb', 'fi'):
        import json
        from pathlib import Path
        path = Path(__file__).with_name('locales') / f'curated.{locale}.json'
        catalog = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        # An observed literal Nordic model error corrupted "Colorectal
        # carcinoma". Keep canonical diagnosis names in their source language
        # until an explicit terminology draft is supplied.
        protected = Path(__file__).with_name('locales') / 'additional-diagnosis-originals.json'
        if protected.exists():
            catalog.update({name: name for name in json.loads(protected.read_text(encoding='utf-8'))})
        catalog['✗ Not registered in UA'] = AVAILABILITY_LABELS[locale]
        catalog.update(STAGING_LABELS[locale])
        catalog.update(privacy_messages(locale))
        return catalog
    title = NSCLC[locale]
    status = {
        'es': ['Respuesta preparada', 'Se necesita una aclaración', 'Preparado'],
        'pt': ['Resposta preparada', 'É necessário esclarecer', 'Pronto'],
        'de': ['Antwort bereit', 'Rückfrage erforderlich', 'Bereit'],
        'fr': ['Réponse prête', 'Précisions nécessaires', 'Prêt'],
    }[locale]
    catalog = {
        'Non-small cell lung cancer': title,
        'Non-small cell lung cancer (NSCLC)': title + ' (NSCLC)',
        'Non-small cell lung cancer - OpenOnco': title + ' - OpenOnco',
        'answered': status[0],
        'needs_clarification': status[1],
        'ok': status[2],
    }
    index = ('es', 'pt', 'de', 'fr').index(locale)
    catalog.update({source: values[index] for source, values in UI_MESSAGES.items()})
    review_aliases = {
        'Солопроєкт. Один власник доставляє оновлення з автоматичними перевірками та простежуваними джерелами. Зовнішній клінічний перегляд є додатковим і записується окремо.': 'Solo project. One maintainer delivers updates with automated checks and source traceability. External clinical review is optional and is recorded separately.',
        'Клінічний зміст має інформаційний характер; технічні перевірки не є схваленням лікування.': 'Clinical content is informational; technical checks are not treatment approval.',
        'Рахуються лише актуальні незалежні перегляди змісту від уповноважених рецензентів; це не схвалення лікування пацієнта.': "Only current independent content reviews by authorized reviewers are counted; this is not approval of a patient's treatment.",
        'Перегляд клінічного змісту очікується': 'Clinical content review pending',
        'Перегляд клінічного змісту очікується (записано 1 із 2 допустимих переглядів)': 'Clinical content review pending (1 of 2 eligible reviews recorded)',
        'Записано необхідні перегляди клінічного змісту': 'Required clinical-content reviews recorded',
        'Цей статус описує перегляди змісту бази знань, а не схвалення плану для вас.': 'This status describes reviews of the knowledge-base content, not approval of a plan for you.',
    }
    catalog.update({source: catalog[english] for source, english in review_aliases.items()})
    catalog['Інтерпретація потребує клінічного перегляду'] = catalog['Interpretation requires clinical review']
    catalog.update(safety_notices_for(locale))
    # Static patient examples retain a Ukrainian source body; dynamic
    # English reports use the canonical safety notice above.
    catalog['У цьому звіті немає інтерпретації молекулярних мішеней, пов’язаної з лікуванням. Це не підтверджує, що результати молекулярних аналізів негативні або що мішеней немає. Обговоріть із лікарем оригінали результатів і те, чи потрібне додаткове тестування.'] = catalog['This report contains no molecular-target interpretation linked to treatment. This does not establish that molecular test results are negative or that no targets exist. Ask your doctor to review the original results and whether further testing is appropriate.']
    catalog.update({source: values[index] for source, values in SHOWCASE_TITLES.items()})
    for source, values in DISEASE_TITLES.items():
        catalog[source] = values[index]
        catalog[source + ' - OpenOnco'] = values[index] + ' - OpenOnco'
    if locale == 'fr':
        catalog.update({
            'Diffuse large B-cell lymphoma: first-line reasoning': 'Lymphome diffus à grandes cellules B : raisonnement en première ligne',
            'Metastatic NSCLC: driver-first treatment reasoning': 'NSCLC métastatique : raisonnement thérapeutique fondé d’abord sur les altérations moléculaires',
            'Multiple myeloma: first-line risk and fitness reasoning': 'Myélome multiple : risque et état général en première ligne',
            'Advanced ovarian cancer: HRD/BRCA first-line maintenance reasoning': 'Cancer de l’ovaire avancé : raisonnement sur le traitement d’entretien HRD/BRCA en première ligne',
        })
    catalog['✗ Not registered in UA'] = AVAILABILITY_LABELS[locale]
    catalog.update(privacy_messages(locale))
    return catalog
