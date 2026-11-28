using System;

namespace RoomGeneration
{
    public sealed class ProceduralGenerator
    {
        public EnvironmentData Generate(RoomData room)
        {
            if (room == null) throw new ArgumentNullException(nameof(room));

            // Placeholder: this is the entry point for the future generation algorithms.
            return new EnvironmentData();
        }
    }
}
