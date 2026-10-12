/* Same-origin shared navigation. Clinical content and input values stay untouched. */
(() => {
  'use strict';
  const mount = document.querySelector('[data-shared-site-header]');
  if (!mount) return;
  const locale = mount.dataset.locale;
  const prefix = code => code === 'en' ? '' : code === 'uk' ? 'ukr/' : `${code}/`;
  const page = mount.dataset.page;
  const missing = new Set(JSON.parse(mount.dataset.missing || '[]'));
  const activePage = {home: 'index', gallery: 'gallery', diseases: 'kb'}[mount.dataset.active] || mount.dataset.active;
  fetch(`/${prefix(locale)}shared-header.fragment`).then(response => {
    if (!response.ok) throw new Error('Navigation unavailable');
    return response.text();
  }).then(markup => {
    mount.innerHTML = markup;
    for (const link of mount.querySelectorAll('.language-menu a[lang]')) {
      link.href = `/${prefix(link.lang)}${missing.has(link.lang) ? '' : page}`;
    }
    for (const link of mount.querySelectorAll('.top-nav a,.header-tools a,.mobile-menu-panel a,.btn-cta-try')) {
      if (new URL(link.href).pathname === `/${prefix(locale)}${activePage}.html`) {
        link.setAttribute('aria-current', 'page');
        if (link.closest('nav')) link.classList.add('active');
      }
    }
    mount.addEventListener('click', event => {
      const link = event.target.closest('.language-menu a[lang]');
      if (link) { try { localStorage.setItem('oo_lang', link.lang); } catch (_) {} }
    });
  }).catch(() => { /* Accessible fallback links are already present. */ });
})();
