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
    ("sur-place-groupes.html", "Sur place & groupes"),
    ("golf.html", 'Simulateur de Golf <span class="badge">Déc.</span>'),
    ("gites.html", 'Gîtes <span class="badge">2027</span>'),
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


def page(file, title, desc, body, home=False):
    links = "".join(
        f'<a href="{h}"{ACTIVE if h == file else ""}>{t}</a>' for h, t in NAV[1:]
    )
    html = f"""<!doctype html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="assets/logo/icon-120.png"><link rel="stylesheet" href="assets/site.css?v={V}">
<script>document.documentElement.classList.add("js");try{{if(localStorage.getItem("ramet-annonce-golf")==="fermee")document.documentElement.classList.add("announce-off")}}catch(e){{}}</script>
</head><body{' class="home"' if home else ''}>
<div class="announce"><span>⛳ Un simulateur de golf ouvre début décembre au Ramet — <a href="golf.html">en savoir plus</a></span><button class="announce-close" aria-label="Fermer l'annonce">×</button></div>
<header class="site-header">
<a class="brand" href="index.html"><img src="assets/logo/icon-120.png" alt="">Le Ramet</a>
<button class="burger" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
<nav class="main-nav" id="nav">{links}<a class="btn btn-gold" href="tel:{TEL}">Commander</a></nav>
</header>
<main>
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div><img src="assets/logo/logo-v-beige-520.png" alt="Le Ramet — gîtes, chambres d'hôtes, séminaires et restauration"></div>
<div><h4>Nous trouver</h4><p><a href="{MAPS}" target="_blank" rel="noopener" class="addr-link">56 rue Maurice Ravel<br>17100 Les Gonds</a></p><p><a href="tel:{TEL}" class="addr-link">{TEL_TXT}</a><br><a href="mailto:{MAIL}" class="addr-link">{MAIL}</a></p></div>
<div><h4>Pizzeria</h4><p>Lun, mar, jeu, ven<br>11h–14h · 18h–21h</p><p>Dimanche 18h–21h<br>Fermé mercredi et samedi</p></div>
<div><h4>Le Ramet</h4><p><a href="la-carte.html">La carte</a><br><a href="sur-place-groupes.html">Sur place & groupes</a><br><a href="golf.html">Golf</a><br><a href="gites.html">Gîtes & chambres d'hôtes</a><br><a href="contact.html">Contact & accès</a></p>
<p><a href="https://www.instagram.com/domaine.du.ramet/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.facebook.com/profile.php?id=100063968103180" target="_blank" rel="noopener">Facebook</a></p></div>
</div><div class="legal">© Le Ramet · <a href="mentions-legales.html">Mentions légales & confidentialité</a></div></footer>
<div class="mobile-bar"><a href="tel:{TEL}">Appeler</a><a href="la-carte.html">La carte</a><a href="{MAPS}" target="_blank" rel="noopener">Itinéraire</a></div>
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
    return f"""<section class="wrap tight reviews-sec reveal" id="avis"><div class="center"><p class="eyebrow">Nos avis</p><h2>Ce que disent nos clients</h2></div>
<div class="rating-card"><div class="rating-score">{GOOGLE["note"]}</div><div>{stars}<p><strong>{GOOGLE["nb"]} avis</strong> sur Google</p></div>
<div class="rating-actions"><a class="btn btn-green" href="{GOOGLE["url"]}" target="_blank" rel="noopener">Lire nos avis sur Google</a><a class="btn btn-outline" style="color:var(--green)" href="{GOOGLE["url"]}" target="_blank" rel="noopener">Laisser un avis</a></div></div>
{f'<div class="reviews">{cards}</div>' if cards else ''}</section>"""


ROAD = """<div class="road reveal">
<div class="step now"><span class="when">Aujourd'hui</span><h3>Pizzeria & salle de réunion</h3><p>Pizzas à emporter ou sur place, et une salle de 16 places avec grand écran pour vos réunions et repas d'équipe.</p><a href="la-carte.html">Voir la carte →</a></div>
<div class="step"><span class="when">Décembre 2026</span><h3>Simulateur de golf</h3><p>Du golf indoor entre amis ou en équipe, pizza à portée de main.</p><a href="golf.html">Découvrir le golf →</a></div>
<div class="step"><span class="when">Été 2027</span><h3>Gîtes & chambres d'hôtes</h3><p>Séjourner au domaine, et des séminaires avec hébergement sur place.</p><a href="gites.html">En savoir plus →</a></div>
</div>"""


# ---------------------------------------------------------------- Accueil
page("index.html", "Le Ramet — Pizzeria aux Gonds près de Saintes, golf indoor & réunions",
     "Pizza du Ramet aux Gonds, près de Saintes : pizzas à emporter et sur place, salle pour réunions et repas d'équipe, simulateur de golf dès décembre.",
     f"""<section class="hero">{ph('terrasse-pizza-batisse', alt="Une pizza devant la bâtisse en pierre du Ramet", eager=True)}
<div class="inner"><h1 class="hero-logo"><img src="assets/logo/logo-hero-beige.png" alt="Le Ramet — gîtes & chambres d'hôtes, séminaires & restauration" width="1100" height="923"></h1>
<p class="sub" style="color:var(--beige);letter-spacing:.18em">+ Simulateur de golf · dès décembre</p>
<div class="actions"><a class="btn btn-gold" href="la-carte.html">Voir la carte</a><a class="btn btn-outline" href="tel:{TEL}">Commander · {TEL_TXT}</a></div></div>
<a class="scroll" href="#bienvenue">Découvrir ↓</a></section>

<section class="wrap center reveal" id="bienvenue"><p class="eyebrow">Bienvenue au Ramet</p><h2>Une pizzeria locale, et un domaine qui grandit</h2>
<p class="muted">À deux pas de Saintes, Pizza du Ramet vous accueille pour des pizzas généreuses, à la pâte façonnée avec une farine locale, à emporter ou sur place. Notre salle accueille aussi vos réunions et repas d'équipe. Un simulateur de golf ouvre début décembre, et nos gîtes et chambres d'hôtes à l'été 2027.</p></section>

<section class="wrap tight stack">
<article class="row reveal">{ph('enfournement', alt="Une pizza enfournée dans le four de la pizzeria")}<div><p class="eyebrow">Savourer</p><h2>Pizza du Ramet</h2>
<p>Pizzas base tomate ou base crème, une pizza du moment chaque semaine, à emporter ou à déguster sur place.</p>
<p><strong>Lun, mar, jeu, ven</strong> 11h–14h · 18h–21h<br><strong>Dimanche</strong> 18h–21h</p><a class="more" href="la-carte.html">Voir la carte</a></div></article>
<article class="row flip reveal">{ph("salle-tables-vertes", alt="La salle de la pizzeria avec son grand écran, ses poutres et ses murs en pierre")}<div><p class="eyebrow">Se réunir · dès aujourd'hui</p><h2>Réunions & repas d'équipe</h2>
<p>Notre salle de 16 places, équipée d'un grand écran, accueille vos réunions informelles, présentations et repas d'équipe, pizzas comprises.</p><a class="more" href="sur-place-groupes.html">Sur place & groupes</a></div></article>
</section>

<section class="band"><div class="wrap split reveal"><div><span class="badge">Ouverture début décembre</span><h2 style="margin-top:18px">Le golf s'invite au Ramet</h2>
<p>Un simulateur de golf s'installe au Ramet mi-novembre et ouvre début décembre. Jouez sur des parcours du monde entier, travaillez votre swing, ou partagez une partie entre amis — pizza à la main.</p>
<ul class="ticks"><li>Parcours virtuels & practice</li><li>Soirées entre amis, anniversaires</li><li>Team building pour les entreprises</li><li>Formule golf + pizza</li></ul>
<a class="btn btn-gold" href="golf.html">Découvrir le simulateur</a></div>{ph(label="Visuel à venir : le simulateur de golf")}</div></section>

<section class="wrap"><p class="eyebrow">Le Ramet grandit</p><h2>Aujourd'hui, et bientôt</h2>{ROAD}</section>

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

page("la-carte.html", "La pizzeria — Pizza du Ramet, Les Gonds",
     "La carte de Pizza du Ramet : pizzas base tomate, base crème, pizza du moment, boissons et allergènes. À emporter ou sur place aux Gonds.",
     page_hero("Pizza du Ramet · à emporter ou sur place", "La pizzeria",
               f"Lun, mar, jeu, ven 11h–14h · 18h–21h · dimanche 18h–21h. Pour commander : <a href=\"tel:{TEL}\" style=\"color:var(--gold)\">{TEL_TXT}</a>.",
               "comptoir-four", "Le comptoir de la pizzeria, le four et l'ancien four à pain")
     + """<nav class="menu-nav" aria-label="Rubriques de la carte"><div class="in"><a href="#tomate">Base tomate</a><a href="#creme">Base crème</a><a href="#moment">Du moment & desserts</a><a href="#boissons">Boissons</a><a href="#galerie">En images</a><a href="#menu-imprime">Le menu</a><a href="#allergenes">Allergènes</a></div></nav>
<div class="wrap" data-gallery>
<section class="menu-sec" id="tomate"><p class="eyebrow">Nos pizzas</p><h2>Base tomate</h2><div class="menu-grid">"""
     + "".join(dish(*d) for d in TOMATE) + """</div></section>
<section class="menu-sec" id="creme"><p class="eyebrow">Nos pizzas</p><h2>Base crème</h2><div class="menu-grid">"""
     + "".join(dish(*d) for d in CREME) + """</div></section>
<section class="menu-sec" id="moment"><p class="eyebrow">Pizza du moment & desserts</p><h2>Du moment & desserts</h2><div class="menu-grid">"""
     + dish("Pizza du moment : La Diavola", "12 €", "Pulpe de tomate, mozzarella, spianata piccante, basilic, origan, olive, huile d'olive. Nouvelle recette chaque semaine.", None, "Cette semaine")
     + dish("Glaces L'Angélys", "4 €", "Chocolat noisette, mangue, framboise, vanille, cacahuète. Les glaces artisanales de Charente-Maritime.", None, "Desserts")
     + dish("Ingrédient supplémentaire", "", "Œuf : 1 € · Fromage / viande : 1,5 € · Légume : 1 €")
     + """</div></section>
<section class="menu-sec" id="boissons"><p class="eyebrow">Pour accompagner</p><h2>Boissons</h2><div class="drinks-grid">"""
     + drinks_html
     + f"""</div></section>
<section class="menu-sec" id="galerie"><div class="gallery-head"><div><p class="eyebrow">En images</p><h2>Côté pizzeria</h2></div>
<div class="car-nav"><button class="car-btn" data-dir="-1" aria-label="Photos précédentes">‹</button><button class="car-btn" data-dir="1" aria-label="Photos suivantes">›</button></div></div>
<div class="carousel" data-gallery data-carousel tabindex="0" aria-label="Photos de la pizzeria, faites glisser">{gal(GALLERY)}</div></section>
<section class="menu-sec" id="menu-imprime"><p class="eyebrow">À consulter ou télécharger</p><h2>Le menu en images</h2>
<div class="menu-sheets">
<a class="sheet" href="img/menu-ramet-1.jpg" data-caption="Le menu — pizzas et boissons"><img src="img/menu-ramet-1.jpg" alt="Menu Pizza du Ramet : pizzas base tomate, base crème, pizza du moment et boissons" loading="lazy"></a>
<a class="sheet" href="img/menu-ramet-2.jpg" data-caption="Le menu — horaires, allergènes et contact"><img src="img/menu-ramet-2.jpg" alt="Menu Pizza du Ramet : horaires, informations allergènes et contact" loading="lazy"></a>
</div>
<div class="actions"><a class="btn btn-gold" href="tel:{TEL}">Commander par téléphone</a><a class="btn btn-outline" style="color:var(--green)" href="img/menu-ramet-1.jpg" download="menu-pizza-du-ramet.jpg">Télécharger le menu</a><a class="btn btn-outline" href="contact.html" style="color:var(--green)">Horaires & accès</a></div>
</section>
<section class="menu-sec" id="allergenes"><p class="eyebrow">Informations</p><h2>Allergènes</h2>
<p class="muted">Tableau indicatif des allergènes présents dans nos recettes. Traces possibles selon approvisionnements.</p>
<div class="table-scroll"><table class="allergens"><thead><tr><th>Pizza</th><th>Gluten</th><th>Lait</th><th>Poisson</th><th>Fruits à coque</th><th>Sulfites</th></tr></thead><tbody>"""
     + allergen_rows
     + """</tbody></table></div>
<div class="note"><strong>Remarques :</strong> supplément œuf : allergène œuf. Supplément fromage / viande : lait si fromage, sulfites possibles si charcuterie. Glaces : certains parfums contiennent des fruits à coque (chocolat noisette) ou de l'arachide (cacahuète). Pour toute allergie ou intolérance, merci de nous consulter avant de commander.</div>
</section>
</div>""")

# ---------------------------------------------------------------- Sur place & groupes
page("sur-place-groupes.html", "Sur place, entreprises & groupes — Pizza du Ramet",
     "Manger sur place à Pizza du Ramet (16 places) et organiser réunions, repas d'équipe ou projections dans une salle équipée d'un grand écran.",
     page_hero("16 places assises · grand écran", "Sur place, entreprises & groupes",
               "Déjeunez ou dînez sur place en toute simplicité, ou réunissez votre équipe dans une salle équipée, avec les pizzas en prime.",
               "terrasse-cour-domaine", "La cour du Ramet")
     + f"""<section class="wrap stack">
<article class="row reveal">{ph('tables-vertes-dessus', alt="Repas en terrasse")}<div><p class="eyebrow">Manger sur place</p><h2>Un espace simple et convivial</h2>
<p>Notre salle vous accueille pour vos repas sur place, en libre-service. Seul, en famille, entre collègues ou entre amis, profitez d'un cadre pratique et chaleureux pour déguster votre pizza — et de la terrasse aux beaux jours.</p>
<p class="muted">Idéal pour une pause déjeuner rapide, un dîner informel, un repas entre collègues ou une soirée autour d'un événement sportif.</p></div></article>
<article class="row flip reveal">{ph("salle-tables-vertes", alt="La salle de la pizzeria avec son grand écran, ses poutres et ses murs en pierre")}<div><p class="eyebrow">Salle équipée</p><h2>Un grand écran pour vos contenus</h2>
<p>La salle est équipée d'un grand écran pour la projection : réunions informelles, présentations, rencontres associatives ou matchs à regarder ensemble.</p>
<ul class="ticks" style="color:var(--ink)"><li>Réunions informelles</li><li>Présentations professionnelles</li><li>Clubs, associations, entreprises</li><li>Événements sportifs</li></ul></div></article>
</section>
<section class="band"><div class="wrap"><div class="center"><p class="eyebrow">Entreprises, associations, clubs</p><h2>Ce que nous proposons</h2></div>
<div class="cards">
<div class="card"><h3>Commandes groupées</h3><p>Une solution simple pour les pauses déjeuner, repas d'équipe ou moments entre collègues.</p></div>
<div class="card"><h3>Réunions informelles</h3><p>Un cadre moins formel qu'une salle classique, avec restauration sur place.</p></div>
<div class="card"><h3>Présentations</h3><p>Une salle équipée d'un grand écran pour la projection de contenus.</p></div>
</div></div></section>
<section class="wrap"><div class="row reveal"><div><p class="eyebrow">Comment organiser une venue ?</p><h2>En quatre étapes</h2>
<ol class="steps"><li>Contactez-nous par téléphone ou par e-mail.</li><li>Indiquez le nombre de personnes (16 places assises).</li><li>Précisez le besoin : repas, réunion, présentation ou projection.</li><li>Nous confirmons les possibilités.</li></ol>
<div class="actions"><a class="btn btn-gold" href="tel:{TEL}">{TEL_TXT}</a><a class="btn btn-outline" style="color:var(--green)" href="mailto:{MAIL}?subject=Organiser%20une%20venue%20au%20Ramet">Écrire un e-mail</a></div></div>
<div><p class="eyebrow">Et bientôt</p><h2>Encore plus de possibilités</h2>
<div class="road" style="grid-template-columns:1fr"><div class="step"><span class="when">Décembre 2026</span><h3>Team building golf</h3><p>Un tournoi sur le simulateur, suivi d'un repas pizza.</p><a href="golf.html">Le simulateur →</a></div>
<div class="step"><span class="when">Été 2027</span><h3>Séminaires avec hébergement</h3><p>Réunion, repas et nuit sur place dans nos gîtes et chambres d'hôtes.</p><a href="gites.html">Les gîtes →</a></div></div></div></div></section>""")

# ---------------------------------------------------------------- Golf
page("golf.html", "Simulateur de golf — Le Ramet, Les Gonds près de Saintes",
     "Simulateur de golf indoor au Ramet, Les Gonds près de Saintes : parcours virtuels, practice, soirées entre amis et team building. Ouverture début décembre 2026.",
     f"""<section class="page-hero">{ph(label="Visuel à venir : joueur devant l'écran du simulateur")}<div class="c">
<span class="badge">Ouverture début décembre 2026 · [date exacte à confirmer]</span>
<h1>Le golf s'invite au Ramet</h1>
<p>Un simulateur de golf indoor aux Gonds, à 5 minutes de Saintes. Parcours du monde entier, practice et défis entre amis — été comme hiver.</p>
<a class="btn btn-gold" href="#prevenir">Être prévenu de l'ouverture</a></div></section>

<section class="wrap"><div class="center"><p class="eyebrow">L'expérience</p><h2>Un vrai swing, des parcours mythiques</h2><p class="muted">Débutant curieux ou golfeur confirmé, chacun y trouve son jeu.</p></div>
<div class="cards">
<div class="card"><h3>Parcours virtuels</h3><p>Jouez 9 ou 18 trous sur des parcours célèbres. [Nombre de parcours à préciser]</p></div>
<div class="card"><h3>Practice & analyse</h3><p>Vitesse de balle, distance, trajectoire : progressez coup après coup.</p></div>
<div class="card"><h3>Jeux & défis</h3><p>Concours d'approche, plus long drive : idéal à plusieurs, même sans être golfeur.</p></div>
</div></section>

<section class="band" id="formules"><div class="wrap"><div class="center"><p class="eyebrow">Formules</p><h2>Pour toutes les occasions</h2><p style="opacity:.8">Tarifs communiqués à l'ouverture.</p></div>
<div class="plans">
<div class="plan"><h3>Partie libre</h3><div class="price">[–] €/h</div><ul><li>Location du simulateur à l'heure</li><li>Jusqu'à [x] joueurs</li><li>Clubs fournis</li></ul><a class="btn btn-outline" href="#prevenir">Me prévenir</a></div>
<div class="plan hl"><span class="badge" style="align-self:flex-start;margin-bottom:12px">Le plus convivial</span><h3>Golf & Pizza</h3><div class="price">[–] €/pers.</div><ul><li>Session de golf entre amis</li><li>Pizza du Ramet + boisson</li><li>Anniversaires, EVG/EVJF</li></ul><a class="btn btn-green" href="#prevenir">Me prévenir</a></div>
<div class="plan"><h3>Entreprises</h3><div class="price">Sur devis</div><ul><li>Team building & tournoi interne</li><li>Salle avec grand écran</li><li>Repas pizza dans notre salle</li></ul><a class="btn btn-outline" href="mailto:{MAIL}?subject=Golf%20entreprise">Demander un devis</a></div>
</div></div></section>

<section class="wrap"><div class="row reveal">{ph('tables-vertes-duo', alt="Deux pizzas en terrasse")}<div><p class="eyebrow">Golf & pizza</p><h2>Jouez, puis passez à table</h2>
<p class="muted">Enchaînez une partie de golf et un repas à la pizzeria, dans la même maison. À l'été 2027, vous pourrez aussi dormir sur place dans nos gîtes et chambres d'hôtes.</p>
<ol class="steps"><li>Réservez votre créneau de golf</li><li>Commandez vos pizzas pour l'après-partie</li><li>Profitez de la salle et de la terrasse</li></ol></div></div></section>

<section class="wrap tight" style="max-width:860px"><h2 class="center">Questions fréquentes</h2>
<details><summary>Faut-il savoir jouer au golf ?</summary><p>Non, le simulateur convient aux débutants comme aux confirmés. Les jeux et défis sont accessibles à tous.</p></details>
<details><summary>Le matériel est-il fourni ?</summary><p>Oui, clubs et balles sont fournis. Vous pouvez aussi venir avec vos propres clubs.</p></details>
<details><summary>Combien de joueurs par session ?</summary><p>[À préciser selon le simulateur — généralement jusqu'à 4 à 6 joueurs.]</p></details>
<details><summary>Comment réserver ?</summary><p>À l'ouverture, par téléphone au {TEL_TXT} [ou en ligne — module de réservation à brancher].</p></details>
</section>

<section class="wrap tight" id="prevenir"><div class="notify"><p class="eyebrow">Soyez les premiers</p><h2>Prévenez-moi de l'ouverture</h2><p style="opacity:.8">Recevez la date d'ouverture et l'offre de lancement.</p>
<form data-subject="Prévenez-moi : ouverture du golf"><input type="email" required placeholder="Votre adresse e-mail" aria-label="Votre adresse e-mail"><button class="btn btn-gold">Me prévenir</button></form></div></section>""")

# ---------------------------------------------------------------- Gîtes (été 2027)
page("gites.html", "Gîtes & chambres d'hôtes — Le Ramet, ouverture été 2027",
     "Le Ramet ouvre ses gîtes et chambres d'hôtes aux Gonds, près de Saintes, à l'été 2027. Soyez informé de l'ouverture.",
     page_hero("Ouverture été 2027", "Gîtes & chambres d'hôtes",
               "Bientôt, vous pourrez séjourner au Ramet : au calme, au cœur de la Saintonge, avec la pizzeria et le golf sur place.",
               "terrasse-cour-domaine", "La cour du domaine")
     + f"""<section class="wrap"><div class="center reveal"><p class="eyebrow">En préparation</p><h2>Un domaine pour se poser</h2>
<p class="muted">Nous préparons des gîtes pour les familles et les groupes, et des chambres d'hôtes pour une nuit ou un week-end. Les photos, capacités et tarifs seront publiés ici à l'approche de l'ouverture.</p></div>
<div class="cards">
<div class="card"><div class="num">01</div><h3>Les gîtes</h3><p>Pour les séjours en famille ou entre amis. [Capacité et équipements à préciser]</p></div>
<div class="card"><div class="num">02</div><h3>Les chambres d'hôtes</h3><p>Pour une nuit ou un week-end, avec petit-déjeuner. [À préciser]</p></div>
<div class="card"><div class="num">03</div><h3>Les séminaires</h3><p>Réunion, repas et hébergement sur place pour les entreprises.</p></div>
</div></section>
<section class="wrap tight"><div class="row reveal">{ph('terrasse-pizza-batisse', alt="La bâtisse en pierre du Ramet")}<div><p class="eyebrow">Tout sur place</p><h2>Dormir, savourer, jouer</h2>
<p class="muted">Nos hôtes auront la pizzeria à quelques pas et le simulateur de golf sous le même toit. En attendant, venez déjà nous rendre visite !</p>
<div class="actions"><a class="btn btn-gold" href="la-carte.html">Voir la carte</a><a class="btn btn-outline" style="color:var(--green)" href="golf.html">Le golf</a></div></div></div></section>
<section class="wrap tight"><div class="notify"><p class="eyebrow">Été 2027</p><h2>Être informé de l'ouverture</h2><p style="opacity:.8">Laissez votre e-mail, nous vous préviendrons dès l'ouverture des réservations.</p>
<form data-subject="Prévenez-moi : ouverture des gîtes"><input type="email" required placeholder="Votre adresse e-mail" aria-label="Votre adresse e-mail"><button class="btn btn-gold">Me prévenir</button></form></div></section>""")

# ---------------------------------------------------------------- Ancrage local
page("ancrage-local.html", "Ancrage local — Pizza du Ramet et la Minoterie Méchain",
     "Pizza du Ramet travaille une farine locale de la Minoterie Méchain à Courcelles : une pizzeria ancrée dans son territoire.",
     page_hero("Du territoire à votre assiette", "Une pizzeria ancrée dans son territoire",
               "Aux Gonds, Pizza du Ramet fait le choix de la proximité, du bon sens et des savoir-faire locaux.",
               "preparation", "Préparation des pizzas")
     + """<section class="wrap stack">
<article class="row reveal">""" + ph('cuisine-four', alt="En cuisine devant le four") + """<div><p class="eyebrow">Le choix d'une farine locale</p><h2>La Minoterie Méchain, à Courcelles</h2>
<p>Pour réaliser nos pâtes, nous avons choisi une farine issue de la Minoterie Méchain, située à Courcelles, à proximité de notre pizzeria.</p>
<p class="muted">Ce choix reflète notre volonté de proposer des pizzas ancrées dans notre territoire, en privilégiant des partenaires proches lorsque cela est possible.</p></div></article>
<article class="row flip reveal">""" + ph('four-cuisson', alt="Pizzas en cuisson dans le four") + """<div><p class="eyebrow">Notre ambition</p><h2>Proche de nos clients et de nos fournisseurs</h2>
<p>Construire une pizzeria proche de ses clients, de ses fournisseurs et de son environnement.</p></div></article>
</section>
<section class="band"><div class="wrap"><div class="cards" style="grid-template-columns:repeat(4,1fr)">
<div class="card"><h3>Proximité géographique</h3></div><div class="card"><h3>Savoir-faire local</h3></div><div class="card"><h3>Authenticité</h3></div><div class="card"><h3>Soutien au tissu local</h3></div>
</div></div></section>""")

# ---------------------------------------------------------------- Contact
HOURS = [(1, "Lundi", "11h00 – 14h00", "18h00 – 21h00"), (2, "Mardi", "11h00 – 14h00", "18h00 – 21h00"),
         (3, "Mercredi", "Fermé", "Fermé"), (4, "Jeudi", "11h00 – 14h00", "18h00 – 21h00"),
         (5, "Vendredi", "11h00 – 14h00", "18h00 – 21h00"), (6, "Samedi", "Fermé", "Fermé"),
         (0, "Dimanche", "Fermé", "18h00 – 21h00")]
rows = "".join(f'<tr data-d="{d}"{CLOSED if m == e == "Fermé" else ""}><td>{n}</td><td>{m}</td><td>{e}</td></tr>' for d, n, m, e in HOURS)
page("contact.html", "Contact & accès — Pizza du Ramet, Les Gonds",
     "Contact, horaires et accès de Pizza du Ramet, 56 rue Maurice Ravel, 17100 Les Gonds. Commandes par téléphone au 06 13 45 70 56.",
     page_hero("Contact & accès", "Retrouvez-nous aux Gonds",
               "Pour vos pizzas à emporter ou à déguster sur place, vos réunions et vos questions sur le golf et les gîtes.")
     + f"""<section class="wrap"><div class="info reveal">
<div class="card"><p class="eyebrow">Adresse</p><h3>56 rue Maurice Ravel<br>17100 Les Gonds</h3><a class="more" href="{MAPS}" target="_blank" rel="noopener">Itinéraire Google Maps</a></div>
<div class="card"><p class="eyebrow">Téléphone</p><h3><a href="tel:{TEL}" style="text-decoration:none">{TEL_TXT}</a></h3><p>Commandes par téléphone ou sur place.</p></div>
<div class="card"><p class="eyebrow">E-mail</p><h3 style="font-size:1rem;word-break:break-all"><a href="mailto:{MAIL}" style="text-decoration:none">{MAIL}</a></h3><p>Groupes, réunions, golf, gîtes.</p></div>
</div></section>
<section class="wrap tight"><div class="row reveal" style="align-items:stretch"><div><p class="eyebrow">Horaires d'ouverture</p><h2>Pizzeria</h2>
<table class="hours"><thead><tr><th>Jour</th><th>Midi</th><th>Soir</th></tr></thead><tbody>{rows}</tbody></table>
<p class="muted" style="margin-top:18px"><strong>Paiement :</strong> carte bancaire ou espèces.</p>
<div class="actions"><a class="btn btn-gold" href="tel:{TEL}">Appeler</a><a class="btn btn-outline" style="color:var(--green)" href="{MAPS}" target="_blank" rel="noopener">Itinéraire</a></div></div>
<iframe class="map" title="Plan d'accès Pizza du Ramet" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=56+rue+Maurice+Ravel,+17100+Les+Gonds&output=embed"></iframe></div></section>""")

# ---------------------------------------------------------------- Mentions légales
page("mentions-legales.html", "Mentions légales — Le Ramet", "Mentions légales et données personnelles du site leramet.fr.",
     page_hero("Informations légales", "Mentions légales", "Informations légales du site www.leramet.fr.")
     + f"""<section class="wrap prose">
<h2>Éditeur du site</h2><p>Le présent site est édité par Pizza du Ramet / Le Ramet, 56 rue Maurice Ravel, 17100 Les Gonds, France. Téléphone : {TEL_TXT} — E-mail : {MAIL}.</p>
<p>Raison sociale : SARL LE RAMET — Forme juridique : SARL — Capital social : 450 000 € — SIRET : 890 663 974 00024 — RCS : Saintes 890 663 974 — Responsable de publication : information à compléter.</p>
<h2>Hébergement</h2><p>Le site est hébergé par OVH SAS, 2 rue Kellermann, 59100 Roubaix, France — www.ovhcloud.com.</p>
<h2>Propriété intellectuelle</h2><p>L'ensemble des contenus présents sur le site (textes, images, graphismes, logo, icônes, photographies, illustrations, structure générale) sont la propriété exclusive de leur auteur ou font l'objet d'une autorisation d'utilisation. Toute reproduction ou exploitation non autorisée est interdite.</p>
<h2 id="donnees">Données personnelles</h2><p>Les informations transmises par e-mail ou téléphone sont destinées exclusivement à Pizza du Ramet afin de répondre aux demandes des utilisateurs. Aucune donnée personnelle n'est cédée, vendue ou transmise à des tiers à des fins commerciales.</p>
<p>La carte d'accès de la page Contact est fournie par Google Maps, qui peut déposer ses propres cookies lors de son affichage.</p>
<h2>Responsabilité</h2><p>Les informations présentes sur le site sont données à titre indicatif et peuvent évoluer. Les horaires, tarifs, recettes, disponibilités et informations pratiques peuvent être modifiés à tout moment. Il est recommandé de contacter directement Pizza du Ramet pour confirmer une information.</p>
</section>""")

print("Pages générées.")
