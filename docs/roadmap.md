# Roadmap

Deux étapes : **MVP 1 (INF3001)** pour la VR alignée et les interactions, puis **MVP 2 (INF3002)** pour le monstre. Les énigmes précises ne sont pas encore choisies : on commence par valider les systèmes qui serviront au jeu.

## Vue d'ensemble

| MVP 1 — INF3001                            | MVP 2 — INF3002                                         |
| ------------------------------------------ | ------------------------------------------------------- |
| **0.** Setup Quest et Unity                | **5.** Production des animations avec FreeMoCap         |
| **1.** Scan, décor et recalage de la pièce | **6.** Préparation et intégration du monstre dans Unity |
| **2.** Tables, QR codes et habillage 3D    | **7.** Navigation et IA                                 |
| **3.** Interactions virtuelles             | **8.** Intégration et tests finaux                      |
| **4.** Boucle de jeu sans monstre          |                                                         |

```mermaid
flowchart LR
    A[Setup Quest et Unity] --> B[Pièce VR alignée]
    B --> C[Tables QR + décor personnalisé]
    B --> D[Objets interactifs]
    C --> E([MVP 1 : boucle jouable])
    D --> E

    F[Animations FreeMoCap] --> G[Monstre intégré dans Unity]
    E --> H[Navigation et IA]
    G --> H
    H --> I([MVP 2 : jeu complet])

    classDef mvp fill:#e6f3ed,stroke:#27775b,color:#173d30
    class E,I mvp
```

La production des animations peut commencer **en parallèle du MVP 1**. Son intégration au jeu arrive dans le MVP 2.

---

## MVP 1 — INF3001 : VR alignée et interactions

### Phase 0 — Setup technique

**But :** faire tourner une scène Unity sur le Quest 3.

- [ ] Configurer Unity, OpenXR, Meta XR et MRUK.
- [ ] Déployer une scène de test sur le casque.
- [ ] Vérifier le suivi spatial et les interactions de base.

**Validé quand :** la scène fonctionne directement sur Quest 3.

### Phase 1 — Scan, décor et recalage de la pièce

**But :** créer un décor VR aligné avec la salle réelle.

- [ ] Scanner la pièce, nettoyer le maillage et retirer les tables du décor statique.
- [ ] Créer une première version thématisée du décor, même simple.
- [ ] Mettre en place l'ambiance sombre, l'éclairage de la scène et l'ambiance sonore générale.
- [ ] Séparer les modèles visibles des géométries de collision.
- [ ] Importer la scène dans Unity et l'aligner avec le suivi du Quest.
- [ ] Ajouter des QR codes fixes pour vérifier et corriger le recalage global.
- [ ] Tester la précision et la stabilité de l'alignement pendant une session.

**Validé quand :** le décor correspond à la pièce réelle et les QR codes fixes permettent de corriger son alignement.

### Phase 2 — Tables amovibles et habillage 3D

**But :** intégrer les tables à n'importe quelle disposition de départ et **les transformer visuellement en éléments du décor**.

- [ ] Identifier les tables, mesurer leurs dimensions et placer leurs QR codes.
- [ ] Détecter leur position et leur orientation avant chaque partie.
- [ ] Placer les modèles 3D correspondants (autels, bureaux, blocs…) à la bonne position.
- [ ] Utiliser des volumes de collision adaptés aux tables.
- [ ] Préparer ces volumes pour la navigation du monstre dans le MVP 2.
- [ ] Tester plusieurs dispositions sans en programmer une liste fixe.

**Validé quand :** chaque table est représentée par un élément du décor bien positionné, avec des collisions cohérentes, même si la disposition change entre deux parties.

> [!NOTE]
> Les tables sont calibrées au démarrage, puis restent fixes pendant le jeu. Leur suivi continu est une extension.

### Phase 3 — Interactions virtuelles

**But :** manipuler des objets qui n'existent que dans le jeu.

- [ ] Ajouter quelques objets virtuels de test.
- [ ] Mettre en place les définitions et instances d'items, leurs capacités, leur physique et leur masse.
- [ ] Gérer les collisions, la casse et les événements distincts d'impact et de bruit, puis tester ces systèmes sans monstre.
- [ ] Intégrer la torche, les cailloux et les fioles sans fixer leurs paramètres de jeu.
- [ ] Implémenter et tester le [ciblage par proximité des mains et les gestes définis](gameplay/items/player_interactions.md) sur Quest 3.
- [ ] Permettre de prendre, déplacer, tourner ou activer un objet selon son rôle.
- [ ] Vérifier que les objets restent au bon endroit dans la scène.

**Validé quand :** les interactions et collisions principales fonctionnent sur le casque. Le contenu des énigmes reste à choisir dans le [catalogue de propositions](gameplay/puzzles.md).

### Phase 4 — Boucle de jeu MVP 1

**But :** avoir une petite partie jouable sans monstre, selon le principe du mode `Peaceful`.

- [ ] Enchaîner recalage de la pièce, détection des tables et lancement du jeu.
- [ ] Choisir une ou plusieurs idées dans le [catalogue d’énigmes](gameplay/puzzles.md), puis ajouter une progression simple avec ces objets.
- [ ] Définir une condition de victoire et la possibilité de recommencer.
- [ ] Tester plusieurs dispositions de tables et une partie complète sur Quest 3.

**MVP 1 validé quand :** on peut terminer une courte partie dans un décor VR aligné, avec tables transformées visuellement et objets virtuels interactifs.

---

## MVP 2 — INF3002 : animations, monstre et IA

Le MVP 2 reprend **la même pièce et les mêmes obstacles**. La référence pour les clips et les transitions est [animations.md](monster/animations.md), conservé tel quel.

### Phase 5 — Production des animations

**But :** produire toutes les animations prévues pour le monstre avec **FreeMoCap**, puis les préparer pour Unity.

- [ ] Reprendre le graphe d'états et la liste des mouvements de `monster/animations.md`.
- [ ] Capturer les mouvements du catalogue avec FreeMoCap.
- [ ] Nettoyer et préparer les animations pour le personnage.
- [ ] Vérifier les transitions et la cohérence des clips.

**Validé quand :** les animations prévues sont exploitables pour l'intégration. Cette phase peut avancer en parallèle du MVP 1.

### Phase 6 — Préparation et intégration du monstre

**But :** avoir un personnage correctement animé dans Unity.

- [ ] Importer et vérifier le modèle 3D, le rig, le skinning et les matériaux.
- [ ] Adapter les animations au squelette du monstre (retargeting si nécessaire).
- [ ] Intégrer les clips et leurs transitions dans Unity.
- [ ] Tester les mouvements et les déformations du personnage.

**Validé quand :** le monstre joue les animations prévues dans la scène, sans problème majeur de rig ou de transition.

### Phase 7 — Navigation, perception et IA

**But :** faire réagir le monstre au joueur et contourner les obstacles.

- [ ] Générer le NavMesh au début de la partie à partir des murs et tables calibrées ; extraire sa triangulation et construire le graphe.
- [ ] Implémenter notre A* et le suivi des chemins pour contourner les obstacles, quelle que soit la disposition des tables.
- [ ] Détecter le joueur par un cône de vision (produit scalaire et raycast) et classer sa distance de perception.
- [ ] Percevoir les bruits environnementaux en excluant ceux liés au monstre.
- [ ] Conserver des pistes en mémoire et estimer les destinations sans communiquer la position cachée du joueur à la FSM ou à la navigation.
- [ ] Implémenter la FSM et ses transitions, les effets `Reaction`, `Slow` et `Stun`, ainsi que les profils de difficulté.
- [ ] Synchroniser les comportements et déplacements avec le système d'animation existant.

**Validé quand :** le monstre se déplace et change de comportement selon la situation, sans traverser les obstacles de la scène.

### Phase 8 — Intégration et tests finaux

**But :** réunir le gameplay du MVP 1 et le monstre.

- [ ] Ajouter le monstre à la boucle de jeu.
- [ ] Gérer la capture du joueur et la défaite.
- [ ] Tester le monstre avec différentes positions de tables.
- [ ] Vérifier les cinq niveaux, dont l'absence de monstre en `Peaceful`, et la cohérence des comportements et transitions.
- [ ] Vérifier l'indépendance du bruit, des effets directs et de la casse, les rebonds successifs et l'exclusion des bruits liés au monstre.
- [ ] Vérifier `attackDistance` et `attackRange`, ainsi que l'absence de frappe à travers les obstacles.
- [ ] Équilibrer masses, seuils, distances, coefficients et durées pendant les tests.
- [ ] Vérifier animations, recalage, interactions et performances sur Quest 3.
- [ ] Corriger les problèmes bloquant une partie complète.

**MVP 2 validé quand :** le joueur peut gagner ou perdre une partie complète, avec un monstre animé qui navigue et réagit dans la pièce calibrée.

---

## Dépendances principales

| Élément                   | Dépend de                                 |
| ------------------------- | ----------------------------------------- |
| Tables et objets virtuels | Repère de la pièce                        |
| Navigation                | Géométrie statique + positions des tables |
| Monstre animé             | Animations produites + personnage préparé |
| IA en jeu                 | Navigation + perception + animations      |
| Partie complète           | MVP 1 + monstre intégré                   |

Les fonctionnalités hors MVP sont regroupées dans [extensions.md](extensions.md). Les ressources d'environnement sont listées dans le [catalogue des assets](environment/assets.md) et les objets de gameplay dans le [catalogue des items](gameplay/items/catalog.md).
