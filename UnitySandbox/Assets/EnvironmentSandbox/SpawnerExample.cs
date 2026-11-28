using RoomGeneration;
using UnityEngine;

namespace EnvironmentSandbox
{
    internal static class SpawnerExample
    {
        public const string MaterialId = "EnvironmentSandbox/SandboxUnlit";

        public static EnvironmentData Create(float floorY) => new()
        {
            Meshes = new[]
            {
                new GeneratedMeshData
                {
                    Name = "Manual Test Panel",
                    Vertices = new[] { Vector3.zero, Vector3.up * 0.85f, new Vector3(1.1f, 0.85f, 0), Vector3.right * 1.1f },
                    Triangles = new[] { 0, 1, 2, 0, 2, 3 },
                    Normals = new[] { Vector3.back, Vector3.back, Vector3.back, Vector3.back },
                    UVs = new[] { Vector2.zero, Vector2.up, Vector2.one, Vector2.right },
                    MaterialId = MaterialId,
                    Transform = new ObjectTransform(new Vector3(-1.9f, floorY + 0.1f, 0.1f),
                        Quaternion.Euler(0, -15, 0), Vector3.one),
                    Collision = MeshCollision.StaticMesh
                }
            },
            Instances = new[]
            {
                new AssetInstanceData
                {
                    AssetId = "EnvironmentSandbox/TestCrate",
                    Transform = new ObjectTransform(new Vector3(1.2f, floorY + 0.325f, -0.55f),
                        Quaternion.Euler(0, 25, 0), Vector3.one * 0.65f)
                }
            }
        };
    }
}
