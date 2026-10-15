# Le Ramet — site internet

Site de Pizza du Ramet / Le Ramet (Les Gonds, près de Saintes) : pizzeria, salle pour groupes, simulateur de golf (décembre 2026), gîtes et chambres d'hôtes (été 2027).

## Modifier le site

Toutes les pages sont générées par `_build.py` (textes, carte, prix, allergènes, photos).

1. Modifier le contenu dans `_build.py` (ou le style dans `assets/site.css`).
2. Régénérer les pages : `python3 _build.py`
3. Prévisualiser : `python3 -m http.server 8765` puis ouvrir http://localhost:8765

## Dossiers

- `img/` : photos optimisées pour le web (position GPS retirée)
- `assets/` : style, script, logos
- `photos/` : originaux de l'iPhone, **non versionnés** (voir `.gitignore`)
- `version-b-moderne.html`, `version-c-immersive.html` : pistes de design alternatives pour l'accueil
