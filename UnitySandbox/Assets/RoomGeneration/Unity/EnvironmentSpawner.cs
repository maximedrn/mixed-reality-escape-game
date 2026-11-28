using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using Object = UnityEngine.Object;

namespace RoomGeneration
{
    // Call from Unity's main thread. The caller owns this spawner and calls Clear on teardown.
    public sealed class EnvironmentSpawner
    {
        public const string RootName = "GeneratedEnvironment";

        private readonly Transform parent;
        private GameObject root;
        private List<Mesh> meshes = new();

        public EnvironmentSpawner(Transform parent = null) => this.parent = parent;

        public GameObject Spawn(EnvironmentData environment)
        {
            if (environment == null) throw new ArgumentNullException(nameof(environment));
            if (environment.Meshes == null || environment.Instances == null)
                throw new ArgumentException("Mesh and instance arrays are required.", nameof(environment));

            var nextRoot = new GameObject(RootName);
            nextRoot.SetActive(false);
            nextRoot.transform.SetParent(parent, false);
            var nextMeshes = new List<Mesh>(environment.Meshes.Length);
            try
            {
                foreach (GeneratedMeshData data in environment.Meshes)
                    SpawnMesh(data, nextRoot.transform, nextMeshes);
                foreach (AssetInstanceData data in environment.Instances)
                    SpawnAsset(data, nextRoot.transform);
            }
            catch
            {
                Release(nextRoot, nextMeshes);
                throw;
            }

            Clear();
            root = nextRoot;
            meshes = nextMeshes;
            root.SetActive(true);
            return root;
        }

        public void Clear()
        {
            Release(root, meshes);
            root = null;
            meshes.Clear();
        }

        private static void SpawnMesh(GeneratedMeshData data, Transform parent, List<Mesh> ownedMeshes)
        {
            ValidateMesh(data);
            Material material = LoadResource<Material>(data.MaterialId);
            var mesh = new Mesh { name = data.Name };
            ownedMeshes.Add(mesh);
            if (data.Vertices.Length > ushort.MaxValue) mesh.indexFormat = IndexFormat.UInt32;
            mesh.vertices = data.Vertices;
            mesh.triangles = data.Triangles;
            if (data.Normals.Length == 0) mesh.RecalculateNormals();
            else mesh.normals = data.Normals;
            if (data.UVs.Length > 0) mesh.uv = data.UVs;
            mesh.RecalculateBounds();

            var instance = new GameObject(data.Name);
            ApplyTransform(instance.transform, parent, data.Transform);
            instance.AddComponent<MeshFilter>().sharedMesh = mesh;
            instance.AddComponent<MeshRenderer>().sharedMaterial = material;
            if (data.Collision != MeshCollision.None)
            {
                var collider = instance.AddComponent<MeshCollider>();
                collider.convex = data.Collision == MeshCollision.ConvexMesh;
                collider.sharedMesh = mesh;
            }
        }

        private static void SpawnAsset(AssetInstanceData data, Transform parent)
        {
            if (data == null) throw new ArgumentException("An asset instance is null.");
            ValidateTransform(data.Transform, data.AssetId);
            GameObject prefab = LoadResource<GameObject>(data.AssetId);
            GameObject instance = Object.Instantiate(prefab, parent, false);
            instance.name = prefab.name;
            ApplyTransform(instance.transform, parent, data.Transform);
        }

        private static T LoadResource<T>(string id) where T : Object
        {
            T resource = string.IsNullOrWhiteSpace(id) ? null : Resources.Load<T>(id);
            if (!resource) throw new InvalidOperationException($"Missing Resources {typeof(T).Name} '{id}'.");
            return resource;
        }

        private static void ApplyTransform(Transform target, Transform parent, ObjectTransform pose)
        {
            target.SetParent(parent, false);
            target.SetLocalPositionAndRotation(pose.Position, pose.Rotation);
            target.localScale = pose.Scale;
        }

        private static void ValidateMesh(GeneratedMeshData data)
        {
            if (data == null || string.IsNullOrWhiteSpace(data.Name))
                throw new ArgumentException("Each mesh needs a name.");
            int count = data.Vertices?.Length ?? 0;
            if (count < 3 || data.Triangles == null || data.Triangles.Length == 0 || data.Triangles.Length % 3 != 0)
                throw new ArgumentException($"Mesh '{data.Name}' requires vertices and triangle index triplets.");
            foreach (int index in data.Triangles)
                if (index < 0 || index >= count)
                    throw new ArgumentException($"Mesh '{data.Name}' has an out-of-range index {index}.");
            foreach (Vector3 vertex in data.Vertices)
                if (!IsFinite(vertex)) throw new ArgumentException($"Mesh '{data.Name}' has a non-finite vertex.");

            if (data.Normals == null || (data.Normals.Length != 0 && data.Normals.Length != count) ||
                data.UVs == null || (data.UVs.Length != 0 && data.UVs.Length != count))
                throw new ArgumentException($"Mesh '{data.Name}' needs zero or one normal and UV per vertex.");
            foreach (Vector3 normal in data.Normals)
                if (!IsFinite(normal)) throw new ArgumentException($"Mesh '{data.Name}' has a non-finite normal.");
            foreach (Vector2 uv in data.UVs)
                if (!float.IsFinite(uv.x) || !float.IsFinite(uv.y))
                    throw new ArgumentException($"Mesh '{data.Name}' has a non-finite UV.");
            if (data.Collision != MeshCollision.None && data.Collision != MeshCollision.StaticMesh &&
                data.Collision != MeshCollision.ConvexMesh)
                throw new ArgumentException($"Mesh '{data.Name}' has an unsupported collision mode.");
            ValidateTransform(data.Transform, data.Name);
        }

        private static void ValidateTransform(ObjectTransform pose, string name)
        {
            Quaternion rotation = pose.Rotation;
            float magnitudeSquared = Quaternion.Dot(rotation, rotation);
            if (!IsFinite(pose.Position) || !IsFinite(pose.Scale) ||
                pose.Scale.x == 0 || pose.Scale.y == 0 || pose.Scale.z == 0 ||
                !float.IsFinite(magnitudeSquared) || Mathf.Abs(magnitudeSquared - 1) > 0.001f)
                throw new ArgumentException($"'{name}' requires a finite transform, nonzero scale and unit rotation.");
        }

        private static bool IsFinite(Vector3 v) => float.IsFinite(v.x) && float.IsFinite(v.y) && float.IsFinite(v.z);

        private static void Release(GameObject previousRoot, List<Mesh> previousMeshes)
        {
            if (previousRoot)
            {
                previousRoot.SetActive(false);
                // Detach before delayed runtime destruction so only one root remains under the owner.
                previousRoot.transform.SetParent(null, false);
                previousRoot.name = RootName + " (retired)";
                Destroy(previousRoot);
            }
            foreach (Mesh mesh in previousMeshes) Destroy(mesh);
        }

        private static void Destroy(Object target)
        {
            if (Application.isPlaying) Object.Destroy(target);
            else Object.DestroyImmediate(target);
        }
    }
}
