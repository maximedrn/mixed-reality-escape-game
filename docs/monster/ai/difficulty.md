# Difficultés

## 1. Niveaux

| Niveau     | Principe                                                                                   |
| ---------- | ------------------------------------------------------------------------------------------ |
| `Peaceful` | Aucun monstre. Escape game uniquement ; les items et les énigmes fonctionnent normalement. |
| `Easy`     | Perception et menace plus permissives pour le joueur.                                      |
| `Normal`   | Profil de référence.                                                                       |
| `Hard`     | Monstre plus difficile à éviter et plus persistant.                                        |
| `Hardcore` | Profil le plus exigeant.                                                                   |

Pour commencer, utiliser les mêmes règles et la même FSM pour tous les niveaux avec monstre. Seuls les paramètres changent. Les différences de règles éventuelles resteront à discuter.

## 2. Profil de difficulté

Un `DifficultyProfile` centralise les paramètres consommés par les autres modules. Il pourra être représenté par un ScriptableObject Unity. Le profil sélectionné est fourni au monstre au début de la partie. En `Peaceful`, le système de jeu ne crée pas le monstre.

Les champs suivants sont proposés comme catalogue initial ; ils ne doivent être intégrés que s'ils correspondent à une mécanique réellement utilisée.

### Perception

| Paramètre             | Utilité                                              |
| --------------------- | ---------------------------------------------------- |
| `visionFov`           | Ouverture du cône de vision.                         |
| `investigateDistance` | Distance maximale d'investigation visuelle.          |
| `chaseDistance`       | Distance maximale de poursuite visuelle.             |
| `attackDistance`      | Distance maximale de la catégorie visuelle `Attack`. |
| `visionAcquireDelay`  | Durée requise avant confirmation visuelle.           |
| `visionLoseDelay`     | Tolérance avant perte de contact.                    |
| `hearingRange`        | Portée maximale de perception d'un bruit.            |
| `hearingThreshold`    | Intensité minimale audible.                          |

### Mémoire et comportement

| Paramètre                     | Utilité                                                                    |
| ----------------------------- | -------------------------------------------------------------------------- |
| `visualMemoryDuration`        | Durée de validité d'une piste visuelle.                                    |
| `noiseMemoryDuration`         | Durée de validité d'une piste sonore.                                      |
| `investigateDuration`         | Budget maximal d'investigation.                                            |
| `investigateDistanceEstimate` | Distance de déplacement estimée pour une piste sonore.                     |
| `searchDuration`              | Budget de recherche.                                                       |
| `searchRadius`                | Étendue de la zone à fouiller.                                             |
| `chasePersistence`            | Durée de poursuite sur dernière estimation après perte visuelle confirmée. |
| `patrolSpeed`                 | Vitesse de patrouille.                                                     |
| `investigateSpeed`            | Vitesse d'investigation.                                                   |
| `searchSpeed`                 | Vitesse de recherche.                                                      |
| `chaseSpeed`                  | Vitesse de poursuite (toujours en marchant).                               |

`visionAcquireDelay` confirme la vue, `visionLoseDelay` tolère sa perte temporaire et `chasePersistence` maintient la poursuite vers la dernière estimation après perte confirmée. Ne pas appliquer deux fois un même délai. La distance estimée d'une observation visuelle peut être dérivée des catégories de détection plutôt que stockée séparément dans le profil.

### Attaque et récupération

| Paramètre          | Utilité                                                                      |
| ------------------ | ---------------------------------------------------------------------------- |
| `attackRange`      | Portée effective de la frappe, cohérente avec l'animation et les collisions. |
| `attackCooldown`   | Délai minimal avant une nouvelle attaque.                                    |
| `recoveryDuration` | Durée de récupération lorsque nécessaire.                                    |

`attackDistance` relève de la perception et peut varier avec la difficulté ; `attackRange` est la portée physique du combat, liée à la morphologie, aux animations, aux volumes de collision et aux obstacles. Leurs origines de mesure peuvent différer. La difficulté ne change pas arbitrairement cette géométrie ni les fenêtres d'impact des animations.

### Réactions aux items

| Paramètre                   | Utilité                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------- |
| `impactThresholdMultiplier` | Résistance aux impacts directs, appliquée au seuil `minImpactStrength` de chaque règle. |
| `slowSpeedMultiplier`       | Facteur de vitesse pendant un ralentissement.                                           |
| `slowDurationMultiplier`    | Facteur de durée de ralentissement.                                                     |
| `stunDurationMultiplier`    | Facteur de durée d'étourdissement.                                                      |

La difficulté peut modifier le FOV, les distances visuelles, les seuils et portées d'audition, la mémoire, la recherche, les vitesses de marche, la résistance aux impacts et les durées ou l'intensité des effets directs lorsque pertinentes. Elle ne modifie ni la masse, la vitesse réelle ou la physique des items, ni leur intensité sonore calculée, leur seuil de casse, la géométrie de frappe ou les fenêtres d'animation. La règle de non-cumul pendant `Stunned` reste décrite dans [item_reactions.md](item_reactions.md) ; les autres paramètres seront fixés pendant les tests.
