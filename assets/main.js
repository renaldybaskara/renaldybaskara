document.documentElement.classList.add('js');
document.querySelectorAll('[data-year]').forEach((node) => { node.textContent = new Date().getFullYear(); });
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll('.section, .project, .skill-grid article').forEach((node) => observer.observe(node));
}
