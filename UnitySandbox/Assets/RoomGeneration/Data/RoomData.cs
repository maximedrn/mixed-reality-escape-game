using System;
using UnityEngine;

namespace RoomGeneration
{
    public sealed class RoomData
    {
        public string Name;
        public RoomSurfaceData Floor;
        public RoomSurfaceData Ceiling;
        public WallData[] Walls = Array.Empty<WallData>();
        public OpeningData[] Openings = Array.Empty<OpeningData>();
        public FurnitureData[] Furniture = Array.Empty<FurnitureData>();
    }

    public sealed class RoomSurfaceData
    {
        public Vector3[] Contour = Array.Empty<Vector3>();
        public string[] Labels = Array.Empty<string>();
    }

    public sealed class WallData
    {
        public Vector3 Start;
        public Vector3 End;
        public float Height;
        public string[] Labels = Array.Empty<string>();
    }

    public enum OpeningKind { Door, Window }

    public sealed class OpeningData
    {
        public OpeningKind Kind;
        public int WallIndex;
        public float Offset;
        public float Bottom;
        public float Width;
        public float Height;
        public string[] Labels = Array.Empty<string>();
    }

    public sealed class FurnitureData
    {
        public Vector3 Center;
        public Vector3 RotationDegrees;
        public Vector3 Size;
        public string[] Labels = Array.Empty<string>();
    }
}
