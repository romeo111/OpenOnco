/* Checked-in display translations only. Never translate input values or engine data. */
(() => {
  'use strict';
  const locale = document.currentScript.dataset.locale;
  const catalogURL = document.currentScript.dataset.catalog || `/${locale}/clinical-translations.json`;
  const contentReviewCopy = {"es":{"Current clinical-content review recorded":"Revisión actual del contenido clínico registrada","Записано актуальний перегляд клінічного змісту":"Revisión actual del contenido clínico registrada","Declared editorial review":"Revisión editorial declarada"},"pt":{"Current clinical-content review recorded":"Revisão atual do conteúdo clínico registada","Записано актуальний перегляд клінічного змісту":"Revisão atual do conteúdo clínico registada","Declared editorial review":"Revisão editorial declarada"},"de":{"Current clinical-content review recorded":"Aktuelle Prüfung des klinischen Inhalts dokumentiert","Записано актуальний перегляд клінічного змісту":"Aktuelle Prüfung des klinischen Inhalts dokumentiert","Declared editorial review":"Angegebene redaktionelle Prüfung"},"fr":{"Current clinical-content review recorded":"Relecture actuelle du contenu clinique consignée","Записано актуальний перегляд клінічного змісту":"Relecture actuelle du contenu clinique consignée","Declared editorial review":"Relecture éditoriale déclarée"},"it":{"Current clinical-content review recorded":"Revisione attuale del contenuto clinico registrata","Записано актуальний перегляд клінічного змісту":"Revisione attuale del contenuto clinico registrata","Declared editorial review":"Revisione editoriale dichiarata"},"da":{"Current clinical-content review recorded":"Aktuel gennemgang af klinisk indhold registreret","Записано актуальний перегляд клінічного змісту":"Aktuel gennemgang af klinisk indhold registreret","Declared editorial review":"Erklæret redaktionel gennemgang"},"sv":{"Current clinical-content review recorded":"Aktuell granskning av kliniskt innehåll registrerad","Записано актуальний перегляд клінічного змісту":"Aktuell granskning av kliniskt innehåll registrerad","Declared editorial review":"Angiven redaktionell granskning"},"nb":{"Current clinical-content review recorded":"Aktuell gjennomgang av klinisk innhold registrert","Записано актуальний перегляд клінічного змісту":"Aktuell gjennomgang av klinisk innhold registrert","Declared editorial review":"Oppgitt redaksjonell gjennomgang"},"fi":{"Current clinical-content review recorded":"Kliinisen sisällön ajantasainen arviointi kirjattu","Записано актуальний перегляд клінічного змісту":"Kliinisen sisällön ajantasainen arviointi kirjattu","Declared editorial review":"Ilmoitettu toimituksellinen arviointi"}};
  const normalize = text => text.replace(/\s+/g, ' ').trim();
  const skip = 'script,style,code,pre,textarea,.lang-switch,.brand-mini,.brand-wordmark,[data-original-source]';
  const observed = new WeakSet();
  let displayTranslatedReport = true;
  const notices = {
    es: 'Traducción preliminar: revisión clínica pendiente.',
    pt: 'Tradução preliminar: revisão clínica pendente.',
    de: 'Vorläufige Übersetzung: klinische Prüfung ausstehend.',
    fr: 'Traduction provisoire : vérification clinique en attente.'
  };
  const originalLabels = {
    es: 'Texto original conservado para verificación',
    pt: 'Texto original preservado para verificação',
    de: 'Originaltext zur Überprüfung beibehalten',
    fr: 'Texte original conservé pour vérification'
  };
  const counters = {
    es: ['Mostrando $1 de $2', 'Página $1 / $2', '$1 capítulos', 'Límite de preguntas alcanzado: $1 por hora.'],
    pt: ['A mostrar $1 de $2', 'Página $1 / $2', '$1 capítulos', 'Limite de perguntas atingido: $1 por hora.'],
    de: ['$1 von $2 angezeigt', 'Seite $1 / $2', '$1 Kapitel', 'Fragenlimit erreicht: $1 pro Stunde.'],
    fr: ['$1 résultats sur $2', 'Page $1 / $2', '$1 chapitres', 'Limite de questions atteinte : $1 par heure.']
  };
  const extraCopy = {
    it: {notice: 'Traduzione preliminare: revisione clinica in attesa.', original: 'Testo originale conservato per la verifica', counters: ['$1 di $2 visualizzati', 'Pagina $1 / $2', '$1 capitoli', 'Limite di domande raggiunto: $1 all’ora.'], diagnostic: 'Segnali di allarme non valutati: ', score: '$1 di $2 risposte · $3 corrette', matches: '— risultati per', pages: 'Pagina $1 di $2 · $3 risultati', chapters: '$1 di $2 capitoli', patient: 'Stai visualizzando l’originale ucraino. Seleziona EN per la bozza inglese, ancora incompleta e in attesa di verifica.'},
    da: {notice: 'Foreløbig oversættelse: klinisk gennemgang afventer.', original: 'Originaltekst bevaret til kontrol', counters: ['Viser $1 af $2', 'Side $1 / $2', '$1 kapitler', 'Spørgsmålsgrænsen er nået: $1 i timen.'], diagnostic: 'Ikke-vurderede advarselstegn: ', score: '$1 af $2 besvaret · $3 korrekte', matches: '— resultater for', pages: 'Side $1 af $2 · $3 resultater', chapters: '$1 af $2 kapitler', patient: 'Du ser den ukrainske original. Vælg EN for det engelske udkast, som stadig er ufuldstændigt og afventer kontrol.'},
    sv: {notice: 'Preliminär översättning: klinisk granskning väntar.', original: 'Originaltext bevarad för kontroll', counters: ['Visar $1 av $2', 'Sida $1 / $2', '$1 kapitel', 'Frågegränsen har nåtts: $1 per timme.'], diagnostic: 'Ej bedömda varningssignaler: ', score: '$1 av $2 besvarade · $3 rätt', matches: '— träffar för', pages: 'Sida $1 av $2 · $3 resultat', chapters: '$1 av $2 kapitel', patient: 'Du ser det ukrainska originalet. Välj EN för det engelska utkastet, som fortfarande är ofullständigt och väntar på granskning.'},
    nb: {notice: 'Foreløpig oversettelse: klinisk gjennomgang gjenstår.', original: 'Originaltekst bevart for kontroll', counters: ['Viser $1 av $2', 'Side $1 / $2', '$1 kapitler', 'Spørsmålsgrensen er nådd: $1 per time.'], diagnostic: 'Ikke-vurderte varselsignaler: ', score: '$1 av $2 besvart · $3 riktige', matches: '— treff for', pages: 'Side $1 av $2 · $3 resultater', chapters: '$1 av $2 kapitler', patient: 'Du ser den ukrainske originalen. Velg EN for det engelske utkastet, som fortsatt er ufullstendig og venter på gjennomgang.'},
    fi: {notice: 'Alustava käännös: kliininen tarkistus on kesken.', original: 'Alkuperäisteksti säilytetty tarkistusta varten', counters: ['Näytetään $1 / $2', 'Sivu $1 / $2', '$1 lukua', 'Kysymysraja saavutettu: $1 tunnissa.'], diagnostic: 'Arvioimattomat varoitusmerkit: ', score: '$1 / $2 vastattu · $3 oikein', matches: '— tulokset haulle', pages: 'Sivu $1 / $2 · $3 tulosta', chapters: '$1 / $2 lukua', patient: 'Näet ukrainankielisen alkuperäistekstin. Valitse EN nähdäksesi englanninkielisen luonnoksen, joka on vielä puutteellinen ja odottaa tarkistusta.'}
  };
  for (const [code, copy] of Object.entries(extraCopy)) {
    notices[code] = copy.notice;
    originalLabels[code] = copy.original;
    counters[code] = copy.counters;
  }
  // BEGIN dosing schedule guard: retain original when cadence is unproven.
  const schedulePatterns = {"es":{"daily":"\\b(?:diari\\w*|cada d[ií]a|al d[ií]a)\\b","weekly":"\\b(?:una|1)\\s+vez\\s+por\\s+semana\\b|\\bsemanal(?:mente)?\\b"},"pt":{"daily":"\\b(?:di[aá]ri\\w*|diariamente|cada dia|por dia|ao dia)\\b","weekly":"\\b(?:uma|1)\\s+vez\\s+por\\s+semana\\b|\\bsemanal(?:mente)?\\b"},"de":{"daily":"\\b(?:t[aä]glich\\w*|jeden tag|pro tag)\\b","weekly":"\\bwöchentlich\\b|\\beinmal\\s+pro\\s+woche\\b"},"fr":{"daily":"\\b(?:quotidien\\w*|chaque jour|par jour)\\b","weekly":"\\b(?:une|1)\\s+(?:seule\\s+)?fois\\s+par\\s+semaine\\b|\\bhebdomadaire\\b"},"it":{"daily":"\\b(?:ogni giorno|al giorno|quotidianamente|giornalier\\w*)\\b","weekly":"\\b(?:settimana|settimanale|settimanalmente)\\b"},"da":{"daily":"\\b(?:daglig\\w*|hver dag)\\b","weekly":"\\b(?:ugentlig\\w*|hver uge)\\b"},"sv":{"daily":"\\b(?:daglig\\w*|varje dag)\\b","weekly":"\\b(?:veckovis|varje vecka|en gång i veckan)\\b"},"nb":{"daily":"\\b(?:daglig\\w*|hver dag)\\b","weekly":"\\b(?:ukentlig\\w*|hver uke)\\b"},"fi":{"daily":"\\b(?:päivittäin|kerran päivässä|joka päivä)\\b","weekly":"\\b(?:viikoittain|kerran viikossa|joka viikko)\\b"}};
  const preserveSchedule = (source, translated, language) => {
    if (source === translated) return true;
    const daily = /\b(?:once daily|every day|daily)\b/i.test(source);
    const weekly = /\b(?:once weekly|every week|weekly)\b/i.test(source);
    if (daily === weekly) return true;
    const forms = schedulePatterns[language];
    if (!forms) return false;
    const hasDaily = new RegExp(forms.daily, 'i').test(translated);
    const hasWeekly = new RegExp(forms.weekly, 'i').test(translated);
    return daily ? hasDaily && !hasWeekly : hasWeekly && !hasDaily;
  };
  // END dosing schedule guard.
  fetch(catalogURL).then(response => {
    if (!response.ok) throw new Error('Translation catalog unavailable');
    return response.json();
  }).then(catalog => {
    Object.assign(catalog, contentReviewCopy[locale] || {});
    for (const [source, translated] of Object.entries(catalog)) {
      if (!preserveSchedule(source, translated, locale)) catalog[source] = source;
    }
    window.OPENONCO_REPORT_LOCALE = locale;
    // Native curated text is an identity entry too. Retained source prose
    // receives a neutral original-text label. Catalog keys can contain
    // mixed-language source text, so do not guess a fragment's language.
    const nativeValues = new Set(Object.entries(catalog).filter(([key, value]) => key !== value).map(([, value]) => value));
    const translate = text => {
      const key = normalize(text);
      if (nativeValues.has(key)) return text;
      const diagnostic = key.match(/^Unevaluated RedFlags: (RF-[A-Z0-9_-]+(?:, RF-[A-Z0-9_-]+)*)$/);
      if (diagnostic) {
        const labels = {es: 'Alertas no evaluadas: ', pt: 'Alertas não avaliados: ', de: 'Nicht ausgewertete Warnhinweise: ', fr: 'Alertes non évaluées : '};
        return (labels[locale] || extraCopy[locale].diagnostic) + diagnostic[1];
      }
      const score = key.match(/^(\d+) of (\d+) answered · (\d+) correct$/);
      if (score) {
        const labels = {es: '$1 de $2 respondidas · $3 correctas', pt: '$1 de $2 respondidas · $3 corretas', de: '$1 von $2 beantwortet · $3 richtig', fr: '$1 réponses sur $2 · $3 correctes'};
        return (labels[locale] || extraCopy[locale].score).replace(/\$(\d)/g, (_, index) => score[Number(index)]);
      }
      const matches = key.match(/^— matches for "(.*)" —$/);
      if (matches) {
        const labels = {es: '— coincidencias para', pt: '— resultados para', de: '— Treffer für', fr: '— résultats pour'};
        return `${labels[locale] || extraCopy[locale].matches} "${matches[1]}" —`;
      }
      const pages = key.match(/^Page (\d+) of (\d+) · (\d+) results$/);
      if (pages) {
        const labels = {es: 'Página $1 de $2 · $3 resultados', pt: 'Página $1 de $2 · $3 resultados', de: 'Seite $1 von $2 · $3 Ergebnisse', fr: 'Page $1 sur $2 · $3 résultats'};
        return (labels[locale] || extraCopy[locale].pages).replace(/\$(\d)/g, (_, index) => pages[Number(index)]);
      }
      const chapters = key.match(/^(\d+) of (\d+) chapters?$/);
      if (chapters) {
        const labels = {es: '$1 de $2 capítulos', pt: '$1 de $2 capítulos', de: '$1 von $2 Kapiteln', fr: '$1 chapitres sur $2'};
        return (labels[locale] || extraCopy[locale].chapters).replace(/\$(\d)/g, (_, index) => chapters[Number(index)]);
      }
      if (Object.prototype.hasOwnProperty.call(catalog, key)) {
        return text.slice(0, text.indexOf(text.trimStart())) + catalog[key] + (text.match(/\s*$/) || [''])[0];
      }
      const patterns = [/^Showing (\d+) of (\d+)$/, /^Page (\d+) \/ (\d+)$/, /^(\d+) chapters$/, /^Question limit reached: (\d+) per hour\.$/];
      for (let index = 0; index < patterns.length; index++) {
        if (patterns[index].test(key)) return key.replace(patterns[index], counters[locale][index]);
      }
      return text;
    };
    const translateOption = text => {
      const badges = new Set(['Curated showcase', 'Curated plan', 'Diagnostic brief', 'Molecular decision example', 'JSON profile']);
      const parts = text.split(' · ');
      const suffix = [];
      while (parts.length > 1 && badges.has(parts[parts.length - 1])) suffix.unshift(translate(parts.pop()));
      let title = parts.join(' · ');
      const icd = title.match(/^(.*)( · ICD-10 .*)$/);
      let icdSuffix = '';
      if (icd) { title = icd[1]; icdSuffix = icd[2]; }
      const line = title.match(/^(.*)( — )(first line|newly diagnosed \(1L\))$/);
      title = line ? translate(line[1]) + line[2] + translate(line[3]) : translate(title);
      return title + icdSuffix + (suffix.length ? ' · ' + suffix.join(' · ') : '');
    };
    window.OPENONCO_DISPLAY_LABEL = translateOption;
    const visit = root => {
      if (!root || root.nodeType !== Node.ELEMENT_NODE || root.matches(skip)) return;
      const doc = root.ownerDocument;
      const walker = doc.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
        acceptNode: node => node.parentElement && !node.parentElement.closest(skip)
          ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT
      });
      let node;
      const retained = [];
      while ((node = walker.nextNode())) {
        // These option labels combine a title with taxonomy/ICD metadata.
        // Translate display components; keep the option's value untouched.
        const localized = node.parentElement.closest('option')
          ? translateOption(node.nodeValue)
          : translate(node.nodeValue);
        if (localized !== node.nodeValue) node.nodeValue = localized;
        else if (normalize(node.nodeValue).length > 180 && catalog[normalize(node.nodeValue)] === normalize(node.nodeValue) && !nativeValues.has(normalize(node.nodeValue)) && !node.parentElement.closest('head,option,.clinical-safety')) retained.push(node);
      }
      for (const original of retained) {
        const span = doc.createElement('span');
        span.className = 'translation-original-fragment';
        const declared = original.parentElement.closest('[lang]');
        const language = declared && declared !== doc.documentElement ? declared.getAttribute('lang').toLowerCase() : '';
        span.lang = /^[a-z]{2,3}(?:-[a-z0-9]{2,8})*$/.test(language) ? language : 'und';
        span.dataset.originalSource = '';
        span.dataset.label = originalLabels[locale];
        original.replaceWith(span);
        span.append(original);
      }
      for (const element of [root, ...root.querySelectorAll('[title],[placeholder],[aria-label]')]) {
        if (element.closest('script,style,code,pre,.lang-switch,[data-original-source]')) continue;
        for (const attribute of ['title', 'placeholder', 'aria-label']) {
          if (element.hasAttribute(attribute)) element.setAttribute(attribute, translate(element.getAttribute(attribute)));
        }
      }
      for (const card of root.querySelectorAll('[data-search]')) {
        if (!card.dataset.localizedSearch) {
          card.dataset.search += ' ' + card.textContent.toLowerCase();
          card.dataset.localizedSearch = locale;
        }
      }
      for (const link of root.querySelectorAll('a[href]:not([data-original-source]):not([hreflang]):not(.lang-other):not(.lang-current)')) {
        const url = new URL(link.getAttribute('href'), doc.baseURI);
        if (url.origin === location.origin && /^\/(?:kb\/|cases\/|handbook\/|plans\/|disease\/|(?:try|ask|prevent|kb|handbook|diseases|gallery)\.html$)/.test(url.pathname)) {
          link.setAttribute('href', `/${locale}${url.pathname}${url.search}${url.hash}`);
        }
      }
      for (const frame of root.querySelectorAll('iframe')) {
        const attach = () => {
          try {
            if (frame.contentDocument && frame.contentDocument.body) attachDocument(frame.contentDocument);
          } catch (_) { /* Cross-origin previews retain their declared language. */ }
        };
        if (!observed.has(frame)) {
          observed.add(frame);
          frame.addEventListener('load', attach);
        }
        attach();
      }
    };
    const patientAvailabilityNotices = {"es": "Está viendo el original ucraniano. Seleccione EN para el borrador inglés, todavía incompleto y pendiente de revisión.", "pt": "Está a ver o original ucraniano. Selecione EN para o rascunho inglês, ainda incompleto e pendente de revisão.", "de": "Sie sehen das ukrainische Original. Wählen Sie EN für den englischen Entwurf, der noch unvollständig ist und geprüft werden muss.", "fr": "Vous consultez l’original ukrainien. Sélectionnez EN pour le brouillon anglais, encore incomplet et en attente de vérification."};
    const documents = new WeakSet();
    for (const [code, copy] of Object.entries(extraCopy)) patientAvailabilityNotices[code] = copy.patient;
    const attachDocument = doc => {
      if (documents.has(doc)) return;
      documents.add(doc);
      if (doc !== document && doc.documentElement.lang === 'uk' && doc.querySelector('.patient-report')) {
        const notice = doc.createElement('aside');
        notice.className = 'patient-language-availability';
        notice.lang = locale;
        notice.textContent = patientAvailabilityNotices[locale];
        notice.style.cssText = 'padding:12px 16px;background:#fff7df;border-left:3px solid #c89032;font:14px/1.5 sans-serif;';
        doc.body.prepend(notice);
      }
      if (doc !== document && (!displayTranslatedReport || doc.documentElement.lang === 'uk')) return;
      doc.documentElement.lang = locale;
      doc.documentElement.dataset.translationLocale = locale;
      if (doc !== document && !doc.querySelector('.translation-notice')) {
        const notice = doc.createElement('aside');
        notice.className = 'translation-notice';
        notice.textContent = notices[locale];
        notice.style.cssText = 'padding:12px 16px;background:#fff7df;border-left:3px solid #c89032;font:14px/1.5 sans-serif;';
        doc.body.prepend(notice);
      }
      const observer = new MutationObserver(changes => {
        observer.disconnect();
        const roots = new Set();
        for (const change of changes) {
          if (change.type === 'characterData') roots.add(change.target.parentElement);
          else if (change.type === 'attributes') roots.add(change.target);
          else for (const child of change.addedNodes) roots.add(child.nodeType === Node.TEXT_NODE ? child.parentElement : child);
        }
        for (const root of roots) visit(root);
        watch();
      });
      const watch = () => observer.observe(doc.body, {subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['title','placeholder','aria-label']});
      visit(doc.body);
      watch();
    };
    const englishButton = document.getElementById('langEnBtn');
    const ukrainianButton = document.getElementById('langUaBtn');
    const reportFrame = document.getElementById('resultFrame');
    if (englishButton && ukrainianButton && reportFrame) {
      const nativeButton = document.createElement('button');
      nativeButton.type = 'button';
      nativeButton.className = 'rt-lang-btn is-active';
      nativeButton.textContent = locale.toUpperCase();
      nativeButton.setAttribute('aria-label', locale.toUpperCase());
      englishButton.after(nativeButton);
      englishButton.classList.remove('is-active');
      for (const button of [englishButton, ukrainianButton]) {
        button.addEventListener('click', () => {
          displayTranslatedReport = false;
          window.OPENONCO_REPORT_LOCALE = null;
          nativeButton.classList.remove('is-active');
          button.classList.add('is-active');
        }, true);
      }
      nativeButton.addEventListener('click', async () => {
        if (englishButton.disabled || ukrainianButton.disabled || (typeof isInteractionLocked === 'function' && isInteractionLocked())) return;
        displayTranslatedReport = true;
        window.OPENONCO_REPORT_LOCALE = locale;
        if (typeof switchResultLang === 'function') await switchResultLang('en');
        englishButton.classList.remove('is-active');
        ukrainianButton.classList.remove('is-active');
        nativeButton.classList.add('is-active');
      });
    }
    attachDocument(document);
    // A native query typed before the catalog arrived must be re-filtered.
    // Restore an existing choice without firing patient/profile changes.
    for (const id of ['diseaseSearch', 'exampleSearch']) {
      const field = document.getElementById(id);
      if (!field || !field.value.trim()) continue;
      const select = document.getElementById(id === 'diseaseSearch' ? 'diseaseSelect' : 'exampleSelect');
      const previous = select && select.value;
      field.dispatchEvent(new Event('input', {bubbles: true}));
      if (select && previous && [...select.options].some(option => option.value === previous)) select.value = previous;
    }
  }).catch(() => {
    // Static translated pages remain usable; do not hide unlocalized output.
    document.documentElement.dataset.translationRuntime = 'unavailable';
    window.OPENONCO_REPORT_LOCALE = null;
    if (typeof highlightLangButtons === 'function') highlightLangButtons();
  });
})();
