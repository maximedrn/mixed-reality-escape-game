# Idées d'énigmes

Ce document sert à **proposer et comparer** les énigmes avant de choisir celles du jeu. Rien dans cette liste n'est automatiquement obligatoire pour le MVP 1.

## Propositions

| Énigme                                | Difficulté technique |
| ------------------------------------- | -------------------- |
| [Tirage de chaîne](puzzles/chaine.md) | Moyenne              |

## Ajouter une énigme

1. Copier [`puzzles/template.md`](puzzles/template.md) dans un nouveau fichier, par exemple `puzzles/nom-de-l-enigme.md`.
2. Décrire l'idée et les interactions, même si tout n'est pas encore décidé.
3. Inscrire les ressources nécessaires dans le [catalogue des assets](../environment/assets.md) ou le [catalogue des items](items/catalog.md), puis les référencer dans la fiche par des liens, sans dupliquer leurs descriptions.
4. Ajouter une ligne au tableau ci-dessus.

## Difficulté technique

| Niveau        | Ordre de grandeur                                           |
| ------------- | ----------------------------------------------------------- |
| **Facile**    | Prendre, poser, activer, ouvrir : interactions classiques   |
| **Moyenne**   | Plusieurs objets ou une logique particulière à synchroniser |
| **Difficile** | Nouveau système technique ou synchronisation complexe…      |

La difficulté concerne **l'implémentation**, pas la difficulté de résolution pour le joueur. Elle peut évoluer après un essai dans Unity.
