# Thème Shopify DUNVEA

Thème Shopify 2.0 sur mesure pour **DUNVEA** — étagères flottantes et miroirs organiques en bois massif.
Architecture inspirée de Horizon (sections JSON, blocs, groupes de sections), page produit construite sur
le modèle de présentation Tikamoon : galerie 60 % / achat 40 %, puis sections empilées sans onglets.

---

## 1. Structure

```
layout/      theme.liquid (gabarit principal), password.liquid
templates/   index, product (+ duo, etagere, miroir, pack), page (+ atelier, faq, contact),
             collection, cart, search, 404, blog, article, password, gift_card, customers/*
sections/    toutes les sections (voir tableau ci-dessous) + header-group.json / footer-group.json
snippets/    icônes, prix, carte produit, fil d'Ariane, note étoilée, JSON-LD, etc.
assets/      base.css, product.css, custom.css, theme.js
config/      settings_schema.json (réglages du thème), settings_data.json
locales/     fr.default.json (tous les textes d'interface)
scripts/     générateurs des templates JSON (non envoyés à Shopify)
```

### Page produit — ordre des sections

| # | Section | Fichier | Contenu |
|---|---------|---------|---------|
| — | Above the fold | `main-product.liquid` | Fil d'Ariane · galerie (grande image + miniatures, zoom plein écran, swipe mobile) · H1 · note avis · badges · 4 points clés · dimensions · prix + prix barré + « Économisez X € » · choix du bois (pastilles) · quantité · « Ajouter au panier » · délai · 4 icônes de réassurance · barre d'achat fixe sur mobile |
| 1 | Description | `product-story.liquid` | Chapitres L'histoire / Les matériaux / La fabrication (texte, image optionnelle en alternance) |
| 2 | Caractéristiques | `product-specs.liquid` | Tableau libellé / valeur, groupé (Étagère / Miroir) |
| 3 | Installation | `product-steps.liquid` | Étapes numérotées + mention « 10 minutes » |
| 4 | Entretien | `product-info-list.liquid` | Liste à icônes |
| 5 | Livraison et retours | `product-info-list.liquid` | Liste à icônes |
| 6 | Avis clients | `product-reviews.liquid` | « Ils ont choisi DUNVEA » — bloc Judge.me, ou « Soyez le premier à donner votre avis » |
| 7 | Complétez votre mur | `complete-your-wall.liquid` | Cross-sell : Miroir/Étagère → Duo, Duo → Pack |
| 8 | Vous aimerez aussi | `product-recommendations.liquid` | Recommandations Shopify |

Chaque produit a son template prérempli avec le copywriting :

| Template | Produit | Cross-sell |
|----------|---------|-----------|
| `product.duo` | Duo Étagère + Miroir (héros) | → Pack |
| `product.etagere` | Étagère seule | → Duo |
| `product.miroir` | Miroir seul | → Duo |
| `product.pack` | Pack 2 étagères + miroir | — |
| `product` (défaut) | tout autre produit | utilise la description Shopify |

---

## 2. Installer le thème dans Shopify

**Option A — intégration GitHub (recommandée)**
1. Shopify Admin → **Boutique en ligne → Thèmes**.
2. **Ajouter un thème → Connecter depuis GitHub**, choisissez le dépôt `riadh-ai/web-dunvea` et la branche.
3. Le thème apparaît dans la bibliothèque. **Personnaliser** pour le prévisualiser, **Publier** quand tout est prêt.
   Chaque modification faite dans l'éditeur est recommitée par Shopify sur la branche.

**Option B — Shopify CLI**
```bash
shopify theme dev --store votre-boutique.myshopify.com   # aperçu local
shopify theme push --unpublished                          # envoi en thème non publié
```

> Le dossier `scripts/` et ce README sont ignorés par Shopify (`.shopifyignore`).

---

## 3. Configurer les produits

### 3.1 Créer les 4 produits

| Produit | Prix | Prix barré (« Prix avant réduction ») | Handle (URL) | Template |
|---------|------|------------------|--------------|----------|
| Miroir Mural Organique | 89 € | — | `miroir-mural-organique-frene-massif` | `product.miroir` |
| Étagère Murale Flottante | 99 € | — | `etagere-murale-flottante-frene-massif` | `product.etagere` |
| **Duo Étagère + Miroir** | 149 € | 188 € | `duo-etagere-miroir-frene-massif` | `product.duo` |
| Pack 2 Étagères + Miroir | 229 € | 287 € | `pack-mural-complet-frene-massif` | `product.pack` |

Pour chaque produit :
1. **Option de variante** : nommez l'option **`Bois`** avec les valeurs **`Frêne massif`** et **`Acajou`**
   (les pastilles de couleur et le JSON-LD reconnaissent ce nom).
2. **Prix barré** : renseignez « Prix avant réduction » sur chaque variante du Duo et du Pack — le badge
   « Prix lot », le prix barré et « Économisez 39 € / 58 € » s'affichent automatiquement.
3. **Images de variante** : associez une image à chaque variante (Frêne / Acajou) — la galerie bascule dessus
   quand le client choisit le bois.
4. **Template** : dans la fiche produit, panneau de droite **Modèle de thème** → choisissez le template du tableau.
5. **Handle** : section « Référencement » → URL et handle.

> Les sections « Complétez votre mur » pointent vers les handles ci-dessus. Si vous en changez un,
> re-sélectionnez le produit dans l'éditeur (Personnaliser → template produit → Complétez votre mur).

### 3.2 Le H1 (titre affiché)

Le H1 utilise le métachamp **`custom.h1`** s'il existe, sinon le titre du produit.
Cela permet d'avoir un titre court dans le panier (« Duo Étagère + Miroir ») et un H1 SEO complet sur la page.

Créer la définition : **Paramètres → Données personnalisées → Produits → Ajouter une définition**
- Nom : `H1` · Espace de nom et clé : `custom.h1` · Type : **Texte sur une seule ligne**

Puis remplir sur chaque produit (valeurs en section 5).

Métachamps optionnels (remplacent les textes de l'éditeur s'ils sont remplis) :
- `custom.bullets` — Liste de textes sur une ligne : les 4 points clés
- `custom.dimensions` — Texte multiligne : le bloc « Dimensions »

### 3.3 Livraison offerte

Le thème **affiche** « Livraison offerte » ; il faut aussi **créer le tarif** :
**Paramètres → Expédition et livraison → France → Ajouter un tarif → Gratuit**.

---

## 4. Créer les pages, menus et collection

**Pages** (Boutique en ligne → Pages → Ajouter une page), puis choisir le **Modèle de thème** :

| Titre | Handle | Template |
|-------|--------|----------|
| L'atelier | `atelier` | `page.atelier` |
| FAQ | `faq` | `page.faq` |
| Contact | `contact` | `page.contact` |

Le contenu de ces pages est déjà dans les templates (modifiable dans l'éditeur) ; le corps de la page Shopify peut rester vide.

**Menus** (Boutique en ligne → Navigation) :
- `main-menu` : Étagères · Miroirs · Le Duo · L'atelier · FAQ
- `footer` : Le Duo · Étagère · Miroir · Pack · L'atelier
- un second menu « Aide » (FAQ · Livraison et retours · Contact · CGV · Mentions légales) à sélectionner dans
  Personnaliser → Pied de page → Menu 2.

**Collection** : la section « Collection mise en avant » de l'accueil affiche tous les produits par défaut.
Vous pouvez créer une collection (ex. « Étagères & miroirs ») et la sélectionner — elle sert aussi au fil d'Ariane.

---

## 5. SEO — à copier-coller dans chaque fiche produit

Fiche produit → **Aperçu du référencement sur les moteurs de recherche → Modifier**.
(Le thème n'ajoute pas « | DUNVEA » si le titre le contient déjà.)

### Duo Étagère + Miroir (produit héros)
- **Titre de la page** : `Duo Étagère Murale + Miroir Bois Massif — Frêne Artisanal | DUNVEA`
- **Méta-description** : `Le duo étagère flottante + miroir organique en frêne massif, fabriqué main dans notre atelier. Fixation invisible, design épuré. Économisez 39€ sur le duo. Livraison offerte.`
- **Handle** : `duo-etagere-miroir-frene-massif`
- **H1 (`custom.h1`)** : `Duo Étagère Flottante + Miroir Organique — Frêne Massif Artisanal`

### Étagère seule
- **Titre** : `Étagère Murale Flottante Bois Massif — Frêne Artisanal | DUNVEA`
- **Méta** : `Étagère flottante en frêne massif, fabriquée main. Design épuré 50×14 cm, fixation invisible incluse. Livraison offerte en France.`
- **Handle** : `etagere-murale-flottante-frene-massif`
- **H1** : `Étagère Murale Flottante — Frêne Massif Artisanal`

### Miroir seul
- **Titre** : `Miroir Mural Organique Bois Massif — Frêne Artisanal | DUNVEA`
- **Méta** : `Miroir organique en frêne massif, forme naturelle unique. Cadre artisanal 53×32 cm, fixation invisible. Livraison offerte.`
- **Handle** : `miroir-mural-organique-frene-massif`
- **H1** : `Miroir Mural Organique — Frêne Massif Artisanal`

### Pack complet
- **Titre** : `Pack Mural 2 Étagères + Miroir Bois Massif | DUNVEA`
- **Méta** : `Pack complet 2 étagères flottantes + miroir organique en frêne massif. Économisez 58€. Fixation invisible, fait main. Livraison offerte.`
- **Handle** : `pack-mural-complet-frene-massif`
- **H1** : `Pack Mural Complet — 2 Étagères + Miroir Frêne Massif`

### Données structurées (JSON-LD) — automatiques
`snippets/structured-data-product.liquid` génère pour chaque produit un schéma **Product** :
`name` (H1), `description` (méta-description), `image`, `brand` DUNVEA, `sku`, `material`, et une **Offer par variante**
(`price` 149.00, `priceCurrency` EUR, `availability` InStock/OutOfStock, livraison gratuite France, retours 14 jours).
`aggregateRating` n'est ajouté **que lorsque des avis existent** (métachamps `reviews.rating` / `reviews.rating_count`).
S'y ajoutent `BreadcrumbList` (fil d'Ariane), `FAQPage` (page FAQ), `Organization` + `WebSite` (accueil).
Vérification : [Test des résultats enrichis Google](https://search.google.com/test/rich-results).

---

## 6. Avis clients — Judge.me

1. Installez **Judge.me Product Reviews** (gratuit) depuis l'App Store Shopify.
2. Personnaliser → **Paramètres de l'application** (App embeds) → activez Judge.me.
3. Sur chaque template produit, section **Avis clients** → **Ajouter un bloc → Applications → Review Widget**.
4. Pour les étoiles sous le H1 et dans le JSON-LD, le thème lit les métachamps standards de Shopify
   `reviews.rating` et `reviews.rating_count`. Vérifiez dans les réglages Judge.me que la synchronisation
   des avis vers les métachamps Shopify est active.

Au lancement, sans avis : la section affiche « Soyez le premier à donner votre avis ».
Sur l'accueil, elle est masquée tant qu'il n'y a ni avis ni bloc Judge.me (réglage « Masquer la section… »).

---

## 7. ⚠️ À compléter avant le lancement

Ces valeurs n'étaient pas connues ; elles sont affichées entre crochets pour ne pas être oubliées.
Remplacez-les dans **Personnaliser** (ou dans les templates JSON).

| Où | Texte à remplacer |
|----|-------------------|
| Bloc « Bouton d'achat » (tous les produits) | `Fabriqué et expédié sous [X] jours ouvrés` |
| Section « Livraison et retours » (tous les produits) | `[X] jours ouvrés` |
| Fiche technique Étagère | Charge supportée `[à confirmer]`, Poids `[à confirmer]` |
| Fiche technique Miroir | Poids `[à confirmer]` |
| FAQ | délai `[X]`, charge `[à confirmer]` kg |
| Contact | `[adresse e-mail]`, `[délai de réponse]` |
| Réglages du thème → Réseaux sociaux | liens Instagram / Pinterest / TikTok |

Pour vérifier qu'il n'en reste aucun : `grep -rn "\[X\]\|\[à confirmer\]\|\[adresse\|\[délai" templates sections`

**Images à ajouter dans l'éditeur** : bannière d'accueil et atelier, images des chapitres de description
(optionnelles, alternance texte/image), image d'installation, photos des deux bois, images des sections « Image et texte ».

**Installation du miroir** : les étapes du miroir sont rédigées d'après « rail dissimulé derrière le cadre » —
relisez-les par rapport à votre système réel.

---

## 8. Identité visuelle

Réglages du thème → **Couleurs / Typographie** :

| Jeton | Valeur | Variable CSS |
|-------|--------|--------------|
| Charbon (texte, bouton) | `#2C2C2A` | `--color-charbon` |
| Terre (accent bois) | `#9C6B3F` | `--color-terre` |
| Beige (fond) | `#F2EEE6` | `--color-beige` |
| Blanc (sections) | `#FFFFFF` | `--color-blanc` |
| Titres | Montserrat 600 (bold 700 pour le prix) | `--font-heading-family` |
| Texte | Montserrat 300 | `--font-body-family` |

Logo : texte « DUNVEA » en capitales, espacement large (Réglages → Logo ; une image peut le remplacer).

**Ajustements CSS** : écrivez-les dans `assets/custom.css` (chargé en dernier) plutôt que dans `base.css` /
`product.css`, pour pouvoir mettre à jour le thème sans perdre vos modifications.

---

## 9. Modifier les textes

- **Au quotidien** : Personnaliser → choisissez le template (ex. Produits → duo) → cliquez sur la section.
- **En masse** : les textes de départ sont dans `scripts/build_product_templates.py` et
  `scripts/build_page_templates.py`. `python3 scripts/build_product_templates.py` régénère les templates —
  **cela écrase les modifications faites dans l'éditeur** sur ces fichiers.
- **Textes d'interface** (« Ajouter au panier », panier, formulaires) : `locales/fr.default.json`.

---

## 10. Ce qui a été vérifié

- `theme-check` (linter officiel Shopify) : 0 erreur ; 2 avertissements de préchargement de police
  (même approche que le thème Dawn).
- Les 27 templates JSON sont validés contre les schémas des sections (types de blocs, ids, valeurs de range/select).
- Rendu local (moteur Liquid + données simulées) de la page produit, de l'accueil, de l'atelier, de la FAQ et
  du contact à 390 px et 1440 px : pas de défilement horizontal, interactions testées (choix du bois → prix,
  variante, image ; miniatures ; barre d'achat fixe mobile).
- **Pas encore testé sur une vraie boutique Shopify** : l'ajout au panier AJAX, les recommandations, les formulaires
  et Judge.me ne fonctionnent qu'en ligne. À contrôler avec `shopify theme dev` ou l'aperçu du thème.
