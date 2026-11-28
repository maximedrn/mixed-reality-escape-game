using System;
using UnityEngine;

namespace RoomGeneration
{
    public sealed class EnvironmentData
    {
        public GeneratedMeshData[] Meshes = Array.Empty<GeneratedMeshData>();
        public AssetInstanceData[] Instances = Array.Empty<AssetInstanceData>();
    }

    public sealed class GeneratedMeshData
    {
        public string Name;
        public Vector3[] Vertices = Array.Empty<Vector3>();
        public int[] Triangles = Array.Empty<int>();
        public Vector3[] Normals = Array.Empty<Vector3>();
        public Vector2[] UVs = Array.Empty<Vector2>();
        public string MaterialId;
        public ObjectTransform Transform = ObjectTransform.Identity;
        public MeshCollision Collision;
    }

    public enum MeshCollision { None, StaticMesh, ConvexMesh }

    public sealed class AssetInstanceData
    {
        public string AssetId;
        public ObjectTransform Transform = ObjectTransform.Identity;
    }

    public readonly struct ObjectTransform
    {
        public static ObjectTransform Identity => new(Vector3.zero, Quaternion.identity, Vector3.one);

        public readonly Vector3 Position;
        public readonly Quaternion Rotation;
        public readonly Vector3 Scale;

        public ObjectTransform(Vector3 position, Quaternion rotation, Vector3 scale)
        {
            Position = position;
            Rotation = rotation;
            Scale = scale;
        }
    }
}
