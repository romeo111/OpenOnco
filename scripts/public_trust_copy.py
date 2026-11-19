"""Shared, informational product scope and review-status explanations.

These are descriptions of evidence, not new clinical release criteria.
"""
from html import escape

LANGUAGES = ('en', 'uk', 'es', 'pt', 'de', 'fr', 'it', 'da', 'sv', 'nb', 'fi')

HEADLINE = dict(zip(LANGUAGES, (
    'Prepare for an oncology discussion — with sources you can check.',
    'Підготуйтеся до розмови з онкологом — із джерелами, які можна перевірити.',
    'Prepare una conversación sobre oncología, con fuentes verificables.',
    'Prepare uma conversa sobre oncologia, com fontes verificáveis.',
    'Bereiten Sie ein onkologisches Gespräch vor — mit überprüfbaren Quellen.',
    'Préparez une discussion en oncologie, avec des sources vérifiables.',
    'Prepara un colloquio oncologico, con fonti verificabili.',
    'Forbered en samtale om kræft med kilder, du kan kontrollere.',
    'Förbered ett samtal om cancer med källor du kan kontrollera.',
    'Forbered en samtale om kreft med kilder du kan kontrollere.',
    'Valmistaudu syöpää koskevaan keskusteluun tarkistettavien lähteiden avulla.',
)))
LEAD = dict(zip(LANGUAGES, (
    'Explore source-linked discussion drafts for clinician review. Patients and caregivers can prepare questions about an existing plan. OpenOnco does not provide an independent medical second opinion or approve treatment.',
    'Переглядайте чернетки з посиланнями на джерела для обговорення з лікарем. Пацієнти й близькі можуть підготувати запитання про вже призначений план. OpenOnco не надає незалежної медичної другої думки й не схвалює лікування.',
    'Explore borradores con fuentes para revisar con un profesional. Pacientes y cuidadores pueden preparar preguntas sobre un plan existente. OpenOnco no ofrece una segunda opinión médica independiente ni aprueba tratamientos.',
    'Explore rascunhos com fontes para revisão clínica. Doentes e cuidadores podem preparar perguntas sobre um plano existente. O OpenOnco não fornece uma segunda opinião médica independente nem aprova tratamentos.',
    'Erkunden Sie Entwürfe mit Quellen zur ärztlichen Prüfung. Patienten und Angehörige können Fragen zu einem bestehenden Plan vorbereiten. OpenOnco bietet keine unabhängige ärztliche Zweitmeinung und genehmigt keine Behandlung.',
    'Consultez des brouillons sourcés à examiner avec un médecin. Patients et proches peuvent préparer des questions sur un plan existant. OpenOnco ne fournit pas de second avis médical indépendant et ne valide pas de traitement.',
    'Esplora bozze con fonti da verificare con un medico. Pazienti e familiari possono preparare domande su un piano esistente. OpenOnco non fornisce un secondo parere medico indipendente né approva trattamenti.',
    'Se udkast med kilder til lægelig gennemgang. Patienter og pårørende kan forberede spørgsmål om en eksisterende plan. OpenOnco giver ikke en uafhængig lægelig second opinion og godkender ikke behandling.',
    'Utforska utkast med källor för läkargranskning. Patienter och närstående kan förbereda frågor om en befintlig plan. OpenOnco ger inte en oberoende medicinsk andra bedömning och godkänner inte behandling.',
    'Se utkast med kilder for legegjennomgang. Pasienter og pårørende kan forberede spørsmål om en eksisterende plan. OpenOnco gir ikke en uavhengig medisinsk ny vurdering og godkjenner ikke behandling.',
    'Tutustu lähteistettyihin luonnoksiin lääkärin arviointia varten. Potilaat ja läheiset voivat valmistella kysymyksiä nykyisestä suunnitelmasta. OpenOnco ei anna riippumatonta lääketieteellistä toista mielipidettä eikä hyväksy hoitoa.',
)))
REVIEW_TITLE = dict(zip(LANGUAGES, (
    'What review status means', 'Що означає статус перевірки',
    'Qué significa el estado de revisión', 'O que significa o estado de revisão',
    'Was der Prüfstatus bedeutet', 'Ce que signifie le statut de relecture',
    'Cosa significa lo stato di revisione', 'Hvad gennemgangsstatus betyder',
    'Vad granskningsstatus betyder', 'Hva gjennomgangsstatus betyr', 'Mitä arviointitila tarkoittaa',
)))
REVIEW_BODY = dict(zip(LANGUAGES, (
    'Technical checks cover software, data structure and source links; they do not establish clinical accuracy. A recorded clinical-content review applies only to its stated scope and revision, not to an individual treatment plan. Missing or outdated reviews do not count as current review. No formal clinical validation is claimed. Every draft requires verification by a qualified oncologist.',
    'Технічні перевірки охоплюють програму, структуру даних і посилання на джерела; вони не доводять клінічну правильність. Записана клінічна рецензія стосується лише зазначеного змісту й версії, а не індивідуального плану лікування. Відсутні або застарілі рецензії не означають актуальної перевірки. Формальна клінічна валідація не заявляється. Кожну чернетку має перевірити кваліфікований онколог.',
    'Las comprobaciones técnicas cubren el software, la estructura de datos y los enlaces; no demuestran exactitud clínica. Una revisión clínica registrada solo se aplica al alcance y la versión indicados, no a un plan individual. Las revisiones ausentes o desactualizadas no cuentan como actuales. No se afirma una validación clínica formal. Un oncólogo cualificado debe verificar cada borrador.',
    'As verificações técnicas abrangem software, estrutura de dados e ligações; não demonstram precisão clínica. Uma revisão clínica registada aplica-se apenas ao âmbito e à versão indicados, não a um plano individual. Revisões ausentes ou desatualizadas não contam como atuais. Não se afirma validação clínica formal. Cada rascunho deve ser verificado por um oncologista qualificado.',
    'Technische Prüfungen betreffen Software, Datenstruktur und Quellenlinks; sie belegen keine klinische Richtigkeit. Eine dokumentierte klinische Inhaltsprüfung gilt nur für den angegebenen Umfang und die Version, nicht für einen individuellen Behandlungsplan. Fehlende oder veraltete Prüfungen gelten nicht als aktuell. Eine formale klinische Validierung wird nicht beansprucht. Jeder Entwurf muss von einem qualifizierten Onkologen geprüft werden.',
    'Les contrôles techniques portent sur le logiciel, la structure des données et les liens ; ils ne prouvent pas l’exactitude clinique. Une relecture clinique enregistrée concerne uniquement le périmètre et la version indiqués, pas un plan individuel. Les relectures absentes ou périmées ne comptent pas comme actuelles. Aucune validation clinique formelle n’est revendiquée. Un oncologue qualifié doit vérifier chaque brouillon.',
    'I controlli tecnici riguardano software, struttura dei dati e collegamenti; non dimostrano accuratezza clinica. Una revisione clinica registrata riguarda solo ambito e versione indicati, non un piano individuale. Revisioni assenti o obsolete non valgono come attuali. Non si dichiara una validazione clinica formale. Ogni bozza deve essere verificata da un oncologo qualificato.',
    'Tekniske kontroller omfatter software, datastruktur og kildelinks; de dokumenterer ikke klinisk korrekthed. En registreret klinisk gennemgang gælder kun det angivne omfang og den angivne version, ikke en individuel behandlingsplan. Manglende eller forældede gennemgange tæller ikke som aktuelle. Der hævdes ingen formel klinisk validering. En kvalificeret onkolog skal kontrollere hvert udkast.',
    'Tekniska kontroller omfattar programvara, datastruktur och källänkar; de bevisar inte klinisk korrekthet. En registrerad klinisk granskning gäller endast angiven omfattning och version, inte en individuell behandlingsplan. Saknade eller föråldrade granskningar räknas inte som aktuella. Ingen formell klinisk validering hävdas. En kvalificerad onkolog måste kontrollera varje utkast.',
    'Tekniske kontroller omfatter programvare, datastruktur og kildelenker; de dokumenterer ikke klinisk riktighet. En registrert klinisk gjennomgang gjelder bare angitt omfang og versjon, ikke en individuell behandlingsplan. Manglende eller utdaterte gjennomganger teller ikke som aktuelle. Det hevdes ingen formell klinisk validering. En kvalifisert onkolog må kontrollere hvert utkast.',
    'Tekniset tarkistukset koskevat ohjelmistoa, tietorakennetta ja lähdelinkkejä; ne eivät osoita kliinistä oikeellisuutta. Kirjattu kliinisen sisällön arviointi koskee vain ilmoitettua laajuutta ja versiota, ei yksilöllistä hoitosuunnitelmaa. Puuttuvia tai vanhentuneita arviointeja ei lasketa ajantasaisiksi. Muodollista kliinistä validointia ei väitetä tehdyksi. Pätevän onkologin on tarkistettava jokainen luonnos.',
)))


REVIEW_METRIC = dict(zip(LANGUAGES, (
    'Review %: indications with at least one current, authorized, independent content review. This is not clinical accuracy or treatment approval.',
    'Рецензовано, %: показання з хоча б однією актуальною незалежною рецензією уповноваженого фахівця. Це не клінічна точність і не схвалення лікування.',
    'Revisión %: indicaciones con al menos una revisión actual, autorizada e independiente. No mide exactitud clínica ni aprobación del tratamiento.',
    'Revisão %: indicações com pelo menos uma revisão atual, autorizada e independente. Não mede precisão clínica nem aprovação do tratamento.',
    'Prüfung %: Indikationen mit mindestens einer aktuellen, autorisierten, unabhängigen Inhaltsprüfung. Keine Messung klinischer Richtigkeit oder Behandlungsgenehmigung.',
    'Relecture % : indications avec au moins une relecture actuelle, autorisée et indépendante. Ce n’est ni une mesure d’exactitude clinique ni une validation du traitement.',
    'Revisione %: indicazioni con almeno una revisione attuale, autorizzata e indipendente. Non misura accuratezza clinica né approvazione del trattamento.',
    'Gennemgang %: indikationer med mindst én aktuel, autoriseret, uafhængig gennemgang. Ikke et mål for klinisk korrekthed eller behandlingsgodkendelse.',
    'Granskning %: indikationer med minst en aktuell, behörig, oberoende granskning. Inte ett mått på klinisk korrekthet eller behandlingsgodkännande.',
    'Gjennomgang %: indikasjoner med minst én aktuell, autorisert, uavhengig gjennomgang. Ikke et mål på klinisk riktighet eller behandlingsgodkjenning.',
    'Arviointi %: käyttöaiheet, joilla on vähintään yksi ajantasainen, valtuutettu ja riippumaton arviointi. Ei kliinisen tarkkuuden mittari eikä hoidon hyväksyntä.',
)))


def messages_for(locale):
    messages = {table['en']: table[locale] for table in (HEADLINE, LEAD, REVIEW_TITLE, REVIEW_BODY, REVIEW_METRIC)}
    messages['Review %'] = REVIEW_METRIC[locale].split(':', 1)[0].strip()
    return messages


def render_review_notice(locale):
    return (
        '<aside class="public-review-notice" data-review-status="informational" '
        'style="margin:1rem 0;padding:1rem;border-left:3px solid #64748b;'
        'background:#f8fafc;color:#25364a;font-size:1rem;line-height:1.6">'
        f'<strong>{escape(REVIEW_TITLE[locale])}</strong>'
        f'<p style="margin:.5rem 0 0">{escape(REVIEW_BODY[locale])}</p></aside>'
    )
