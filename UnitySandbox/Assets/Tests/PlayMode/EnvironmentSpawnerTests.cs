using System;
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Object = UnityEngine.Object;

namespace RoomGeneration.Tests
{
    public sealed class EnvironmentSpawnerTests
    {
        private GameObject owner;
        private EnvironmentSpawner spawner;

        [SetUp]
        public void SetUp()
        {
            owner = new GameObject("Spawner Test");
            spawner = new EnvironmentSpawner(owner.transform);
        }

        [TearDown]
        public void TearDown()
        {
            spawner.Clear();
            Object.Destroy(owner);
        }

        [UnityTest]
        public IEnumerator SpawnsMeshAndResourcesPrefabAndReleasesOldMeshes()
        {
            var data = CreateOutput();
            GameObject first = spawner.Spawn(data);
            Assert.That(first.name, Is.EqualTo("GeneratedEnvironment"));
            Assert.That(first.transform.parent, Is.EqualTo(owner.transform));
            Assert.That(first.transform.childCount, Is.EqualTo(2));

            Transform surface = first.transform.GetChild(0);
            Mesh mesh = surface.GetComponent<MeshFilter>().sharedMesh;
            Assert.That(mesh.vertices, Is.EqualTo(data.Meshes[0].Vertices));
            Assert.That(mesh.triangles, Is.EqualTo(data.Meshes[0].Triangles));
            Assert.That(mesh.normals, Is.EqualTo(data.Meshes[0].Normals));
            Assert.That(mesh.uv, Is.EqualTo(data.Meshes[0].UVs));
            Assert.That(surface.localPosition, Is.EqualTo(new Vector3(1, 2, 3)));
            Assert.That(surface.GetComponent<MeshCollider>().sharedMesh, Is.EqualTo(mesh));
            Assert.That(surface.GetComponent<MeshRenderer>().sharedMaterial,
                Is.SameAs(Resources.Load<Material>("EnvironmentSandbox/SandboxUnlit")));

            Transform prefab = first.transform.GetChild(1);
            Assert.That(prefab.localPosition, Is.EqualTo(new Vector3(-1, 0.5f, 1)));
            Assert.That(Quaternion.Angle(prefab.localRotation, Quaternion.Euler(0, 30, 0)), Is.LessThan(0.01f));
            Assert.That(prefab.localScale, Is.EqualTo(Vector3.one * 0.5f));
            Assert.That(prefab.GetComponent<BoxCollider>(), Is.Not.Null);

            GameObject second = spawner.Spawn(data);
            Assert.That(owner.transform.childCount, Is.EqualTo(1));
            Assert.That(first.activeSelf, Is.False);
            yield return null;
            Assert.That(first == null, Is.True);
            Assert.That(mesh == null, Is.True);

            Mesh secondMesh = second.GetComponentInChildren<MeshFilter>().sharedMesh;
            spawner.Clear();
            Assert.That(owner.transform.childCount, Is.Zero);
            yield return null;
            Assert.That(second == null, Is.True);
            Assert.That(secondMesh == null, Is.True);
            Assert.That(spawner.Spawn(new EnvironmentData()).transform.childCount, Is.Zero);
        }

        [Test]
        public void FailedSpawnKeepsPreviousEnvironment()
        {
            GameObject first = spawner.Spawn(CreateOutput());
            var invalid = CreateOutput();
            invalid.Instances[0].AssetId = "EnvironmentSandbox/MissingAsset";
            Assert.That(Assert.Throws<InvalidOperationException>(() => spawner.Spawn(invalid)).Message,
                Does.Contain("MissingAsset"));
            Assert.That(first.activeInHierarchy, Is.True);
            Assert.That(owner.transform.childCount, Is.EqualTo(1));
        }

        private static EnvironmentData CreateOutput() => new()
        {
            Meshes = new[]
            {
                new GeneratedMeshData
                {
                    Name = "Test Mesh",
                    Vertices = new[] { Vector3.zero, Vector3.forward, Vector3.right },
                    Triangles = new[] { 0, 1, 2 },
                    Normals = new[] { Vector3.up, Vector3.up, Vector3.up },
                    UVs = new[] { Vector2.zero, Vector2.up, Vector2.right },
                    MaterialId = "EnvironmentSandbox/SandboxUnlit",
                    Transform = new ObjectTransform(new Vector3(1, 2, 3), Quaternion.identity, Vector3.one),
                    Collision = MeshCollision.StaticMesh
                }
            },
            Instances = new[]
            {
                new AssetInstanceData
                {
                    AssetId = "EnvironmentSandbox/TestCrate",
                    Transform = new ObjectTransform(new Vector3(-1, 0.5f, 1), Quaternion.Euler(0, 30, 0), Vector3.one * 0.5f)
                }
            }
        };
    }
}
