"""Explicit display terminology; source disease codes remain unchanged."""
import re


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

UI_MESSAGES = {
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
    return catalog
