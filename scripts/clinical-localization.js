/* Checked-in display translations only. Never translate input values or engine data. */
(() => {
  'use strict';
  const locale = document.currentScript.dataset.locale;
  const catalogURL = document.currentScript.dataset.catalog || `/${locale}/clinical-translations.json`;
  const normalize = text => text.replace(/\s+/g, ' ').trim();
  const skip = 'script,style,code,pre,textarea,.lang-switch,[data-original-source]';
  const observed = new WeakSet();
  let displayTranslatedReport = true;
  const notices = {
    es: 'Traducción preliminar: revisión clínica pendiente.',
    pt: 'Tradução preliminar: revisão clínica pendente.',
    de: 'Vorläufige Übersetzung: klinische Prüfung ausstehend.',
    fr: 'Traduction provisoire : vérification clinique en attente.'
  };
  const originalLabels = {
    es: 'Texto original en inglés conservado para verificación',
    pt: 'Texto original em inglês preservado para verificação',
    de: 'Englischer Originaltext zur Überprüfung beibehalten',
    fr: 'Texte original anglais conservé pour vérification'
  };
  const counters = {
    es: ['Mostrando $1 de $2', 'Página $1 / $2', '$1 capítulos', 'Límite de preguntas alcanzado: $1 por hora.'],
    pt: ['A mostrar $1 de $2', 'Página $1 / $2', '$1 capítulos', 'Limite de perguntas atingido: $1 por hora.'],
    de: ['$1 von $2 angezeigt', 'Seite $1 / $2', '$1 Kapitel', 'Fragenlimit erreicht: $1 pro Stunde.'],
    fr: ['$1 résultats sur $2', 'Page $1 / $2', '$1 chapitres', 'Limite de questions atteinte : $1 par heure.']
  };
  fetch(catalogURL).then(response => {
    if (!response.ok) throw new Error('Translation catalog unavailable');
    return response.json();
  }).then(catalog => {
    window.OPENONCO_REPORT_LOCALE = locale;
    // Native curated text is an identity entry too; only English source prose
    // should receive an English-original label.
    const nativeValues = new Set(Object.entries(catalog).filter(([key, value]) => key !== value).map(([, value]) => value));
    const translate = text => {
      const key = normalize(text);
      if (nativeValues.has(key)) return text;
      const diagnostic = key.match(/^Unevaluated RedFlags: (RF-[A-Z0-9_-]+(?:, RF-[A-Z0-9_-]+)*)$/);
      if (diagnostic) {
        const labels = {es: 'Alertas no evaluadas: ', pt: 'Alertas não avaliados: ', de: 'Nicht ausgewertete Warnhinweise: ', fr: 'Alertes non évaluées : '};
        return labels[locale] + diagnostic[1];
      }
      const score = key.match(/^(\d+) of (\d+) answered · (\d+) correct$/);
      if (score) {
        const labels = {es: '$1 de $2 respondidas · $3 correctas', pt: '$1 de $2 respondidas · $3 corretas', de: '$1 von $2 beantwortet · $3 richtig', fr: '$1 réponses sur $2 · $3 correctes'};
        return labels[locale].replace(/\$(\d)/g, (_, index) => score[Number(index)]);
      }
      const matches = key.match(/^— matches for "(.*)" —$/);
      if (matches) {
        const labels = {es: '— coincidencias para', pt: '— resultados para', de: '— Treffer für', fr: '— résultats pour'};
        return `${labels[locale]} "${matches[1]}" —`;
      }
      const pages = key.match(/^Page (\d+) of (\d+) · (\d+) results$/);
      if (pages) {
        const labels = {es: 'Página $1 de $2 · $3 resultados', pt: 'Página $1 de $2 · $3 resultados', de: 'Seite $1 von $2 · $3 Ergebnisse', fr: 'Page $1 sur $2 · $3 résultats'};
        return labels[locale].replace(/\$(\d)/g, (_, index) => pages[Number(index)]);
      }
      const chapters = key.match(/^(\d+) of (\d+) chapters?$/);
      if (chapters) {
        const labels = {es: '$1 de $2 capítulos', pt: '$1 de $2 capítulos', de: '$1 von $2 Kapiteln', fr: '$1 chapitres sur $2'};
        return labels[locale].replace(/\$(\d)/g, (_, index) => chapters[Number(index)]);
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
        span.lang = 'en';
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
    const documents = new WeakSet();
    const attachDocument = doc => {
      if (documents.has(doc)) return;
      documents.add(doc);
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
      const reloadReport = () => {
        if (reportFrame.srcdoc) reportFrame.srcdoc = reportFrame.srcdoc;
        else if (reportFrame.src) reportFrame.src = reportFrame.src;
      };
      for (const button of [englishButton, ukrainianButton]) {
        button.addEventListener('click', () => {
          displayTranslatedReport = false;
          window.OPENONCO_REPORT_LOCALE = null;
          nativeButton.classList.remove('is-active');
          button.classList.add('is-active');
          reloadReport();
        }, true);
      }
      nativeButton.addEventListener('click', () => {
        if (englishButton.disabled || ukrainianButton.disabled || (typeof isInteractionLocked === 'function' && isInteractionLocked())) return;
        displayTranslatedReport = true;
        window.OPENONCO_REPORT_LOCALE = locale;
        if (typeof switchResultLang === 'function') switchResultLang('en');
        englishButton.classList.remove('is-active');
        ukrainianButton.classList.remove('is-active');
        nativeButton.classList.add('is-active');
        reloadReport();
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
