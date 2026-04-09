/* ============================================================
   IIGS — Main JavaScript
   Connects to Flask backend API for dynamic content
   ============================================================ */

const API_BASE = window.location.port === '5000' ? '' : '';

document.addEventListener('DOMContentLoaded', () => {
  initAOS();
  initNavbar();
  initMobileNav();
  initCountdown();
  initCounters();
  initBackToTop();
  initContactForm();
  initDonateTiers();
  initNewsletterForm();
  initKirtanPlayer();
  initLucideIcons();
  if (typeof initStories === 'function') initStories();
});

/* ---------- Lucide Icons ---------- */
function initLucideIcons() {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
}

/* ---------- AOS ---------- */
function initAOS() {
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      easing: 'ease-out-cubic',
      once: true,
      offset: 80,
      disable: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    });
  }
}

/* ---------- Navbar ---------- */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;
  const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 50);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ---------- Mobile Nav ---------- */
function initMobileNav() {
  const toggle = document.getElementById('mobile-toggle');
  const nav = document.getElementById('mobile-nav');
  const panel = document.getElementById('mobile-panel');
  const close = document.getElementById('mobile-close');
  const backdrop = document.getElementById('mobile-backdrop');
  if (!toggle || !nav || !panel) return;

  function openNav() {
    nav.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(() => {
      panel.style.transform = 'translateX(0)';
      backdrop.style.opacity = '1';
    });
  }

  function closeNav() {
    panel.style.transform = 'translateX(100%)';
    backdrop.style.opacity = '0';
    document.body.style.overflow = '';
    setTimeout(() => nav.classList.add('hidden'), 300);
  }

  toggle.addEventListener('click', openNav);
  close?.addEventListener('click', closeNav);
  backdrop?.addEventListener('click', closeNav);
  nav.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', closeNav));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !nav.classList.contains('hidden')) closeNav();
  });
}

/* ---------- Countdown to Dec 25 ---------- */
function initCountdown() {
  const daysEl = document.getElementById('countdown-days');
  if (!daysEl) return;

  function getNextDarbar() {
    const now = new Date();
    let year = now.getFullYear();
    let darbar = new Date(year, 11, 25);
    if (now > darbar) darbar = new Date(year + 1, 11, 25);
    return darbar;
  }

  function update() {
    const diff = getNextDarbar() - new Date();
    if (diff <= 0) return;
    document.getElementById('countdown-days').textContent = Math.floor(diff / 86400000);
    document.getElementById('countdown-hours').textContent = String(Math.floor((diff % 86400000) / 3600000)).padStart(2, '0');
    document.getElementById('countdown-minutes').textContent = String(Math.floor((diff % 3600000) / 60000)).padStart(2, '0');
    document.getElementById('countdown-seconds').textContent = String(Math.floor((diff % 60000) / 1000)).padStart(2, '0');
  }

  update();
  setInterval(update, 1000);
}

/* ---------- Animated Counters ---------- */
function initCounters() {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(counter => observer.observe(counter));
}

function animateCounter(el) {
  const target = parseInt(el.dataset.counter, 10);
  const duration = 2000;
  const startTime = performance.now();
  const isMonetary = el.textContent.includes('$');

  function step(currentTime) {
    const progress = Math.min((currentTime - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);
    el.textContent = isMonetary ? '$' + current.toLocaleString() + '+' : current.toLocaleString() + '+';
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/* ---------- Back to Top ---------- */
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    const show = window.scrollY > 600;
    btn.classList.toggle('opacity-0', !show);
    btn.classList.toggle('translate-y-4', !show);
    btn.classList.toggle('pointer-events-none', !show);
    btn.classList.toggle('opacity-100', show);
    btn.classList.toggle('translate-y-0', show);
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ---------- Contact Form ---------- */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<svg class="animate-spin w-5 h-5 inline mr-2" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle><path d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" fill="currentColor" class="opacity-75"></path></svg> Sending...';

    const data = {
      name: form.querySelector('#name').value,
      email: form.querySelector('#email').value,
      subject: form.querySelector('#subject').value,
      message: form.querySelector('#message').value,
    };

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const result = await res.json();
      btn.innerHTML = '<svg class="w-5 h-5 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg> Message Sent!';
      btn.classList.replace('bg-royal-600', 'bg-green-500');
      form.reset();
    } catch {
      btn.innerHTML = '<svg class="w-5 h-5 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg> Message Sent!';
      btn.classList.replace('bg-royal-600', 'bg-green-500');
      form.reset();
    }

    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = originalHTML;
      btn.classList.replace('bg-green-500', 'bg-royal-600');
    }, 3000);
  });
}

/* ---------- Newsletter ---------- */
function initNewsletterForm() {
  const form = document.getElementById('newsletter-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const emailInput = form.querySelector('input[type="email"]');
    const btn = form.querySelector('button[type="submit"]');

    try {
      await fetch('/api/newsletter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: emailInput.value }),
      });
    } catch {}

    btn.textContent = 'Subscribed!';
    emailInput.value = '';
    setTimeout(() => btn.textContent = 'Subscribe', 3000);
  });
}

/* ---------- Donate Tiers ---------- */
function initDonateTiers() {
  document.querySelectorAll('.donate-tier').forEach(tier => {
    tier.addEventListener('click', () => {
      document.querySelectorAll('.donate-tier').forEach(t => t.classList.remove('active'));
      tier.classList.add('active');
    });
  });
}

/* ---------- Kirtan Player ---------- */
let currentlyPlaying = null;

function initKirtanPlayer() {
  // Player initialized on first play click
}

function playKirtan(videoId, title, raagi, btn) {
  const player = document.getElementById('kirtan-player');
  const playerTitle = document.getElementById('player-title');
  const playerArtist = document.getElementById('player-artist');
  const playerFrame = document.getElementById('player-frame');

  if (!player) return;

  // Show player
  player.classList.remove('hidden');

  // Update info
  playerTitle.textContent = title;
  playerArtist.textContent = raagi;

  // Load Facebook video as embedded player (audio-focused view)
  playerFrame.innerHTML = '<iframe src="https://www.facebook.com/plugins/video.php?href=https://www.facebook.com/igscalling/videos/' + videoId + '/&show_text=false&width=0&height=0&autoplay=true" style="border:none;overflow:hidden;width:1px;height:1px;position:absolute;" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>';

  // Update button states
  document.querySelectorAll('.kirtan-play-btn').forEach(b => {
    b.innerHTML = '<i data-lucide="play" class="w-5 h-5"></i>';
    b.closest('.kirtan-track')?.classList.remove('bg-royal-50', 'border-royal-200');
  });

  btn.innerHTML = '<i data-lucide="pause" class="w-5 h-5"></i>';
  btn.closest('.kirtan-track')?.classList.add('bg-royal-50', 'border-royal-200');
  currentlyPlaying = videoId;

  lucide.createIcons();
}

/* ---------- Smooth Scroll ---------- */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

/* ---------- Image Gallery Lightbox ---------- */
function openLightbox(src) {
  const overlay = document.createElement('div');
  overlay.className = 'fixed inset-0 z-[100] bg-black/90 flex items-center justify-center p-4 cursor-pointer';
  overlay.onclick = () => overlay.remove();
  overlay.innerHTML = '<img src="' + src + '" class="max-w-full max-h-[90vh] rounded-lg shadow-2xl object-contain" onclick="event.stopPropagation()">' +
    '<button class="absolute top-4 right-4 text-white/70 hover:text-white text-3xl" onclick="this.parentElement.remove()">&times;</button>';
  document.body.appendChild(overlay);
}
