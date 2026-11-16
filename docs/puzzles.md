# Idées d'énigmes

Ce document sert à **proposer et comparer** les énigmes avant de choisir celles du jeu. Rien dans cette liste n'est automatiquement obligatoire pour le MVP 1.

## Propositions

| Énigme                                       | Difficulté technique | Statut              |
| -------------------------------------------- | -------------------- | ------------------- |
| [Clé et coffre](puzzles/key-chest.md)        | Facile               | Exemple, non retenu |
| [Pièce miniature](puzzles/miniature-room.md) | Difficile            | Exemple, non retenu |

> [!NOTE]
> Ces deux fiches sont là pour montrer comment documenter une idée. Elles ne représentent **pas** un choix de gameplay.

## Ajouter une énigme

1. Copier [`puzzles/template.md`](puzzles/template.md) dans un nouveau fichier, par exemple `puzzles/nom-de-l-enigme.md`.
2. Décrire l'idée et les interactions, même si tout n'est pas encore décidé.
3. Ajouter **ses assets directement dans la fiche**, sans toucher à `assets.md`.
4. Ajouter une ligne au tableau ci-dessus.
5. Si l'équipe retient l'énigme, passer son statut à **Retenue** et ajouter les assets à produire dans [`assets.md`](assets.md), avec un lien vers la fiche.

## Statuts

| Statut               | Signification                   |
| -------------------- | ------------------------------- |
| **Proposée**         | Idée en discussion              |
| **Retenue**          | L'équipe a choisi de l'intégrer |
| **En développement** | Implémentation commencée        |
| **Terminée**         | Fonctionne dans le jeu          |
| **Écartée**          | Non retenue pour le moment      |

## Difficulté technique

| Niveau        | Ordre de grandeur                                                     |
| ------------- | --------------------------------------------------------------------- |
| **Facile**    | Prendre, poser, activer, ouvrir : interactions classiques             |
| **Moyenne**   | Plusieurs objets ou une logique particulière à synchroniser           |
| **Difficile** | Nouveau système technique, scène miniature, synchronisation complexe… |

La difficulté concerne **l'implémentation**, pas la difficulté de résolution pour le joueur. Elle peut évoluer après un essai dans Unity.
