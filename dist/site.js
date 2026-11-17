(() => {
  'use strict';

  const menu = document.getElementById('menu');
  const links = document.getElementById('navlinks');
  const progress = document.getElementById('progress');
  const compact = matchMedia('(max-width: 1100px)');
  const navigation = [...links.querySelectorAll('a[href^="#"]')];

  function closeMenu(restoreFocus = false) {
    links.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', 'Abrir menú');
    if (restoreFocus) menu.focus();
  }

  menu.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });
  navigation.forEach(link => link.addEventListener('click', () => closeMenu()));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && links.classList.contains('open')) {
      closeMenu(true);
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('header')) closeMenu();
  });
  links.addEventListener('focusout', event => {
    if (!links.contains(event.relatedTarget) && event.relatedTarget !== menu) {
      closeMenu();
    }
  });
  compact.addEventListener('change', () => closeMenu());
  document.addEventListener('presentationopen', () => closeMenu());
  // Collapse navigation only after its controls have been wired up.
  document.documentElement.classList.add('nav-ready');
  menu.hidden = false;

  const sections = [...document.querySelectorAll('main section[id]')];
  function updateScroll() {
    const height = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${height > 0 ? Math.min(100, scrollY / height * 100) : 0}%`;
    const current = sections.filter(section => section.getBoundingClientRect().top <= 120).at(-1);
    navigation.forEach(link => {
      const active = current?.id === link.hash.slice(1);
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  let scheduled = false;
  function scheduleUpdate() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      updateScroll();
      scheduled = false;
    });
  }
  addEventListener('scroll', scheduleUpdate, { passive: true });
  addEventListener('resize', scheduleUpdate);
  addEventListener('load', scheduleUpdate);
  document.fonts?.ready.then(scheduleUpdate);
  updateScroll();

  // Content is always visible; animate only elements as they enter the viewport.
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        if (!reduce.matches) {
          entry.target.animate(
            [{ opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'none' }],
            { duration: 650, easing: 'ease-out' },
          );
        }
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('[data-reveal]').forEach(element => observer.observe(element));
  }
})();
