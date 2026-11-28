using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace RoomGeneration.Tests
{
    public sealed class RoomSandboxTests
    {
        private const string ScenePath = "Assets/Scenes/SampleScene.unity";
        private Scene scene;
        private Keyboard keyboard;

        [UnityTest]
        public IEnumerator SampleSceneBootstrapsSettlesAndSwitchesRoomsAndFixture()
        {
            keyboard = InputSystem.AddDevice<Keyboard>();
            yield return SceneManager.LoadSceneAsync(ScenePath, LoadSceneMode.Additive);
            scene = SceneManager.GetSceneByPath(ScenePath);

            GameObject[] sandboxes = System.Array.FindAll(scene.GetRootGameObjects(), root => root.name == "Environment Sandbox");
            Assert.That(sandboxes, Has.Length.EqualTo(1));
            GameObject sandbox = sandboxes[0];
            Transform player = sandbox.transform.Find("Sandbox Player");
            var controller = player.GetComponent<CharacterController>();
            Assert.That(player.GetComponentInChildren<Camera>(), Is.Not.Null);
            Transform inputDebug = sandbox.transform.Find("RoomInputDebug");
            Assert.That(inputDebug.Find("Floor").GetComponent<LineRenderer>().positionCount, Is.EqualTo(4));
            Assert.That(sandbox.transform.Find("GeneratedEnvironment").childCount, Is.Zero);
            Assert.That(sandbox.transform.Find("SandboxPhysics").GetComponentsInChildren<BoxCollider>().Length,
                Is.EqualTo(3));

            float timeout = Time.realtimeSinceStartup + 3;
            while (!controller.isGrounded && Time.realtimeSinceStartup < timeout) yield return null;
            Assert.That(controller.isGrounded, Is.True);

            yield return Press(Key.F2);
            Assert.That(sandbox.transform.Find("RoomInputDebug/Floor").GetComponent<LineRenderer>().positionCount,
                Is.EqualTo(6));
            yield return Press(Key.F3);
            Transform generated = sandbox.transform.Find("GeneratedEnvironment");
            Assert.That(generated.childCount, Is.EqualTo(2));
            Assert.That(generated.Find("TestCrate").GetComponent<BoxCollider>(), Is.Not.Null);
            yield return Press(Key.F3);
            Assert.That(sandbox.transform.Find("GeneratedEnvironment").childCount, Is.Zero);
        }

        [UnityTearDown]
        public IEnumerator TearDown()
        {
            if (keyboard != null && keyboard.added) InputSystem.RemoveDevice(keyboard);
            Scene loaded = scene.IsValid() ? scene : SceneManager.GetSceneByPath(ScenePath);
            if (loaded.IsValid() && loaded.isLoaded) yield return SceneManager.UnloadSceneAsync(loaded);
        }

        private IEnumerator Press(Key key)
        {
            InputSystem.QueueStateEvent(keyboard, new KeyboardState(key));
            yield return null;
            yield return null;
            InputSystem.QueueStateEvent(keyboard, new KeyboardState());
            yield return null;
            yield return null;
        }
    }
}
