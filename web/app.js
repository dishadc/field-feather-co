const grid = document.getElementById('product-grid');

fetch('products.json')
  .then(r => r.json())
  .then(products => {
    products.forEach(p => {
      const hasLink = p.checkout_url && p.checkout_url.startsWith('http');
      const el = document.createElement('article');
      el.className = 'product';
      el.innerHTML = `
        <span class="badge">${p.status}</span>
        <h3>${p.title}</h3>
        <p>SKU: ${p.sku}</p>
        <p class="price">$${p.price.toFixed(2)}</p>
        <p>SEO: ${p.keyword}</p>
        <p>Channel: ${p.channel.toUpperCase()}</p>
        <a class="buy ${hasLink ? '' : 'disabled'}" href="${hasLink ? p.checkout_url : '#'}" target="_blank" rel="noopener">${hasLink ? 'Buy now' : 'Checkout link pending'}</a>
      `;
      grid.appendChild(el);
    });
  })
  .catch(() => {
    grid.innerHTML = '<p>Unable to load product catalog.</p>';
  });
