const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');

function closeMenu() {
  menuButton?.setAttribute('aria-expanded', 'false');
  nav?.classList.remove('is-open');
}

menuButton?.addEventListener('click', () => {
  const opening = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(opening));
  nav.classList.toggle('is-open', opening);
});

document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});

nav?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});

const lensInsights = {
  framing: 'One account emphasizes protection; the other, loss of access. The underlying event is the same.',
  event: 'Both accounts describe a city closing a park after heavy rain. This shared event gives us a basis for comparison.',
  actor: 'Both accounts identify the city as the actor. Their different emphases can still shape how a reader understands its action.'
};

document.querySelectorAll('[data-lens-button]').forEach(button => {
  button.addEventListener('click', () => {
    const lens = button.dataset.lensButton;
    document.querySelector('.story-board').dataset.lens = lens;
    document.querySelectorAll('[data-lens-button]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    document.querySelector('.lens-insight').textContent = lensInsights[lens];
  });
});
