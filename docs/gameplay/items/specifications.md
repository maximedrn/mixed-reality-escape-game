# Spécifications des items

## 1. Types et capacités

Le type concret identifie l'objet (torche, caillou, fiole, indice...). Ses capacités décrivent ce qu'il peut faire. Elles se combinent librement, sans créer un enum distinct pour chaque combinaison d'items.

| Capacité       | Signification                                |
| -------------- | -------------------------------------------- |
| `QuestItem`    | Utilisable dans une énigme.                  |
| `Throwable`    | Peut être lancé.                             |
| `Breakable`    | Peut se casser.                              |
| `Interactable` | Peut être manipulé ou utilisé par le joueur. |

Implémentation C# proposée :

```csharp
[Flags]
public enum ItemCapabilities
{
    None         = 0,
    QuestItem    = 1 << 0,
    Throwable    = 1 << 1,
    Breakable    = 1 << 2,
    Interactable = 1 << 3
}
```

Tous les items physiques peuvent produire un bruit lors d'un impact significatif, même sans lancer préalable. Un bruit perçu peut détourner l'attention du monstre selon sa FSM ; les effets directs dépendent des règles d'impact de l'item, sans capacité supplémentaire.

## 2. Spécifications communes

Les champs suivants constituent un **catalogue de propriétés proposées**, pas une liste à implémenter intégralement pour tous les objets.

### Définition (configuration)

| Champ            | Type                       | Utilisation                                                                                          |
| ---------------- | -------------------------- | ---------------------------------------------------------------------------------------------------- |
| `id`             | String                     | Identifiant de la définition de l'item.                                                              |
| `capabilities`   | ItemCapabilities           | Capacités combinées.                                                                                 |
| `isGrabbable`    | Bool                       | L'objet peut être pris en main.                                                                      |
| `isReusable`     | Bool                       | L'objet peut être réutilisé après usage, tant qu'il existe.                                          |
| `mass`           | Float                      | Masse en kg des items physiques mobiles, utilisée pour les calculs physiques et les impacts directs. |
| `breakThreshold` | Float                      | Vitesse minimale pour casser un objet `Breakable`.                                                   |
| `impactRules`    | Collection de `ImpactRule` | Effets directs configurables selon la sévérité de l'impact.                                          |

La masse d'un objet physique mobile est strictement positive et correspond à celle de son Rigidbody Unity : ne pas maintenir deux valeurs indépendantes. Un objet statique ou sans physique dynamique n'a pas forcément de masse configurable. Un indice immobile n'a pas besoin de `breakThreshold` ni de règles d'impact.

Chaque `ImpactRule` associe un `effect` (`None`, `Reaction`, `Slow` ou `Stun`), un seuil `minImpactStrength` et une `baseDuration` lorsqu'elle est pertinente. `Reaction` peut se terminer avec l'action ou l'animation, sans durée propre. Une collection vide signifie qu'aucun effet direct n'est configuré ; aucun item n'est obligé de posséder toutes les règles. Le type de collection et sa représentation C# seront choisis pendant l'implémentation.

```text
impactSpeed = length(preImpactVelocity)
impactStrength = mass * impactSpeed
```

`preImpactVelocity` est mesurée juste avant la collision. `impactSpeed` est en m/s et `impactStrength` en kg·m/s : ce nom de gameplay désigne la quantité de mouvement avant impact, indicateur simplifié de sévérité, et non une force en newtons. Cette approche suffit au MVP ; voir les [collisions et événements](environment_interactions.md).

### État dynamique (instance)

| Information | Type    | Utilisation                           |
| ----------- | ------- | ------------------------------------- |
| `position`  | Vector3 | Position dans la scène.               |
| `velocity`  | Vector3 | Vélocité courante.                    |
| `isHeld`    | Bool    | Objet tenu.                           |
| `isBroken`  | Bool    | Objet cassé.                          |
| `isActive`  | Bool    | Objet activé, par exemple une torche. |

La position et la vélocité sont fournies par le Transform et le Rigidbody lorsqu'ils existent. Il n'est pas nécessaire de dupliquer ces données.

## 3. Équilibrage

Les seuils, durées et effets individuels seront définis progressivement avec le [catalogue](catalog.md), puis ajustés en jeu. Aucun barème numérique n'est fixé ici.
