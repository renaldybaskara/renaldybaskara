document.documentElement.classList.add('js');

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const body = document.body;

document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

if (reducedMotion) {
  body.classList.add('ready');
} else {
  window.addEventListener('load', () => {
    window.requestAnimationFrame(() => body.classList.add('ready'));
  });
}

const revealTargets = [...document.querySelectorAll('.reveal')];
if (!reducedMotion && 'IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6%' });
  revealTargets.forEach((target) => revealObserver.observe(target));
} else {
  revealTargets.forEach((target) => target.classList.add('is-visible'));
}

const navLinks = [...document.querySelectorAll('nav a[href^="#"]')];
const navSections = navLinks
  .map((link) => document.querySelector(link.getAttribute('href')))
  .filter(Boolean);
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

const projectRail = document.querySelector('#project-rail');
const projectCards = projectRail ? [...projectRail.querySelectorAll('[data-project]')] : [];
const projectPrev = document.querySelector('[data-project-prev]');
const projectNext = document.querySelector('[data-project-next]');
let projectTimer = null;
let projectPaused = false;

function nearestProjectIndex() {
  if (!projectRail || !projectCards.length) return 0;
  return projectCards.reduce((best, card, index) => (
    Math.abs(card.offsetLeft - projectRail.scrollLeft) < Math.abs(projectCards[best].offsetLeft - projectRail.scrollLeft)
      ? index
      : best
  ), 0);
}

function moveProject(direction = 1) {
  if (!projectRail || !projectCards.length) return;
  const nextIndex = (nearestProjectIndex() + direction + projectCards.length) % projectCards.length;
  projectRail.scrollTo({ left: projectCards[nextIndex].offsetLeft - 2, behavior: reducedMotion ? 'auto' : 'smooth' });
}

function stopProjectAutoplay() {
  window.clearInterval(projectTimer);
  projectTimer = null;
}

function startProjectAutoplay() {
  stopProjectAutoplay();
  if (reducedMotion || projectPaused || document.hidden || body.classList.contains('drawer-open') || projectCards.length < 2) return;
  projectTimer = window.setInterval(() => moveProject(1), 4600);
}

function pauseProjectAutoplay() {
  projectPaused = true;
  stopProjectAutoplay();
}

function resumeProjectAutoplay() {
  projectPaused = false;
  startProjectAutoplay();
}

if (projectRail) {
  ['mouseenter', 'focusin', 'pointerdown', 'touchstart'].forEach((eventName) => {
    projectRail.addEventListener(eventName, pauseProjectAutoplay, { passive: true });
  });
  ['mouseleave', 'focusout', 'pointerup', 'touchend'].forEach((eventName) => {
    projectRail.addEventListener(eventName, resumeProjectAutoplay, { passive: true });
  });
  projectRail.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') { event.preventDefault(); moveProject(1); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); moveProject(-1); }
  });
  startProjectAutoplay();
}
projectPrev?.addEventListener('click', () => { moveProject(-1); startProjectAutoplay(); });
projectNext?.addEventListener('click', () => { moveProject(1); startProjectAutoplay(); });
document.addEventListener('visibilitychange', () => {
  if (document.hidden) stopProjectAutoplay();
  else startProjectAutoplay();
});

const projectDataNode = document.querySelector('#project-data');
let projectData = {};
try {
  projectData = projectDataNode ? JSON.parse(projectDataNode.textContent) : {};
} catch (error) {
  console.error('Unable to read project data.', error);
}

const drawer = document.querySelector('#project-drawer');
const drawerOverlay = document.querySelector('[data-drawer-overlay]');
const drawerClose = document.querySelector('[data-drawer-close]');
const drawerType = document.querySelector('[data-drawer-type]');
const drawerTitle = document.querySelector('[data-drawer-title]');
const drawerDescription = document.querySelector('[data-drawer-description]');
const drawerDetails = document.querySelector('[data-drawer-details]');
const drawerTags = document.querySelector('[data-drawer-tags]');
const drawerActions = document.querySelector('[data-drawer-actions]');
const gallery = document.querySelector('[data-gallery]');
const gallerySlides = document.querySelector('[data-gallery-slides]');
const galleryControls = document.querySelector('[data-gallery-controls]');
const galleryStatus = document.querySelector('[data-gallery-status]');
const galleryPrev = document.querySelector('[data-gallery-prev]');
const galleryNext = document.querySelector('[data-gallery-next]');

let activeProject = null;
let activeImages = [];
let activeImageIndex = 0;
let galleryTimer = null;
let drawerOpener = null;

function stopGalleryAutoplay() {
  window.clearInterval(galleryTimer);
  galleryTimer = null;
}

function renderGallery() {
  if (!gallerySlides || !galleryStatus || !galleryControls || !gallery) return;
  [...gallerySlides.children].forEach((image, index) => {
    image.classList.toggle('is-active', index === activeImageIndex);
    image.setAttribute('aria-hidden', index === activeImageIndex ? 'false' : 'true');
  });
  gallery.classList.toggle('is-empty', activeImages.length === 0);
  galleryControls.hidden = activeImages.length <= 1;
  galleryStatus.textContent = activeImages.length ? `${activeImageIndex + 1} / ${activeImages.length}` : '';
}

function moveGallery(direction = 1) {
  if (activeImages.length < 2) return;
  activeImageIndex = (activeImageIndex + direction + activeImages.length) % activeImages.length;
  renderGallery();
}

function startGalleryAutoplay() {
  stopGalleryAutoplay();
  if (reducedMotion || document.hidden || activeImages.length < 2 || !body.classList.contains('drawer-open')) return;
  galleryTimer = window.setInterval(() => moveGallery(1), 3500);
}

function createDetails(details) {
  if (!drawerDetails) return;
  drawerDetails.replaceChildren();
  details.forEach(([term, description]) => {
    const row = document.createElement('div');
    const dt = document.createElement('dt');
    const dd = document.createElement('dd');
    dt.textContent = term;
    dd.textContent = description;
    row.append(dt, dd);
    drawerDetails.append(row);
  });
}

function createTags(tags) {
  if (!drawerTags) return;
  drawerTags.replaceChildren();
  tags.forEach((tag) => {
    const item = document.createElement('li');
    item.textContent = tag;
    drawerTags.append(item);
  });
}

function createActions(actions) {
  if (!drawerActions) return;
  drawerActions.replaceChildren();
  actions.forEach(({ label, url }) => {
    const link = document.createElement('a');
    link.className = 'button button-primary';
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = label;
    drawerActions.append(link);
  });
}

function createGallery(images) {
  if (!gallerySlides) return;
  gallerySlides.replaceChildren();
  activeImages = images;
  activeImageIndex = 0;
  images.forEach(({ src, alt }) => {
    const image = document.createElement('img');
    image.src = src;
    image.alt = alt;
    image.loading = 'eager';
    gallerySlides.append(image);
  });
  renderGallery();
  startGalleryAutoplay();
}

function focusableDrawerElements() {
  if (!drawer) return [];
  return [...drawer.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')]
    .filter((element) => !element.hidden && element.offsetParent !== null);
}

function trapDrawerFocus(event) {
  if (event.key !== 'Tab' || !body.classList.contains('drawer-open')) return;
  const focusable = focusableDrawerElements();
  if (!focusable.length) { event.preventDefault(); drawer.focus(); return; }
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
  if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
}

function openProject(projectId, opener) {
  const project = projectData[projectId];
  if (!project || !drawer || !drawerOverlay) return;
  activeProject = projectId;
  drawerOpener = opener || document.activeElement;
  drawerType.textContent = project.type;
  drawerTitle.textContent = project.title;
  drawerDescription.textContent = project.description;
  createDetails(project.details || []);
  createTags(project.tags || []);
  createActions(project.actions || []);
  createGallery(project.images || []);
  drawerOverlay.hidden = false;
  drawer.setAttribute('aria-hidden', 'false');
  body.classList.add('drawer-open');
  window.requestAnimationFrame(() => {
    drawerOverlay.classList.add('is-open');
    drawer.classList.add('is-open');
    drawerClose?.focus();
  });
  stopProjectAutoplay();
}

function closeProject() {
  if (!drawer || !drawerOverlay || !body.classList.contains('drawer-open')) return;
  stopGalleryAutoplay();
  drawer.classList.remove('is-open');
  drawerOverlay.classList.remove('is-open');
  drawer.setAttribute('aria-hidden', 'true');
  body.classList.remove('drawer-open');
  const finishClose = () => {
    drawerOverlay.hidden = true;
    activeProject = null;
    drawerOpener?.focus();
    drawerOpener = null;
    startProjectAutoplay();
  };
  if (reducedMotion) finishClose();
  else window.setTimeout(finishClose, 580);
}

projectCards.forEach((card) => {
  card.addEventListener('click', () => openProject(card.dataset.project, card));
});
drawerClose?.addEventListener('click', closeProject);
drawerOverlay?.addEventListener('click', closeProject);
galleryPrev?.addEventListener('click', () => { moveGallery(-1); startGalleryAutoplay(); });
galleryNext?.addEventListener('click', () => { moveGallery(1); startGalleryAutoplay(); });
gallery?.addEventListener('mouseenter', stopGalleryAutoplay);
gallery?.addEventListener('mouseleave', startGalleryAutoplay);
gallery?.addEventListener('focusin', stopGalleryAutoplay);
gallery?.addEventListener('focusout', startGalleryAutoplay);

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && activeProject) closeProject();
  trapDrawerFocus(event);
});
