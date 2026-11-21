# Monstre

## Concept

Humanoïde d'environ trois mètres, très maigre, aux bras disproportionnés. Il se déplace le dos voûté, la tête basse et les épaules tombantes. Sa démarche est boiteuse et lourde ; il semble épuisé. Il ne court jamais, même pendant une poursuite.

Sa menace repose sur son allonge, sa persistance, ses réactions et la difficulté à l'éviter dans une pièce unique, pas sur une vitesse de course élevée.

## Règles générales

Le monstre est immortel et [patrouille](ai/behavior.md) sans stimulus exploitable. Sa [perception](ai/perception.md) est limitée ; les [items](ai/item_reactions.md) peuvent le distraire ou interrompre temporairement. En difficulté [`Peaceful`](ai/difficulty.md), aucun monstre n'est généré.

Son déplacement virtuel ne doit jamais obliger le joueur à courir ou esquiver physiquement vers un obstacle réel.

## Ressources du personnage

| Ressource | Situation |
| --- | --- |
| Modèles 3D | `assets/motion/monster/models/generated.glb` et `rigged.glb` sont présents ; modèle final à confirmer. |
| Rig et skinning | Modèle riggé disponible ; qualité des déformations et intégration Unity à vérifier. |
| Matériaux et textures | Apparence finale et adaptation à Unity à vérifier. |
| Animations | Clips et références dans le [catalogue des animations](animations.md) ; intégration au jeu à vérifier. |
| Sons du monstre | Besoins et fichiers finaux à définir. |

Ces ressources concernent le personnage, pas le décor statique de l'[environnement](../environment/assets.md).

## Documentation

- [Animations](animations.md)
- [Architecture de l'IA](ai/README.md)
