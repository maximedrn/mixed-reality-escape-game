# Catalogue des assets d'environnement

Ce catalogue couvre l'architecture, le décor structurel, le mobilier, le rangement et l'éclairage fixe. Les [items](../gameplay/items/catalog.md), le [monstre](../monster/README.md) et les ressources de recalage de l'[architecture](../architecture.md) ont leurs propres documents. Un modèle 3D d'item reste techniquement un asset Unity/Blender ; la séparation est documentaire.

> [!IMPORTANT]
> Pour l'instant, les listes d'assets et d'items se basent sur la scène de présentation réalisée sous Blender. Elles ne sont pas définitives et restent modifiables. Par exemple, les sources de lumière seront probablement supprimées en dehors du mode Peaceful. La disposition et les ajustements du mobilier pourront également évoluer.

**Référence des modèles :** la scène locale `blender/presentation/room-presentation-dense.blend`, inspectée en lecture seule. Une *variante* désigne un modèle distinct. `—` dans la colonne « Variantes » indique qu'aucun modèle n'est encore choisi.

| État                 | Signification                                                     |
| -------------------- | ----------------------------------------------------------------- |
| Modélisé             | Géométrie créée dans Blender et présente dans la scène inspectée. |
| Présent dans Blender | Modèle de pack identifié et placé dans la scène inspectée.        |
| À adapter            | Ressource existante dont l'adaptation au jeu reste à faire.       |
| À produire           | Ressource prévue mais absente.                                    |
| À définir            | Besoin, modèle ou choix non arrêté.                               |
| À vérifier           | Disponibilité ou intégration non confirmée.                       |

## Architecture et décor structurel

| Asset                    | Description                                                       | Source  | État     |
| ------------------------ | ----------------------------------------------------------------- | ------- | -------- |
| Murs en pierre           | Parement mural ; `Wall_Stone_N/S/E/W`.                            | Blender | Modélisé |
| Sol en pierre            | Dalles, usure et joints formant un seul sol.                      | Blender | Modélisé |
| Cercle alchimique du sol | Gravure intégrée aux dalles, `Alchemy_Engraved_Recesses`.         | Blender | Modélisé |
| Plafond voûté            | Voûte gothique avec parement `Ceiling_Stone` et reprises locales. | Blender | Modélisé |
| Piliers                  | Surfaces usées du pilier mural et du pilier d'angle.              | Blender | Modélisé |
| Entablements             | Bande périphérique et chapiteaux adaptés aux piliers.             | Blender | Modélisé |
| Nervures de voûte        | Nervures diagonales et de rive formant un réseau architectural.   | Blender | Modélisé |
| Portes                   | Portes médiévales adaptées aux ouvertures de la salle.            | Blender | Modélisé |
| Encadrements de portes   | Encadrements adaptés aux ouvertures.                              | Blender | Modélisé |

Le scan brut, les surfaces de référence, les supports de génération et les objets masqués restent hors catalogue. La géométrie visible et les volumes de collision ou de navigation ont des responsabilités distinctes ; voir l'[architecture](../architecture.md) et la [navigation du monstre](../monster/ai/navigation.md).

## Mobilier

Les modèles ci-dessous sont **placés dans la présentation Blender**. Leur présence ne prouve pas qu'ils représentent déjà les tables physiques suivies par QR code.

| Asset                          | Description                                                                                 | Variantes | Source                | État                 |
| ------------------------------ | ------------------------------------------------------------------------------------------- | --------: | --------------------- | -------------------- |
| Grande table d'alchimie        | Table `Table_Large` du décor.                                                               |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Établi de recherche            | Établi `Workbench`.                                                                         |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Tabourets                      | Modèle `Stool`.                                                                             |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Chaise                         | Siège `Chair_1`.                                                                            |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Bibliothèques                  | Modèle `Bookcase_2`.                                                                        |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Étagères arquées               | Modèle `Shelf_Arch`.                                                                        |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Armoire basse                  | Modèle `Cabinet`.                                                                           |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Meuble à étagères              | Modèle `Nightstand_Shelf`.                                                                  |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Lutrin                         | Support `BookStand` ; le manuscrit posé dessus est un [item](../gameplay/items/catalog.md). |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Étagère murale simple          | Modèle `Shelf_Simple`.                                                                      |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Petites tables                 | Modèle distinct à préciser ; aucun n'est identifié sous ce nom dans la scène.               |         — | À définir             | À définir            |
| Habillage des tables physiques | Modèles séparés du décor, à associer aux tables réellement mesurées et calibrées.           |         — | À définir             | À définir            |

## Rangement

| Asset             | Description                                                                                                   | Variantes | Source                | État                 |
| ----------------- | ------------------------------------------------------------------------------------------------------------- | --------: | --------------------- | -------------------- |
| Coffres           | `SM_Magic_Chest_Body` et `SM_Magic_Chest_Lid` forment chaque coffre.                                          |         1 | Magic Props           | Présent dans Blender |
| Tonneaux          | Modèle `Barrel`.                                                                                              |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Caisses en bois   | Modèle `Crate_Wooden`.                                                                                        |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Caisse métallique | Modèle `Crate_Metal`.                                                                                         |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Sac               | Modèle `Bag`.                                                                                                 |         1 | Fantasy Props MegaKit | Présent dans Blender |

Les bourses d'ingrédients et les grandes bourses, y compris les modèles suspendus, sont recensées avec les [items](../gameplay/items/catalog.md).

## Éclairage fixe

| Asset             | Description                                                                   | Variantes | Source                | État                 |
| ----------------- | ----------------------------------------------------------------------------- | --------: | --------------------- | -------------------- |
| Torches murales   | Modèle `Torch_Metal` avec flamme visuelle ; les lampes Unity sont techniques. |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Lanternes murales | Modèle `Lantern_Wall`.                                                        |         1 | Fantasy Props MegaKit | Présent dans Blender |
| Lustre            | Aucun lustre relevé dans la scène ; besoin et modèle à préciser.              |         — | À définir             | À définir            |

La torche portable du joueur et les bougies figurent dans le [catalogue des items](../gameplay/items/catalog.md).

## Matériaux, textures et ambiance

| Ressource                        | Description                                                                                        | Source                                      | État                                                |
| -------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------- | --------------------------------------------------- |
| Matériaux architecturaux         | Palette de pierre irrégulière, mortier, sol usé, bois et fer des portes présents dans le `.blend`. | Blender                                     | Modélisé                                            |
| Matériaux du mobilier            | Matériaux bois et métal adaptés aux modèles du MegaKit.                                            | Fantasy Props MegaKit, adaptés dans Blender | Présent dans Blender                                |
| Éclairage global de présentation | Sources techniques de la scène Blender, distinctes des luminaires décoratifs.                      | Blender                                     | Présent dans Blender ; intégration Unity à vérifier |
| Ambiance sonore générale         | Ressource sonore de la salle à choisir ou produire.                                                | À définir                                   | À définir                                           |

Les effets propres à un item et les sons d'impact ou de casse relèvent des [interactions physiques des items](../gameplay/items/environment_interactions.md). Le modèle, le rig, les matériaux, les sons et les [animations du monstre](../monster/animations.md) relèvent de la [documentation du monstre](../monster/README.md).

## Sources et périmètre

Les identifiants `source_pack` et `source_asset` de la scène ont été rapprochés des archives locales `blender/assets/Fantasy Props MegaKit[Standard].zip` et `blender/assets/Magic_Props.zip`. Les crédits et licences figurent dans le fichier local `blender/presentation/ASSET_CREDITS.md`. `Avramania_Free_Collection.zip` se trouve aussi dans `blender/assets/`, mais aucun de ses modèles n'a été relevé dans cette scène. Le dossier `blender/` est actuellement ignoré par Git ; la disponibilité locale d'un modèle ne vaut ni sa présence dans le dépôt versionné ni son utilisation dans le jeu.

Les éléments architecturaux ont été créés ou adaptés dans Blender. Les [QR codes et transformations](../architecture.md) ainsi que les colliders et obstacles de navigation sont des ressources techniques, hors des tableaux de décor. L'intégration Unity et la validation sur Quest 3 restent à vérifier.

## Ressources d'énigmes

| Asset  | Description                                                                                          | Variantes | Source       | État       |
| ------ | ---------------------------------------------------------------------------------------------------- | --------: | ------------ | ---------- |
| Trappe | Texture de petite porte / trappe. Prévoir les positions ouvertes et fermé et l'animation d'ouverture |         — | à récupérer  | À vérifier |

Une ressource peut figurer dans ce catalogue sans que l'[énigme associée](../gameplay/puzzles.md) soit retenue. Les objets de gameplay figurent dans le [catalogue des items](../gameplay/items/catalog.md).
