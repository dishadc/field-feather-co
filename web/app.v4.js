const state = { products: [], filtered: [] };

async function loadProducts() {
  const res = await fetch('products.json');
  const raw = await res.json();
  state.products = raw.map(normalizeProduct);
  state.filtered = [...state.products];
}

function money(v) { return `$${Number(v || 0).toFixed(2)}`; }

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
  if (sku.includes('STATE')) return 'Regional';
  if (sku.includes('MIGRATION')) return 'Seasonal';
  if (sku.includes('WARBLER')) return 'Species';
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
  const m = (p.sku || '').match(/DIGI-STATE-([A-Z-]+)/);
  if (m) return m[1].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  return 'United States';
}

function deliveryLine(type) {
  return type === 'Print-on-Demand' ? 'Print-on-Demand · Ships in 3–5 days' : 'Digital Download · PDF';
}

function resolveImage(p) {
  if (p.image && /^https?:\/\//.test(p.image)) return p.image;
  return `https://picsum.photos/seed/${seed(p.sku || p.title || p.keyword || 'bird')}/400/300`;
}

function normalizeProduct(p) {
  const type = inferType(p);
  return {
    ...p,
    type,
    collection: inferCollection(p),
    species: inferSpecies(p),
    region: inferRegion(p),
    delivery: p.delivery || deliveryLine(type),
    image: resolveImage(p)
  };
}

function productCard(p, i = 0, feature = false) {
  const hasLink = p.checkout_url && p.checkout_url.startsWith('http');
  const featureClass = feature ? 'feature-span' : '';
  return `
  <article class="card product-card ${featureClass} reveal delay-${i % 4}">
    <figure>
      <img class="product-thumb" src="${p.image}" alt="Preview of ${p.title}" loading="lazy" onerror="this.onerror=null; this.src='https://picsum.photos/seed/${seed(p.sku || p.title)}/400/300';" />
    </figure>
    <div class="product-meta">
      <div class="badges"><span class="badge">${p.type}</span>${p.sku.includes('WARBLER') ? '<span class="badge">Limited Edition</span>' : ''}</div>
      <h3>${p.title}</h3>
      <p class="price">${money(p.price)}</p>
      <p class="meta-line"><small>${p.delivery}</small></p>
      <div class="card-actions" style="display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.6rem;">
        ${hasLink ? `<a class="btn btn-primary" href="${p.checkout_url}" target="_blank" rel="noopener">Add to Cart</a>` : ''}
        <a class="btn btn-secondary" href="product.html?sku=${encodeURIComponent(p.sku)}">Details →</a>
      </div>
    </div>
  </article>`;
}

function initTheme() {
  const root = document.documentElement;
  const pref = localStorage.getItem('ff-theme');
  if (pref === 'dark' || pref === 'light') root.setAttribute('data-theme', pref);
  const toggles = document.querySelectorAll('[data-theme-toggle]');
  toggles.forEach(btn => btn.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('ff-theme', next);
  }));
}

function initTopbarScroll() {
  const bar = document.querySelector('.topbar');
  if (!bar) return;
  const update = () => bar.classList.toggle('scrolled', window.scrollY > 8);
  window.addEventListener('scroll', update, { passive: true });
  update();
}

function initParallax() {
  const art = document.querySelector('[data-parallax]');
  if (!art) return;
  window.addEventListener('scroll', () => {
    const y = Math.min(18, window.scrollY * 0.045);
    art.style.setProperty('--parallax', `${y}px`);
  }, { passive: true });
}

function renderHome() {
  const target = document.getElementById('home-featured');
  if (!target) return;
  const featured = [...state.products].sort((a,b) => (b.checkout_url ? 1 : 0) - (a.checkout_url ? 1 : 0)).slice(0,6);
  target.innerHTML = featured.map((p, i) => productCard(p, i, i===0)).join('');

  const countEl = document.getElementById('live-count');
  if (countEl) {
    const live = state.products.filter(p => p.checkout_url && p.checkout_url.startsWith('http')).length;
    countEl.textContent = `${live} live downloads now available`;
  }
}

function uniq(arr) { return [...new Set(arr.filter(Boolean))].sort(); }

function renderShop() {
  const grid = document.getElementById('shop-grid');
  if (!grid) return;

  const typeSel = document.getElementById('filter-type');
  const speciesSel = document.getElementById('filter-species');
  const regionSel = document.getElementById('filter-region');
  const q = document.getElementById('filter-q');
  if (!typeSel || !speciesSel || !regionSel || !q) return;

  speciesSel.innerHTML = '<option value="">All species</option>' + uniq(state.products.map(p => p.species)).map(s => `<option>${s}</option>`).join('');
  regionSel.innerHTML = '<option value="">All regions</option>' + uniq(state.products.map(p => p.region)).map(r => `<option>${r}</option>`).join('');

  function apply() {
    const needle = (q.value || '').toLowerCase().trim();
    state.filtered = state.products.filter(p => {
      if (typeSel.value && p.type !== typeSel.value) return false;
      if (speciesSel.value && p.species !== speciesSel.value) return false;
      if (regionSel.value && p.region !== regionSel.value) return false;
      if (needle && !(String(p.title).toLowerCase().includes(needle) || String(p.sku).toLowerCase().includes(needle) || String(p.keyword || '').toLowerCase().includes(needle))) return false;
      return true;
    });
    grid.innerHTML = state.filtered.map((p,i) => productCard(p,i)).join('');
    const total = document.getElementById('shop-count');
    if (total) total.textContent = `${state.filtered.length} products`;
  }

  [typeSel, speciesSel, regionSel, q].forEach(el => el && el.addEventListener('input', apply));
  apply();
}

function renderProductDetail() {
  const root = document.getElementById('product-detail');
  if (!root) return;
  const sku = new URLSearchParams(location.search).get('sku');
  const p = state.products.find(x => x.sku === sku) || state.products[0];
  if (!p) return;

  const hasLink = p.checkout_url && p.checkout_url.startsWith('http');
  root.innerHTML = `
    <div class="card detail-image">
      <img src="${p.image}" alt="Preview image for ${p.title}" onerror="this.onerror=null; this.src='https://picsum.photos/seed/${seed(p.sku || p.title)}/800/600';" />
    </div>
    <div class="card" style="padding:1rem 1.1rem;">
      <p class="eyebrow">${p.collection}</p>
      <h1 class="section-title" style="font-size:2.2rem; margin:.2rem 0 0.7rem;">${p.title}</h1>
      <p class="price" style="font-size:1.28rem; margin:.2rem 0 .8rem;">${money(p.price)}</p>
      <p class="meta-line">${p.delivery}</p>
      ${hasLink ? `<a class="btn btn-primary" href="${p.checkout_url}" target="_blank" rel="noopener">Add to Cart</a>` : ''}
      <div class="tabs" role="tablist" aria-label="Product info tabs">
        <button class="tab-btn" role="tab" aria-selected="true" data-tab="desc">Description</button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="specs">Specs</button>
        <button class="tab-btn" role="tab" aria-selected="false" data-tab="reviews">Reviews</button>
      </div>
      <section class="tab-panel active" id="tab-desc" role="tabpanel">
        <p>Every bird has a story. This download helps you record yours with clear, printable layouts and clean field-note structure.</p>
      </section>
      <section class="tab-panel" id="tab-specs" role="tabpanel">
        <ul>
          <li>Format: PDF / printable worksheet source</li>
          <li>Delivery: Instant digital download</li>
          <li>Use: Personal field journaling and life-list tracking</li>
          <li>Region focus: ${p.region}</li>
        </ul>
      </section>
      <section class="tab-panel" id="tab-reviews" role="tabpanel">
        <p>New release collection — customer review module activates as orders complete.</p>
      </section>
    </div>`;

  const tabs = root.querySelectorAll('.tab-btn');
  tabs.forEach(btn => btn.addEventListener('click', () => {
    tabs.forEach(b => b.setAttribute('aria-selected', 'false'));
    btn.setAttribute('aria-selected', 'true');
    root.querySelectorAll('.tab-panel').forEach(pn => pn.classList.remove('active'));
    root.querySelector('#tab-' + btn.dataset.tab).classList.add('active');
  }));

  const rel = document.getElementById('related-grid');
  if (rel) {
    const related = state.products.filter(x => x.collection === p.collection && x.sku !== p.sku).slice(0,4);
    rel.innerHTML = related.map((x,i) => productCard(x,i)).join('');
  }
}

function renderDownloads() {
  const grid = document.getElementById('downloads-grid');
  if (!grid) return;
  const all = state.products.filter(p => p.type === 'Digital Download');
  grid.innerHTML = all.map((p,i) => productCard(p,i, i % 7 === 0)).join('');
}

(async function boot() {
  initTheme();
  initTopbarScroll();
  initParallax();
  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  try {
    await loadProducts();
  } catch (e) {
    const targets = document.querySelectorAll('[data-catalog-error]');
    targets.forEach(t => t.textContent = 'Catalog is updating. Please refresh in a moment.');
    return;
  }

  [renderHome, renderShop, renderProductDetail, renderDownloads].forEach(fn => {
    try { fn(); } catch (e) { console.error(e); }
  });
})();
