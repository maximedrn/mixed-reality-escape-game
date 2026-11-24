namespace Project.Persistence
{
    using System;
    using System.Collections.Generic;

    /// <summary>Contains a completed session and the measurements saved with it.</summary>
    public sealed class GameSessionRecord
    {
        /// <summary>Gets or sets the finished session.</summary>
        public GameSessionRow Session { get; set; }

        /// <summary>Gets or sets statistics for the puzzles in the session.</summary>
        public IReadOnlyList<SessionPuzzleStatsRow> Puzzles { get; set; } =
            Array.Empty<SessionPuzzleStatsRow>();

        /// <summary>Gets or sets statistics for the monster spawns in the session.</summary>
        public IReadOnlyList<SessionMonsterStatsRow> Monsters { get; set; } =
            Array.Empty<SessionMonsterStatsRow>();

        /// <summary>Gets or sets statistics for the items used in the session.</summary>
        public IReadOnlyList<SessionItemStatsRow> Items { get; set; } =
            Array.Empty<SessionItemStatsRow>();

        /// <summary>Gets or sets the furniture poses measured for the session.</summary>
        public IReadOnlyList<SessionFurniturePoseRow> Furniture { get; set; } =
            Array.Empty<SessionFurniturePoseRow>();

        /// <summary>Gets or sets the optional room calibration summary.</summary>
        public SessionRoomCalibrationRow RoomCalibration { get; set; }
    }
}
