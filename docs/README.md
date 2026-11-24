# Tohannic: No Way Out

> Escape game en **VR alignée avec une vraie pièce**, développé sur **Meta Quest 3**.

## Le concept

Le joueur explore une version virtuelle de la pièce réelle, sur le thème d'une **salle d'alchimie médiévale fantasy low-poly**. L'échelle et les obstacles virtuels doivent correspondre à la salle physique.

Le MVP utilise une seule pièce en VR. Le Quest et des QR codes fixes assurent le recalage ; les tables, repérées par leurs propres QR codes avant chaque partie, reçoivent un habillage virtuel et restent fixes pendant la session. Les items restent purement virtuels et fonctionnent aussi en mode `Peaceful`, sans monstre. Le détail spatial figure dans l'[architecture](architecture.md) ; la MR et le suivi continu des tables sont des [extensions](extensions.md).

## Les deux MVP

| MVP                 | Objectif                                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------ |
| **MVP 1 — INF3001** | Salle VR alignée, tables détectées et transformées visuellement, objets interactifs et courte boucle de jeu. |
| **MVP 2 — INF3002** | Monstre animé, perception visuelle et auditive, réactions aux collisions, mémoire, FSM et navigation.        |

Le déroulement détaillé est dans la [roadmap](roadmap.md).

## Documentation

- [Architecture](architecture.md) — les trois catégories d'objets et le recalage.
- [Schéma SQLite](database/README.md) — configuration, classement, statistiques et données initiales.
- [Environnement](environment/README.md) — la salle virtuelle et sa direction artistique.
- [Assets d'environnement](environment/assets.md) — architecture, mobilier, rangement et éclairage fixe.
- [Gameplay](gameplay/README.md) — règles générales.
- [Items](gameplay/items/README.md) — catalogue, spécifications et physique.
- [Interactions joueur/items](gameplay/items/player_interactions.md) — gestes et manipulation des items en VR.
- [Idées d’énigmes](gameplay/puzzles.md) — les propositions de l’équipe, sans choix imposé.
- [Monstre](monster/README.md) — concept et ressources du personnage.
- [Architecture de l'IA](monster/ai/README.md) — modules et échanges.
- [Animations du monstre](monster/animations.md) — document de référence.
- [Roadmap](roadmap.md) — toutes les phases des MVP 1 et 2.
- [Extensions](extensions.md) — les fonctionnalités qu'on garde pour plus tard.
