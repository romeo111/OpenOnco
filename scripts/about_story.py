"""Keep the extended project story in both source-language templates."""
import html
import re

ENGLISH = {
    'Наша мета': 'Our purpose',
    'Менше непрозорості у складних клінічних рішеннях': 'Make complex clinical decisions easier to understand',
    'Онкологічне лікування рідко зводиться до однієї очевидної відповіді. Лікарю потрібно зіставити діагноз, стадію, біомаркери, попереднє лікування та ризики — а пацієнту важливо розуміти, про що говорити на прийомі.': 'Cancer treatment rarely has a single obvious answer. Clinicians need to consider the diagnosis, stage, biomarkers, previous treatment and risks. Patients need to understand what to discuss at their appointment.',
    'Мета OpenOnco — зробити цей шлях видимим: показати можливі треки поруч, пояснити, що саме впливає на вибір, і дати посилання на джерела. Це опора для підготовки й спільного обговорення, а не автоматичне призначення.': 'OpenOnco aims to make that process visible: show possible paths side by side, explain what influences the choice and link to sources. It supports preparation and discussion, rather than automatically prescribing treatment.',
    'Просте правило': 'A simple rule',
    'Якщо твердження не можна простежити до правила та джерела, воно не має ставати частиною плану.': 'A claim must be traceable to a rule and a source before it can become part of a plan.',
    'Підхід': 'Our approach',
    'Не «відповідь від AI», а відтворюваний шлях до розмови з лікарем': 'A reproducible process for preparing a conversation with a clinician',
    'Структуруємо клінічний контекст': 'Structure the clinical context',
    'Профіль описує важливі для рішення факти: тип пухлини, стадію, біомаркери, стан людини та вже проведене лікування.': 'The profile describes facts relevant to the decision: tumour type, stage, biomarkers, general condition and previous treatment.',
    'Зіставляємо його з правилами та джерелами': 'Compare it with rules and sources',
    'Правила працюють із версіонованою базою знань. Вони не вгадують препарат чи дозу, а показують, чому певний варіант потрапив у поле зору.': 'Rules use a versioned knowledge base. They explain why an option is considered, without guessing a drug or a dose.',
    'Показуємо результат так, щоб його можна було перевірити': 'Present results that can be checked',
    'Користувач бачить варіанти поруч, застереження й посилання на першоджерела — щоб підготувати питання для консиліуму або онколога.': 'Users see options side by side, warnings and links to original sources, to prepare questions for a tumour board or oncologist.',
    'Вкладена робота': 'The work behind it',
    'Найбільше зусиль — не в красивій відповіді, а в тому, щоб вона була обґрунтованою': 'The main effort goes into making results well supported',
    'База знань замість довільного тексту': 'A structured knowledge base',
    'Команда описує хвороби, схеми лікування, індикації, застереження та джерела як окремі пов’язані сутності. Так зміни не губляться в абзацах, а проходять через версії й перевірки.': 'The team records diseases, regimens, indications, warnings and sources as separate linked entities. Changes can then be versioned and checked, rather than getting lost in paragraphs.',
    'Перевірюваність на кожному кроці': 'Traceability at every step',
    'Для клінічних тверджень фіксується походження. Правила, результат і публічні приклади можна переглянути, а не просто прийняти «на віру».': 'Clinical claims have recorded provenance. Rules, results and public examples can be inspected rather than taken on trust.',
    'Безпека як межа, а не примітка дрібним шрифтом': 'Safety defines the boundaries',
    'Система не підміняє діагностику, не працює з невідкладними станами, не виконує персональний розрахунок доз і не приймає рішення замість лікаря.': 'The system does not replace diagnosis, handle emergencies, calculate personalised doses or make decisions on behalf of a clinician.',
    'Наступний крок': 'Next step',
    'Подивіться, як виглядає перевірюваний план': 'See what a traceable plan looks like',
    'Спробуйте синтетичний приклад або відкрийте конструктор. Не вводьте персональні дані пацієнта.': 'Try a synthetic example or open the plan builder. Do not enter personal patient information.',
    'Відкрити конструктор плану': 'Open the plan builder',
    'Переглянути приклади': 'Explore examples',
    'Перейти до інструментів OpenOnco': 'Explore OpenOnco tools',
}


def english_sections(uk_page):
    sections = re.findall(r'<section class="about-(?:purpose|work|effort|action)".*?</section>', uk_page, re.S)
    if len(sections) != 4:
        raise ValueError('Expected all four shared project-story sections')
    translated = []
    for section in sections:
        for source, target in sorted(ENGLISH.items(), key=lambda pair: len(pair[0]), reverse=True):
            section = section.replace(source, html.escape(target, quote=False))
        section = section.replace('/ukr/', '/')
        if re.search(r'[\u0400-\u04ff]', section):
            raise ValueError('Missing English project-story copy')
        translated.append(section)
    return '\n'.join(translated[:3]), translated[3]
