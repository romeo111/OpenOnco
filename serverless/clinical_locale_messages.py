"""Curated safety, review and interaction messages; no clinical decisions."""

LANGUAGES = ('es', 'pt', 'de', 'fr')
MESSAGES = {
    'Yes': ('Sí', 'Sim', 'Ja', 'Oui'),
    'No': ('No', 'Não', 'Nein', 'Non'),
    'Unknown': ('Desconocido', 'Desconhecido', 'Unbekannt', 'Inconnu'),
    'Loading…': ('Cargando…', 'A carregar…', 'Wird geladen…', 'Chargement…'),
    'Clinical sign-offs': ('Aprobaciones clínicas', 'Aprovações clínicas', 'Klinische Freigaben', 'Validations cliniques'),
    'No clinical sign-offs recorded yet.': ('Todavía no se ha registrado ninguna aprobación clínica.', 'Ainda não foi registada nenhuma aprovação clínica.', 'Es sind noch keine klinischen Freigaben dokumentiert.', 'Aucune validation clinique n’a encore été enregistrée.'),
    'Clinical review pending': ('Revisión clínica pendiente', 'Revisão clínica pendente', 'Klinische Prüfung ausstehend', 'Vérification clinique en attente'),
    'Not clinically reviewed': ('Sin revisión clínica', 'Sem revisão clínica', 'Nicht klinisch geprüft', 'Non vérifié sur le plan clinique'),
    'Pick an option first.': ('Seleccione primero una opción.', 'Selecione primeiro uma opção.', 'Wählen Sie zunächst eine Antwort aus.', 'Sélectionnez d’abord une réponse.'),
    '✓ Correct': ('✓ Correcto', '✓ Correto', '✓ Richtig', '✓ Correct'),
    'Check answer': ('Comprobar respuesta', 'Verificar resposta', 'Antwort prüfen', 'Vérifier la réponse'),
    'Practice questions': ('Preguntas de práctica', 'Perguntas de prática', 'Übungsfragen', 'Questions d’entraînement'),
    'Plan Builder': ('Constructor de planes', 'Construtor de planos', 'Planerstellung', 'Constructeur de plans'),
    'Handbook': ('Manual', 'Manual', 'Handbuch', 'Manuel'),
    'Source-linked clinical knowledge base': ('Base de conocimientos clínicos con fuentes', 'Base de conhecimentos clínicos com fontes', 'Klinische Wissensbasis mit Quellen', 'Base de connaissances cliniques avec sources'),
    'Internal tandem duplication (ITD)': ('Duplicación interna en tándem (ITD)', 'Duplicação interna em tandem (ITD)', 'Interne Tandemduplikation (ITD)', 'Duplication interne en tandem (ITD)'),
    'FLT3 internal tandem duplication (ITD)': ('Duplicación interna en tándem de FLT3 (ITD)', 'Duplicação interna em tandem de FLT3 (ITD)', 'Interne Tandemduplikation von FLT3 (ITD)', 'Duplication interne en tandem de FLT3 (ITD)'),
    'Acute Myeloid Leukemia': ('Leucemia mieloide aguda', 'Leucemia mieloide aguda', 'Akute myeloische Leukämie', 'Leucémie aiguë myéloïde'),
    'Diffuse Large B-Cell Lymphoma': ('Linfoma difuso de células B grandes', 'Linfoma difuso de grandes células B', 'Diffuses großzelliges B-Zell-Lymphom', 'Lymphome diffus à grandes cellules B'),
    'Review status': ('Estado de revisión', 'Estado da revisão', 'Prüfstatus', 'Statut de révision'),
    'Correct answer:': ('Respuesta correcta:', 'Resposta correta:', 'Richtige Antwort:', 'Réponse correcte :'),
    'ESCAT: clinical review pending': ('ESCAT: revisión clínica pendiente', 'ESCAT: revisão clínica pendente', 'ESCAT: klinische Prüfung ausstehend', 'ESCAT : vérification clinique en attente'),
    'Надішліть клінічну ситуацію текстом.': ('Envíe el caso clínico en texto.', 'Envie o caso clínico por escrito.', 'Senden Sie den klinischen Fall als Text.', 'Décrivez le cas clinique par écrit.'),
    'Shorten the request to one clinical vignette without patient identifiers.': ('Reduzca la consulta a un caso clínico sin identificadores del paciente.', 'Reduza o pedido a um caso clínico sem identificadores do doente.', 'Beschränken Sie die Anfrage auf einen klinischen Fall ohne Patientenkennungen.', 'Limitez la demande à un cas clinique sans identifiants du patient.'),
    'The request looks like model instructions, not a clinical vignette. Send only the oncology case.': ('La consulta parece contener instrucciones para el modelo. Envíe únicamente el caso oncológico.', 'O pedido parece conter instruções para o modelo. Envie apenas o caso oncológico.', 'Die Anfrage scheint Anweisungen an das Modell zu enthalten. Senden Sie ausschließlich den onkologischen Fall.', 'La demande semble contenir des instructions destinées au modèle. Envoyez uniquement le cas oncologique.'),
    'Send an oncology clinical vignette: diagnosis or suspicion, stage/extent, ECOG/WHO, biomarkers, and the specific question.': ('Envíe un caso oncológico: diagnóstico o sospecha, estadio o extensión, ECOG/WHO, biomarcadores y la pregunta concreta.', 'Envie um caso oncológico: diagnóstico ou suspeita, estádio ou extensão, ECOG/WHO, biomarcadores e a pergunta concreta.', 'Senden Sie einen onkologischen Fall: Diagnose oder Verdacht, Stadium oder Ausdehnung, ECOG/WHO, Biomarker und konkrete Frage.', 'Envoyez un cas oncologique : diagnostic ou suspicion, stade ou extension, ECOG/WHO, biomarqueurs et question précise.'),
    'Clarify the clinical question and key data: diagnosis/suspicion, stage or extent, ECOG/WHO, biomarkers, and answer options.': ('Aclare la pregunta clínica y los datos esenciales: diagnóstico o sospecha, estadio o extensión, ECOG/WHO, biomarcadores y opciones de respuesta.', 'Clarifique a pergunta clínica e os dados essenciais: diagnóstico ou suspeita, estádio ou extensão, ECOG/WHO, biomarcadores e opções de resposta.', 'Präzisieren Sie die klinische Frage und die wesentlichen Angaben: Diagnose oder Verdacht, Stadium oder Ausdehnung, ECOG/WHO, Biomarker und Antwortoptionen.', 'Précisez la question clinique et les données essentielles : diagnostic ou suspicion, stade ou extension, ECOG/WHO, biomarqueurs et options de réponse.'),
    'I cannot answer reliably until suspicious biomarkers or drugs are verified.': ('No puedo responder de forma fiable hasta verificar los biomarcadores o medicamentos dudosos.', 'Não posso responder de forma fiável antes de verificar os biomarcadores ou medicamentos duvidosos.', 'Eine zuverlässige Antwort ist erst nach Prüfung der fraglichen Biomarker oder Medikamente möglich.', 'Une réponse fiable nécessite d’abord la vérification des biomarqueurs ou médicaments douteux.'),
    'Clarify or correct biomarker(s):': ('Aclare o corrija los biomarcadores:', 'Clarifique ou corrija os biomarcadores:', 'Präzisieren oder korrigieren Sie die Biomarker:', 'Précisez ou corrigez les biomarqueurs :'),
    'Clarify or correct drug(s):': ('Aclare o corrija los medicamentos:', 'Clarifique ou corrija os medicamentos:', 'Präzisieren oder korrigieren Sie die Medikamente:', 'Précisez ou corrigez les médicaments :'),
    '. They were not found in the OpenOnco KB vocabulary.': ('. No se encontraron en el vocabulario de OpenOnco KB.', '. Não foram encontrados no vocabulário da OpenOnco KB.', '. Sie wurden nicht im Vokabular von OpenOnco KB gefunden.', '. Ils n’ont pas été trouvés dans le vocabulaire d’OpenOnco KB.'),
    'Verification needed:': ('Verificación necesaria:', 'Verificação necessária:', 'Überprüfung erforderlich:', 'Vérification nécessaire :'),
    'Input validation blocked engine execution.': ('La validación de los datos impidió ejecutar el motor.', 'A validação dos dados impediu a execução do motor.', 'Die Eingabeprüfung hat die Ausführung der Engine verhindert.', 'La vérification des données a empêché l’exécution du moteur.'),
    'Input exceeded the free-text guard length.': ('La consulta supera la longitud permitida.', 'O pedido excede o comprimento permitido.', 'Die Anfrage überschreitet die zulässige Länge.', 'La demande dépasse la longueur autorisée.'),
    'Prompt-injection guard blocked processing.': ('La protección contra instrucciones ajenas al caso bloqueó el procesamiento.', 'A proteção contra instruções alheias ao caso bloqueou o processamento.', 'Der Schutz vor fremden Modellanweisungen hat die Verarbeitung verhindert.', 'La protection contre les instructions étrangères au cas a bloqué le traitement.'),
    'Non-oncology or underspecified request guard blocked processing.': ('No se procesó la consulta porque no es oncológica o faltan datos.', 'O pedido não foi processado por não ser oncológico ou por faltarem dados.', 'Die Anfrage wurde wegen fehlendem onkologischem Bezug oder unzureichenden Angaben nicht verarbeitet.', 'La demande n’a pas été traitée faute de contexte oncologique ou de précisions suffisantes.'),
}


def messages_for(locale):
    code = locale.lower().split('-')[0]
    return {source: values[LANGUAGES.index(code)] for source, values in MESSAGES.items()} if code in LANGUAGES else {}


def localize_response(answer, locale):
    """Only translate user-facing fields; leave all engine/extraction data intact."""
    catalog = messages_for(locale)
    if not catalog:
        return answer

    def text(value):
        if value in catalog:
            return catalog[value]
        for prefix in ('Clarify or correct biomarker(s):', 'Clarify or correct drug(s):', 'Verification needed:'):
            if value.startswith(prefix):
                value = catalog[prefix] + value[len(prefix):]
                ending = '. They were not found in the OpenOnco KB vocabulary.'
                if value.endswith(ending):
                    value = value[:-len(ending)] + catalog[ending]
                return value
        return value

    result = dict(answer)
    for key in ('direct_answer', 'safety_note'):
        if isinstance(result.get(key), str):
            result[key] = text(result[key])
    for key in ('rationale', 'clarifying_questions', 'engine_limitations'):
        if isinstance(result.get(key), list):
            result[key] = [text(v) if isinstance(v, str) else v for v in result[key]]
    return result
