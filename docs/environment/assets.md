# Catalogue des assets d'environnement

Ce catalogue recense l'architecture, le mobilier, le rangement et l'éclairage fixe. Voir la [classification assets/items](../gameplay/items/README.md) et le [catalogue des items](../gameplay/items/catalog.md).

> [!IMPORTANT]
> Pour l'instant, les listes d'assets et d'items se basent sur la scène de présentation réalisée sous Blender. Elles ne sont pas définitives : des ressources peuvent être ajoutées, supprimées ou modifiées. Par exemple, les sources de lumière seront probablement supprimées en dehors du mode Peaceful. La disposition et les ajustements du mobilier pourront également évoluer.

**Référence :** scène locale `blender/presentation/room-presentation-dense.blend`, inspectée en lecture seule. Une *variante* est un modèle distinct ; `—` signifie qu'aucun modèle n'est choisi.

## États

L'état décrit la disponibilité de la ressource, pas son intégration fonctionnelle dans Unity.

| État        | Signification                                       |
| ----------- | --------------------------------------------------- |
| Disponible  | Ressource existante et accessible.                  |
| À adapter   | Ressource disponible nécessitant des modifications. |
| À produire  | Ressource à créer.                                  |
| À récupérer | Ressource à rechercher ou importer.                 |
| À définir   | Caractéristiques ou modèle non définis.             |
| À vérifier  | Disponibilité ou information non confirmée.         |

## Architecture et décor structurel

| Asset                    | Modèle                                                   | Source  | État       |
| ------------------------ | -------------------------------------------------------- | ------- | ---------- |
| Murs en pierre           | `Wall_Stone_N/S/E/W`                                     | Blender | Disponible |
| Sol en pierre            | Dalles, usure et joints                                  | Blender | Disponible |
| Cercle alchimique du sol | `Alchemy_Engraved_Recesses`, gravure intégrée aux dalles | Blender | Disponible |
| Plafond voûté            | `Ceiling_Stone` et reprises locales                      | Blender | Disponible |
| Piliers                  | Pilier mural et pilier d'angle, surfaces usées           | Blender | Disponible |
| Entablements             | Bande périphérique et chapiteaux adaptés aux piliers     | Blender | Disponible |
| Nervures de voûte        | Nervures diagonales et de rive                           | Blender | Disponible |
| Portes                   | Modèles médiévaux adaptés aux ouvertures                 | Blender | Disponible |
| Encadrements de portes   | Modèles adaptés aux ouvertures                           | Blender | Disponible |

Le scan brut, les supports de génération et les objets masqués restent hors catalogue. Les volumes de collision et de navigation relèvent de l'[architecture](../architecture.md) et de la [navigation](../monster/ai/navigation.md).

## Mobilier

Ces modèles sont placés dans la présentation Blender ; leur présence ne prouve pas qu'ils représentent les tables physiques suivies par QR code.

| Asset                          | Modèle                                                                              | Variantes | Source                | État       |
| ------------------------------ | ----------------------------------------------------------------------------------- | --------: | --------------------- | ---------- |
| Grande table d'alchimie        | `Table_Large`                                                                       |         1 | Fantasy Props MegaKit | Disponible |
| Établi de recherche            | `Workbench`                                                                         |         1 | Fantasy Props MegaKit | Disponible |
| Tabourets                      | `Stool`                                                                             |         1 | Fantasy Props MegaKit | Disponible |
| Chaise                         | `Chair_1`                                                                           |         1 | Fantasy Props MegaKit | Disponible |
| Bibliothèques                  | `Bookcase_2`                                                                        |         1 | Fantasy Props MegaKit | Disponible |
| Étagères arquées               | `Shelf_Arch`                                                                        |         1 | Fantasy Props MegaKit | Disponible |
| Armoire basse                  | `Cabinet`                                                                           |         1 | Fantasy Props MegaKit | Disponible |
| Meuble à étagères              | `Nightstand_Shelf`                                                                  |         1 | Fantasy Props MegaKit | Disponible |
| Lutrin                         | `BookStand` ; manuscrit dans le [catalogue des items](../gameplay/items/catalog.md) |         1 | Fantasy Props MegaKit | Disponible |
| Étagère murale simple          | `Shelf_Simple`                                                                      |         1 | Fantasy Props MegaKit | Disponible |
| Petites tables                 | Modèle distinct non identifié dans la scène                                         |         — | À définir             | À définir  |
| Habillage des tables physiques | Modèles séparés du décor, associés aux tables mesurées et calibrées                 |         — | À définir             | À définir  |

## Rangement

| Asset             | Modèle                                                           | Variantes | Source                | État       |
| ----------------- | ---------------------------------------------------------------- | --------: | --------------------- | ---------- |
| Coffres           | `SM_Magic_Chest_Body` + `SM_Magic_Chest_Lid` (un coffre logique) |         1 | Magic Props           | Disponible |
| Tonneaux          | `Barrel`                                                         |         1 | Fantasy Props MegaKit | Disponible |
| Caisses en bois   | `Crate_Wooden`                                                   |         1 | Fantasy Props MegaKit | Disponible |
| Caisse métallique | `Crate_Metal`                                                    |         1 | Fantasy Props MegaKit | Disponible |
| Sac               | `Bag`                                                            |         1 | Fantasy Props MegaKit | Disponible |

Les bourses, y compris les modèles suspendus, figurent parmi les [items](../gameplay/items/catalog.md).

## Éclairage fixe

| Asset             | Modèle                             | Variantes | Source                | État       |
| ----------------- | ---------------------------------- | --------: | --------------------- | ---------- |
| Torches murales   | `Torch_Metal` avec flamme visuelle |         1 | Fantasy Props MegaKit | Disponible |
| Lanternes murales | `Lantern_Wall`                     |         1 | Fantasy Props MegaKit | Disponible |
| Lustre            | Modèle non relevé dans la scène    |         — | À définir             | À définir  |

Les lampes Unity sont techniques ; la torche portable et les bougies figurent parmi les [items](../gameplay/items/catalog.md).

## Matériaux, textures et ambiance

| Ressource                        | Modèle                                                       | Source                                      | État       |
| -------------------------------- | ------------------------------------------------------------ | ------------------------------------------- | ---------- |
| Matériaux architecturaux         | Pierre irrégulière, mortier, sol usé, bois et fer des portes | Blender                                     | Disponible |
| Matériaux du mobilier            | Bois et métal adaptés aux modèles du MegaKit                 | Fantasy Props MegaKit, adaptés dans Blender | Disponible |
| Éclairage global de présentation | Sources techniques de la scène Blender                       | Blender                                     | Disponible |
| Ambiance sonore générale         | Ressource à choisir ou produire                              | À définir                                   | À définir  |

Les effets et sons d'impact ou de casse relèvent des [items](../gameplay/items/environment_interactions.md) ; le modèle, le rig, les matériaux, les sons et les [animations du monstre](../monster/animations.md) relèvent de sa [documentation](../monster/README.md).

## Sources et périmètre

Les identifiants `source_pack` et `source_asset` ont été rapprochés des archives locales `blender/assets/Fantasy Props MegaKit[Standard].zip` et `blender/assets/Magic_Props.zip`. Les crédits et licences figurent dans `blender/presentation/ASSET_CREDITS.md`. L'archive `Avramania_Free_Collection.zip` est présente localement, sans modèle relevé dans cette scène. Le dossier `blender/` est ignoré par Git : disponibilité locale et présence dans le dépôt versionné sont distinctes.

Les éléments architecturaux ont été créés ou adaptés dans Blender. Les [QR codes et transformations](../architecture.md), colliders et obstacles de navigation sont des ressources techniques. L'intégration Unity et la validation sur Quest 3 restent à vérifier.

## Ressources d'énigmes

| Asset  | Modèle                                                                                | Variantes | Source      | État        |
| ------ | ------------------------------------------------------------------------------------- | --------: | ----------- | ----------- |
| Trappe | Texture de petite porte / trappe ; positions ouverte et fermée, animation d'ouverture |         — | À récupérer | À récupérer |

Une ressource peut figurer ici sans que l'[énigme associée](../gameplay/puzzles.md) soit retenue ; les objets de gameplay figurent parmi les [items](../gameplay/items/catalog.md).
