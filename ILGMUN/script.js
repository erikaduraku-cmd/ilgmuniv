const nav = document.getElementById('site-nav');
const navToggle = document.querySelector('.nav-toggle');

if (nav && navToggle) {
  navToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
    navToggle.textContent = isOpen ? '×' : '☰';
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.textContent = '☰';
    });
  });
}

const target = new Date('2026-11-13T00:00:00+01:00').getTime();

function tick() {
  let diff = Math.max(0, target - Date.now());
  const days = Math.floor(diff / 86400000);
  diff -= days * 86400000;
  const hours = Math.floor(diff / 3600000);
  diff -= hours * 3600000;
  const minutes = Math.floor(diff / 60000);
  diff -= minutes * 60000;
  const seconds = Math.floor(diff / 1000);

  [
    ['days', days],
    ['hours', hours],
    ['minutes', minutes],
    ['seconds', seconds],
  ].forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) element.textContent = String(value).padStart(2, '0');
  });
}

tick();
setInterval(tick, 1000);

function setupModal(modalId, openSelector, closeSelector) {
  const modal = document.getElementById(modalId);
  const openButton = document.querySelector(openSelector);
  const closeButtons = document.querySelectorAll(closeSelector);

  if (!modal || !openButton) return;

  function openModal() {
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-lock');
  }

  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-lock');
  }

  openButton.addEventListener('click', openModal);
  closeButtons.forEach((button) => button.addEventListener('click', closeModal));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeModal();
  });
}

setupModal('ilgmun1-modal', '[data-open-ilgmun1]', '[data-close-ilgmun1]');
setupModal('ilgmun2-modal', '[data-open-ilgmun2]', '[data-close-ilgmun2]');
