namespace Project.Monster
{
    /// <summary>Represents the high-level behavior of the monster.</summary>
    public enum MonsterState
    {
        /// <summary>The monster is following its patrol route.</summary>
        Patrolling,

        /// <summary>The monster is pursuing its target.</summary>
        Chasing,

        /// <summary>The monster is searching for a lost target.</summary>
        Searching,

        /// <summary>The monster is returning to its patrol route.</summary>
        Returning,
    }
}
