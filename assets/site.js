// En-tête : fond plein au défilement (accueil) + menu mobile
const header = document.querySelector('.site-header');
const nav = document.querySelector('.main-nav');
document.querySelector('.burger')?.addEventListener('click', e => {
  const open = nav.classList.toggle('open');
  header.classList.toggle('open', open);
  e.currentTarget.setAttribute('aria-expanded', open);
});
const announce = document.querySelector('.announce');
// hauteur réelle du bandeau, utilisée par le CSS pour que la photo d'accueil remplisse l'écran
const setAnn = () => document.documentElement.style.setProperty('--ann', (announce && !document.documentElement.classList.contains('announce-off') ? announce.offsetHeight : 0) + 'px');
setAnn(); addEventListener('resize', setAnn);
const onScroll = () => {
  header.classList.toggle('solid', scrollY > 60);
  // Accueil : l'en-tête fixe démarre sous le bandeau d'annonce
  if (document.body.classList.contains('home') && announce) header.style.top = Math.max(0, announce.offsetHeight - scrollY) + 'px';
};
addEventListener('resize', onScroll);
addEventListener('scroll', onScroll); onScroll();

// Apparition douce des blocs
const io = new IntersectionObserver(es => es.forEach(x => x.isIntersecting && x.target.classList.add('in')), { threshold: .12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Compte à rebours golf — remettre le bloc #count dans golf (_build.py) une fois la date fixée
const OPEN = new Date('2026-12-05T10:00:00');
const count = document.getElementById('count');
if (count) {
  const tick = () => {
    const s = Math.max(0, (OPEN - new Date()) / 1000), b = count.querySelectorAll('b');
    b[0].textContent = Math.floor(s / 86400); b[1].textContent = Math.floor(s % 86400 / 3600); b[2].textContent = Math.floor(s % 3600 / 60);
  };
  tick(); setInterval(tick, 30000);
}

// Formulaires "me prévenir" : ouvrent un e-mail prérempli (pas de serveur nécessaire)
document.querySelectorAll('form[data-subject]').forEach(f => f.addEventListener('submit', e => {
  e.preventDefault();
  const mail = f.querySelector('input[type=email]').value;
  location.href = 'mailto:emmanuelle.morel@leramet.fr?subject=' + encodeURIComponent(f.dataset.subject) +
    '&body=' + encodeURIComponent('Bonjour,\n\nMerci de me prévenir à cette adresse : ' + mail + '\n');
  f.innerHTML = '<p>Merci ! Votre messagerie s\'ouvre pour envoyer la demande.</p>';
}));

// La carte : onglet actif selon la section visible
const tabs = document.querySelectorAll('.menu-nav a');
if (tabs.length) {
  const secs = [...tabs].map(a => document.querySelector(a.getAttribute('href')));
  const mark = () => {
    let i = 0; secs.forEach((s, k) => { if (s.getBoundingClientRect().top < 200) i = k; });
    if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) i = secs.length - 1; // bas de page
    tabs.forEach((t, k) => t.classList.toggle('on', k === i));
  };
  addEventListener('scroll', mark); mark();
}

// Contact : surligner le jour actuel dans les horaires
const today = document.querySelector(`.hours tr[data-d="${new Date().getDay()}"]`);
today?.classList.add('today');

// Galerie : clic sur une photo -> visionneuse plein écran (flèches, clavier, glisser au doigt)
document.querySelectorAll('[data-gallery]').forEach(gallery => {
  // chaque visionneuse ne prend que ses propres photos (un carrousel peut être imbriqué dans la page)
  const items = [...gallery.querySelectorAll('a[data-caption]')].filter(a => a.parentElement.closest('[data-gallery]') === gallery);
  if (!items.length) return;
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Photos en grand');
  lb.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="lb-btn lb-prev" aria-label="Photo précédente">‹</button>' +
    '<button class="lb-btn lb-next" aria-label="Photo suivante">›</button>' +
    '<button class="lb-btn lb-close" aria-label="Fermer">×</button>';
  document.body.appendChild(lb);
  const img = lb.querySelector('img'), cap = lb.querySelector('figcaption');
  let i = 0, opener = null;
  const show = k => {
    i = (k + items.length) % items.length;
    img.src = items[i].getAttribute('href');
    img.alt = items[i].dataset.caption || '';
    cap.innerHTML = (items[i].dataset.caption || '') + `<span>${i + 1} / ${items.length}</span>`;
    // précharge la suivante pour un défilement fluide
    new Image().src = items[(i + 1) % items.length].getAttribute('href');
  };
  const open = k => { opener = document.activeElement; show(k); lb.classList.add('open'); document.body.style.overflow = 'hidden'; lb.querySelector('.lb-close').focus(); };
  const close = () => { lb.classList.remove('open'); document.body.style.overflow = ''; opener?.focus(); };
  items.forEach((a, k) => a.addEventListener('click', e => { e.preventDefault(); open(k); }));
  lb.querySelector('.lb-prev').onclick = () => show(i - 1);
  lb.querySelector('.lb-next').onclick = () => show(i + 1);
  lb.querySelector('.lb-close').onclick = close;
  lb.addEventListener('click', e => { if (e.target === lb) close(); });
  addEventListener('keydown', e => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(i - 1);
    if (e.key === 'ArrowRight') show(i + 1);
  });
  let x0 = null;
  lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });
});

// Carrousel coulissant : flèches, glisser à la souris, et clic = photo en grand (sauf après un glisser)
document.querySelectorAll('[data-carousel]').forEach(car => {
  const sec = car.closest('section');
  const btns = sec ? sec.querySelectorAll('.car-btn') : [];
  const step = () => Math.max(car.clientWidth * 0.8, 260);
  btns.forEach(b => b.addEventListener('click', () => car.scrollBy({ left: step() * Number(b.dataset.dir), behavior: 'smooth' })));
  const update = () => {
    if (btns.length < 2) return;
    btns[0].disabled = car.scrollLeft <= 4;
    btns[1].disabled = car.scrollLeft + car.clientWidth >= car.scrollWidth - 4;
  };
  car.addEventListener('scroll', update, { passive: true }); addEventListener('resize', update);
  car.querySelectorAll('img').forEach(i => i.addEventListener('load', update));
  update();
  car.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { e.preventDefault(); car.scrollBy({ left: step(), behavior: 'smooth' }); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); car.scrollBy({ left: -step(), behavior: 'smooth' }); }
  });
  // glisser à la souris (au doigt, le défilement natif suffit)
  let down = false, x0 = 0, s0 = 0, moved = false;
  car.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    down = true; moved = false; x0 = e.clientX; s0 = car.scrollLeft;
  });
  addEventListener('pointermove', e => {
    if (!down) return;
    const dx = e.clientX - x0;
    if (!moved && Math.abs(dx) > 6) { moved = true; car.classList.add('dragging'); }
    if (moved) car.scrollLeft = s0 - dx;
  });
  addEventListener('pointerup', () => {
    if (!down) return; down = false;
    if (moved) {
      car.classList.remove('dragging');
      // recaler sur la photo la plus proche
      const mid = car.scrollLeft + car.clientWidth / 2;
      let best = null, d = Infinity;
      car.querySelectorAll('a').forEach(a => { const c = a.offsetLeft + a.offsetWidth / 2, dd = Math.abs(c - mid); if (dd < d) { d = dd; best = a; } });
      if (best) car.scrollTo({ left: best.offsetLeft + best.offsetWidth / 2 - car.clientWidth / 2, behavior: 'smooth' });
    }
  });
  // un glisser ne doit pas ouvrir la photo en grand
  car.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopImmediatePropagation(); moved = false; } }, true);
});

// Bandeau d'annonce : la croix le ferme, et il reste fermé lors des visites suivantes
document.querySelector('.announce-close')?.addEventListener('click', () => {
  document.documentElement.classList.add('announce-off');
  setAnn();
  try { localStorage.setItem('ramet-annonce-golf', 'fermee'); } catch (e) {}
  onScroll();
});
