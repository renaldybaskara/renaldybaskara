document.documentElement.classList.add('js');

document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealTargets = document.querySelectorAll('.reveal, .project, .skill-grid article');

if (!reducedMotion && 'IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  revealTargets.forEach((target) => revealObserver.observe(target));
} else {
  revealTargets.forEach((target) => target.classList.add('is-visible'));
}

const navLinks = [...document.querySelectorAll('nav a[href^="#"]')];
const navSections = navLinks.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
if ('IntersectionObserver' in window && navSections.length) {
  const navObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navLinks.forEach((link) => {
        link.classList.toggle('is-current', link.getAttribute('href') === `#${entry.target.id}`);
      });
    });
  }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });
  navSections.forEach((section) => navObserver.observe(section));
}


const imageDialog = document.querySelector('.image-dialog');
if (imageDialog && typeof imageDialog.showModal === 'function') {
  const dialogImage = imageDialog.querySelector('[data-dialog-image]');
  const closeDialog = imageDialog.querySelector('[data-close-dialog]');
  document.querySelectorAll('[data-preview-src]').forEach((preview) => {
    preview.addEventListener('click', () => {
      dialogImage.src = preview.dataset.previewSrc;
      dialogImage.alt = preview.dataset.previewAlt;
      imageDialog.showModal();
    });
  });
  closeDialog.addEventListener('click', () => imageDialog.close());
  imageDialog.addEventListener('click', (event) => {
    if (event.target === imageDialog) imageDialog.close();
  });
}
