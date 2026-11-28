using System;
using RoomGeneration;
using UnityEngine;
using UnityEngine.Rendering;

namespace EnvironmentSandbox
{
    internal static class RoomDebugView
    {
        private static readonly int BaseColor = Shader.PropertyToID("_BaseColor");
        private static readonly Color FloorColor = new(0.23f, 0.94f, 0.76f);
        private static readonly Color CeilingColor = new(0.55f, 0.68f, 1f);
        private static readonly Color WallColor = new(0.62f, 0.70f, 0.78f);
        private static readonly Color DoorColor = new(1f, 0.73f, 0.25f);
        private static readonly Color WindowColor = new(0.24f, 0.76f, 1f);
        private static readonly Color FurnitureColor = new(0.92f, 0.43f, 0.94f);

        public static GameObject Draw(RoomData room, Transform parent, Material material)
        {
            var root = new GameObject("RoomInputDebug");
            root.transform.SetParent(parent, false);
            var lines = new LineDrawing(root.transform, material);
            lines.Add("Floor", FloorColor, 0.04f, true, room.Floor.Contour);
            lines.Add("Ceiling", CeilingColor, 0.04f, true, room.Ceiling.Contour);

            for (int i = 0; i < room.Walls.Length; i++)
            {
                WallData wall = room.Walls[i];
                Rectangle(lines, $"Wall {i}", wall.Start, new Vector3(wall.End.x - wall.Start.x, 0, wall.End.z - wall.Start.z),
                    wall.Height, WallColor, 0.018f);
            }

            for (int i = 0; i < room.Openings.Length; i++)
            {
                OpeningData opening = room.Openings[i];
                WallData wall = room.Walls[opening.WallIndex];
                Vector3 along = new Vector3(wall.End.x - wall.Start.x, 0, wall.End.z - wall.Start.z).normalized;
                Vector3 bottom = wall.Start + along * opening.Offset + Vector3.up * opening.Bottom;
                Color color = opening.Kind == OpeningKind.Door ? DoorColor : WindowColor;
                Rectangle(lines, $"{opening.Kind} {i}", bottom, along * opening.Width, opening.Height, color, 0.055f);
            }

            for (int i = 0; i < room.Furniture.Length; i++) DrawFurniture(lines, room.Furniture[i], i);
            return root;
        }

        private static void Rectangle(LineDrawing lines, string name, Vector3 start, Vector3 across, float height,
            Color color, float width)
        {
            Vector3 up = Vector3.up * height;
            lines.Add(name, color, width, true, start, start + across, start + across + up, start + up);
        }

        private static void DrawFurniture(LineDrawing lines, FurnitureData item, int index)
        {
            Vector3 half = item.Size * 0.5f;
            Quaternion rotation = Quaternion.Euler(item.RotationDegrees);
            var bottom = new[]
            {
                new Vector3(-half.x, -half.y, -half.z), new Vector3(half.x, -half.y, -half.z),
                new Vector3(half.x, -half.y, half.z), new Vector3(-half.x, -half.y, half.z)
            };
            Vector3 up = rotation * (Vector3.up * item.Size.y);
            for (int i = 0; i < bottom.Length; i++) bottom[i] = item.Center + rotation * bottom[i];
            Vector3[] top = Array.ConvertAll(bottom, point => point + up);
            string name = $"Furniture {index}";
            lines.Add(name + " bottom", FurnitureColor, 0.025f, true, bottom);
            lines.Add(name + " top", FurnitureColor, 0.025f, true, top);
            for (int i = 0; i < bottom.Length; i++)
                lines.Add(name + $" edge {i}", FurnitureColor, 0.025f, false, bottom[i], top[i]);
        }

        private sealed class LineDrawing
        {
            private readonly Transform parent;
            private readonly Material material;
            private readonly MaterialPropertyBlock properties = new();

            public LineDrawing(Transform parent, Material material)
            {
                this.parent = parent;
                this.material = material;
            }

            public void Add(string name, Color color, float width, bool closed, params Vector3[] points)
            {
                var line = new GameObject(name).AddComponent<LineRenderer>();
                line.transform.SetParent(parent, false);
                line.useWorldSpace = false;
                line.loop = closed;
                line.positionCount = points.Length;
                line.SetPositions(points);
                line.startWidth = width;
                line.endWidth = width;
                line.shadowCastingMode = ShadowCastingMode.Off;
                line.receiveShadows = false;
                line.sharedMaterial = material;
                properties.SetColor(BaseColor, color);
                line.SetPropertyBlock(properties);
            }
        }
    }
}
