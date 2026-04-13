const state = { products: [], filtered: [] };

function money(v) {
  return `$${Number(v || 0).toFixed(2)}`;
}

function seed(text) {
  return encodeURIComponent(String(text || 'bird-journal').toLowerCase().replace(/[^a-z0-9]+/g, '-'));
}

function inferType(p) {
  if (p.type) return p.type;
  return (p.sku || '').startsWith('POD-') ? 'Print-on-Demand' : 'Digital Download';
}

function inferCollection(p) {
  if (p.collection) return p.collection;
  const sku = p.sku || '';
  if (sku.includes('STATE')) return 'State Life Lists';
  if (sku.includes('MIGRATION')) return 'Migration Trackers';
  if (sku.includes('WARBLER')) return 'Warbler Journals';
  return 'Field Notes';
}

function inferSpecies(p) {
  if (p.species) return p.species;
  const sku = p.sku || '';
  if (sku.includes('WARBLER')) return 'Warbler';
  if (sku.includes('MIGRATION')) return 'Mixed Species';
  if (sku.includes('STATE')) return 'Regional Mix';
  return 'Mixed Species';
}

function inferRegion(p) {
  if (p.region) return p.region;
  const match = (p.sku || '').match(/DIGI-STATE-([A-Z-]+)/);
  if (match) return match[1].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  return 'United States';
}

function deliveryLine(type) {
  return type === 'Print-on-Demand' ? 'Print-on-Demand · Ships in 3–5 days' : 'Digital Download · PDF';
}

function resolveImage(p) {
  if (p.image && /^https?:\/\//.test(p.image)) return p.image;
  const sku = (p.sku || '').toLowerCase();
  if (sku) return `assets/previews/${sku}.svg`;
  return `https://picsum.photos/seed/${seed(p.sku || p.title || p.keyword || 'bird')}/800/600`;
}

function normalizeProduct(p) {
  const type = inferType(p);
  const hasCheckout = !!(p.checkout_url && p.checkout_url.startsWith('http'));
  const published = p.published === true || p.published === 'true';
  const purchasable = p.purchasable === true || p.purchasable === 'true' || (hasCheckout && published);

  return {
    ...p,
    published,
    purchasable,
    type,
    collection: inferCollection(p),
    species: inferSpecies(p),
    region: inferRegion(p),
    delivery: p.delivery || deliveryLine(type),
    image: resolveImage(p)
  };
}

function siteRootUrl() {
  const script = document.currentScript || document.querySelector('script[src*="app.v8.js"]');
  if (script?.src) return new URL('.', script.src);
  return new URL('../', window.location.href);
}

async function loadProducts() {
  const res = await fetch(new URL('products.json', siteRootUrl()));
  const raw = await res.json();
  state.products = raw.map(normalizeProduct);
  state.filtered = [...state.products];
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function badgeMarkup(p) {
  if (!p.purchasable) return '<span class="badge neutral">Coming Soon</span>';
  if (p.type === 'Digital Download') return '<span class="badge download">Digital Download</span>';
  return '<span class="badge">Print Edition</span>';
}

function productCard(p, i = 0) {
  return `
    <article class="card product-card reveal delay-${i % 4}">
      <a class="card-hit" href="product.html?sku=${encodeURIComponent(p.sku)}" aria-label="View details for ${escapeHtml(p.title)}"></a>
      <div class="product-media">
        <img class="product-thumb" src="${p.image}" alt="Preview of ${escapeHtml(p.title)}" loading="lazy" onerror="this.onerror=null;this.src='https://picsum.photos/seed/field-feather-fallback/800/600';" />
      </div>
      <div class="product-meta">
        <div class="product-meta-top">
          ${badgeMarkup(p)}
        </div>
        <h3 class="product-title">${escapeHtml(p.title)}</h3>
        <p class="product-meta-line">${escapeHtml(p.collection)} &middot; ${escapeHtml(p.delivery)}</p>
        <div class="product-bottom">
          <span class="price">${money(p.price)}</span>
          <span class="card-link-text">Details →</span>
        </div>
      </div>
    </article>`;
}

function setActiveThemeIcon(button, theme) {
  if (!button) return;
  button.innerHTML = theme === 'dark'
    ? '<span class="sr-only">Switch to light mode</span><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2.4M12 19.6V22M4.93 4.93l1.7 1.7M17.37 17.37l1.7 1.7M2 12h2.4M19.6 12H22M4.93 19.07l1.7-1.7M17.37 6.63l1.7-1.7"></path></svg>'
    : '<span class="sr-only">Switch to dark mode</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11Z"></path></svg>';
}

function initTheme() {
  const root = document.documentElement;
  const saved = localStorage.getItem('ff-theme');
  const preferred = saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  root.setAttribute('data-theme', preferred);

  const toggles = document.querySelectorAll('[data-theme-toggle]');
  toggles.forEach(button => setActiveThemeIcon(button, preferred));
  toggles.forEach(button => {
    button.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('ff-theme', next);
      toggles.forEach(btn => setActiveThemeIcon(btn, next));
    });
  });
}

function initTopbarScroll() {
  const bar = document.querySelector('.topbar');
  if (!bar) return;
  const update = () => bar.classList.toggle('scrolled', window.scrollY > 8);
  window.addEventListener('scroll', update, { passive: true });
  update();
}

function initMobileNav() {
  const button = document.querySelector('[data-nav-toggle]');
  const panel = document.querySelector('[data-mobile-panel]');
  if (!button || !panel) return;

  button.innerHTML = '<span class="sr-only">Toggle navigation</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"></path></svg>';

  const setOpen = open => {
    button.setAttribute('aria-expanded', String(open));
    panel.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
  };

  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    setOpen(open);
  });

  panel.querySelectorAll('a, button').forEach(el => {
    el.addEventListener('click', () => setOpen(false));
  });
}

function initParallax() {
  const art = document.querySelector('[data-parallax]');
  if (!art || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const update = () => {
    const y = Math.min(26, window.scrollY * 0.03);
    art.style.transform = `translateY(${y}px)`;
  };
  window.addEventListener('scroll', update, { passive: true });
  update();
}

function initReveals() {
  const items = document.querySelectorAll('.reveal');
  if (!items.length) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach(el => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  items.forEach(el => observer.observe(el));
}


function slugToLabel(slug) {
  return String(slug || '')
    .split('-')
    .filter(Boolean)
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function initNewsletterAttribution() {
  const links = document.querySelectorAll('[data-newsletter-source]');
  links.forEach(link => {
    try {
      const url = new URL(link.getAttribute('href'), window.location.href);
      url.searchParams.set('mw_source', link.dataset.newsletterSource || 'unknown');
      url.searchParams.set('mw_offer', link.dataset.newsletterOffer || 'Morning Warbler');
      url.searchParams.set('mw_cluster', link.dataset.newsletterCluster || 'editorial');
      link.setAttribute('href', url.pathname + url.search);
    } catch (error) {
      console.error(error);
    }

    link.addEventListener('click', () => {
      try {
        const key = 'ff-newsletter-clicks';
        const current = JSON.parse(localStorage.getItem(key) || '[]');
        current.push({
          source: link.dataset.newsletterSource || 'unknown',
          offer: link.dataset.newsletterOffer || 'Morning Warbler',
          cluster: link.dataset.newsletterCluster || 'editorial',
          ts: new Date().toISOString()
        });
        localStorage.setItem(key, JSON.stringify(current.slice(-100)));
      } catch (error) {
        console.error(error);
      }
    });
  });
}

function initNewsletterWelcomeContext() {
  const target = document.querySelector('[data-newsletter-context]');
  if (!target) return;
  const params = new URLSearchParams(window.location.search);
  const source = params.get('mw_source');
  const offer = params.get('mw_offer');
  const cluster = params.get('mw_cluster');
  if (!source && !offer && !cluster) return;

  const clusterLabels = {
    beginner: 'beginner birding',
    'beginner-gear': 'beginner gear',
    backyard: 'backyard birding',
    migration: 'migration coverage',
    'migration-tools': 'migration tools',
    regional: 'regional birding',
    'migration-event': 'hawkwatch coverage',
    'gear-trust': 'gear comparisons'
  };

  const sourceLabel = slugToLabel(source);
  const clusterLabel = clusterLabels[cluster] || 'the journal';
  const offerLabel = offer || 'The Morning Warbler';
  target.innerHTML = `<strong>Starting point:</strong> You arrived from ${sourceLabel || clusterLabel}. This page stays paired with ${offerLabel} so the next step feels connected to why you came.`;
}


function initMorningWarblerRecommendations() {
  const grid = document.querySelector('[data-newsletter-recommendation-grid]');
  if (!grid) return;

  const params = new URLSearchParams(window.location.search);
  const cluster = params.get('mw_cluster') || 'editorial';
  const recommendationsByCluster = {
    beginner: [
      { title: 'Essential Birding Gear for Beginners', href: '../essential-birding-gear-for-beginners/index.html', body: 'Build out the simple tools that make a first month outdoors easier.' },
      { title: 'Backyard Birding for Beginners', href: '../backyard-birding-for-beginners/index.html', body: 'Turn everyday feeder watching into a steadier habit.' },
      { title: 'Best Birding Apps in 2026', href: '../best-birding-apps/index.html', body: 'Keep your digital birding tools useful without letting them take over.' },
    ],
    'beginner-gear': [
      { title: 'Best Binoculars for Birding in 2026', href: '../best-binoculars-for-birding/index.html', body: 'Compare optics with a calmer shortlist already in mind.' },
      { title: 'Best Bird Field Guides Compared', href: '../best-bird-field-guides/index.html', body: 'Choose the guide that matches how you actually learn birds.' },
      { title: 'Birdwatching for Beginners', href: '../birdwatching-for-beginners/index.html', body: 'Reconnect gear choices to the broader field habit you are building.' },
    ],
    backyard: [
      { title: 'How to Attract More Birds to Your Yard Naturally', href: '../attract-birds-to-your-yard/index.html', body: 'Improve your patch with habitat changes that compound over time.' },
      { title: 'Best Backyard Bird Feeders', href: '../best-backyard-bird-feeders/index.html', body: 'Choose feeder setups that fit the species and rhythm you want.' },
      { title: 'Birdwatching for Beginners', href: '../birdwatching-for-beginners/index.html', body: 'Keep backyard observation connected to broader birding skill.' },
    ],
    migration: [
      { title: 'How to Use eBird to Track Migration in Real Time', href: '../how-to-use-ebird-migration/index.html', body: 'Turn seasonal movement into cleaner field decisions.' },
      { title: 'Hawk Migration Explained', href: '../hawk-migration/index.html', body: 'Follow a more event-driven side of migration with sharper timing.' },
      { title: 'How to Identify Birds', href: '../how-to-identify-birds/index.html', body: 'Strengthen the ID habits that matter most during seasonal turnover.' },
    ],
    'migration-tools': [
      { title: 'Spring Bird Migration', href: '../spring-bird-migration/index.html', body: 'Zoom back out to the bigger seasonal rhythm.' },
      { title: 'Hawk Migration Explained', href: '../hawk-migration/index.html', body: 'Compare broad migration tracking with focused watch-site behavior.' },
      { title: 'Best Birding Apps in 2026', href: '../best-birding-apps/index.html', body: 'Keep your app stack practical and field-friendly.' },
    ],
    regional: [
      { title: 'Birdwatching for Beginners', href: '../birdwatching-for-beginners/index.html', body: 'Tie local species knowledge back to stronger all-purpose habits.' },
      { title: 'Spring Bird Migration', href: '../spring-bird-migration/index.html', body: 'See how seasonal movement changes what is likely in your area.' },
      { title: 'Backyard Birding for Beginners', href: '../backyard-birding-for-beginners/index.html', body: 'Turn regional familiarity into a repeatable neighborhood practice.' },
    ],
    'migration-event': [
      { title: 'Spring Bird Migration', href: '../spring-bird-migration/index.html', body: 'Step back into the broader seasonal movement picture.' },
      { title: 'How to Identify Hawks in Flight', href: '../how-to-identify-hawks/index.html', body: 'Sharpen the field marks and silhouettes that matter most at watch sites.' },
      { title: 'How to Use eBird to Track Migration in Real Time', href: '../how-to-use-ebird-migration/index.html', body: 'Add cleaner data-reading habits to your next hawkwatch.' },
    ],
    'gear-trust': [
      { title: 'Birdwatching for Beginners', href: '../birdwatching-for-beginners/index.html', body: 'Reconnect tool decisions to the field habits they are meant to support.' },
      { title: 'Essential Birding Gear for Beginners', href: '../essential-birding-gear-for-beginners/index.html', body: 'Keep your buying plan simple and field-ready.' },
      { title: 'How to Identify Birds', href: '../how-to-identify-birds/index.html', body: 'Make sure better tools are reinforcing better observation.' },
    ],
    editorial: [
      { title: 'Birdwatching for Beginners', href: '../birdwatching-for-beginners/index.html', body: 'Start with the clearest on-ramp into the journal.' },
      { title: 'Spring Bird Migration', href: '../spring-bird-migration/index.html', body: 'Follow one of the strongest seasonal coverage paths in the journal.' },
      { title: 'Birds in Texas', href: '../birds-in-texas/index.html', body: 'See how regional pages turn familiar birds into a steadier practice.' },
    ]
  };

  const items = recommendationsByCluster[cluster] || recommendationsByCluster.editorial;
  grid.innerHTML = items.map(item => `
    <article class="card panel" style="padding:1rem;">
      <h4 style="margin-top:0;">${item.title}</h4>
      <p style="color:var(--muted);">${item.body}</p>
      <a class="btn btn-secondary" href="${item.href}">Open article</a>
    </article>`).join('');
}

function renderMarquee() {
  const track = document.getElementById('bird-track');
  if (!track) return;
  const names = [
    'Warbler field journals',
    'State life lists',
    'Migration observation logs',
    'Quietly refined downloads',
    'Made for generous note-taking',
    'Seasonal paper rituals'
  ];
  const joined = names.map(item => `<span class="marquee-item">${item}</span>`).join('<span class="marquee-item" aria-hidden="true">•</span>');
  track.innerHTML = `${joined}<span class="marquee-item" aria-hidden="true">•</span>${joined}`;
}

function renderHome() {
  const target = document.getElementById('home-featured');
  if (target) {
    const featured = [...state.products]
      .sort((a, b) => Number(b.purchasable) - Number(a.purchasable))
      .slice(0, 6);
    target.innerHTML = featured.map((p, i) => productCard(p, i)).join('');
  }

  const countEl = document.getElementById('live-count');
  if (countEl) {
    const live = state.products.filter(p => p.purchasable).length;
    countEl.textContent = live > 0
      ? `${live} field-ready pieces are available for immediate download today.`
      : 'The collection is in preview while checkout finishes its final setup.';
  }
}

function uniq(arr) {
  return [...new Set(arr.filter(Boolean))].sort();
}

function renderShop() {
  const grid = document.getElementById('shop-grid');
  if (!grid) return;

  const typeSel = document.getElementById('filter-type');
  const speciesSel = document.getElementById('filter-species');
  const regionSel = document.getElementById('filter-region');
  const q = document.getElementById('filter-q');
  if (!typeSel || !speciesSel || !regionSel || !q) return;

  typeSel.innerHTML = '<option value="">All formats</option>' + uniq(state.products.map(p => p.type)).map(s => `<option>${escapeHtml(s)}</option>`).join('');
  speciesSel.innerHTML = '<option value="">All species</option>' + uniq(state.products.map(p => p.species)).map(s => `<option>${escapeHtml(s)}</option>`).join('');
  regionSel.innerHTML = '<option value="">All regions</option>' + uniq(state.products.map(p => p.region)).map(s => `<option>${escapeHtml(s)}</option>`).join('');

  function apply() {
    const needle = (q.value || '').toLowerCase().trim();
    state.filtered = state.products.filter(p => {
      if (typeSel.value && p.type !== typeSel.value) return false;
      if (speciesSel.value && p.species !== speciesSel.value) return false;
      if (regionSel.value && p.region !== regionSel.value) return false;
      if (needle) {
        const haystack = [p.title, p.sku, p.keyword, p.collection, p.region, p.species].join(' ').toLowerCase();
        if (!haystack.includes(needle)) return false;
      }
      return true;
    });

    grid.innerHTML = state.filtered.map((p, i) => productCard(p, i)).join('');
    initReveals();

    const total = document.getElementById('shop-count');
    if (total) total.textContent = `${state.filtered.length} pieces in the collection`;

    const note = document.getElementById('shop-live-note');
    if (note) {
      const liveVisible = state.filtered.filter(p => p.purchasable).length;
      note.textContent = liveVisible > 0
        ? `${liveVisible} are ready for checkout right now.`
        : 'Browse the collection while checkout-enabled releases are being staged.';
    }
  }

  [typeSel, speciesSel, regionSel, q].forEach(el => el.addEventListener('input', apply));
  apply();
}

function renderProductDetail() {
  const root = document.getElementById('product-detail');
  if (!root) return;
  const sku = new URLSearchParams(location.search).get('sku');
  const p = state.products.find(item => item.sku === sku) || state.products[0];
  if (!p) return;

  root.innerHTML = `
    <div class="card detail-image reveal">
      <img src="${p.image}" alt="Preview image for ${escapeHtml(p.title)}" onerror="this.onerror=null;this.src='https://picsum.photos/seed/field-feather-detail-fallback/1200/900';" />
    </div>
    <article class="card detail-card reveal delay-1">
      <p class="eyebrow">${escapeHtml(p.collection)}</p>
      <h1 class="section-title">${escapeHtml(p.title)}</h1>
      <p class="editorial-copy">A composed field companion for birders who want useful structure, generous writing space, and a product that feels as considered as the observations it holds.</p>
      <div class="detail-price-row">
        <span class="price">${money(p.price)}</span>
        ${badgeMarkup(p)}
      </div>
      <p class="microcopy">${escapeHtml(p.delivery)} &middot; Region focus: ${escapeHtml(p.region)} &middot; Species focus: ${escapeHtml(p.species)}</p>
      <div class="detail-actions">
        ${p.purchasable
          ? `<a class="btn btn-primary" href="${p.checkout_url}" target="_blank" rel="noopener">Purchase</a>`
          : '<span class="badge neutral">Coming Soon</span>'}
        <a class="btn btn-quiet" href="downloads.html">View more downloads</a>
      </div>
      <div class="tabs" role="tablist" aria-label="Product information tabs">
        <button class="tab-btn" role="tab" aria-selected="true" data-tab="desc">Overview</button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="specs">Details</button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="reviews">Notes</button>
      </div>
      <section class="tab-panel active" id="tab-desc" role="tabpanel">
        <p>Designed with clean hierarchy and quiet margins so sightings, seasonal observations, and route notes feel orderly from the first page to the last.</p>
      </section>
      <section class="tab-panel" id="tab-specs" role="tabpanel">
        <ul>
          <li>Collection: ${escapeHtml(p.collection)}</li>
          <li>Format: ${escapeHtml(p.type)}</li>
          <li>Delivery: ${escapeHtml(p.delivery)}</li>
          <li>Best for: ${escapeHtml(p.region)} birding sessions and personal record-keeping</li>
        </ul>
      </section>
      <section class="tab-panel" id="tab-reviews" role="tabpanel">
        <p>Customer notes will appear here as the collection grows. For now, each release is written to feel thoughtful, useful, and easy to revisit season after season.</p>
      </section>
    </article>`;

  const tabs = root.querySelectorAll('.tab-btn');
  tabs.forEach(button => {
    button.addEventListener('click', () => {
      tabs.forEach(tab => tab.setAttribute('aria-selected', 'false'));
      button.setAttribute('aria-selected', 'true');
      root.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
      root.querySelector(`#tab-${button.dataset.tab}`).classList.add('active');
    });
  });

  const related = document.getElementById('related-grid');
  if (related) {
    const items = state.products.filter(item => item.collection === p.collection && item.sku !== p.sku).slice(0, 4);
    related.innerHTML = items.map((item, i) => productCard(item, i)).join('');
  }
}

function renderDownloads() {
  const grid = document.getElementById('downloads-grid');
  if (!grid) return;
  const items = state.products.filter(p => p.type === 'Digital Download');
  grid.innerHTML = items.map((p, i) => productCard(p, i)).join('');

  const total = document.getElementById('downloads-count');
  if (total) total.textContent = `${items.length} instant-download pieces currently shown.`;
}

(async function boot() {
  initTheme();
  initTopbarScroll();
  initMobileNav();
  initParallax();
  renderMarquee();
  initNewsletterAttribution();
  initNewsletterWelcomeContext();
  initMorningWarblerRecommendations();

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  try {
    await loadProducts();
  } catch (error) {
    document.querySelectorAll('[data-catalog-error]').forEach(node => {
      node.textContent = 'The catalog is being refreshed. Please try again in a moment.';
    });
    return;
  }

  [renderHome, renderShop, renderProductDetail, renderDownloads].forEach(fn => {
    try {
      fn();
    } catch (error) {
      console.error(error);
    }
  });

  initReveals();
})();
