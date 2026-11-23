namespace Project.GameFlow.Domain
{
    /// <summary>Describes expected errors while creating or advancing a session.</summary>
    public enum SessionError
    {
        /// <summary>The session identifier was empty.</summary>
        InvalidId,

        /// <summary>The requested state cannot follow the current state.</summary>
        InvalidTransition,
    }
}
