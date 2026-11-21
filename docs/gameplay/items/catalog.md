# Catalogue des items

Ce catalogue réunit les types d'objets de gameplay et les modèles susceptibles d'y servir. **Un modèle présent dans Blender n'implique aucune capacité de manipulation ou fonction de gameplay validée.** Les variantes correspondent aux modèles distincts identifiés dans la scène locale `blender/presentation/room-presentation-dense.blend`, inspectée en lecture seule. `—` indique qu'aucun modèle n'est encore choisi.

> [!IMPORTANT]
> Pour l'instant, les listes d'assets et d'items se basent sur la scène de présentation réalisée sous Blender. Elles ne sont pas définitives et restent modifiables. Par exemple, les sources de lumière seront probablement supprimées en dehors du mode Peaceful. La disposition et les ajustements du mobilier pourront également évoluer.

La [définition des capacités](specifications.md) et les [interactions physiques](environment_interactions.md) sont communes aux items. Les rôles restant à choisir sont signalés sans attribuer automatiquement `Throwable`, `Breakable`, `isGrabbable` ou un effet sur le monstre.

## Éclairage

| Item            | Description / rôle                                                                                                                                              | Variantes | Source                | État                            |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------: | --------------------- | ------------------------------- |
| Torche portable | Éclairage principal du joueur ; modèle portable et modalités d'utilisation à choisir. Les torches murales sont des [assets fixes](../../environment/assets.md). |         — | À définir             | Rôle retenu ; modèle à définir  |
| Bougies         | Modèle `Candle_1` avec flamme visuelle. Usage de gameplay à définir.                                                                                            |         1 | Fantasy Props MegaKit | Modèle présent ; rôle à définir |

## Distraction

| Item      | Description / rôle                                                                                       | Variantes | Source                | État                             |
| --------- | -------------------------------------------------------------------------------------------------------- | --------: | --------------------- | -------------------------------- |
| Cailloux  | Distraction sonore par collision ; modèle et règles d'impact à définir.                                  |         — | À définir             | Rôle envisagé ; modèle à définir |
| Bouteille | Modèle `Bottle_1` ; les bouteilles sont envisagées comme distraction sonore. Casse et usage à confirmer. |         1 | Fantasy Props MegaKit | Modèle présent ; rôle à définir  |

## Alchimie et contenants

| Item                                           | Description / rôle                                                                                                                                    | Variantes | Source                | État                              |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------: | --------------------- | --------------------------------- |
| Fiole vide                                     | Contenant sans liquide identifié ; aucun modèle explicitement distingué comme vide.                                                                   |         — | À définir             | À définir                         |
| Petite fiole                                   | Modèle `SM_Magic_SmallBottle` ; contenu et fonction à définir.                                                                                        |         1 | Magic Props           | Modèle présent ; rôle à définir   |
| Ensemble de petites bouteilles                 | Modèle composé `SmallBottles_1`.                                                                                                                      |         1 | Fantasy Props MegaKit | Modèle présent ; rôle à définir   |
| Bouchon de fiole                               | Aucun bouchon autonome identifié.                                                                                                                     |         — | À définir             | À définir                         |
| Fioles contenant un liquide / potions colorées | Modèles `SM_Magic_PotionBottle_Blue`, `SM_Magic_PotionBottle_Green` et `SM_Magic_PotionBottle_Red` ; leur apparence n'établit pas un effet de potion. |         3 | Magic Props           | Modèles présents ; rôle à définir |
| Potion, modèle 4                               | Modèle `Potion_4` ; mécanique et contenu à définir.                                                                                                   |         1 | Fantasy Props MegaKit | Modèle présent ; rôle à définir   |
| Chaudron                                       | Modèle `SM_Magic_Cauldron` ; équipement classé comme item, manipulation à définir.                                                                    |         1 | Magic Props           | Modèle présent ; rôle à définir   |
| Appareil de distillation                       | Équipement envisagé, non identifié dans la scène de présentation.                                                                                     |         — | À définir             | À définir                         |
| Balance                                        | Équipement envisagé, non identifié dans la scène de présentation.                                                                                     |         — | À définir             | À définir                         |
| Mortier et pilon                               | Ensemble `SM_Magic_MortarPestle`.                                                                                                                     |         1 | Magic Props           | Modèle présent ; rôle à définir   |
| Bocal d'ingrédients                            | Modèle `SM_Magic_IngredientJar` ; contenu à définir.                                                                                                  |         1 | Magic Props           | Modèle présent ; rôle à définir   |
| Calice                                         | Modèle `Chalice`.                                                                                                                                     |         1 | Fantasy Props MegaKit | Modèle présent ; rôle à définir   |
| Chope                                          | Modèle `Mug`.                                                                                                                                         |         1 | Fantasy Props MegaKit | Modèle présent ; rôle à définir   |
| Autres ustensiles d'alchimie                   | Besoins supplémentaires à préciser avant de choisir un modèle.                                                                                        |         — | À définir             | À définir                         |

Une énigme de mélange de liquides, d'ingrédients et de recettes est **une proposition**, sans système de fluides ni fabrication de potions défini pour le MVP.

## Ingrédients

| Item                  | Description / rôle                                            | Variantes | Source      | État                            |
| --------------------- | ------------------------------------------------------------- | --------: | ----------- | ------------------------------- |
| Cristal               | Modèle `SM_Magic_Crystal` ; aucune propriété magique arrêtée. |         1 | Magic Props | Modèle présent ; rôle à définir |
| Groupe de champignons | Modèle `SM_Magic_MushroomCluster`.                            |         1 | Magic Props | Modèle présent ; rôle à définir |
| Bourse d'ingrédients  | Modèle `SM_Magic_IngredientPouch` ; contenu à définir.        |         1 | Magic Props | Modèle présent ; rôle à définir |
| Autres ingrédients    | Nature, modèles et rôle à préciser.                           |         — | À définir   | À définir                       |

## Documents et indices

| Item                        | Description / rôle                                                                             | Variantes | Source                        | État                                 |
| --------------------------- | ---------------------------------------------------------------------------------------------- | --------: | ----------------------------- | ------------------------------------ |
| Groupes de livres moyens    | `BookGroup_Medium_1`, `BookGroup_Medium_2`, `BookGroup_Medium_3`.                              |         3 | Fantasy Props MegaKit         | Modèles présents ; lecture à définir |
| Petits groupes de livres    | `BookGroup_Small_1`, `BookGroup_Small_2`, `BookGroup_Small_3`.                                 |         3 | Fantasy Props MegaKit         | Modèles présents ; lecture à définir |
| Livres isolés               | `Book_5` et `Book_7`.                                                                          |         2 | Fantasy Props MegaKit         | Modèles présents ; lecture à définir |
| Piles de livres             | `Book_Stack_1` et `Book_Stack_2`.                                                              |         2 | Fantasy Props MegaKit         | Modèles présents ; lecture à définir |
| Grimoires                   | Modèle `SM_Magic_Spellbook`, complété par des pages procédurales dans la présentation Blender. |         1 | Magic Props + Blender         | Modèles présents ; lecture à définir |
| Parchemins magiques         | Modèle `SM_Magic_Scroll`.                                                                      |         1 | Magic Props                   | Modèle présent ; contenu à définir   |
| Parchemins, modèle 2        | Modèle `Scroll_2`.                                                                             |         1 | Fantasy Props MegaKit         | Modèle présent ; contenu à définir   |
| Manuscrit ouvert sur lutrin | Modèle procédural `Dense_Open_Grimoire_Pages_Mesh`, distinct du lutrin fixe.                   |         1 | Géométrie procédurale Blender | Modélisé ; contenu à définir         |
| Parchemins déroulés         | Modèle procédural `Dense_Unrolled_Parchment_Mesh`.                                             |         1 | Géométrie procédurale Blender | Modélisé ; contenu à définir         |

## Accessoires et décoration potentiellement utiles

| Item                       | Description / rôle                                                                          | Variantes | Source                                                | État                              |
| -------------------------- | ------------------------------------------------------------------------------------------- | --------: | ----------------------------------------------------- | --------------------------------- |
| Râtelier mural à chevilles | Modèle `Peg_Rack`, élément mural ; éventuelle fonction de jeu à définir.                    |         1 | Fantasy Props MegaKit                                 | Modèle présent ; rôle à définir   |
| Grandes bourses            | Modèle `Pouch_Large`, complété par des cordons dans la présentation lorsqu'il est suspendu. |         1 | Fantasy Props MegaKit + géométrie procédurale Blender | Modèles présents ; rôle à définir |

## Items propres aux énigmes proposées

| Item   | Description / rôle                  | Variantes | Source  | État       |
| ------ | ----------------------------------- | --------: | ------- | ---------- |
| Chaine | Corde texturer en chaine simuler    |         — | À créer | À produire |

Une ressource peut figurer dans ce catalogue sans que l'énigme associée soit retenue.

## Fiches des premiers rôles envisagés

| Item               | Rôle connu ou proposé                                                                                  | Capacités et propriétés restant à définir                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Torche             | Éclairer le joueur au MVP ; sa lumière n'est pas un stimulus visuel propre pour l'IA du monstre.       | Modèle portable, masse éventuelle, disponibilité, règles d'impact et modalités de manipulation.        |
| Caillou            | Produire une distraction sonore lors d'un impact. Réutilisation proposée si l'objet reste récupérable. | Modèle, masse, capacité de lancer, seuils et effet direct éventuel sur le monstre.                     |
| Bouteille ou fiole | Produire potentiellement un bruit ; la casse d'une fiole est envisagée.                                | Correspondance entre modèles et rôles, masse, seuil de casse, réutilisation et règles d'impact direct. |

La non-réutilisation d'une fiole après sa casse et la protection des indices indispensables contre une perte rendant la partie insoluble restent des **propositions**, à décider avec les énigmes retenues.

Les valeurs de masse, bruit, seuil et durée seront fixées après implémentation et tests. Les modalités détaillées d'interaction joueur/items feront l'objet d'une documentation ultérieure. Voir les [réactions du monstre](../../monster/ai/item_reactions.md).
