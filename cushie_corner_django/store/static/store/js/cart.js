// Cart page specific JS
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(cookie => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}

function updateTotals(total, cartCount) {
  ['cart-total', 'cart-total-2'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = '₹' + parseFloat(total).toFixed(2);
  });
  const badge = document.getElementById('cart-badge');
  if (badge) badge.textContent = cartCount;
}

function removeItem(itemId) {
  const row = document.getElementById('cart-item-' + itemId);
  if (row) {
    row.style.transition = 'all 0.4s ease';
    row.style.opacity = '0';
    row.style.transform = 'translateX(40px)';
  }
  fetch('/api/remove-from-cart/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify({ item_id: itemId })
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      setTimeout(() => {
        if (row) row.remove();
        updateTotals(data.total, data.cart_count);
        if (data.cart_count === 0) location.reload();
      }, 400);
    }
  });
}

function updateQty(itemId, newQty) {
  if (newQty < 1) { removeItem(itemId); return; }
  const qtyEl = document.getElementById('qty-' + itemId);
  if (qtyEl) qtyEl.textContent = newQty;

  fetch('/api/update-cart/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify({ item_id: itemId, quantity: newQty })
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) updateTotals(data.total, data.cart_count);
    // Update qty buttons to use new qty
    const row = document.getElementById('cart-item-' + itemId);
    if (row) {
      const btns = row.querySelectorAll('.qty-btn');
      btns[0].setAttribute('onclick', `updateQty(${itemId}, ${newQty - 1})`);
      btns[1].setAttribute('onclick', `updateQty(${itemId}, ${newQty + 1})`);
    }
  });
}
