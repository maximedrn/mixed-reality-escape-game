namespace Project.GameFlow.Domain
{
    using System;

    /// <summary>Identifies a game session across state changes.</summary>
    public readonly struct SessionId
    {
        /// <summary>Initializes a new instance of the <see cref="SessionId"/> struct.</summary>
        /// <param name="value">The value to check when creating a session.</param>
        public SessionId(Guid value)
        {
            this.Value = value;
        }

        /// <summary>Gets the underlying identifier.</summary>
        public Guid Value { get; }
    }
}
