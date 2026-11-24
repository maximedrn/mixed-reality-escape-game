namespace Project.Persistence
{
    using System.Collections.Generic;
    using SQLite;

    /// <summary>Contains the typed configuration for one catalog version.</summary>
    public sealed class GameCatalog
    {
        /// <summary>Initializes a new instance of the <see cref="GameCatalog"/> class.</summary>
        /// <param name="connection">The connection reading the catalog snapshot.</param>
        /// <param name="version">The requested catalog version.</param>
        internal GameCatalog(
            SQLiteConnection connection,
            ContentVersionRow version
        )
        {
            this.Version = version;
            this.Publication = connection.Find<PublishedContentVersionRow>(
                version.Id
            );
            this.AssetRefs = ReadVersionedRows<AssetRefRow>(
                connection,
                version.Id
            );
            this.Difficulties = connection
                .Table<DifficultyRow>()
                .Where(row => row.ContentVersionId == version.Id)
                .OrderBy(row => row.DisplayOrder)
                .ToList();
            this.InteractionProfiles = ReadVersionedRows<InteractionProfileRow>(
                connection,
                version.Id
            );
            this.InteractionFeedbackSettings =
                ReadVersionedRows<InteractionFeedbackSettingRow>(
                    connection,
                    version.Id
                );
            this.PhysicsProfiles = ReadVersionedRows<PhysicsProfileRow>(
                connection,
                version.Id
            );
            this.Rooms = ReadVersionedRows<RoomRow>(connection, version.Id);
            this.RoomCalibrationSettings =
                ReadVersionedRows<RoomCalibrationSettingRow>(
                    connection,
                    version.Id
                );
            this.RoomAnchors = ReadVersionedRows<RoomAnchorRow>(
                connection,
                version.Id
            );
            this.RoomDecorations = ReadVersionedRows<RoomDecorationRow>(
                connection,
                version.Id
            );
            this.RoomLights = ReadVersionedRows<RoomLightRow>(
                connection,
                version.Id
            );
            this.Furniture = ReadVersionedRows<FurnitureRow>(
                connection,
                version.Id
            );
            this.QrMarkers = ReadVersionedRows<QrMarkerRow>(
                connection,
                version.Id
            );
            this.RankedLayouts = ReadVersionedRows<RankedLayoutRow>(
                connection,
                version.Id
            );
            this.RankedLayoutFurniture =
                ReadVersionedRows<RankedLayoutFurnitureRow>(
                    connection,
                    version.Id
                );
            this.ItemCapabilityKinds = connection
                .Table<ItemCapabilityKindRow>()
                .OrderBy(row => row.Id)
                .ToList();
            this.InteractionKinds = connection
                .Table<InteractionKindRow>()
                .OrderBy(row => row.Id)
                .ToList();
            this.ImpactEffectKinds = connection
                .Table<ImpactEffectKindRow>()
                .OrderBy(row => row.Id)
                .ToList();
            this.Items = ReadVersionedRows<ItemRow>(connection, version.Id);
            this.ItemCapabilities = ReadVersionedRows<ItemCapabilityRow>(
                connection,
                version.Id
            );
            this.ItemImpactRules = ReadVersionedRows<ItemImpactRuleRow>(
                connection,
                version.Id
            );
            this.ItemInteractionPoints =
                ReadVersionedRows<ItemInteractionPointRow>(
                    connection,
                    version.Id
                );
            this.ItemFreeSettings = ReadVersionedRows<ItemFreeSettingRow>(
                connection,
                version.Id
            );
            this.ItemRotateSettings = ReadVersionedRows<ItemRotateSettingRow>(
                connection,
                version.Id
            );
            this.ItemSlideSettings = ReadVersionedRows<ItemSlideSettingRow>(
                connection,
                version.Id
            );
            this.ItemPressSettings = ReadVersionedRows<ItemPressSettingRow>(
                connection,
                version.Id
            );
            this.ItemLightSettings = ReadVersionedRows<ItemLightSettingRow>(
                connection,
                version.Id
            );
            this.Scenarios = ReadVersionedRows<ScenarioRow>(
                connection,
                version.Id
            );
            this.Rulesets = ReadVersionedRows<RulesetRow>(
                connection,
                version.Id
            );
            this.RulesetRoomLights = ReadVersionedRows<RulesetRoomLightRow>(
                connection,
                version.Id
            );
            this.ScenarioItems = ReadVersionedRows<ScenarioItemRow>(
                connection,
                version.Id
            );
            this.RulesetItems = ReadVersionedRows<RulesetItemRow>(
                connection,
                version.Id
            );
            this.Leaderboards = ReadVersionedRows<LeaderboardRow>(
                connection,
                version.Id
            );
            this.Puzzles = ReadVersionedRows<PuzzleRow>(connection, version.Id);
            this.PuzzleVariants = ReadVersionedRows<PuzzleVariantRow>(
                connection,
                version.Id
            );
            this.RulesetPuzzles = ReadVersionedRows<RulesetPuzzleRow>(
                connection,
                version.Id
            );
            this.RulesetPuzzlePrerequisites =
                ReadVersionedRows<RulesetPuzzlePrerequisiteRow>(
                    connection,
                    version.Id
                );
            this.PuzzleSteps = ReadVersionedRows<PuzzleStepRow>(
                connection,
                version.Id
            );
            this.PuzzleHints = ReadVersionedRows<PuzzleHintRow>(
                connection,
                version.Id
            );
            this.PuzzleStepConditions =
                ReadVersionedRows<PuzzleStepConditionRow>(
                    connection,
                    version.Id
                );
            this.PuzzleItemEventConditions =
                ReadVersionedRows<PuzzleItemEventConditionRow>(
                    connection,
                    version.Id
                );
            this.PuzzleRotationConditions =
                ReadVersionedRows<PuzzleRotationConditionRow>(
                    connection,
                    version.Id
                );
            this.PuzzleAssemblyConditions =
                ReadVersionedRows<PuzzleAssemblyConditionRow>(
                    connection,
                    version.Id
                );
            this.PuzzleCodeConditions =
                ReadVersionedRows<PuzzleCodeConditionRow>(
                    connection,
                    version.Id
                );
            this.PuzzlePullConditions =
                ReadVersionedRows<PuzzlePullConditionRow>(
                    connection,
                    version.Id
                );
            this.PuzzleStepActions = ReadVersionedRows<PuzzleStepActionRow>(
                connection,
                version.Id
            );
            this.PuzzleItemActions = ReadVersionedRows<PuzzleItemActionRow>(
                connection,
                version.Id
            );
            this.PuzzleAudioActions = ReadVersionedRows<PuzzleAudioActionRow>(
                connection,
                version.Id
            );
            this.Monsters = ReadVersionedRows<MonsterRow>(
                connection,
                version.Id
            );
            this.MonsterProfiles = ReadVersionedRows<MonsterProfileRow>(
                connection,
                version.Id
            );
            this.MonsterNavigationSettings =
                ReadVersionedRows<MonsterNavigationSettingRow>(
                    connection,
                    version.Id
                );
            this.MonsterAbilityKinds = connection
                .Table<MonsterAbilityKindRow>()
                .OrderBy(row => row.Id)
                .ToList();
            this.MonsterProfileAbilities =
                ReadVersionedRows<MonsterProfileAbilityRow>(
                    connection,
                    version.Id
                );
            this.MonsterClips = ReadVersionedRows<MonsterClipRow>(
                connection,
                version.Id
            );
            this.MonsterAnimationBindings =
                ReadVersionedRows<MonsterAnimationBindingRow>(
                    connection,
                    version.Id
                );
            this.MonsterAudioBindings =
                ReadVersionedRows<MonsterAudioBindingRow>(
                    connection,
                    version.Id
                );
            this.RulesetMonsters = ReadVersionedRows<RulesetMonsterRow>(
                connection,
                version.Id
            );
        }

        /// <summary>Gets the catalog version and its label.</summary>
        public ContentVersionRow Version { get; }

        /// <summary>Gets publication details when the catalog has been published.</summary>
        public PublishedContentVersionRow Publication { get; }

        /// <summary>Gets the asset refs.</summary>
        public IReadOnlyList<AssetRefRow> AssetRefs { get; }

        /// <summary>Gets the difficulties.</summary>
        public IReadOnlyList<DifficultyRow> Difficulties { get; }

        /// <summary>Gets the interaction profiles.</summary>
        public IReadOnlyList<InteractionProfileRow> InteractionProfiles { get; }

        /// <summary>Gets the interaction feedback settings.</summary>
        public IReadOnlyList<InteractionFeedbackSettingRow> InteractionFeedbackSettings { get; }

        /// <summary>Gets the physics profiles.</summary>
        public IReadOnlyList<PhysicsProfileRow> PhysicsProfiles { get; }

        /// <summary>Gets the rooms.</summary>
        public IReadOnlyList<RoomRow> Rooms { get; }

        /// <summary>Gets the room calibration settings.</summary>
        public IReadOnlyList<RoomCalibrationSettingRow> RoomCalibrationSettings { get; }

        /// <summary>Gets the room anchors.</summary>
        public IReadOnlyList<RoomAnchorRow> RoomAnchors { get; }

        /// <summary>Gets the room decorations.</summary>
        public IReadOnlyList<RoomDecorationRow> RoomDecorations { get; }

        /// <summary>Gets the room lights.</summary>
        public IReadOnlyList<RoomLightRow> RoomLights { get; }

        /// <summary>Gets the furniture.</summary>
        public IReadOnlyList<FurnitureRow> Furniture { get; }

        /// <summary>Gets the qr markers.</summary>
        public IReadOnlyList<QrMarkerRow> QrMarkers { get; }

        /// <summary>Gets the ranked layouts.</summary>
        public IReadOnlyList<RankedLayoutRow> RankedLayouts { get; }

        /// <summary>Gets the ranked layout furniture.</summary>
        public IReadOnlyList<RankedLayoutFurnitureRow> RankedLayoutFurniture { get; }

        /// <summary>Gets the item capability kinds.</summary>
        public IReadOnlyList<ItemCapabilityKindRow> ItemCapabilityKinds { get; }

        /// <summary>Gets the interaction kinds.</summary>
        public IReadOnlyList<InteractionKindRow> InteractionKinds { get; }

        /// <summary>Gets the impact effect kinds.</summary>
        public IReadOnlyList<ImpactEffectKindRow> ImpactEffectKinds { get; }

        /// <summary>Gets the items.</summary>
        public IReadOnlyList<ItemRow> Items { get; }

        /// <summary>Gets the item capabilities.</summary>
        public IReadOnlyList<ItemCapabilityRow> ItemCapabilities { get; }

        /// <summary>Gets the item impact rules.</summary>
        public IReadOnlyList<ItemImpactRuleRow> ItemImpactRules { get; }

        /// <summary>Gets the item interaction points.</summary>
        public IReadOnlyList<ItemInteractionPointRow> ItemInteractionPoints { get; }

        /// <summary>Gets the item free settings.</summary>
        public IReadOnlyList<ItemFreeSettingRow> ItemFreeSettings { get; }

        /// <summary>Gets the item rotate settings.</summary>
        public IReadOnlyList<ItemRotateSettingRow> ItemRotateSettings { get; }

        /// <summary>Gets the item slide settings.</summary>
        public IReadOnlyList<ItemSlideSettingRow> ItemSlideSettings { get; }

        /// <summary>Gets the item press settings.</summary>
        public IReadOnlyList<ItemPressSettingRow> ItemPressSettings { get; }

        /// <summary>Gets the item light settings.</summary>
        public IReadOnlyList<ItemLightSettingRow> ItemLightSettings { get; }

        /// <summary>Gets the scenarios.</summary>
        public IReadOnlyList<ScenarioRow> Scenarios { get; }

        /// <summary>Gets the rulesets.</summary>
        public IReadOnlyList<RulesetRow> Rulesets { get; }

        /// <summary>Gets the ruleset room lights.</summary>
        public IReadOnlyList<RulesetRoomLightRow> RulesetRoomLights { get; }

        /// <summary>Gets the scenario items.</summary>
        public IReadOnlyList<ScenarioItemRow> ScenarioItems { get; }

        /// <summary>Gets the ruleset items.</summary>
        public IReadOnlyList<RulesetItemRow> RulesetItems { get; }

        /// <summary>Gets the leaderboards.</summary>
        public IReadOnlyList<LeaderboardRow> Leaderboards { get; }

        /// <summary>Gets the puzzles.</summary>
        public IReadOnlyList<PuzzleRow> Puzzles { get; }

        /// <summary>Gets the puzzle variants.</summary>
        public IReadOnlyList<PuzzleVariantRow> PuzzleVariants { get; }

        /// <summary>Gets the ruleset puzzles.</summary>
        public IReadOnlyList<RulesetPuzzleRow> RulesetPuzzles { get; }

        /// <summary>Gets the ruleset puzzle prerequisites.</summary>
        public IReadOnlyList<RulesetPuzzlePrerequisiteRow> RulesetPuzzlePrerequisites { get; }

        /// <summary>Gets the puzzle steps.</summary>
        public IReadOnlyList<PuzzleStepRow> PuzzleSteps { get; }

        /// <summary>Gets the puzzle hints.</summary>
        public IReadOnlyList<PuzzleHintRow> PuzzleHints { get; }

        /// <summary>Gets the puzzle step conditions.</summary>
        public IReadOnlyList<PuzzleStepConditionRow> PuzzleStepConditions { get; }

        /// <summary>Gets the puzzle item event conditions.</summary>
        public IReadOnlyList<PuzzleItemEventConditionRow> PuzzleItemEventConditions { get; }

        /// <summary>Gets the puzzle rotation conditions.</summary>
        public IReadOnlyList<PuzzleRotationConditionRow> PuzzleRotationConditions { get; }

        /// <summary>Gets the puzzle assembly conditions.</summary>
        public IReadOnlyList<PuzzleAssemblyConditionRow> PuzzleAssemblyConditions { get; }

        /// <summary>Gets the puzzle code conditions.</summary>
        public IReadOnlyList<PuzzleCodeConditionRow> PuzzleCodeConditions { get; }

        /// <summary>Gets the puzzle pull conditions.</summary>
        public IReadOnlyList<PuzzlePullConditionRow> PuzzlePullConditions { get; }

        /// <summary>Gets the puzzle step actions.</summary>
        public IReadOnlyList<PuzzleStepActionRow> PuzzleStepActions { get; }

        /// <summary>Gets the puzzle item actions.</summary>
        public IReadOnlyList<PuzzleItemActionRow> PuzzleItemActions { get; }

        /// <summary>Gets the puzzle audio actions.</summary>
        public IReadOnlyList<PuzzleAudioActionRow> PuzzleAudioActions { get; }

        /// <summary>Gets the monsters.</summary>
        public IReadOnlyList<MonsterRow> Monsters { get; }

        /// <summary>Gets the monster profiles.</summary>
        public IReadOnlyList<MonsterProfileRow> MonsterProfiles { get; }

        /// <summary>Gets the monster navigation settings.</summary>
        public IReadOnlyList<MonsterNavigationSettingRow> MonsterNavigationSettings { get; }

        /// <summary>Gets the monster ability kinds.</summary>
        public IReadOnlyList<MonsterAbilityKindRow> MonsterAbilityKinds { get; }

        /// <summary>Gets the monster profile abilities.</summary>
        public IReadOnlyList<MonsterProfileAbilityRow> MonsterProfileAbilities { get; }

        /// <summary>Gets the monster clips.</summary>
        public IReadOnlyList<MonsterClipRow> MonsterClips { get; }

        /// <summary>Gets the monster animation bindings.</summary>
        public IReadOnlyList<MonsterAnimationBindingRow> MonsterAnimationBindings { get; }

        /// <summary>Gets the monster audio bindings.</summary>
        public IReadOnlyList<MonsterAudioBindingRow> MonsterAudioBindings { get; }

        /// <summary>Gets the ruleset monsters.</summary>
        public IReadOnlyList<RulesetMonsterRow> RulesetMonsters { get; }

        /// <summary>Reads only records belonging to the requested version.</summary>
        /// <typeparam name="T">The mapped row type.</typeparam>
        /// <param name="connection">The connection reading the catalog snapshot.</param>
        /// <param name="versionId">The requested catalog version.</param>
        /// <returns>The versioned records for this table.</returns>
        private static IReadOnlyList<T> ReadVersionedRows<T>(
            SQLiteConnection connection,
            string versionId
        )
            where T : VersionedRow, new()
        {
            return connection
                .Table<T>()
                .Where(row => row.ContentVersionId == versionId)
                .ToList();
        }
    }
}
