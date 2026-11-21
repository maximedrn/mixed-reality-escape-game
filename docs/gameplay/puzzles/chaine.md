# Tirage de chaine

**Difficulté technique :** Moyenne

## Principe

Une chaine est posé au sol / pend du plafond et est physiquement simulé(algorithme utilisé a préciser si l'idée est satisfaisante). Le joueur doit tirer sur la chaine pour relacher une trappe dans la pièce (pas forcement visible mais entendable).
La trappe relache est objet lié à une autre quete

## Déroulement

1. Le joueur voit la chaine
2. Il tire sur cette dernière
3. Un son se produit, indiquant qu'une trappe c'est ouverte (ou non si pas de sons)
4. De cette trappe un objet tombe
5. Le joueur enchaine sur une autre quête lié a cette objet

## Assets nécessaires

- [Chaine — catalogue des items](../items/catalog.md#items-propres-aux-énigmes-proposées)
- [Trappe — catalogue des assets](../../environment/assets.md#ressources-dénigmes)

## Difficultés techniques

- Simulation physique de la corde (différente option, à décider en fonction des performances voulues)
- Génération des trappes de manières cohérentes (pas les unes a coté des autres, pas au dessus des murs)

## Remarques

Variantes, questions ouvertes, références ou petit schéma si nécessaire.
