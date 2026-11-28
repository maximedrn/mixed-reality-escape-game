using System;
using System.IO;
using RoomGeneration;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;

namespace EnvironmentSandbox
{
    internal sealed class RoomSandbox : MonoBehaviour
    {
        private const string ScenePath = "Assets/Scenes/SampleScene.unity";
        private EnvironmentSpawner spawner;
        private readonly ProceduralGenerator generator = new();
        private SandboxFps player;
        private Material material;
        private RoomData room;
        private GameObject debugRoot;
        private GameObject physicsRoot;
        private bool showSpawnerExample;
        private string loadError;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void Bootstrap()
        {
            // Remove a previous subscription when entering Play Mode without a domain reload.
            SceneManager.sceneLoaded -= OnSceneLoaded;
            SceneManager.sceneLoaded += OnSceneLoaded;
            for (int i = 0; i < SceneManager.sceneCount; i++) Install(SceneManager.GetSceneAt(i));
        }

        private static void OnSceneLoaded(Scene scene, LoadSceneMode mode) => Install(scene);

        private static void Install(Scene scene)
        {
            if (!scene.isLoaded || scene.path != ScenePath) return;
            foreach (GameObject root in scene.GetRootGameObjects())
                if (root.TryGetComponent(out RoomSandbox _)) return;

            var sandbox = new GameObject("Environment Sandbox");
            SceneManager.MoveGameObjectToScene(sandbox, scene);
            sandbox.AddComponent<RoomSandbox>();
        }

        private void Awake()
        {
            material = Resources.Load<Material>(SpawnerExample.MaterialId);
            if (!material)
            {
                loadError = $"Missing sandbox material '{SpawnerExample.MaterialId}'.";
                Debug.LogError(loadError, this);
                return;
            }

            var playerObject = new GameObject("Sandbox Player");
            SceneManager.MoveGameObjectToScene(playerObject, gameObject.scene);
            playerObject.transform.SetParent(transform, false);
            player = playerObject.AddComponent<SandboxFps>();
            player.Configure(FindCamera());
            spawner = new EnvironmentSpawner(transform);
            LoadRoom("rectangle.json");
        }

        private Camera FindCamera()
        {
            foreach (GameObject root in gameObject.scene.GetRootGameObjects())
                if (root.CompareTag("MainCamera") && root.TryGetComponent(out Camera camera)) return camera;

            var fallback = new GameObject("Sandbox Camera");
            SceneManager.MoveGameObjectToScene(fallback, gameObject.scene);
            fallback.AddComponent<AudioListener>();
            return fallback.AddComponent<Camera>();
        }

        private void Update()
        {
            Keyboard keyboard = Keyboard.current;
            if (keyboard == null || spawner == null) return;
            if (keyboard.f1Key.wasPressedThisFrame) LoadRoom("rectangle.json");
            else if (keyboard.f2Key.wasPressedThisFrame) LoadRoom("polygon.json");
            if (room != null && keyboard.f3Key.wasPressedThisFrame)
            {
                bool show = !showSpawnerExample;
                Spawn(room, show);
                showSpawnerExample = show;
            }
        }

        private void LoadRoom(string fileName)
        {
            RoomData nextRoom;
            try
            {
                string path = Path.Combine(Application.streamingAssetsPath, "Rooms", fileName);
                nextRoom = RoomLoader.Load(path);
            }
            catch (Exception error) when (error is IOException or FormatException or RoomValidationException)
            {
                loadError = error.Message;
                Debug.LogError(loadError, this);
                return;
            }

            Spawn(nextRoom, showSpawnerExample);
            Remove(debugRoot);
            Remove(physicsRoot);
            debugRoot = RoomDebugView.Draw(nextRoom, transform, material);
            physicsRoot = SandboxPhysics.Create(nextRoom, transform, material);
            room = nextRoom;
            loadError = null;
            player.ResetPose(new Vector3(0, room.Floor.Contour[0].y + 0.08f, 1.3f), 180f);
        }

        private void Spawn(RoomData data, bool showExample)
        {
            EnvironmentData output = showExample
                ? SpawnerExample.Create(data.Floor.Contour[0].y)
                : generator.Generate(data);
            spawner.Spawn(output);
        }

        private static void Remove(GameObject root)
        {
            if (!root) return;
            root.SetActive(false);
            root.transform.SetParent(null, false);
            Destroy(root);
        }

        private void OnGUI()
        {
            string roomName = room?.Name ?? "Room unavailable";
            string fixture = showSpawnerExample ? "on" : "off";
            GUILayout.BeginArea(new Rect(14, 14, Screen.width - 28, 155));
            GUILayout.Label($"{roomName}    |    Spawner demo: {fixture}");
            GUILayout.Label("Click Game view to look   •   WASD / ZQSD / arrows to move   •   Esc to release");
            GUILayout.Label("F1 rectangle   •   F2 concave room   •   F3 spawner demo");
            if (!string.IsNullOrEmpty(loadError)) GUILayout.Label(loadError);
            GUILayout.EndArea();
        }

        private void OnDestroy() => spawner?.Clear();
    }
}
