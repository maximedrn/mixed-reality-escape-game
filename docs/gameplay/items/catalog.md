# Catalogue des items

Ce catalogue recense les types d'items et leurs modèles, selon la [classification assets/items](README.md). Une ressource disponible n'a pas nécessairement de rôle, de capacité ou d'intégration Unity validés. Les variantes sont les modèles distincts identifiés dans la scène locale `blender/presentation/room-presentation-dense.blend` ; `—` signifie qu'aucun modèle n'est choisi. Les [états de disponibilité](../../environment/assets.md#états) sont communs aux deux catalogues.

> [!IMPORTANT]
> Pour l'instant, les listes d'assets et d'items se basent sur la scène de présentation réalisée sous Blender. Elles ne sont pas définitives : des ressources peuvent être ajoutées, supprimées ou modifiées. Par exemple, les sources de lumière seront probablement supprimées en dehors du mode Peaceful. La disposition et les ajustements du mobilier pourront également évoluer.

Voir les [capacités](specifications.md) et les [interactions physiques](environment_interactions.md).

## Éclairage

| Item            | Modèle                          | Variantes | Source                | État       |
| --------------- | ------------------------------- | --------: | --------------------- | ---------- |
| Torche portable | Modèle portable à choisir       |         — | À définir             | À définir  |
| Bougies         | `Candle_1` avec flamme visuelle |         1 | Fantasy Props MegaKit | Disponible |

Les torches murales sont des [assets fixes](../../environment/assets.md).

## Distraction

| Item      | Modèle           | Variantes | Source                | État       |
| --------- | ---------------- | --------: | --------------------- | ---------- |
| Cailloux  | Modèle à choisir |         — | À définir             | À définir  |
| Bouteille | `Bottle_1`       |         1 | Fantasy Props MegaKit | Disponible |

## Alchimie et contenants

| Item                                           | Modèle                                                                                   | Variantes | Source                | État       |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------- | --------: | --------------------- | ---------- |
| Fiole vide                                     | Aucun modèle explicitement distingué comme vide                                          |         — | À définir             | À définir  |
| Petite fiole                                   | `SM_Magic_SmallBottle`                                                                   |         1 | Magic Props           | Disponible |
| Ensemble de petites bouteilles                 | `SmallBottles_1` (modèle composé)                                                        |         1 | Fantasy Props MegaKit | Disponible |
| Bouchon de fiole                               | Aucun bouchon autonome identifié                                                         |         — | À définir             | À définir  |
| Fioles contenant un liquide / potions colorées | `SM_Magic_PotionBottle_Blue`, `SM_Magic_PotionBottle_Green`, `SM_Magic_PotionBottle_Red` |         3 | Magic Props           | Disponible |
| Potion, modèle 4                               | `Potion_4`                                                                               |         1 | Fantasy Props MegaKit | Disponible |
| Chaudron                                       | `SM_Magic_Cauldron`                                                                      |         1 | Magic Props           | Disponible |
| Appareil de distillation                       | Modèle non identifié dans la scène                                                       |         — | À définir             | À définir  |
| Balance                                        | Modèle non identifié dans la scène                                                       |         — | À définir             | À définir  |
| Mortier et pilon                               | `SM_Magic_MortarPestle` (ensemble)                                                       |         1 | Magic Props           | Disponible |
| Bocal d'ingrédients                            | `SM_Magic_IngredientJar`                                                                 |         1 | Magic Props           | Disponible |
| Calice                                         | `Chalice`                                                                                |         1 | Fantasy Props MegaKit | Disponible |
| Chope                                          | `Mug`                                                                                    |         1 | Fantasy Props MegaKit | Disponible |
| Autres ustensiles d'alchimie                   | Modèles à préciser                                                                       |         — | À définir             | À définir  |

Le contenu des fioles, potions et bocaux n'est pas fixé ; leur apparence ne détermine aucun effet.

Une énigme de mélange de liquides, d'ingrédients et de recettes est **une proposition**, sans système de fluides ni fabrication de potions défini pour le MVP.

## Ingrédients

| Item                  | Modèle                       | Variantes | Source      | État       |
| --------------------- | ---------------------------- | --------: | ----------- | ---------- |
| Cristal               | `SM_Magic_Crystal`           |         1 | Magic Props | Disponible |
| Groupe de champignons | `SM_Magic_MushroomCluster`   |         1 | Magic Props | Disponible |
| Bourse d'ingrédients  | `SM_Magic_IngredientPouch`   |         1 | Magic Props | Disponible |
| Autres ingrédients    | Nature et modèles à préciser |         — | À définir   | À définir  |

## Documents et indices

| Item                        | Modèle                                                                                                                          | Variantes | Source                              | État       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------: | ----------------------------------- | ---------- |
| Groupes de livres           | `BookGroup_Medium_1`, `BookGroup_Medium_2`, `BookGroup_Medium_3`, `BookGroup_Small_1`, `BookGroup_Small_2`, `BookGroup_Small_3` |         6 | Fantasy Props MegaKit               | Disponible |
| Livres isolés               | `Book_5`, `Book_7`                                                                                                              |         2 | Fantasy Props MegaKit               | Disponible |
| Piles de livres             | `Book_Stack_1`, `Book_Stack_2`                                                                                                  |         2 | Fantasy Props MegaKit               | Disponible |
| Grimoires                   | `SM_Magic_Spellbook` + pages procédurales                                                                                       |         1 | Magic Props + Blender               | Disponible |
| Parchemins                  | `SM_Magic_Scroll` (Magic Props), `Scroll_2` (Fantasy Props MegaKit)                                                             |         2 | Magic Props ; Fantasy Props MegaKit | Disponible |
| Manuscrit ouvert sur lutrin | `Dense_Open_Grimoire_Pages_Mesh`, distinct du lutrin fixe                                                                       |         1 | Géométrie procédurale Blender       | Disponible |
| Parchemins déroulés         | `Dense_Unrolled_Parchment_Mesh`                                                                                                 |         1 | Géométrie procédurale Blender       | Disponible |

La lecture, l'ouverture et le transport de ces documents restent à définir.

## Accessoires et décoration potentiellement utiles

| Item                       | Modèle                                                     | Variantes | Source                                                | État       |
| -------------------------- | ---------------------------------------------------------- | --------: | ----------------------------------------------------- | ---------- |
| Râtelier mural à chevilles | `Peg_Rack`                                                 |         1 | Fantasy Props MegaKit                                 | Disponible |
| Grandes bourses            | `Pouch_Large` + cordons procéduraux lorsqu'il est suspendu |         1 | Fantasy Props MegaKit + géométrie procédurale Blender | Disponible |

## Items propres aux énigmes proposées

| Item   | Modèle                           | Variantes | Source  | État       |
| ------ | -------------------------------- | --------: | ------- | ---------- |
| Chaine | Corde texturer en chaine simuler |         — | À créer | À produire |

Une ressource peut figurer dans ce catalogue sans que l'énigme associée soit retenue.

## Fiches des premiers rôles envisagés

| Item               | Rôle connu ou proposé                                                                                    | À définir                                                                        |
| ------------------ | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Torche             | Éclairage principal ; lumière sans [stimulus visuel autonome](../../monster/ai/perception.md) pour l'IA. | Modèle portable, masse éventuelle, disponibilité, règles d'impact.               |
| Caillou            | Distraction sonore par impact ; réutilisation proposée si récupérable.                                   | Modèle, masse, lancer, seuils, effet direct éventuel.                            |
| Bouteille ou fiole | Bruit potentiel ; casse d'une fiole envisagée.                                                           | Correspondance modèle/rôle, masse, seuil de casse, réutilisation, impact direct. |

La non-réutilisation d'une fiole après sa casse et la protection des indices indispensables contre une perte rendant la partie insoluble restent des **propositions**, à décider avec les énigmes retenues.

Les valeurs de masse, bruit, seuil et durée seront fixées pendant les tests ; voir les [spécifications](specifications.md) et les [réactions du monstre](../../monster/ai/item_reactions.md).
