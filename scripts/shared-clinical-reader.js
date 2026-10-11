/* Same-origin source documents and checked-in catalogs only; no translation API. */
(() => {
  'use strict';
  const locale = document.currentScript.dataset.locale;
  const frame = document.querySelector('[data-shared-clinical-source]');
  const header = document.querySelector('[data-reader-header]');
  const clinicalSections = /^\/(?:kb|cases|handbook|plans|disease)\//;
  fetch(`/${locale}/shared-header.fragment`).then(response => {
    if (!response.ok) throw new Error('Header unavailable');
    return response.text();
  }).then(markup => {
    header.innerHTML = markup;
    const page = location.pathname.replace(new RegExp(`^/${locale}/`), '');
    for (const link of header.querySelectorAll('.language-menu a[lang]')) {
      const code = link.lang;
      const prefix = code === 'en' ? '' : code === 'uk' ? 'ukr/' : `${code}/`;
      link.href = `/${prefix}${page}`;
    }
  }).catch(() => {
    // Keep an accessible source/navigation fallback if an asset cannot load.
    const home = document.createElement('a');
    home.href = `/${locale}/`;
    home.textContent = 'OpenOnco';
    header.replaceChildren(home);
  });
  const attach = () => {
    const doc = frame.contentDocument;
    if (!doc || !doc.body) return;
    const style = doc.createElement('style');
    style.textContent = '.top-bar.site-header,.translation-notice{display:none!important}html,body{min-height:0!important;height:auto!important}';
    doc.head.append(style);
    const resize = () => { frame.style.height = `${Math.max(600, doc.documentElement.scrollHeight, doc.body.scrollHeight)}px`; };
    new ResizeObserver(resize).observe(doc.body);
    resize();
    doc.addEventListener('click', event => {
      if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const link = typeof event.target.closest === 'function' ? event.target.closest('a[href]') : null;
      if (!link || link.hasAttribute('download') || link.target === '_blank') return;
      const target = new URL(link.href, doc.location.href);
      if (target.origin !== location.origin || !target.pathname.endsWith('.html')) return;
      if (target.pathname === doc.location.pathname && target.hash) return;
      event.preventDefault();
      location.href = clinicalSections.test(target.pathname)
        ? `/${locale}${target.pathname}${target.search}${target.hash}`
        : `${target.pathname}${target.search}${target.hash}`;
    });
  };
  frame.addEventListener('load', attach);
  if (frame.contentDocument?.readyState === 'complete') attach();
})();
