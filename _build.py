"""Génère les pages du site Le Ramet.

Modifier le contenu ici puis lancer :  python3 _build.py
L'en-tête, le pied de page et la barre mobile sont communs à toutes les pages.
"""
from pathlib import Path
import time

# Change à chaque génération : force les navigateurs à recharger le style
V = int(time.time())

ROOT = Path(__file__).parent
TEL, TEL_TXT, MAIL = "+33613457056", "06 13 45 70 56", "emmanuelle.morel@leramet.fr"
ACTIVE, CLOSED = ' class="active"', ' class="closed"'
MAPS = "https://www.google.com/maps/search/?api=1&query=56+rue+Maurice+Ravel+17100+Les+Gonds"

NAV = [
    ("index.html", "Accueil"),
    ("la-carte.html", "La pizzeria"),
    ("sur-place-groupes.html", "Séminaires & salle de réunion"),
    ("golf.html", 'Simulateur de Golf <span class="badge">Déc.</span>'),
    ("gites.html", 'Gîtes & Chambres d\'hôtes <span class="badge">2027</span>'),
    ("ancrage-local.html", "Ancrage local"),
    ("contact.html", "Contact"),
]


def pic(name):
    """Chemin d'une photo, versionné par sa date de modification : une photo retouchée se recharge partout."""
    return f"img/{name}.jpg?v={int((ROOT / 'img' / f'{name}.jpg').stat().st_mtime)}"


def ph(img=None, label="Photo", alt="", eager=False):
    """Bloc photo ; sans image, affiche un emplacement à remplir."""
    if not img:
        return f'<div class="ph" data-label="{label}"></div>'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<div class="ph" data-label="{label}"><img src="{pic(img)}" alt="{alt}" {load}></div>'


HERO_IMG = {"index.html": "terrasse-pizza-batisse", "la-carte.html": "comptoir-four", "sur-place-groupes.html": "salle-tables-vertes", "contact.html": "facade-longere"}


def top_tint(file):
    """Couleur de la zone d'état iPhone = haut de la photo d'accueil (sous le voile vert), pour un raccord sans bande."""
    img = HERO_IMG.get(file)
    if not img:
        return ""
    from PIL import Image
    im = Image.open(ROOT / "img" / f"{img}.jpg").convert("RGB")
    w, h = im.size
    r, g, b = im.crop((0, 0, w, int(h * .04))).resize((1, 1)).getpixel((0, 0))
    c = "#%02x%02x%02x" % tuple(int(x * .4 + y * .6) for x, y in zip((r, g, b), (36, 58, 55)))
    return f'<meta name="theme-color" content="{c}"><style>html,body{{background:{c}!important}}</style>'


def page(file, title, desc, body, home=False, overlay=False):
    links = "".join(
        f'<a href="{h}"{ACTIVE if h == file else ""}>{t}</a>' for h, t in NAV[1:]
    )
    html = f"""<!doctype html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="theme-color" content="#3E5C58">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="assets/logo/icon-120.png"><link rel="stylesheet" href="assets/site.css?v={V}">
<script>document.documentElement.classList.add("js");try{{if(localStorage.getItem("ramet-annonce-golf")==="fermee")document.documentElement.classList.add("announce-off")}}catch(e){{}}</script>
</head><body{' class="home"' if home else (' class="overlay"' if overlay else '')}>
<div class="announce"><span>⛳ Un simulateur de golf ouvre début décembre au Ramet — <a href="golf.html">en savoir plus</a></span><button class="announce-close" aria-label="Fermer l'annonce">×</button></div>
<header class="site-header">
<a class="brand" href="index.html"><img src="assets/logo/icon-120.png" alt="">Le Ramet</a>
<button class="burger" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
<nav class="main-nav" id="nav">{links}<a class="btn btn-gold" href="tel:{TEL}">Appeler</a></nav>
</header>
<main>
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div><img src="assets/logo/logo-v-beige-520.png" alt="Le Ramet — gîtes, chambres d'hôtes, séminaires et restauration"></div>
<div><h4>Nous trouver</h4><p><a href="{MAPS}" target="_blank" rel="noopener" class="addr-link">56 rue Maurice Ravel<br>17100 Les Gonds</a></p><p><a href="tel:{TEL}" class="addr-link">{TEL_TXT}</a><br><a href="mailto:{MAIL}" class="addr-link">{MAIL}</a></p></div>
<div><h4>Pizzeria</h4><p>Lun, mar, jeu, ven<br>11h–14h · 18h–21h</p><p>Dimanche 18h–21h<br>Fermé mercredi et samedi</p></div>
<div><h4>Le Ramet</h4><p><a href="la-carte.html">La pizzeria</a><br><a href="sur-place-groupes.html">Séminaires & salle de réunion</a><br><a href="golf.html">Simulateur de golf</a><br><a href="gites.html">Gîtes & Chambres d'hôtes</a><br><a href="contact.html">Contact & accès</a><br><a href="ancrage-local.html">Ancrage local</a></p>
<p><a href="https://www.instagram.com/domaine.du.ramet/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.facebook.com/profile.php?id=100063968103180" target="_blank" rel="noopener">Facebook</a></p></div>
</div><div class="legal">© Le Ramet · <a href="mentions-legales.html">Mentions légales & confidentialité</a></div></footer>
<nav class="mobile-bar" aria-label="Actions rapides"><a href="tel:{TEL}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg><span>Appeler</span></a><a href="la-carte.html"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 9H9V2H7v7H5V2H3v7c0 2.12 1.66 3.84 3.75 3.97V22h2.5v-9.03C11.34 12.84 13 11.12 13 9V2h-2v7zm5-3v8h2.5v8H21V2c-2.76 0-5 2.24-5 4z"/></svg><span>La carte</span></a><a href="{MAPS}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg><span>Itinéraire</span></a></nav>
<script src="assets/site.js?v={V}"></script>
</body></html>
"""
    (ROOT / file).write_text(html, encoding="utf-8")


def page_hero(eyebrow, h1, text, img=None, alt=""):
    return f"""<section class="page-hero">{ph(img, alt=alt, eager=True) if img else ''}<div class="c">
<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p>{text}</p></div></section>"""


GALLERY = [
    ("pizza-jambon-cru", "La Violetta : jambon cru, roquette et parmesan"),
    ("cuisine-four", "En cuisine devant le four"),
    ("four-cuisson", "Pizzas en cuisson"),
    ("pizza-automne-portrait", "L'Automne Gourmande : potimarron et magret de canard"),
    ("pizza-mache-noix", "La Biquette : chèvre, mâche, noix et miel"),
    ("preparation", "Préparation des pizzas"),
]


def gal(items):
    """Galerie : chaque photo s'ouvre en grand dans la visionneuse."""
    return "".join(f'<a href="{pic(i)}" data-caption="{c}"><img src="{pic(i)}" alt="{c}" loading="lazy"></a>' for i, c in items)


# Avis Google : note relevée sur la fiche Google « PIZZA LE RAMET » (à mettre à jour de temps en temps)
GOOGLE = {"note": "5,0", "nb": 28, "releve": "15 octobre 2026",
          "url": "https://maps.google.com/?cid=9312144320937828134"}
# Avis écrits affichés sur le site : uniquement avec l'accord de leur auteur.
# Format : ("Prénom N.", "texte de l'avis", "mois année")
AVIS = []


def avis_section():
    stars = '<span class="stars" aria-hidden="true">★★★★★</span>'
    cards = "".join(
        f'<figure class="review"><div class="review-stars" aria-label="5 étoiles sur 5">★★★★★</div>'
        f'<blockquote>« {t} »</blockquote><figcaption><span class="avatar" aria-hidden="true">{n[0]}</span>{n}<small>{d} · avis Google</small></figcaption></figure>'
        for n, t, d in AVIS)
    return f"""<section class="wrap tight reviews-sec reveal" id="avis"><h2 class="g-title">Ce que disent nos clients</h2>
<div class="avis-note"><div class="rating-score">{GOOGLE["note"]}</div>{stars}<p><strong>{GOOGLE["nb"]} avis</strong> sur Google</p></div>
<div class="avis-links"><a href="{GOOGLE["url"]}" target="_blank" rel="noopener">Lire nos avis sur Google</a><a href="{GOOGLE["url"]}" target="_blank" rel="noopener">Laisser un avis</a></div>
{f'<div class="reviews">{cards}</div>' if cards else ''}</section>"""


ROAD = """<div class="road reveal">
<div class="step now"><span class="when">Aujourd'hui</span><h3>Pizzeria & salle de réunion</h3><p>Pizzas à emporter ou sur place, et une salle de 16 places avec grand écran pour vos réunions et repas d'équipe.</p><a href="la-carte.html">Voir la carte →</a></div>
<div class="step"><span class="when">Décembre 2026</span><h3>Simulateur de golf</h3><p>Du golf indoor entre amis ou en équipe, pizza à portée de main.</p><a href="golf.html">Découvrir le golf →</a></div>
<div class="step"><span class="when">Été 2027</span><h3>Gîtes & chambres d'hôtes</h3><p>Séjourner au domaine, et des séminaires avec hébergement sur place.</p><a href="gites.html">En savoir plus →</a></div>
</div>"""


# ---------------------------------------------------------------- Accueil
page("index.html", "Le Ramet — Pizzeria, séminaires et simulateur de golf aux Gonds, près de Saintes",
     "Pizza du Ramet aux Gonds, près de Saintes : pizzas à emporter et sur place, salle pour réunions et repas d'équipe, simulateur de golf dès décembre.",
     f"""<section class="hero">{ph('terrasse-pizza-batisse', alt="Une pizza devant la bâtisse en pierre du Ramet", eager=True)}
<div class="inner"><h1 class="hero-logo"><img src="assets/logo/logo-hero-beige.png" alt="Le Ramet — gîtes & chambres d'hôtes, séminaires & restauration" width="1100" height="923"></h1>
<p class="sub" style="color:var(--beige);letter-spacing:.18em">+ Simulateur de golf · dès décembre</p>
<div class="actions"><a class="btn btn-gold" href="la-carte.html">Voir la carte</a><a class="btn btn-outline" href="tel:{TEL}">Commander · {TEL_TXT}</a><a class="btn btn-outline hero-way" href="{MAPS}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>Itinéraire</a></div></div>
<a class="scroll" href="#bienvenue">Découvrir ↓</a></section>

<section class="wrap center reveal" id="bienvenue"><p class="eyebrow">Bienvenue au Ramet</p><h2>Une pizzeria locale, et un domaine qui grandit</h2>
<p class="muted">À deux pas de Saintes, Pizza du Ramet vous accueille pour des pizzas généreuses, à la pâte façonnée avec une farine locale, à emporter ou sur place. Notre salle accueille aussi vos réunions et repas d'équipe. Un simulateur de golf ouvre début décembre, et nos gîtes et chambres d'hôtes à l'été 2027.</p></section>

<section class="wrap tight stack">
<article class="row reveal">{ph('enfournement', alt="Une pizza enfournée dans le four de la pizzeria")}<div><p class="eyebrow">Savourer</p><h2>Pizza du Ramet</h2>
<p>Pizzas base tomate ou base crème, une pizza du moment chaque semaine, à emporter ou à déguster sur place.</p>
<p><strong>Lun, mar, jeu, ven</strong> 11h–14h · 18h–21h<br><strong>Dimanche</strong> 18h–21h</p><a class="more" href="la-carte.html">Voir la carte</a></div></article>
<article class="row flip reveal">{ph("salle-tables-vertes", alt="La salle de la pizzeria avec son grand écran, ses poutres et ses murs en pierre")}<div><p class="eyebrow">Se réunir · dès aujourd'hui</p><h2>Réunions & repas d'équipe</h2>
<p>Notre salle de 16 places, équipée d'un grand écran, accueille vos réunions informelles, présentations et repas d'équipe, pizzas comprises.</p><a class="more" href="sur-place-groupes.html">Séminaires & salle de réunion</a></div></article>
</section>

<section class="band"><div class="wrap split reveal"><div><span class="badge">Ouverture début décembre</span><h2 style="margin-top:18px">Le golf s'invite au Ramet</h2>
<p>Un simulateur de golf ouvre au Ramet début décembre. Jouez sur des parcours du monde entier, travaillez votre swing, ou partagez une partie entre amis — pizza à la main.</p>
<ul class="ticks"><li>Parcours virtuels & practice</li><li>Soirées entre amis, anniversaires</li><li>Team building pour les entreprises</li><li>Formule golf + pizza</li></ul>
<a class="btn btn-gold" href="golf.html">Découvrir le simulateur</a></div>{ph(label="Visuel à venir : le simulateur de golf")}</div></section>

<section class="wrap"><div class="g-head"><h2 class="g-title">Le Ramet grandit</h2>
<div class="car-nav"><button class="car-btn" data-dir="-1" aria-label="Précédent">‹</button><button class="car-btn" data-dir="1" aria-label="Suivant">›</button></div></div>
<div class="g-pola g-car" data-carousel tabindex="0" aria-label="Le Ramet grandit, faites glisser">
<a href="la-carte.html"><div class="ph"><img src="{pic('enfournement')}" alt="La pizzeria" loading="lazy"></div><span class="when">Ouverte</span><span class="nm">La pizzeria</span></a>
<a href="golf.html"><div class="ph" data-label="Photo du golf à venir"></div><span class="when">Décembre 2026</span><span class="nm">Le simulateur de golf</span></a>
<a href="gites.html"><div class="ph"><img src="{pic('facade-longere')}" alt="La longère du Ramet" loading="lazy"></div><span class="when">Été 2027</span><span class="nm">Les gîtes &amp; chambres d'hôtes</span></a>
</div></section>

{avis_section()}

<section class="wrap tight center reveal"><img src="assets/logo/logo-v-vert-520.png" alt="" style="height:130px;width:auto;margin:0 auto 24px">
<h2>Le goût local, l'esprit convivial</h2></section>
""", home=True)

# ---------------------------------------------------------------- La carte (menu v2)
def dish(name, price, desc, img=None, tag=None):
    t = f'<span class="tag new">{tag}</span>' if tag else ""
    photo = f'<a class="ph" href="{pic(img)}" data-caption="{name}"><img src="{pic(img)}" alt="Pizza {name}" loading="lazy"></a>' if img else ""
    return f'<div class="dish{"" if img else " noimg"}">{photo}<div><h3>{name}<span>{price}</span></h3><p>{desc}</p>{t}</div></div>'

TOMATE = [
    ("Margherita", "8,5 €", "Pulpe de tomate, mozzarella, huile d'olive, basilic frais.", None, None),
    ("Regina", "12 €", "Pulpe de tomate, mozzarella, jambon blanc, champignons, olives, origan.", "pizza-regina", None),
    ("Végétarienne", "13 €", "Pulpe de tomate, mozzarella, oignons rissolés, champignons, cœur d'artichaut, tomate cerise, huile d'olive, olives, origan.", None, "Nouveau"),
    ("Paysanne", "13 €", "Pulpe de tomate, mozzarella, oignons rissolés, champignons, lardons fumés, jambon blanc, huile d'olive, origan.", None, "Nouveau"),
    ("Andalouse", "13 €", "Pulpe de tomate, mozzarella, oignons rissolés, chorizo, poivrons, huile d'olive, origan.", None, None),
    ("Violetta", "15 €", "Pulpe de tomate, mozzarella, jambon cru, tomates cerise, roquette, copeaux de parmesan, pignons de pin, huile d'olive, basilic frais.", "pizza-jambon-cru", None),
]
CREME = [
    ("Quatre Fromages", "14 €", "Crème de ricotta, mozzarella, gorgonzola, pecorino.", None, None),
    ("Biquette", "14 €", "Crème fraîche, mozzarella, chèvre, mâche, noix, miel.", "pizza-mache-noix", None),
    ("Cascade", "14 €", "Crème de ricotta, mozzarella, oignons rissolés, truite fumée, roquette, aneth, zeste de citron.", "pizza-cascade", None),
    ("Pistacchio", "15 €", "Pesto pistache, mozzarella, mortadelle, pistaches concassées, zeste de citron, basilic frais.", "pizza-mortadelle-pistache", None),
    ("Automne Gourmande", "15 €", "Purée de potimarron, mozzarella, oignons rissolés, magret de canard séché, copeaux de parmesan, zeste d'orange, pignons de pin, huile d'olive, basilic.", "pizza-magret-potimarron", "Nouveau"),
]
DRINKS = {
    "Vins": [("Rosé La Raballe 75 cl", "12 €"), ("Lambrusco Emilia IGT Amabile 75 cl", "12 €")],
    "Bières": [("Chouffe 33 cl", "5 €"), ("Duvel 33 cl", "5 €"), ("Pelforth 25 cl", "3,50 €"), ("Triple Karmeliet 25 cl", "4,50 €")],
    "Sodas": [("Eau plate, eau gazeuse 50 cl", "1,50 €"), ("Soda 33 cl · Jus de pomme 20 cl", "2 €"), ("Thé glacé, citronnés 35 cl · Limonade 27,5 cl", "3 €")],
}
# Allergènes : (pizza, gluten, lait, poisson, fruits à coque, sulfites) — repris du menu imprimé
ALLERGENS = [
    ("Margherita", "✕", "✕", "", "", ""), ("Regina", "✕", "✕", "", "", ""),
    ("Andalouse", "✕", "✕", "", "", "✕ (chorizo)"), ("Végétarienne", "✕", "✕", "", "", ""),
    ("Violetta", "✕", "✕", "", "✕ (pignons de pin)", ""), ("Quatre Fromages", "✕", "✕", "", "", ""),
    ("Biquette", "✕", "✕", "", "✕ (noix)", ""), ("Cascade", "✕", "✕", "✕", "", ""),
    ("Pistacchio", "✕", "✕", "", "✕ (pistaches)", "✕ (mortadelle)"), ("Paysanne", "✕", "✕", "", "", "✕ (lardons)"),
    ("Automne Gourmande", "✕", "✕", "", "✕ (pignons de pin, noisettes)", "✕ (magret de canard fumé)"),
]
allergen_rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in ALLERGENS)
drinks_html = "".join(
    f'<h3 class="drinks-title">{g}</h3><div class="drinks">' + "".join(f"<div><span>{n}</span><b>{p}</b></div>" for n, p in items) + "</div>"
    for g, items in DRINKS.items())

# Pizza du moment, dessert et suppléments (mettre à jour ici chaque semaine)
MOMENT = ("La Diavola", "12 €", "Pulpe de tomate, mozzarella, spianata piccante, basilic, origan, olive, huile d'olive")
DESSERT = ("Glaces L'Angélys", "4 €", "Chocolat noisette, mangue, framboise, vanille, cacahuète")
SUPP = "Œuf 1 € · Fromage / viande 1,5 € · Légume 1 €"


def ardoise(items):
    """Liste de pizzas façon ardoise : nom + prix, ingrédients dessous."""
    return "<ul>" + "".join(
        f'<li><div class="ln"><span class="nm">{n}{"<span class=nv>nouveau</span>" if t else ""}</span><span class="pr">{p}</span></div><p>{d.rstrip(".")}</p></li>'
        for n, p, d, i, t in items) + "</ul>"


def ardoise_drinks(groups):
    return "".join(f'<h2>{g}</h2><ul class="sm">' + "".join(
        f'<li><div class="ln"><span class="nm">{n}</span><span class="pr">{p}</span></div></li>' for n, p in DRINKS[g]) + "</ul>"
        for g in groups)


page("la-carte.html", "La pizzeria — Pizza du Ramet, Les Gonds",
     "La carte de Pizza du Ramet : pizzas base tomate, base crème, pizza du moment, boissons et allergènes. À emporter ou sur place aux Gonds.",
     f"""<section class="hero">{ph('comptoir-four', alt="Le comptoir de la pizzeria, le four et l'ancien four à pain", eager=True)}
<div class="inner"><p class="sub">Pizza du Ramet · à emporter ou sur place</p><h1 class="hero-title">La pizzeria</h1>
<div class="actions"><a class="btn btn-gold" href="#moment">Voir la carte</a><a class="btn btn-outline" href="tel:{TEL}">Commander · {TEL_TXT}</a></div></div></section>
<div class="carte-c" data-gallery><div class="in">
<div class="c-head"><h1>À l'ardoise</h1><p class="c-hours">Lundi, mardi, jeudi, vendredi · <b>11h – 14h</b> & <b>18h – 21h</b><br>Dimanche · <b>18h – 21h</b></p></div>
<div class="c-moment" id="moment"><span class="k">Pizza du moment</span><h2>{MOMENT[0]}</h2><p>{MOMENT[2]}</p><span class="pr">{MOMENT[1]}</span><small>Nouvelle recette chaque semaine</small></div>
<div class="c-cols"><div id="tomate"><h2>Base tomate</h2>{ardoise(TOMATE)}</div><div id="creme"><h2>Base crème</h2>{ardoise(CREME)}
<h2 class="mt">Dessert</h2><ul><li><div class="ln"><span class="nm">{DESSERT[0]}</span><span class="pr">{DESSERT[1]}</span></div><p>{DESSERT[2]}</p></li></ul>
<p class="supp">Ingrédient supplémentaire : {SUPP}</p></div></div>
<div class="c-cols" id="boissons"><div>{ardoise_drinks(["Vins", "Bières"])}</div><div>{ardoise_drinks(["Sodas"])}</div></div>
<section class="c-sec" id="galerie"><div class="gallery-head"><h2>En images</h2>
<div class="car-nav"><button class="car-btn" data-dir="-1" aria-label="Photos précédentes">‹</button><button class="car-btn" data-dir="1" aria-label="Photos suivantes">›</button></div></div>
<div class="carousel" data-gallery data-carousel tabindex="0" aria-label="Photos de la pizzeria, faites glisser">{gal(GALLERY)}</div></section>
<section class="c-sec" id="menu-imprime"><h2>Le menu en images</h2>
<div class="menu-sheets">
<a class="sheet" href="img/menu-ramet-1.jpg" data-caption="Le menu — pizzas et boissons"><img src="img/menu-ramet-1.jpg" alt="Menu Pizza du Ramet : pizzas base tomate, base crème, pizza du moment et boissons" loading="lazy"></a>
<a class="sheet" href="img/menu-ramet-2.jpg" data-caption="Le menu — horaires, allergènes et contact"><img src="img/menu-ramet-2.jpg" alt="Menu Pizza du Ramet : horaires, informations allergènes et contact" loading="lazy"></a>
</div>
<div class="c-foot"><a class="btn btn-gold" href="tel:{TEL}">Commander · {TEL_TXT}</a><a class="btn btn-outline" href="img/menu-ramet-1.jpg" download="menu-pizza-du-ramet.jpg">Télécharger le menu</a></div></section>
<section class="c-sec" id="allergenes"><h2>Allergènes</h2>
<p class="supp">Tableau indicatif des allergènes présents dans nos recettes. Traces possibles selon approvisionnements.</p>
<div class="table-scroll"><table class="allergens"><thead><tr><th>Pizza</th><th>Gluten</th><th>Lait</th><th>Poisson</th><th>Fruits à coque</th><th>Sulfites</th></tr></thead><tbody>{allergen_rows}</tbody></table></div>
<div class="note"><strong>Remarques :</strong> supplément œuf : allergène œuf. Supplément fromage / viande : lait si fromage, sulfites possibles si charcuterie. Glaces : certains parfums contiennent des fruits à coque (chocolat noisette) ou de l'arachide (cacahuète). Pour toute allergie ou intolérance, merci de nous consulter avant de commander.</div>
</section>
</div></div>""", home=True)

# ---------------------------------------------------------------- Pages intérieures : helpers de style
def head(title, sub="", img=None, alt="", kicker="", when="", pos=50):
    """En-tête de page : bandeau photo fondu (proportions fixes) + titre centré."""
    banner = f'<div class="p-banner" style="--pos:{pos}%"><img src="{pic(img)}" alt="{alt}" fetchpriority="high"></div>' if img else ""
    k = f'<span class="k">{kicker}</span>' if kicker else ""
    w = f'<span class="when">{when}</span>' if when else ""
    p = f"<p>{sub}</p>" if sub else ""
    return f'{banner}<div class="p-head">{k}<h1>{title}</h1>{p}{w}</div>'


def slate(title, lines, intro="", foot=""):
    """Panneau ardoise : lignes « nom ........ valeur », avec une description facultative."""
    out = []
    for i, ln in enumerate(lines):
        nm, val = ln[0], ln[1]
        desc = ln[2] if len(ln) > 2 else ""
        href = ln[3] if len(ln) > 3 else ""
        cls = ln[4] if len(ln) > 4 else ""
        last = " row-last" if i == len(lines) - 1 else ""
        tag = f'a href="{href}"' if href else "div"
        end = "a" if href else "div"
        line = f'<{tag} class="ln{" " + cls if cls else ""}{"" if desc else last}"><span class="nm">{nm}</span><span class="dots"></span><span class="when">{val}</span></{end}>'
        if desc:
            line += f'<p class="d{last}">{desc}</p>'
        out.append(line)
    i = f'<p class="intro">{intro}</p>' if intro else ""
    f = f'<div class="foot">{foot}</div>' if foot else ""
    t = f"<h2>{title}</h2>" if title else ""
    return f'<div class="slate reveal"><div class="frame">{t}{i}{"".join(out)}{f}</div></div>'


# ---------------------------------------------------------------- Sur place & groupes (même construction que l'accueil)
page("sur-place-groupes.html", "Séminaires & salle de réunion — Le Ramet",
     "Séminaires et salle de réunion au Ramet (16 places, grand écran) : réunions, repas d'équipe et projections, pizzas comprises.",
     f"""<section class="hero">{ph('salle-tables-vertes', alt="La salle de la pizzeria, ses poutres et son grand écran", eager=True)}
<div class="inner"><p class="sub">16 places assises · grand écran · pizzas comprises</p><h1 class="hero-title">Séminaires<br>& salle de réunion</h1>
<div class="actions"><a class="btn btn-gold" href="#venue">Organiser une venue</a><a class="btn btn-outline" href="tel:{TEL}">Appeler · {TEL_TXT}</a></div></div></section>

<section class="wrap center reveal"><h2>Une salle simple, chaleureuse et équipée</h2>
<p class="muted">Sous les poutres et les murs en pierre de la pizzeria, notre salle accueille aussi bien un déjeuner sur le pouce qu'une réunion d'équipe ou un match à regarder ensemble — avec les pizzas qui sortent du four à côté.</p></section>

<section class="wrap tight stack">
<article class="row reveal">{ph('pizza-burrata-terrasse', alt="Pizzas et boissons sur une table de la terrasse")}<div><p class="eyebrow">Manger sur place</p><h2>À table, en salle ou en terrasse</h2>
<p>Seul, en famille, entre collègues ou entre amis : installez-vous en salle ou, aux beaux jours, sur la terrasse de la cour. Service en libre-service, pizzas tout juste sorties du four.</p>
<p><strong>Lun, mar, jeu, ven</strong> 11h–14h · 18h–21h<br><strong>Dimanche</strong> 18h–21h</p><a class="more" href="la-carte.html">Voir la carte</a></div></article>
<article class="row flip reveal">{ph('salle-grand-ecran', alt="Le grand écran de la salle, les poutres et les murs en pierre")}<div><p class="eyebrow">Se réunir</p><h2>Un grand écran pour vos contenus</h2>
<p>Réunions informelles, présentations, rencontres associatives ou soirées match : branchez-vous sur le grand écran et commandez les pizzas pour toute la table.</p><a class="more" href="#venue">Organiser une venue</a></div></article>
</section>

<section class="band"><div class="wrap split reveal"><div><span class="badge">Entreprises · associations · clubs</span><h2 style="margin-top:18px">Votre équipe au Ramet</h2>
<p>Un cadre moins formel qu'une salle de réunion classique, à cinq minutes de Saintes, avec la restauration sur place.</p>
<ul class="ticks"><li>Commandes groupées pour les pauses déjeuner</li><li>Repas d'équipe jusqu'à 16 personnes</li><li>Présentations et projections sur grand écran</li><li>Bientôt : team building golf et séminaires avec hébergement</li></ul>
<a class="btn btn-gold" href="mailto:{MAIL}?subject=Demande%20pour%20un%20groupe%20au%20Ramet">Demander un devis</a></div>{ph('comptoir-four', alt="Le comptoir de la pizzeria et le four")}</div></section>

<section class="wrap"><div class="g-head"><h2 class="g-title">Et bientôt, encore plus</h2>
<div class="car-nav"><button class="car-btn" data-dir="-1" aria-label="Précédent">‹</button><button class="car-btn" data-dir="1" aria-label="Suivant">›</button></div></div>
<div class="g-pola g-car" data-carousel tabindex="0" aria-label="Les prochaines possibilités, faites glisser">
<a href="la-carte.html"><div class="ph"><img src="{pic('salle-grand-ecran')}" alt="La salle de la pizzeria" loading="lazy"></div><span class="when">Dès aujourd'hui</span><span class="nm">Repas & réunions</span></a>
<a href="golf.html"><div class="ph" data-label="Photo du golf à venir"></div><span class="when">Décembre 2026</span><span class="nm">Team building golf</span></a>
<a href="gites.html"><div class="ph"><img src="{pic('facade-batisse')}" alt="La bâtisse du Ramet" loading="lazy"></div><span class="when">Été 2027</span><span class="nm">Séminaires avec hébergement</span></a>
</div></section>

<section class="wrap tight" id="venue"><div class="center" style="max-width:640px"><h2 class="sec-title">Organiser une venue</h2>
<ol class="num-steps" style="text-align:left"><li>Contactez-nous par téléphone ou par e-mail.</li><li>Indiquez le nombre de personnes (16 places assises).</li><li>Précisez le besoin : repas, réunion, présentation ou projection.</li><li>Nous confirmons les possibilités.</li></ol>
<div class="u-links c"><a href="tel:{TEL}">Appeler le {TEL_TXT}</a><a href="mailto:{MAIL}?subject=Organiser%20une%20venue%20au%20Ramet">Écrire un e-mail</a></div></div></section>

<section class="wrap tight center reveal"><img src="assets/logo/logo-v-vert-520.png" alt="" style="height:130px;width:auto;margin:0 auto 24px">
<h2>Le goût local, l'esprit convivial</h2></section>
""", home=True)

# ---------------------------------------------------------------- Golf (même construction que l'accueil)
page("golf.html", "Simulateur de golf — Le Ramet, Les Gonds près de Saintes",
     "Simulateur de golf indoor au Ramet, Les Gonds près de Saintes : parcours virtuels, practice, soirées entre amis et team building. Ouverture début décembre 2026.",
     f"""<section class="hero hero-golf"><div class="ph" data-label=""></div>
<div class="inner"><p class="sub">Ouverture début décembre 2026</p><h1 class="hero-title">Simulateur<br>de golf</h1>
<div class="actions"><a class="btn btn-gold" href="tel:{TEL}">Appeler · {TEL_TXT}</a><a class="btn btn-outline" href="#formules">Voir les formules</a></div></div></section>

<section class="wrap center reveal"><h2>Le golf s'invite au Ramet</h2>
<p class="muted">Un simulateur de golf indoor aux Gonds, à 5 minutes de Saintes. Parcours du monde entier, practice et défis entre amis — été comme hiver, et une pizza en sortant du green.</p></section>

<section class="wrap tight stack">
<article class="row reveal">{ph(label="Photo du simulateur à venir")}<div><p class="eyebrow">Jouer</p><h2>Parcours mythiques & practice</h2>
<p>Jouez 9 ou 18 trous sur des parcours célèbres, travaillez votre swing grâce aux données de chaque coup (vitesse, distance, trajectoire), ou lancez des défis : plus long drive, concours d'approche.</p>
<p class="muted">Débutant curieux ou golfeur confirmé, clubs disponibles à la location.</p></div></article>

</section>

<section class="wrap tight" id="formules">{slate("Les formules", [
        ("Partie libre", "à l'heure", "Location du simulateur, jusqu'à 6 joueurs, clubs en location."),
        ("Golf & Pizza", "entre amis", "Une session de golf, puis pizza et boisson."),
        ("Soirée golf", "en soirée", "Une soirée entre amis ou en famille, golf et pizzas pour tout le groupe, sur réservation."),
        ("Entreprises", "sur devis", "Team building et tournoi interne, repas dans la salle.", f"mailto:{MAIL}?subject=Golf%20entreprise"),
    ], intro="Tarifs communiqués à l'ouverture", foot=f'<a href="mailto:{MAIL}?subject=Golf%20au%20Ramet">Demander un devis</a>')}</section>

<section class="wrap stack">
<article class="row reveal">{ph('tables-vertes-duo', alt="Deux pizzas sur une table de la terrasse")}<div><p class="eyebrow">Golf & pizza</p><h2>Jouez, puis passez à table</h2>
<p>Enchaînez une partie et un repas à la pizzeria, dans la même maison. À l'été 2027, vous pourrez aussi dormir sur place.</p><a class="more" href="la-carte.html">Voir la carte</a></div></article>
</section>

<section class="wrap tight"><h2 class="sec-title">Questions fréquentes</h2><div class="faq">
<details><summary>Faut-il savoir jouer au golf ?</summary><p>Non, le simulateur convient aux débutants comme aux confirmés. Les jeux et défis sont accessibles à tous.</p></details>
<details><summary>Le matériel est-il fourni ?</summary><p>Les clubs sont disponibles à la location, et vous pouvez aussi venir avec les vôtres. Les balles sont obligatoirement fournies par le Ramet.</p></details>
<details><summary>Combien de joueurs par session ?</summary><p>Jusqu'à 6 joueurs par session.</p></details>
<details><summary>Comment réserver ?</summary><p>À l'ouverture, par téléphone au {TEL_TXT}.</p></details>
</div></section>


<section class="wrap tight center reveal"><img src="assets/logo/logo-v-vert-520.png" alt="" style="height:130px;width:auto;margin:0 auto 24px">
<h2>Le goût local, l'esprit convivial</h2></section>
""", home=True)

# ---------------------------------------------------------------- Gîtes (été 2027)
page("gites.html", "Gîtes & Chambres d'hôtes — Le Ramet, ouverture été 2027",
     "Le Ramet ouvre ses gîtes et chambres d'hôtes aux Gonds, près de Saintes, à l'été 2027.",
     f"""<section class="hero hero-center">{ph('facade-batisse', alt="La bâtisse et la longère du Ramet", eager=True)}
<div class="inner"><p class="sub">Ouverture été 2027</p><h1 class="hero-title">Gîtes &<br>Chambres d'hôtes</h1>
<div class="actions"><a class="btn btn-gold" href="tel:{TEL}">Appeler · {TEL_TXT}</a></div></div></section>

<section class="wrap center reveal"><h2>Un domaine pour se poser</h2>
<p class="muted">Bientôt, vous pourrez séjourner au Ramet : au calme, au cœur de la Saintonge, avec la pizzeria et le golf sur place. Photos, capacités et tarifs seront publiés ici à l'approche de l'ouverture.</p></section>

<section class="wrap tight">{slate("En préparation", [
        ("Les gîtes", "familles & amis", "Pour les séjours en famille ou entre amis."),
        ("Les chambres d'hôtes", "une nuit, un week-end", "Avec petit-déjeuner."),
        ("Les séminaires", "entreprises", "Réunion, repas et hébergement sur place.", "sur-place-groupes.html"),
    ])}</section>

<section class="wrap stack">
<article class="row reveal">{ph('facade-longere', alt="La longère du Ramet")}<div><p class="eyebrow">Tout sur place</p><h2>Dormir, savourer, jouer</h2>
<p>Nos hôtes auront la pizzeria à quelques pas et le simulateur de golf sous le même toit. En attendant, venez déjà nous rendre visite !</p>
<div class="u-links"><a href="la-carte.html">La pizzeria</a><a href="golf.html">Simulateur de golf</a></div></div></article>
</section>

<section class="wrap tight center reveal"><img src="assets/logo/logo-v-vert-520.png" alt="" style="height:130px;width:auto;margin:0 auto 24px">
<h2>Le goût local, l'esprit convivial</h2></section>
""", home=True)

# ---------------------------------------------------------------- Ancrage local
page("ancrage-local.html", "Ancrage local — Pizza du Ramet et la Minoterie Méchain",
     "Pizza du Ramet travaille une farine locale de la Minoterie Méchain à Courcelles : une pizzeria ancrée dans son territoire.",
     f"""<section class="hero hero-center">{ph('preparation', alt="Préparation des pizzas", eager=True)}
<div class="inner"><p class="sub">Du territoire à votre assiette</p><h1 class="hero-title">Ancrage<br>local</h1>
<div class="actions"><a class="btn btn-gold" href="la-carte.html">Voir la carte</a><a class="btn btn-outline" href="tel:{TEL}">Commander · {TEL_TXT}</a></div></div></section>

<section class="wrap center reveal"><h2>Le goût du coin</h2>
<p class="muted">Aux Gonds, Pizza du Ramet fait le choix de la proximité, du bon sens et des savoir-faire locaux, en travaillant avec des partenaires proches dès que possible.</p></section>

<section class="wrap tight stack">
<article class="row reveal">{ph('cuisine-four', alt="En cuisine devant le four")}<div><p class="eyebrow">La farine</p><h2>La Minoterie Méchain, à Courcelles</h2>
<p>Pour réaliser nos pâtes, nous avons choisi une farine issue de la Minoterie Méchain, à quelques kilomètres de la pizzeria.</p></div></article>
<article class="row reveal">{ph('four-cuisson', alt="Pizzas en cuisson dans le four")}<div><p class="eyebrow">Les glaces</p><h2>L'Angélys, glacier charentais</h2>
<p>Pour le dessert, des glaces artisanales de Charente-Maritime : chocolat noisette, mangue, framboise, vanille, cacahuète.</p><a class="more" href="la-carte.html">Voir la carte</a></div></article>
</section>

<section class="wrap tight">{slate("Nos engagements", [
        ("Proximité", "partenaires locaux"),
        ("Savoir-faire", "pâte faite maison"),
        ("Authenticité", "recettes simples"),
        ("Tissu local", "Saintonge"),
    ])}</section>

<section class="wrap tight center reveal"><img src="assets/logo/logo-v-vert-520.png" alt="" style="height:130px;width:auto;margin:0 auto 24px">
<h2>Le goût local, l'esprit convivial</h2></section>
""", home=True)

# ---------------------------------------------------------------- Contact
HOURS = [(1, "Lundi", "11h – 14h · 18h – 21h"), (2, "Mardi", "11h – 14h · 18h – 21h"), (3, "Mercredi", "fermé"),
         (4, "Jeudi", "11h – 14h · 18h – 21h"), (5, "Vendredi", "11h – 14h · 18h – 21h"), (6, "Samedi", "fermé"),
         (0, "Dimanche", "18h – 21h")]
hours_lines = "".join(
    f'<div class="ln{" closed" if h == "fermé" else ""}" data-day="{d}"><span class="nm">{n}</span><span class="dots"></span><span class="when">{h}</span></div>'
    for d, n, h in HOURS)
page("contact.html", "Contact & accès — Pizza du Ramet, Les Gonds",
     "Contact, horaires et accès de Pizza du Ramet, 56 rue Maurice Ravel, 17100 Les Gonds. Commandes par téléphone au 06 13 45 70 56.",
     f"""<section class="hero hero-center">{ph('facade-longere', alt="La longère du Ramet", eager=True)}
<div class="inner"><p class="sub">56 rue Maurice Ravel · Les Gonds</p><h1 class="hero-title">Contact<br>& accès</h1>
<div class="actions"><a class="btn btn-gold" href="tel:{TEL}">Appeler · {TEL_TXT}</a><a class="btn btn-outline" href="{MAPS}" target="_blank" rel="noopener">Itinéraire</a></div></div></section>

<section class="wrap center reveal"><h2>Retrouvez-nous aux Gonds</h2>
<p class="muted">À cinq minutes de Saintes. Pour vos pizzas à emporter ou sur place, vos réunions, et vos questions sur le golf et les gîtes.</p></section>

<section class="wrap tight">{slate("Nous joindre", [
        ("Adresse", "56 rue Maurice Ravel, Les Gonds", "", MAPS),
        ("Téléphone", TEL_TXT, "", f"tel:{TEL}"),
        ("E-mail", MAIL, "", f"mailto:{MAIL}"),
        ("Paiement", "carte ou espèces"),
    ], intro="Commandes par téléphone ou sur place")}</section>

<section class="wrap stack">
<article class="row reveal"><div class="polaroid"><iframe class="map" title="Plan d'accès Pizza du Ramet" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=56+rue+Maurice+Ravel,+17100+Les+Gonds&output=embed"></iframe></div>
<div><div class="slate hours-lines"><div class="frame"><h2>Horaires</h2><p class="intro">Pizzeria</p>{hours_lines}</div></div>
<div class="u-links"><a href="tel:{TEL}">Appeler</a><a href="{MAPS}" target="_blank" rel="noopener">Itinéraire</a></div></div></article>
</section>

<section class="wrap tight center reveal"><img src="assets/logo/logo-v-vert-520.png" alt="" style="height:130px;width:auto;margin:0 auto 24px">
<h2>Le goût local, l'esprit convivial</h2></section>
""", home=True)

# ---------------------------------------------------------------- Mentions légales
page("mentions-legales.html", "Mentions légales — Le Ramet", "Mentions légales et données personnelles du site leramet.fr.",
     head("Mentions légales", "Informations légales du site www.leramet.fr.", kicker="Informations légales")
     + f"""<section class="wrap prose">
<h2>Éditeur du site</h2><p>Le présent site est édité par Pizza du Ramet / Le Ramet, 56 rue Maurice Ravel, 17100 Les Gonds, France. Téléphone : {TEL_TXT} — E-mail : {MAIL}.</p>
<p>Raison sociale : SARL LE RAMET — Forme juridique : SARL — Capital social : 450 000 € — SIRET : 890 663 974 00024 — RCS : Saintes 890 663 974 — Responsable de publication : Emmanuelle Morel, gérante.</p>
<h2>Hébergement</h2><p>Le site est hébergé par OVH SAS, 2 rue Kellermann, 59100 Roubaix, France — www.ovhcloud.com.</p>
<h2>Propriété intellectuelle</h2><p>L'ensemble des contenus présents sur le site (textes, images, graphismes, logo, icônes, photographies, illustrations, structure générale) sont la propriété exclusive de leur auteur ou font l'objet d'une autorisation d'utilisation. Toute reproduction ou exploitation non autorisée est interdite.</p>
<h2 id="donnees">Données personnelles</h2><p>Les informations transmises par e-mail ou téléphone sont destinées exclusivement à Pizza du Ramet afin de répondre aux demandes des utilisateurs. Aucune donnée personnelle n'est cédée, vendue ou transmise à des tiers à des fins commerciales.</p>
<p>La carte d'accès de la page Contact est fournie par Google Maps, qui peut déposer ses propres cookies lors de son affichage.</p>
<h2>Responsabilité</h2><p>Les informations présentes sur le site sont données à titre indicatif et peuvent évoluer. Les horaires, tarifs, recettes, disponibilités et informations pratiques peuvent être modifiés à tout moment. Il est recommandé de contacter directement Pizza du Ramet pour confirmer une information.</p>
</section>""")

print("Pages générées.")
