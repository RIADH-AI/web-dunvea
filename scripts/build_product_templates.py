#!/usr/bin/env python3
"""
Génère les templates produit JSON (templates/product*.json) à partir du
copywriting DUNVEA. Les textes vivent ici pour rester lisibles et relus ;
le JSON produit est ensuite modifiable dans l'éditeur de thème Shopify.

Usage : python3 scripts/build_product_templates.py
Attention : relancer le script écrase les modifications faites dans l'éditeur
sur ces templates (récupérez-les d'abord avec `shopify theme pull`).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"

HANDLE_DUO = "duo-etagere-miroir-frene-massif"
HANDLE_PACK = "pack-mural-complet-frene-massif"


def p(*paragraphs):
    return "".join(f"<p>{x}</p>" for x in paragraphs)


def blocks(items):
    """items : liste de (id, type, settings) -> (blocks, block_order)"""
    out, order = {}, []
    for bid, btype, settings in items:
        out[bid] = {"type": btype, "settings": clean(settings)}
        order.append(bid)
    return out, order


def clean(settings):
    """Retire les réglages vides (Shopify refuse un richtext vide)."""
    return {k: v for k, v in settings.items() if v != ""}


def section(stype, settings, items=None):
    sec = {"type": stype, "settings": clean(settings)}
    if items:
        sec["blocks"], sec["block_order"] = blocks(items)
    return sec


# ---------------------------------------------------------------------------
# Blocs communs
# ---------------------------------------------------------------------------
REASSURANCE = {
    "icon_1": "truck", "title_1": "Livraison offerte", "text_1": "France métropolitaine",
    "icon_2": "return", "title_2": "Retours 14 jours", "text_2": "Dans l'emballage d'origine",
    "icon_3": "wood", "title_3": "Bois massif véritable", "text_3": "Ni placage, ni MDF",
    "icon_4": "hand", "title_4": "Fabriqué main", "text_4": "Dans notre atelier",
}

SWATCHES = "Frêne: #D9B98C\nFrêne massif: #D9B98C\nAcajou: #6E3B2B"
LEAD_TIME = "Fabriqué et expédié sous [X] jours ouvrés"


def main_product(eyebrow, bullets, dimensions, badge_3=""):
    return section("main-product", {
        "show_breadcrumbs": True, "sticky_bar": True, "padding_top": 16, "padding_bottom": 64,
    }, [
        ("title", "title", {"eyebrow": eyebrow}),
        ("rating", "rating", {"show_empty": True}),
        ("badges", "badges", {"badge_1": "Fait main", "badge_2": "Bois massif", "badge_3": badge_3}),
        ("bullets", "bullets", {f"bullet_{i + 1}": b for i, b in enumerate(bullets)}),
        ("dimensions", "dimensions", {"label": "Dimensions", "text": dimensions}),
        ("price", "price", {"show_savings": True, "tax_note": "TVA incluse · Livraison offerte en France métropolitaine"}),
        ("variant_picker", "variant_picker", {"swatch_colors": SWATCHES}),
        ("quantity", "quantity", {}),
        ("buy_buttons", "buy_buttons", {"show_dynamic_checkout": False, "lead_time": LEAD_TIME}),
        ("reassurance", "reassurance", REASSURANCE),
    ])


CHAPTER_MATERIALS = ("chapter-materiaux", "chapter", {
    "eyebrow": "Les matériaux",
    "heading": "Du bois massif, de bout en bout",
    "text": p(
        "Le frêne est l'un des bois les plus nobles d'Europe. Dense, résistant, naturellement veiné — il est utilisé en ébénisterie depuis des siècles pour les pièces qui doivent durer. Sa couleur naturelle, entre le blond et le miel, s'intègre aussi bien dans un intérieur scandinave que dans un appartement haussmannien.",
        "Chaque pièce est taillée dans un bloc unique. Pas de placage, pas de MDF caché sous une couche de vernis. Du bois massif de bout en bout. C'est ce que vous touchez quand vous passez la main sur le bois — le grain réel, pas une imitation imprimée.",
        "<strong>Vous préférez une teinte plus profonde ?</strong> L'acajou est un bois sombre, au grain profond et chaleureux. Sa couleur brun-rouge apporte immédiatement une présence chaleureuse et sophistiquée.",
    ),
    "show_placeholder": False, "ratio": "portrait",
})

CARE = section("product-info-list", {
    "anchor": "entretien", "eyebrow": "Entretien", "heading": "Le bois massif ne demande presque rien",
    "intro": p("Quelques gestes simples suffisent à le garder beau pendant des années."),
    "note": p("Le frêne vieillit en beauté. Son grain se patine naturellement — c'est un signe de qualité, pas un défaut."),
    "background": "beige", "padding_top": 96, "padding_bottom": 96,
}, [
    ("care-1", "item", {"icon": "leaf", "title": "Dépoussiérer", "text": "Un chiffon doux et sec suffit."}),
    ("care-2", "item", {"icon": "close", "title": "Éviter l'eau stagnante", "text": "Essuyez rapidement une trace d'eau ou un verre posé sur le bois."}),
    ("care-3", "item", {"icon": "wood", "title": "Nourrir le bois (optionnel)", "text": "Une huile naturelle — lin ou tung — une à deux fois par an, si vous voulez raviver le grain."}),
    ("care-4", "item", {"icon": "check", "title": "Le miroir", "text": "Il se nettoie avec un spray vitres classique, appliqué sur le chiffon plutôt que sur le verre."}),
])

SHIPPING = section("product-info-list", {
    "anchor": "livraison", "eyebrow": "Livraison et retours", "heading": "Expédié avec soin, chez vous",
    "intro": "", "note": "", "background": "blanc", "padding_top": 96, "padding_bottom": 96,
}, [
    ("ship-1", "item", {"icon": "truck", "title": "Livraison offerte", "text": "En France métropolitaine, sans minimum d'achat."}),
    ("ship-2", "item", {"icon": "clock", "title": "Délai", "text": "Fabrication artisanale + expédition : [X] jours ouvrés."}),
    ("ship-3", "item", {"icon": "box", "title": "Emballage renforcé", "text": "Spécialement conçu pour protéger le bois massif pendant le transport."}),
    ("ship-4", "item", {"icon": "return", "title": "Retours sous 14 jours", "text": "Le produit doit être renvoyé dans son emballage d'origine."}),
])

REVIEWS = section("product-reviews", {
    "eyebrow": "Avis clients", "heading": "Ils ont choisi DUNVEA",
    "empty_title": "Soyez le premier à donner votre avis",
    "empty_text": p("Vous avez installé une pièce DUNVEA chez vous ? Racontez-nous comment elle a trouvé sa place."),
    "hide_when_empty": False, "background": "beige", "padding_top": 96, "padding_bottom": 96,
})

RECOMMENDATIONS = section("product-recommendations", {
    "heading": "Vous aimerez aussi", "products_to_show": 3, "intent": "related",
    "background": "blanc", "padding_top": 96, "padding_bottom": 96,
})


def installation(heading, steps, note):
    return section("product-steps", {
        "anchor": "installation", "eyebrow": "Installation", "heading": heading,
        "intro": p("Tout est fourni. Vous avez besoin d'une perceuse et d'un niveau à bulle. C'est tout."),
        "note": note, "background": "blanc", "padding_top": 96, "padding_bottom": 96,
    }, [(f"step-{i + 1}", "step", {"title": t, "text": d}) for i, (t, d) in enumerate(steps)])


def specs(groups):
    items = []
    for gi, (title, rows) in enumerate(groups):
        items.append((f"group-{gi + 1}", "group", {"title": title}))
        for ri, (label, value) in enumerate(rows):
            items.append((f"row-{gi + 1}-{ri + 1}", "row", {"label": label, "value": value}))
    return section("product-specs", {
        "anchor": "caracteristiques", "eyebrow": "Fiche technique",
        "heading": "Dimensions et caractéristiques", "intro": "",
        "background": "blanc", "padding_top": 96, "padding_bottom": 96,
    }, items)


def story(chapters):
    return section("product-story", {
        "anchor": "description", "eyebrow": "", "heading": "",
        "background": "beige", "padding_top": 96, "padding_bottom": 96,
    }, chapters)


def upsell(handle, eyebrow, heading, text, includes, button):
    return section("complete-your-wall", {
        "product": handle, "eyebrow": eyebrow, "heading": heading, "text": text,
        "button_label": button, "background": "beige", "padding_top": 96, "padding_bottom": 96,
    }, [(f"inc-{i + 1}", "include", {"text": t}) for i, t in enumerate(includes)])


SPEC_SHELF = [
    ("Dimensions", "50 × 14 × 5 cm (L × P × H)"),
    ("Matériau", "Frêne massif européen ou acajou"),
    ("Finition", "Naturelle, huile protectrice"),
    ("Arête avant", "Biseautée à la main"),
    ("Fixation", "Système invisible inclus (vis + chevilles + gabarit de perçage)"),
    ("Charge supportée", "[à confirmer]"),
    ("Poids", "[à confirmer]"),
]
SPEC_MIRROR = [
    ("Dimensions", "53 × 32 cm"),
    ("Cadre", "Frêne massif européen ou acajou"),
    ("Miroir", "Verre de qualité optique"),
    ("Forme", "Organique, chaque pièce est unique"),
    ("Fixation", "Rail dissimulé derrière le cadre"),
    ("Poids", "[à confirmer]"),
]

STEPS_DUO = [
    ("Positionnez le gabarit", "Placez le gabarit de perçage au mur (inclus dans la boîte) et vérifiez l'horizontalité au niveau à bulle."),
    ("Percez et chevillez", "Percez les 2 trous, insérez les chevilles."),
    ("Vissez les supports", "Vissez les supports invisibles."),
    ("Accrochez", "Accrochez l'étagère et le miroir."),
]
NOTE_INSTALL = p("<strong>Temps total : 10 minutes.</strong> Le système fonctionne sur mur placo et béton.")


def write(name, data):
    path = TEMPLATES / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("écrit", path.relative_to(ROOT))


def template(sections):
    return {"sections": dict(sections), "order": [k for k, _ in sections]}


# ---------------------------------------------------------------------------
# DUO — produit héros
# ---------------------------------------------------------------------------
duo = template([
    ("main", main_product(
        "Notre duo signature",
        [
            "Frêne massif européen — chaque pièce est unique",
            "Fixation invisible incluse — zéro vis apparente",
            "Fabriqué main dans notre atelier — pas de production de masse",
            "Livraison offerte en France métropolitaine",
        ],
        "Étagère : 50 × 14 × 5 cm\nMiroir : 53 × 32 cm",
        "Économisez 39 €",
    )),
    ("story", story([
        ("chapter-histoire", "chapter", {
            "eyebrow": "L'histoire", "heading": "Un mur qui a du caractère",
            "text": p(
                "Un mur vide raconte peu de choses. Le Duo DUNVEA — une étagère flottante et un miroir organique — transforme n'importe quel mur en un espace qui a du caractère. L'étagère semble flotter, le miroir adoucit les lignes. Ensemble, ils créent un point focal naturel dans votre salon, votre entrée ou votre bureau.",
                "Ce n'est pas du mobilier décoratif jetable. C'est du frêne massif européen, travaillé à la main, conçu pour durer et vieillir avec grâce. Dans dix ans, le grain du bois aura pris une patine que l'aggloméré ne connaîtra jamais.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
        CHAPTER_MATERIALS,
        ("chapter-fabrication", "chapter", {
            "eyebrow": "La fabrication", "heading": "Le même atelier, les mêmes mains",
            "text": p(
                "Chaque étagère et chaque miroir sort du même atelier, des mêmes mains. La découpe, le ponçage, la mise en forme du biseau, la finition — tout est fait manuellement. Ce n'est pas un argument marketing : c'est une contrainte que nous avons choisie, parce qu'une machine ne sent pas le bois comme un artisan le sent.",
                "Le résultat : deux pièces ne sont jamais parfaitement identiques. Les veines du bois, la nuance exacte de la couleur, la subtilité du grain — ce sont les signatures de votre pièce.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
    ])),
    ("specs", specs([("Étagère", SPEC_SHELF), ("Miroir", SPEC_MIRROR)])),
    ("installation", installation("Dix minutes, une perceuse, un niveau.", STEPS_DUO, NOTE_INSTALL)),
    ("care", CARE),
    ("shipping", SHIPPING),
    ("reviews", REVIEWS),
    ("upsell", upsell(
        HANDLE_PACK, "Complétez votre mur", "Passez au mur complet",
        p("Ajoutez une seconde étagère pour habiller un mur entier. Le pack réunit les trois pièces, taillées dans le même bois et finies de la même main."),
        ["2 étagères flottantes + 1 miroir organique", "58 € d'économie par rapport aux pièces séparées", "Fixation invisible incluse pour les trois pièces"],
        "Découvrir le pack",
    )),
    ("recommendations", RECOMMENDATIONS),
])

# ---------------------------------------------------------------------------
# ÉTAGÈRE seule
# ---------------------------------------------------------------------------
etagere = template([
    ("main", main_product(
        "",
        [
            "Frêne massif européen ou acajou — chaque pièce est unique",
            "Fixation invisible incluse — l'étagère semble flotter",
            "Fabriquée main dans notre atelier — pas de production de masse",
            "Livraison offerte en France métropolitaine",
        ],
        "50 × 14 × 5 cm (L × P × H)",
    )),
    ("story", story([
        ("chapter-histoire", "chapter", {
            "eyebrow": "L'histoire", "heading": "Une planche de bois, rien d'autre",
            "text": p(
                "Une étagère flottante n'a qu'une chose à montrer : son bois. Pas d'équerre, pas de vis apparente — la planche sort du mur, nette, comme si elle y avait toujours été. Au-dessus d'un bureau, dans une entrée, à côté d'un lit, elle accueille ce que vous y posez sans prendre toute la place.",
                "Son arête avant est biseautée à la main : la ligne s'allège, le bois accroche la lumière. Et parce qu'il s'agit de bois massif, pas d'aggloméré plaqué, elle prendra avec les années une patine que les matériaux reconstitués ne connaissent pas.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
        CHAPTER_MATERIALS,
        ("chapter-fabrication", "chapter", {
            "eyebrow": "La fabrication", "heading": "Découpée, poncée, huilée à la main",
            "text": p(
                "La découpe, le ponçage, la mise en forme du biseau, la finition à l'huile — chaque étape est faite manuellement dans notre atelier. C'est plus lent, et c'est voulu : une machine ne sent pas le bois comme un artisan le sent.",
                "Deux étagères ne sont donc jamais parfaitement identiques. Les veines, la nuance exacte de la couleur, la subtilité du grain — ce sont les signatures de votre pièce.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
    ])),
    ("specs", specs([("Étagère", SPEC_SHELF)])),
    ("installation", installation("Dix minutes, une perceuse, un niveau.", [
        ("Positionnez le gabarit", "Placez le gabarit de perçage au mur (inclus dans la boîte) et vérifiez l'horizontalité au niveau à bulle."),
        ("Percez et chevillez", "Percez les 2 trous, insérez les chevilles."),
        ("Vissez les supports", "Vissez les supports invisibles."),
        ("Posez l'étagère", "Glissez l'étagère sur ses supports. Elle est prête à recevoir vos objets."),
    ], NOTE_INSTALL)),
    ("care", CARE),
    ("shipping", SHIPPING),
    ("reviews", REVIEWS),
    ("upsell", upsell(
        HANDLE_DUO, "Complétez votre mur", "Ajoutez le miroir, économisez 39 €",
        p("L'étagère semble flotter, le miroir adoucit les lignes. Ensemble, ils créent un point focal naturel dans une entrée, un salon ou un bureau."),
        ["1 étagère flottante + 1 miroir organique", "Le même bois, la même finition", "Fixation invisible incluse pour les deux pièces"],
        "Découvrir le duo",
    )),
    ("recommendations", RECOMMENDATIONS),
])

# ---------------------------------------------------------------------------
# MIROIR seul
# ---------------------------------------------------------------------------
miroir = template([
    ("main", main_product(
        "",
        [
            "Cadre en frêne massif européen ou acajou — chaque forme est unique",
            "Verre de qualité optique",
            "Fixation invisible incluse — rail dissimulé derrière le cadre",
            "Fabriqué main · Livraison offerte en France métropolitaine",
        ],
        "53 × 32 cm",
    )),
    ("story", story([
        ("chapter-histoire", "chapter", {
            "eyebrow": "L'histoire", "heading": "Une forme libre, taillée à la main",
            "text": p(
                "Un miroir rectangulaire reflète une pièce. Un miroir organique l'adoucit. Le cadre DUNVEA suit une ligne libre, sans angle droit, mise en forme à la main dans le bois massif — une forme que vous ne retrouverez pas deux fois à l'identique.",
                "Dans une entrée, il accueille. Au-dessus d'une console ou d'une étagère, il ouvre le mur sans l'alourdir. Le verre de qualité optique renvoie une image nette ; le bois qui l'entoure lui donne de la chaleur.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
        CHAPTER_MATERIALS,
        ("chapter-fabrication", "chapter", {
            "eyebrow": "La fabrication", "heading": "Chaque courbe est poncée à la main",
            "text": p(
                "Le cadre est découpé, mis en forme, poncé puis huilé dans notre atelier. Les courbes sont reprises à la main jusqu'à ce que le bois soit doux sous les doigts — une machine ne sent pas le bois comme un artisan le sent.",
                "Le résultat : deux miroirs ne sont jamais parfaitement identiques. Les veines, la nuance de la couleur, le dessin exact de la courbe — ce sont les signatures de votre pièce.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
    ])),
    ("specs", specs([("Miroir", SPEC_MIRROR)])),
    ("installation", installation("Dix minutes, une perceuse, un niveau.", [
        ("Repérez l'emplacement", "Marquez la position des fixations au mur et vérifiez l'horizontalité au niveau à bulle."),
        ("Percez et chevillez", "Percez les 2 trous, insérez les chevilles."),
        ("Vissez les fixations", "Vissez les fixations fournies dans la boîte."),
        ("Accrochez le miroir", "Accrochez le miroir par son rail dissimulé derrière le cadre."),
    ], NOTE_INSTALL)),
    ("care", CARE),
    ("shipping", SHIPPING),
    ("reviews", REVIEWS),
    ("upsell", upsell(
        HANDLE_DUO, "Complétez votre mur", "Ajoutez l'étagère, économisez 39 €",
        p("Une étagère flottante sous le miroir, et l'entrée est faite : un endroit pour les clés, un vase, un livre. Le duo réunit les deux pièces dans le même bois."),
        ["1 miroir organique + 1 étagère flottante", "Le même bois, la même finition", "Fixation invisible incluse pour les deux pièces"],
        "Découvrir le duo",
    )),
    ("recommendations", RECOMMENDATIONS),
])

# ---------------------------------------------------------------------------
# PACK 2 étagères + miroir
# ---------------------------------------------------------------------------
pack = template([
    ("main", main_product(
        "Le mur complet",
        [
            "2 étagères + 1 miroir — de quoi habiller un mur entier",
            "Frêne massif européen ou acajou — chaque pièce est unique",
            "Fixation invisible incluse pour les trois pièces",
            "Livraison offerte en France métropolitaine",
        ],
        "Étagères : 2 × (50 × 14 × 5 cm)\nMiroir : 53 × 32 cm",
        "Économisez 58 €",
    )),
    ("story", story([
        ("chapter-histoire", "chapter", {
            "eyebrow": "L'histoire", "heading": "Un mur entier, pensé d'un seul geste",
            "text": p(
                "Deux étagères et un miroir, taillés dans le même bois et finis de la même main : les veines se répondent, les teintes s'accordent. Le mur ne ressemble plus à une addition d'objets, mais à une composition.",
                "Composez-le à votre façon. Le miroir au centre et une étagère de chaque côté, pour une entrée symétrique. Ou les deux étagères décalées à côté du miroir, pour un salon plus vivant. Dans tous les cas, aucune vis n'est visible.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
        CHAPTER_MATERIALS,
        ("chapter-fabrication", "chapter", {
            "eyebrow": "La fabrication", "heading": "Trois pièces, le même atelier",
            "text": p(
                "Chaque étagère et le miroir sortent du même atelier, des mêmes mains. La découpe, le ponçage, la mise en forme du biseau, la finition — tout est fait manuellement. Ce n'est pas un argument marketing : c'est une contrainte que nous avons choisie, parce qu'une machine ne sent pas le bois comme un artisan le sent.",
                "Le résultat : deux pièces ne sont jamais parfaitement identiques. Les veines du bois, la nuance exacte de la couleur, la subtilité du grain — ce sont les signatures de votre mur.",
            ),
            "show_placeholder": False, "ratio": "portrait",
        }),
    ])),
    ("specs", specs([("Étagères (× 2)", SPEC_SHELF), ("Miroir", SPEC_MIRROR)])),
    ("installation", installation("Trente minutes pour tout le mur.", [
        ("Prévoyez la composition", "Disposez les pièces au sol ou marquez-les au mur au crayon pour valider l'équilibre."),
        ("Positionnez les gabarits", "Placez le gabarit de perçage (inclus) pour chaque étagère et vérifiez au niveau à bulle."),
        ("Percez, chevillez, vissez", "Percez les trous, insérez les chevilles, vissez les supports invisibles."),
        ("Accrochez", "Posez les étagères sur leurs supports et accrochez le miroir par son rail dissimulé."),
    ], p("<strong>Comptez 10 minutes par pièce.</strong> Le système fonctionne sur mur placo et béton."))),
    ("care", CARE),
    ("shipping", SHIPPING),
    ("reviews", REVIEWS),
    ("recommendations", RECOMMENDATIONS),
])

# ---------------------------------------------------------------------------
# Template par défaut (tout nouveau produit) — description Shopify
# ---------------------------------------------------------------------------
default = template([
    ("main", main_product(
        "",
        [
            "Bois massif — chaque pièce est unique",
            "Fixation invisible incluse",
            "Fabriqué main dans notre atelier",
            "Livraison offerte en France métropolitaine",
        ],
        "",
    )),
    ("story", section("product-story", {
        "anchor": "description", "eyebrow": "Description", "heading": "",
        "background": "beige", "padding_top": 96, "padding_bottom": 96,
    })),
    ("care", CARE),
    ("shipping", SHIPPING),
    ("reviews", REVIEWS),
    ("recommendations", RECOMMENDATIONS),
])

write("product.json", default)
write("product.duo.json", duo)
write("product.etagere.json", etagere)
write("product.miroir.json", miroir)
write("product.pack.json", pack)
