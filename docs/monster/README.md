# Monstre

## Concept

Humanoïde d'environ trois mètres, très maigre, aux bras disproportionnés. Il se déplace le dos voûté, la tête basse et les épaules tombantes. Sa démarche est boiteuse et lourde ; il semble épuisé. Il ne court jamais, même pendant une poursuite.

Sa menace repose sur son allonge, sa persistance, ses réactions et la difficulté à l'éviter dans une pièce unique, pas sur une vitesse de course élevée.

## Règles

- En l'absence de stimulus exploitable, il patrouille continuellement. Les pauses d'animation liées à une action restent possibles, mais il n'a pas d'état comportemental `Idle`.
- Il perçoit surtout des directions et des indices par la vision et l'audition. Il ne connaît pas en permanence la position exacte du joueur.
- Les tables et les murs sont pris en compte dans la perception et la navigation.
- Le monstre est immortel. Les bruits environnementaux perçus peuvent le distraire ; les impacts directs peuvent provoquer `Reaction`, le ralentir ou l'étourdir temporairement.
- Le niveau de difficulté adapte son comportement et ses paramètres. En `Peaceful`, aucun monstre n'est généré.
- Les déplacements virtuels du monstre ne doivent jamais exiger du joueur qu'il coure ou esquive physiquement vers des obstacles réels.

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
- [Comportements](ai/behavior.md)
- [Perception](ai/perception.md)
- [Mémoire](ai/memory.md)
- [Navigation](ai/navigation.md)
- [Intégration des animations](ai/animation_integration.md)
- [Réactions aux items](ai/item_reactions.md)
- [Difficulté](ai/difficulty.md)
