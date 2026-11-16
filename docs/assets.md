# Assets

Liste des ressources **communes aux MVP**. On garde ici ce qui sert au jeu, sans imposer d’énigme tant que l’équipe ne les a pas choisies.

- **À produire** : créer ou scanner.
- **À adapter** : ressource existante à modifier.
- **À définir** : choix artistique ou modèle pas encore arrêté.

## MVP 1 — Environnement VR

| Asset                                | Travail attendu                                                                                     | Source                                  | État                 |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- | --------------------------------------- | -------------------- |
| **Scan 3D de la salle**              | Relever la géométrie fixe, sans intégrer définitivement les tables                                  | ScanSpace ou autre outil de scan        | À produire           |
| **Décor statique thématisé**         | Nettoyer le scan ; habiller sol, murs, plafond et ouvertures en gardant l'échelle réelle            | Blender                                 | À produire           |
| **Matériaux et textures du décor**   | Définir l'apparence de la pièce selon le thème choisi                                               | Blender / Unity / ressources existantes | À définir            |
| **Modèle 3D des tables**             | Créer une représentation thématisée des tables, indépendante du décor fixe : autel, bloc, bureau…   | Blender / ressource existante           | À produire / adapter |
| **Matériaux et textures des tables** | Assortir les tables au décor choisi                                                                 | Blender / Unity                         | À définir            |
| **Objet virtuel de test**            | Une forme simple pour valider la sélection, la prise et les mouvements avant de choisir les énigmes | Primitive Unity                         | À produire           |

> [!NOTE]
> Les tables sont calibrées **avant chaque partie** par QR code. Elles peuvent avoir différentes positions d'une partie à l'autre, sans configuration prédéfinie. Leur habillage visuel fait partie du MVP 1.

## MVP 2 — Monstre

| Asset                                | Travail attendu                                                        | Source                          | État       |
| ------------------------------------ | ---------------------------------------------------------------------- | ------------------------------- | ---------- |
| **Modèle 3D du monstre**             | Reprendre et adapter le Goblin existant ou le modèle finalement retenu | Modèle existant / Blender       | À adapter  |
| **Rig et skinning**                  | Vérifier squelette, poids et déformations                              | Blender                         | À vérifier |
| **Matériaux et textures du monstre** | Vérifier et adapter son apparence pour Unity                           | Ressources existantes / Blender | À adapter  |
| **Animations du monstre**            | Produire les mouvements et leurs transitions selon le document dédié   | FreeMoCap / Blender / Unity     | En cours   |

Les animations sont détaillées dans [monster_animations.md](monster_animations.md), pas recopiées ici.

## Ressources techniques

Elles ne sont pas forcément des modèles Blender, mais sont nécessaires pour utiliser les assets correctement.

| Ressource                  | À quoi ça sert                                      |
| -------------------------- | --------------------------------------------------- |
| QR codes fixes de la pièce | Corriger le recalage global                         |
| QR codes des tables        | Identifier et placer les meubles avant la partie    |
| Repères et transformations | Relier scan, salle, QR codes et modèles 3D          |
| Colliders simplifiés       | Représenter les volumes fixes et ceux des tables    |
| Obstacles de navigation    | Permettre au monstre de contourner murs et mobilier |

Le dépôt possède déjà un générateur de marqueurs dans `tools/markers`.

## Assets des énigmes retenues

**Cette section reste vide tant que l'équipe n'a pas choisi les énigmes.**

Chaque idée conserve d'abord sa liste d'assets dans sa propre [fiche](puzzles.md). Quand une énigme est retenue, on ajoute ici uniquement les ressources à produire, avec un lien vers cette fiche. Si deux énigmes utilisent le même modèle, on ne le liste qu'une seule fois.

| Asset                         | Utilisé par | État |
| ----------------------------- | ----------- | ---- |
| *À compléter après sélection* | —           | —    |
