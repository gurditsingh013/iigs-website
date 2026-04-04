/* ============================================================
   IIGS — Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize all modules
  initAOS();
  initNavbar();
  initMobileNav();
  initCountdown();
  initCounters();
  initBackToTop();
  initContactForm();
  initDonateTiers();
  initLucideIcons();
});

/* ---------- Lucide Icons ---------- */
function initLucideIcons() {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
}

/* ---------- AOS (Animate on Scroll) ---------- */
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

/* ---------- Navbar Scroll Effect ---------- */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  const onScroll = () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ---------- Mobile Navigation ---------- */
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

  // Close on nav link click
  nav.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', closeNav);
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !nav.classList.contains('hidden')) {
      closeNav();
    }
  });
}

/* ---------- Darbar-E-Khalsa Countdown ---------- */
function initCountdown() {
  const daysEl = document.getElementById('countdown-days');
  const hoursEl = document.getElementById('countdown-hours');
  const minutesEl = document.getElementById('countdown-minutes');
  const secondsEl = document.getElementById('countdown-seconds');

  if (!daysEl) return;

  // Next Darbar-E-Khalsa: December 25
  function getNextDarbar() {
    const now = new Date();
    let year = now.getFullYear();
    let darbar = new Date(year, 11, 25); // Dec 25
    if (now > darbar) {
      darbar = new Date(year + 1, 11, 25);
    }
    return darbar;
  }

  function update() {
    const now = new Date();
    const target = getNextDarbar();
    const diff = target - now;

    if (diff <= 0) {
      daysEl.textContent = '0';
      hoursEl.textContent = '0';
      minutesEl.textContent = '0';
      secondsEl.textContent = '0';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    daysEl.textContent = days;
    hoursEl.textContent = String(hours).padStart(2, '0');
    minutesEl.textContent = String(minutes).padStart(2, '0');
    secondsEl.textContent = String(seconds).padStart(2, '0');
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
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);

    if (isMonetary) {
      el.textContent = '$' + current.toLocaleString() + '+';
    } else {
      el.textContent = current.toLocaleString() + '+';
    }

    if (progress < 1) {
      requestAnimationFrame(step);
    }
  }

  requestAnimationFrame(step);
}

/* ---------- Back to Top ---------- */
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 600) {
      btn.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
      btn.classList.add('opacity-100', 'translate-y-0');
    } else {
      btn.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
      btn.classList.remove('opacity-100', 'translate-y-0');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* ---------- Contact Form ---------- */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const btn = form.querySelector('button[type="submit"]');
    const originalHTML = btn.innerHTML;

    // Show loading state
    btn.disabled = true;
    btn.innerHTML = `
      <svg class="animate-spin w-5 h-5" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
        <path d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" fill="currentColor" class="opacity-75"></path>
      </svg>
      Sending...
    `;

    // Simulate send (replace with actual API call)
    setTimeout(() => {
      btn.innerHTML = `
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>
        </svg>
        Message Sent!
      `;
      btn.classList.remove('bg-saffron-500', 'hover:bg-saffron-600');
      btn.classList.add('bg-green-500');

      form.reset();

      setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
        btn.classList.add('bg-saffron-500', 'hover:bg-saffron-600');
        btn.classList.remove('bg-green-500');
      }, 3000);
    }, 1500);
  });
}

/* ---------- Donation Tier Selection ---------- */
function initDonateTiers() {
  const tiers = document.querySelectorAll('.donate-tier');

  tiers.forEach(tier => {
    tier.addEventListener('click', () => {
      tiers.forEach(t => t.classList.remove('active'));
      tier.classList.add('active');
    });
  });
}

/* ---------- YouTube Lazy Load ---------- */
function loadYouTube(el) {
  const iframe = document.createElement('iframe');
  iframe.src = 'https://www.youtube.com/embed/?listType=user_uploads&list=iigscalling&autoplay=1';
  iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
  iframe.allowFullscreen = true;
  iframe.className = 'absolute inset-0 w-full h-full';
  el.innerHTML = '';
  el.appendChild(iframe);
  el.classList.remove('cursor-pointer');
}

/* ---------- Smooth scroll for anchor links ---------- */
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
