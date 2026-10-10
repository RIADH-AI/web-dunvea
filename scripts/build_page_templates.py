#!/usr/bin/env python3
"""
Génère les templates JSON de la page d'accueil, des pages secondaires
(atelier, FAQ, contact) et des templates système.

Usage : python3 scripts/build_page_templates.py
Attention : relancer le script écrase les modifications faites dans l'éditeur
sur ces templates (récupérez-les d'abord avec `shopify theme pull`).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

URL_DUO = "/products/duo-etagere-miroir-frene-massif"
HANDLE_DUO = "duo-etagere-miroir-frene-massif"


def p(*paragraphs):
    return "".join(f"<p>{x}</p>" for x in paragraphs)


def clean(settings):
    return {k: v for k, v in settings.items() if v != ""}


def section(stype, settings=None, items=None):
    sec = {"type": stype, "settings": clean(settings or {})}
    if items:
        sec["blocks"] = {bid: {"type": t, "settings": clean(s)} for bid, t, s in items}
        sec["block_order"] = [bid for bid, _, _ in items]
    return sec


def template(sections, layout=None):
    data = {"sections": dict(sections), "order": [k for k, _ in sections]}
    if layout:
        data["layout"] = layout
    return data


def write(name, data):
    path = TEMPLATES / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("écrit", path.relative_to(ROOT))


WOODS = section("wood-comparison", {
    "eyebrow": "Deux bois", "heading": "Clair ou profond, toujours massif",
    "text": p("Chaque pièce DUNVEA existe en deux essences. Le choix se fait selon la lumière de la pièce et l'ambiance que vous cherchez."),
    "background": "blanc", "padding_top": 112, "padding_bottom": 112,
}, [
    ("frene", "wood", {
        "name": "Frêne massif", "swatch": "#D9B98C",
        "text": "Un bois clair, au grain fin et élégant, originaire d'Europe. Sa couleur naturelle, dorée et miel, éclaire un mur sans l'écraser. Dense et très résistant, c'est un bois d'ébéniste par excellence.",
        "traits": "Clair, Grain fin, Très résistant, Européen",
    }),
    ("acajou", "wood", {
        "name": "Acajou", "swatch": "#6E3B2B",
        "text": "Un bois sombre, au grain profond et chaleureux. Sa couleur brun-rouge apporte immédiatement une présence chaleureuse et sophistiquée. Un bois noble, connu pour sa durabilité et sa beauté.",
        "traits": "Sombre, Grain profond, Durable, Noble",
    }),
])

REASSURANCE_ITEMS = [
    ("r1", "item", {"icon": "truck", "title": "Livraison offerte", "text": "France métropolitaine"}),
    ("r2", "item", {"icon": "return", "title": "Retours 14 jours", "text": "Dans l'emballage d'origine"}),
    ("r3", "item", {"icon": "wood", "title": "Bois massif véritable", "text": "Ni placage, ni MDF"}),
    ("r4", "item", {"icon": "hand", "title": "Fabriqué main", "text": "Dans notre atelier"}),
]

# ---------------------------------------------------------------------------
# Page d'accueil
# ---------------------------------------------------------------------------
index = template([
    ("hero", section("image-banner", {
        "eyebrow": "Fait main · Bois massif",
        "heading": "Le bois massif, à hauteur de mur",
        "heading_tag": "h1",
        "text": p("Étagères flottantes et miroirs organiques, taillés à la main dans le frêne et l'acajou. Fixation invisible : on ne voit que le bois."),
        "button_label_1": "Découvrir le duo", "button_link_1": URL_DUO,
        "button_label_2": "Toute la collection", "button_link_2": "/collections/all",
        "style": "dark", "overlay": 40, "alignment": "left", "vertical": "bottom", "height": "large",
    })),
    ("reassurance", section("reassurance-bar", {"background": "beige", "padding": 48}, REASSURANCE_ITEMS)),
    ("duo", section("featured-product", {
        "product": HANDLE_DUO,
        "ratio": "portrait",
        "eyebrow": "Notre duo signature",
        "heading": "L'étagère et le miroir, ensemble",
        "text": p("L'étagère semble flotter, le miroir adoucit les lignes. Ensemble, ils créent un point focal naturel dans votre salon, votre entrée ou votre bureau."),
        "button_label": "Découvrir le duo", "reverse": False,
        "background": "blanc", "padding_top": 112, "padding_bottom": 112,
    }, [
        ("i1", "include", {"text": "1 étagère flottante 50 × 14 cm + 1 miroir organique 53 × 32 cm"}),
        ("i2", "include", {"text": "Frêne massif européen ou acajou"}),
        ("i3", "include", {"text": "Fixation invisible incluse pour les deux pièces"}),
        ("i4", "include", {"text": "39 € d'économie par rapport aux pièces séparées"}),
    ])),
    ("collection", section("featured-collection", {
        "eyebrow": "La collection", "heading": "Quatre pièces, deux bois",
        "text": p("Une étagère, un miroir, et les deux réunis. Rien de plus — chaque pièce est pensée pour aller avec les autres."),
        "products_to_show": 4, "columns": "4", "center": True,
        "button_label": "Voir toute la collection",
        "background": "beige", "padding_top": 112, "padding_bottom": 112,
    })),
    ("manifesto", section("rich-text", {
        "eyebrow": "Notre parti pris",
        "heading": "Une machine ne sent pas le bois comme un artisan le sent.",
        "heading_tag": "p", "style": "quote",
        "text": p("C'est pour cela que la découpe, le ponçage, le biseau et la finition de chaque pièce sont faits à la main, dans notre atelier. C'est plus lent. C'est voulu."),
        "button_label": "Découvrir l'atelier", "button_link": "/pages/atelier", "button_secondary": True,
        "alignment": "center", "background": "beige", "padding_top": 96, "padding_bottom": 112,
    })),
    ("woods", WOODS),
    ("atelier", section("image-with-text", {
        "ratio": "portrait", "reverse": True, "wide_media": True,
        "eyebrow": "L'atelier",
        "heading": "Deux pièces ne sont jamais identiques",
        "text": p(
            "Chaque étagère et chaque miroir est taillé dans un bloc unique. Les veines du bois, la nuance exacte de la couleur, la subtilité du grain — ce sont les signatures de votre pièce.",
            "Pas de placage, pas de MDF caché sous une couche de vernis. Du bois massif de bout en bout, conçu pour durer et vieillir avec grâce.",
        ),
        "button_label": "Voir comment nous travaillons", "button_link": "/pages/atelier", "button_secondary": True,
        "background": "beige", "padding_top": 112, "padding_bottom": 112,
    })),
    ("install", section("multicolumn", {
        "eyebrow": "Installation", "heading": "Dix minutes, une perceuse, un niveau",
        "text": p("Tout est fourni dans la boîte. Le système fonctionne sur mur placo et béton."),
        "marker": "number", "center": False, "background": "blanc", "padding_top": 112, "padding_bottom": 112,
    }, [
        ("c1", "column", {"title": "Positionnez le gabarit", "text": p("Le gabarit de perçage est inclus. Un coup de niveau, deux repères.")}),
        ("c2", "column", {"title": "Percez et vissez", "text": p("Deux trous, deux chevilles, les supports invisibles.")}),
        ("c3", "column", {"title": "Accrochez", "text": p("L'étagère glisse sur ses supports, le miroir se pose sur son rail. Aucune vis ne reste visible.")}),
    ])),
    ("reviews", section("product-reviews", {
        "eyebrow": "Avis clients", "heading": "Ils ont choisi DUNVEA",
        "empty_title": "Soyez le premier à donner votre avis",
        "hide_when_empty": True, "background": "beige", "padding_top": 96, "padding_bottom": 96,
    })),
    ("newsletter", section("newsletter", {
        "eyebrow": "Newsletter", "heading": "Des nouvelles de l'atelier",
        "text": p("Nouvelles pièces, coulisses de fabrication, conseils d'aménagement. Un e-mail par mois, pas plus."),
        "background": "blanc", "padding_top": 96, "padding_bottom": 96,
    })),
])

# ---------------------------------------------------------------------------
# Page Atelier
# ---------------------------------------------------------------------------
atelier = template([
    ("hero", section("image-banner", {
        "eyebrow": "L'atelier",
        "heading": "Le même atelier, les mêmes mains",
        "heading_tag": "h1",
        "text": p("Chaque pièce DUNVEA est découpée, poncée et finie à la main. Voici comment."),
        "style": "dark", "overlay": 45, "alignment": "left", "vertical": "bottom", "height": "small",
    })),
    ("intro", section("rich-text", {
        "eyebrow": "Notre parti pris",
        "heading": "Moins de pièces, mieux faites.",
        "text": p(
            "Nous avons choisi de ne fabriquer que quelques objets : une étagère flottante, un miroir organique, et les deux réunis. Tout notre temps va à ces pièces-là.",
            "Le travail manuel n'est pas un argument marketing : c'est une contrainte que nous avons choisie. Elle nous oblige à regarder chaque planche, à suivre son fil, à décider où passera la coupe. Une machine ne sent pas le bois comme un artisan le sent.",
        ),
        "alignment": "center", "background": "beige", "padding_top": 112, "padding_bottom": 80,
    })),
    ("process", section("multicolumn", {
        "eyebrow": "La fabrication", "heading": "Quatre étapes, toutes à la main",
        "marker": "number", "ratio": "portrait", "center": False,
        "background": "beige", "padding_top": 40, "padding_bottom": 112,
    }, [
        ("s1", "column", {"title": "Le choix du bois", "text": p("Chaque pièce est taillée dans un bloc unique de frêne massif européen ou d'acajou. Nous lisons le fil et les veines avant de décider de la coupe.")}),
        ("s2", "column", {"title": "La découpe", "text": p("L'étagère est mise à dimension, le cadre du miroir dessiné suivant une ligne libre. Aucune forme n'est reproduite à l'identique.")}),
        ("s3", "column", {"title": "Le ponçage et le biseau", "text": p("L'arête avant de l'étagère est biseautée à la main ; les courbes du miroir sont reprises jusqu'à ce que le bois soit doux sous les doigts.")}),
        ("s4", "column", {"title": "La finition", "text": p("Une huile protectrice nourrit le bois et révèle son grain, sans le recouvrir d'une couche de vernis plastique.")}),
    ])),
    ("massif", section("image-with-text", {
        "ratio": "portrait", "reverse": False, "wide_media": True,
        "eyebrow": "Le matériau",
        "heading": "Du bois massif, de bout en bout",
        "text": p(
            "Pas de placage, pas de MDF caché sous une couche de vernis. Ce que vous touchez quand vous passez la main sur une pièce DUNVEA, c'est le grain réel du bois, pas une imitation imprimée.",
            "Le bois massif vit : il se patine, prend la lumière, gagne en caractère avec les années. Dans dix ans, votre étagère aura pris une teinte que l'aggloméré ne connaîtra jamais.",
        ),
        "background": "blanc", "padding_top": 112, "padding_bottom": 112,
    })),
    ("woods", WOODS),
    ("unique", section("image-with-text", {
        "ratio": "portrait", "reverse": True, "wide_media": True,
        "eyebrow": "Pièces uniques",
        "heading": "Les signatures de votre pièce",
        "text": p(
            "Parce que tout est fait à la main, deux pièces ne sont jamais parfaitement identiques. Les veines du bois, la nuance exacte de la couleur, la subtilité du grain varient d'une planche à l'autre.",
            "Ce ne sont pas des défauts : ce sont les traces du bois et du geste. Ce qui fait que votre étagère est la vôtre.",
        ),
        "background": "beige", "padding_top": 112, "padding_bottom": 112,
    })),
    ("stats", section("stats", {"background": "blanc", "padding_top": 96, "padding_bottom": 96}, [
        ("k1", "stat", {"value": "100 %", "label": "bois massif"}),
        ("k2", "stat", {"value": "0", "label": "vis apparente"}),
        ("k3", "stat", {"value": "10 min", "label": "d'installation"}),
        ("k4", "stat", {"value": "14 jours", "label": "pour changer d'avis"}),
    ])),
    ("cta", section("featured-collection", {
        "eyebrow": "La collection", "heading": "Les pièces de l'atelier",
        "products_to_show": 4, "columns": "4", "center": True,
        "button_label": "Voir toute la collection",
        "background": "beige", "padding_top": 112, "padding_bottom": 112,
    })),
])

# ---------------------------------------------------------------------------
# Page FAQ
# ---------------------------------------------------------------------------
faq_items = [
    ("g-livraison", "group", {"title": "Livraison"}),
    ("q-livraison-prix", "question", {"question": "Combien coûte la livraison ?", "answer": p("La livraison est offerte en France métropolitaine, sans minimum d'achat.")}),
    ("q-livraison-delai", "question", {"question": "Quel est le délai de livraison ?", "answer": p("Chaque pièce est fabriquée à la main. Comptez [X] jours ouvrés entre votre commande et la livraison, fabrication et expédition comprises. Vous recevez un e-mail de suivi dès l'envoi du colis.")}),
    ("q-livraison-zone", "question", {"question": "Livrez-vous en dehors de la France métropolitaine ?", "answer": p("La livraison offerte concerne la France métropolitaine. Pour la Corse, l'outre-mer ou l'étranger, écrivez-nous avant de commander : nous vous indiquerons les possibilités.")}),
    ("q-livraison-emballage", "question", {"question": "Comment les pièces sont-elles emballées ?", "answer": p("Dans un emballage renforcé, spécialement conçu pour protéger le bois massif et le verre du miroir pendant le transport.")}),

    ("g-retours", "group", {"title": "Retours"}),
    ("q-retours-delai", "question", {"question": "Puis-je retourner un produit ?", "answer": p("Oui. Les retours sont acceptés sous 14 jours après réception, à condition que le produit soit renvoyé dans son emballage d'origine.")}),
    ("q-retours-comment", "question", {"question": "Comment faire un retour ?", "answer": p("Écrivez-nous depuis la page <a href=\"/pages/contact\">Contact</a> en indiquant votre numéro de commande. Nous vous expliquons la marche à suivre.")}),
    ("q-retours-abime", "question", {"question": "Mon colis est arrivé abîmé, que faire ?", "answer": p("Prenez quelques photos du colis et de la pièce, puis écrivez-nous rapidement avec votre numéro de commande. Nous trouverons une solution avec vous.")}),

    ("g-installation", "group", {"title": "Installation"}),
    ("q-install-materiel", "question", {"question": "De quoi ai-je besoin pour installer une étagère ou un miroir ?", "answer": p("D'une perceuse et d'un niveau à bulle. Tout le reste est fourni : vis, chevilles et gabarit de perçage pour l'étagère, rail dissimulé pour le miroir.")}),
    ("q-install-temps", "question", {"question": "Combien de temps faut-il ?", "answer": p("Environ 10 minutes par pièce : positionner le gabarit, percer deux trous, visser les supports, accrocher.")}),
    ("q-install-mur", "question", {"question": "Est-ce compatible avec un mur en placo ?", "answer": p("Oui. Le système de fixation fonctionne sur mur placo et sur béton.")}),
    ("q-install-charge", "question", {"question": "Quel poids l'étagère peut-elle supporter ?", "answer": p("[à confirmer] kg, répartis sur la longueur de l'étagère.")}),

    ("g-bois", "group", {"title": "Le bois et son entretien"}),
    ("q-bois-massif", "question", {"question": "S'agit-il vraiment de bois massif ?", "answer": p("Oui. Chaque pièce est taillée dans un bloc unique : pas de placage, pas de MDF, pas d'aggloméré. Du bois massif de bout en bout.")}),
    ("q-bois-choix", "question", {"question": "Frêne ou acajou : lequel choisir ?", "answer": p("Le frêne massif européen est clair, entre le blond et le miel, avec un grain fin — il s'accorde aussi bien à un intérieur scandinave qu'à un appartement haussmannien. L'acajou est sombre, brun-rouge, au grain profond : il apporte une présence plus chaleureuse et sophistiquée.")}),
    ("q-bois-unique", "question", {"question": "Ma pièce ressemblera-t-elle exactement à la photo ?", "answer": p("Pas tout à fait, et c'est voulu. Le bois est naturel et chaque pièce est faite à la main : les veines, la nuance et le grain varient légèrement d'une pièce à l'autre.")}),
    ("q-bois-entretien", "question", {"question": "Comment entretenir le bois ?", "answer": p("Un chiffon doux et sec pour dépoussiérer, pas d'eau stagnante sur le bois. Si vous le souhaitez, une huile naturelle (lin ou tung) une à deux fois par an pour nourrir le bois. Le miroir se nettoie avec un spray vitres classique.")}),

    ("g-commande", "group", {"title": "Commande et paiement"}),
    ("q-paiement", "question", {"question": "Quels moyens de paiement acceptez-vous ?", "answer": p("Les moyens de paiement disponibles s'affichent au moment de régler votre commande. Le paiement est entièrement sécurisé.")}),
    ("q-modifier", "question", {"question": "Puis-je modifier ma commande ?", "answer": p("Écrivez-nous le plus vite possible depuis la page <a href=\"/pages/contact\">Contact</a>. Tant que la pièce n'est pas expédiée, nous faisons notre possible pour l'adapter.")}),
]

faq = template([
    ("faq", section("faq", {
        "eyebrow": "Questions fréquentes", "heading": "Vos questions, nos réponses", "heading_tag": "h1",
        "text": p("Livraison, installation, entretien du bois : l'essentiel est ici. Pour le reste, écrivez-nous."),
        "background": "beige", "padding_top": 80, "padding_bottom": 96,
    }, faq_items)),
    ("cta", section("rich-text", {
        "heading": "Une autre question ?", "heading_tag": "h2",
        "text": p("Nous lisons chaque message et y répondons personnellement."),
        "button_label": "Nous écrire", "button_link": "/pages/contact", "button_secondary": False,
        "alignment": "center", "background": "blanc", "padding_top": 96, "padding_bottom": 96,
    })),
])

# ---------------------------------------------------------------------------
# Page Contact
# ---------------------------------------------------------------------------
contact = template([
    ("main", section("main-page", {
        "show_breadcrumbs": False, "show_title": True,
        "background": "beige", "padding_top": 80, "padding_bottom": 0,
    })),
    ("form", section("contact-form", {
        "eyebrow": "", "heading": "Écrivez-nous",
        "text": p("Une question sur une pièce, une commande ou un projet d'aménagement ? Nous vous répondons personnellement."),
        "background": "beige", "padding_top": 48, "padding_bottom": 112,
    }, [
        ("email", "info", {"icon": "mail", "title": "E-mail", "text": p("[adresse e-mail]")}),
        ("delay", "info", {"icon": "clock", "title": "Délai de réponse", "text": p("[délai de réponse]")}),
        ("pro", "info", {"icon": "pin", "title": "Professionnels", "text": p("Architectes, décorateurs, hôtels : parlez-nous de votre projet.")}),
    ])),
    ("faq", section("rich-text", {
        "heading": "Avant d'écrire", "heading_tag": "h2",
        "text": p("Livraison, retours, installation, entretien : la plupart des réponses sont dans notre FAQ."),
        "button_label": "Lire la FAQ", "button_link": "/pages/faq", "button_secondary": True,
        "alignment": "center", "background": "blanc", "padding_top": 96, "padding_bottom": 96,
    })),
])

# ---------------------------------------------------------------------------
# Templates système
# ---------------------------------------------------------------------------
write("index.json", index)
write("page.atelier.json", atelier)
write("page.faq.json", faq)
write("page.contact.json", contact)
write("page.json", template([("main", section("main-page", {"show_breadcrumbs": False, "show_title": True}))]))
write("collection.json", template([("main", section("main-collection", {"per_page": 24, "columns": "3", "show_description": True, "show_sort": True}))]))
write("list-collections.json", template([("main", section("main-list-collections", {"heading": "Collections"}))]))
write("cart.json", template([("main", section("main-cart", {"show_note": False}))]))
write("search.json", template([("main", section("main-search"))]))
write("404.json", template([("main", section("main-404"))]))
write("blog.json", template([("main", section("main-blog"))]))
write("article.json", template([("main", section("main-article"))]))
write("password.json", template([("main", section("main-password"))], layout="password"))
for name in ["account", "activate_account", "addresses", "login", "order", "register", "reset_password"]:
    write(f"customers/{name}.json", template([("main", section("main-customer"))]))
