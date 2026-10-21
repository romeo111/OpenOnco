/* Read-only public FDA reports. No patient input, persistence or engine integration. */
(() => {
  'use strict';
  function dateOnly(value) {
    if (typeof value !== 'string') return null;
    if (!/^(?:\d{8}|\d{4}-\d{2}-\d{2})$/.test(value)) return null;
    const match = /^(\d{4})(\d{2})(\d{2})$/.exec(value.replaceAll('-', ''));
    if (!match) return null;
    const iso = `${match[1]}-${match[2]}-${match[3]}`;
    const parsed = new Date(`${iso}T00:00:00Z`);
    return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === iso ? iso : null;
  }
  function element(tag, text) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function textValues(items, key) {
    return Array.isArray(items) ? items.flatMap(item =>
      item && typeof item[key] === 'string' && item[key].trim() ? [item[key]] : []) : [];
  }
  function renderReport(report, index, copy) {
    const card = element('details');
    card.open = index === 0;
    const id = typeof report.safetyreportid === 'string' ? report.safetyreportid : String(index + 1);
    const received = dateOnly(report.receivedate);
    card.append(element('summary', `${copy.report} ${id} · ${copy.received}: ${received || copy.unknown}`));
    const facts = element('dl');
    for (const [label, values] of [
      [copy.drugs, textValues(report.patient?.drug, 'medicinalproduct')],
      [copy.reactions, textValues(report.patient?.reaction, 'reactionmeddrapt')],
    ]) {
      facts.append(element('dt', label));
      const value = element('dd', values.length ? values.join('; ') : copy.unknown);
      if (values.length) { value.lang = 'en'; value.setAttribute('translate', 'no'); }
      facts.append(value);
    }
    card.append(facts);
    if (typeof report.safetyreportid === 'string' && /^\d+(?:-\d+)?$/.test(report.safetyreportid)) {
      const link = element('a', copy.record_source);
      const source = new URL('https://api.fda.gov/drug/event.json');
      source.search = new URLSearchParams({search: `safetyreportid:"${report.safetyreportid}"`, limit: '1'}).toString();
      link.href = source.href;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      card.append(link);
    }
    return card;
  }
  function validQuery(value) {
    const url = new URL(value);
    const params = url.searchParams;
    if (url.origin !== 'https://api.fda.gov' || url.pathname !== '/drug/event.json'
      || url.username || url.password || url.hash
      || params.get('limit') !== '5' || params.get('skip') !== '0'
      || params.get('sort') !== 'receivedate:desc' || !params.get('search')
      || [...params.keys()].some(key => !['search', 'limit', 'skip', 'sort'].includes(key) || params.getAll(key).length !== 1)) {
      throw new Error('Invalid FDA query');
    }
    return url.href;
  }
  for (const root of document.querySelectorAll('[data-openfda-card]')) {
    if (root.dataset.openfdaReady) continue;
    root.dataset.openfdaReady = 'true';
    const button = root.querySelector('[data-openfda-load]');
    const status = root.querySelector('[data-openfda-status]');
    const updated = root.querySelector('[data-openfda-updated]');
    const total = root.querySelector('[data-openfda-total]');
    const results = root.querySelector('[data-openfda-results]');
    const copy = JSON.parse(root.dataset.copy);
    let query;
    try { query = validQuery(root.dataset.queryUrl); }
    catch (_) { status.textContent = copy.error; continue; }
    button.disabled = false;
    let busy = false;
    button.addEventListener('click', async () => {
      if (busy) return;
      busy = true;
      button.disabled = true;
      root.setAttribute('aria-busy', 'true');
      status.textContent = copy.loading;
      updated.textContent = copy.initial;
      total.textContent = '—';
      results.replaceChildren();
      results.hidden = true;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 20000);
      try {
        const response = await fetch(query, {
          credentials: 'omit', referrerPolicy: 'no-referrer', cache: 'no-store',
          redirect: 'error', signal: controller.signal,
        });
        const payload = await response.json();
        if (response.status === 404 && payload?.error?.code === 'NOT_FOUND' && payload?.error?.message === 'No matches found!') {
          total.textContent = '0';
          updated.textContent = copy.unknown;
          status.textContent = copy.empty;
        } else {
          const page = payload?.meta?.results;
          if (!response.ok || !page || !Number.isInteger(page.total) || page.total < 0
            || !Array.isArray(payload.results) || payload.results.length > 5
            || page.total < payload.results.length || (page.total > 0 && !payload.results.length)
            || payload.results.some(report => !report || typeof report !== 'object' || Array.isArray(report))) {
            throw new Error('Unavailable FDA reports');
          }
          const date = dateOnly(payload.meta.last_updated);
          updated.replaceChildren();
          if (date) { const time = element('time', date); time.dateTime = date; updated.append(time); }
          else updated.textContent = copy.unknown;
          total.textContent = String(page.total);
          for (const [index, report] of payload.results.entries()) results.append(renderReport(report, index, copy));
          results.hidden = !payload.results.length;
          status.textContent = payload.results.length
            ? copy.loaded.replace('{shown}', String(payload.results.length)).replace('{total}', String(page.total))
            : copy.empty;
        }
        button.textContent = copy.refresh;
      } catch (_) {
        results.replaceChildren();
        results.hidden = true;
        total.textContent = '—';
        updated.textContent = copy.unknown;
        status.textContent = copy.error;
        button.textContent = copy.retry;
      } finally {
        clearTimeout(timer);
        busy = false;
        button.disabled = false;
        root.setAttribute('aria-busy', 'false');
      }
    });
  }
})();
