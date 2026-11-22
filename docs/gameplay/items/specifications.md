# Spécifications des items

## 1. Types et capacités

Le type concret identifie l'objet (torche, caillou, fiole, indice...). Les quatre capacités statiques ci-dessous sont indépendantes et combinables. Les noms `is…` désignent le test du flag correspondant dans `capabilities`, et non des champs supplémentaires.

| Test | Flag | Signification |
| --- | --- | --- |
| `isGrabbable` | `Grabbable` | L'item peut être saisi, déplacé et lancé directement ou indirectement. |
| `isManipulable` | `Manipulable` | L'item possède au moins une manipulation spécifique et continue en `Pinch`. |
| `isActivatable` | `Activatable` | L'item possède au moins une activation ponctuelle en `Point`. |
| `isBreakable` | `Breakable` | L'item peut être brisé. |

Implémentation C# proposée :

```csharp
[Flags]
public enum ItemCapabilities
{
    None        = 0,
    Grabbable   = 1 << 0,
    Manipulable = 1 << 1,
    Activatable = 1 << 2,
    Breakable   = 1 << 3
}
```

La saisie concerne l'item entier ; les manipulations et activations spécifiques utilisent les [points d'interaction](player_interactions.md#points-dinteraction) lorsqu'ils sont nécessaires. `Grabbable` suffit pour les deux modes de lancer. `Breakable` est indépendant des gestes. L'association à une énigme ou une quête décrit le rôle de l'item, sans flag supplémentaire.

`Reusable` et `EquippedItem` restent **à définir** et ne font pas partie des capacités retenues.

Le bruit d'impact ne requiert pas de capacité dédiée ; voir les [interactions physiques](environment_interactions.md). Les effets directs sur le monstre restent configurés par `impactRules`.

## 2. Spécifications communes

Les champs suivants constituent un **catalogue de propriétés proposées**, pas une liste à implémenter intégralement pour tous les objets.

`ItemDefinition` contient l'identification, les capacités et les propriétés configurables ; chaque `ItemInstance` y fait référence et porte son état dynamique.

### Définition (configuration)

| Champ            | Type                       | Utilisation                                        |
| ---------------- | -------------------------- | -------------------------------------------------- |
| `id`             | String                     | Identifiant de la définition.                      |
| `capabilities`   | ItemCapabilities           | Flags statiques combinés.                          |
| `mass`           | Float                      | Masse en kg des items physiques mobiles.           |
| `breakThreshold` | Float                      | Vitesse minimale pour casser un objet `Breakable`. |
| `impactRules`    | Collection de `ImpactRule` | Effets directs selon la sévérité de l'impact.      |

La masse d'un objet physique mobile est strictement positive et correspond à celle de son Rigidbody Unity : ne pas maintenir deux valeurs indépendantes. Un objet statique ou sans physique dynamique n'a pas forcément de masse configurable. Un indice immobile n'a pas besoin de `breakThreshold` ni de règles d'impact.

Chaque `ImpactRule` associe un `effect` (`None`, `Reaction`, `Slow` ou `Stun`), un seuil `minImpactStrength` et une `baseDuration` lorsqu'elle est pertinente. `Reaction` peut se terminer avec l'action ou l'animation, sans durée propre. Une collection vide signifie qu'aucun effet direct n'est configuré ; aucun item n'est obligé de posséder toutes les règles. Le type de collection et sa représentation C# seront choisis pendant l'implémentation.

La vitesse, le bruit et la sévérité sont définis dans les [collisions et événements](environment_interactions.md).

### État dynamique (instance)

| Information | Type    | Utilisation                           |
| ----------- | ------- | ------------------------------------- |
| `position`  | Vector3 | Position dans la scène.               |
| `velocity`  | Vector3 | Vélocité courante.                    |
| `isHeld`    | Bool    | Objet tenu.                           |
| `isBroken`  | Bool    | Objet cassé.                          |
| `isActive`  | Bool    | Objet activé, par exemple une torche. |

La position et la vélocité sont fournies par le Transform et le Rigidbody lorsqu'ils existent. Il n'est pas nécessaire de dupliquer ces données.
Une capacité statique comme `Breakable` ne remplace pas l'état courant : un item cassé peut rester `Breakable` sans pouvoir être cassé de nouveau.

## 3. Équilibrage

Les seuils, durées et effets individuels seront définis progressivement avec le [catalogue](catalog.md), puis ajustés en jeu. Aucun barème numérique n'est fixé ici.
