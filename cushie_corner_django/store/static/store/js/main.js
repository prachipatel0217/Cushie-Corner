// ===== PRELOADER =====
window.addEventListener('load', () => {
  setTimeout(() => {
    const preloader = document.getElementById('preloader');
    if (preloader) preloader.classList.add('hidden');
  }, 1800);
});

// ===== NAVBAR SCROLL =====
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });
}

// ===== HAMBURGER MENU =====
const hamburger = document.getElementById('hamburger');
const menu = document.getElementById('menu');
if (hamburger && menu) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    menu.classList.toggle('open');
  });
  // Close on nav link click
  menu.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('open');
      menu.classList.remove('open');
    });
  });
}

// ===== SCROLL REVEAL =====
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 80);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal-card, .reveal-left, .reveal-right').forEach(el => {
  revealObserver.observe(el);
});

// ===== TOAST NOTIFICATION =====
function showToast(message, duration = 3000) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), duration);
}

// ===== ADD TO CART =====
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function addToCart(productId, btn) {
  if (btn) {
    btn.classList.add('loading');
    btn.disabled = true;
  }
  fetch('/api/add-to-cart/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify({ product_id: productId })
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      showToast(data.message || 'Added to cart!');
      const badge = document.getElementById('cart-badge');
      if (badge) {
        badge.textContent = data.cart_count;
        badge.style.transform = 'scale(1.4)';
        setTimeout(() => badge.style.transform = '', 300);
      }
    }
  })
  .catch(() => showToast('Something went wrong. Please try again.'))
  .finally(() => {
    if (btn) {
      btn.classList.remove('loading');
      btn.disabled = false;
    }
  });
}

// ===== CONTACT FORM =====
const contactForm = document.getElementById('contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = contactForm.querySelector('.submit-btn');
    btn.disabled = true;
    btn.querySelector('span').textContent = 'Sending...';

    const formData = new FormData(contactForm);
    const data = Object.fromEntries(formData.entries());

    fetch('/api/contact/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(res => {
      if (res.success) {
        showToast(res.message);
        contactForm.reset();
      } else {
        showToast(res.message || 'Please fill in all fields.');
      }
    })
    .catch(() => showToast('Something went wrong.'))
    .finally(() => {
      btn.disabled = false;
      btn.querySelector('span').textContent = 'Send Message';
    });
  });
}

// ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ===== STAGGER REVEAL ON PRODUCTS =====
document.querySelectorAll('.reveal-card').forEach((card, i) => {
  card.style.transitionDelay = `${i * 60}ms`;
});
