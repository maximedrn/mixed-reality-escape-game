using System;
using UnityEngine;

namespace RoomGeneration
{
    public sealed class RoomValidationException : Exception
    {
        public RoomValidationException(string message, Exception inner = null) : base(message, inner) { }
    }

    public static class RoomValidator
    {
        private const float Tolerance = 0.0001f;

        public static void Validate(RoomData room)
        {
            if (room == null) throw Invalid("room", "is required");
            if (string.IsNullOrWhiteSpace(room.Name)) throw Invalid("name", "is required");
            ValidateSurface(room.Floor, "floor");
            ValidateSurface(room.Ceiling, "ceiling");
            if (room.Ceiling.Contour[0].y - room.Floor.Contour[0].y <= Tolerance)
                throw Invalid("ceiling.contour", "must be above the floor");

            if (room.Walls == null) throw Invalid("walls", "must be an array");
            for (int i = 0; i < room.Walls.Length; i++)
            {
                WallData wall = room.Walls[i];
                string field = $"walls[{i}]";
                if (wall == null) throw Invalid(field, "must be a wall");
                RequireFinite(wall.Start, field + ".start");
                RequireFinite(wall.End, field + ".end");
                if (Mathf.Abs(wall.Start.y - wall.End.y) > Tolerance || WallLength(wall) <= Tolerance)
                    throw Invalid(field, "must have a nonzero horizontal baseline");
                RequirePositive(wall.Height, field + ".height");
            }

            if (room.Openings == null) throw Invalid("openings", "must be an array");
            for (int i = 0; i < room.Openings.Length; i++)
            {
                OpeningData opening = room.Openings[i];
                string field = $"openings[{i}]";
                if (opening == null) throw Invalid(field, "must be an opening");
                if (opening.Kind != OpeningKind.Door && opening.Kind != OpeningKind.Window)
                    throw Invalid(field + ".kind", "must be a door or window");
                if (opening.WallIndex < 0 || opening.WallIndex >= room.Walls.Length)
                    throw Invalid(field + ".wallIndex", "must reference an existing wall");
                RequirePositive(opening.Width, field + ".width");
                RequirePositive(opening.Height, field + ".height");
                WallData wall = room.Walls[opening.WallIndex];
                if (!float.IsFinite(opening.Offset) || !float.IsFinite(opening.Bottom) ||
                    opening.Offset < 0 || opening.Bottom < 0 ||
                    (double)opening.Offset + opening.Width > WallLength(wall) + Tolerance ||
                    (double)opening.Bottom + opening.Height > wall.Height + Tolerance)
                    throw Invalid(field, "must fit within its wall");
            }

            if (room.Furniture == null) throw Invalid("furniture", "must be an array");
            for (int i = 0; i < room.Furniture.Length; i++)
            {
                FurnitureData item = room.Furniture[i];
                string field = $"furniture[{i}]";
                if (item == null) throw Invalid(field, "must be a furniture volume");
                RequireFinite(item.Center, field + ".center");
                RequireFinite(item.RotationDegrees, field + ".rotationDegrees");
                RequirePositive(item.Size.x, field + ".size.x");
                RequirePositive(item.Size.y, field + ".size.y");
                RequirePositive(item.Size.z, field + ".size.z");
            }
        }

        private static void ValidateSurface(RoomSurfaceData surface, string field)
        {
            Vector3[] points = surface?.Contour;
            field += ".contour";
            if (points == null || points.Length < 3)
                throw Invalid(field, "must contain at least three vertices");

            for (int i = 0; i < points.Length; i++)
            {
                RequireFinite(points[i], $"{field}[{i}]");
                if (Mathf.Abs(points[i].y - points[0].y) > Tolerance)
                    throw Invalid($"{field}[{i}]", "must lie in the horizontal plane of the contour");
            }

            double twiceArea = 0;
            for (int i = 0; i < points.Length; i++)
            {
                Vector3 a = points[i];
                Vector3 b = points[(i + 1) % points.Length];
                Vector3 c = points[(i + 2) % points.Length];
                if (Length(a, b) <= Tolerance)
                    throw Invalid(field, $"has a duplicate or too-close vertex at edge {i}");
                if (Side(a, b, c) == 0 && (OnSegment(a, b, c) || OnSegment(b, c, a)))
                    throw Invalid(field, $"has overlapping adjacent edges at vertex {(i + 1) % points.Length}");

                for (int j = i + 2; j < points.Length; j++)
                {
                    if (i == 0 && j == points.Length - 1) continue;
                    if (Intersects(a, b, points[j], points[(j + 1) % points.Length]))
                        throw Invalid(field, $"has intersecting edges {i} and {j}");
                }

                twiceArea += Cross(points[0], a, b);
            }
            if (Math.Abs(twiceArea) <= 2.0 * Tolerance * Tolerance)
                throw Invalid(field, "must enclose a nonzero area");
        }

        private static bool Intersects(Vector3 a, Vector3 b, Vector3 c, Vector3 d)
        {
            int abc = Side(a, b, c);
            int abd = Side(a, b, d);
            int cda = Side(c, d, a);
            int cdb = Side(c, d, b);
            return (abc * abd < 0 && cda * cdb < 0) ||
                   (abc == 0 && OnSegment(a, b, c)) || (abd == 0 && OnSegment(a, b, d)) ||
                   (cda == 0 && OnSegment(c, d, a)) || (cdb == 0 && OnSegment(c, d, b));
        }

        private static int Side(Vector3 a, Vector3 b, Vector3 point)
        {
            double cross = Cross(a, b, point);
            return Math.Abs(cross) <= Tolerance * Length(a, b) ? 0 : Math.Sign(cross);
        }

        private static bool OnSegment(Vector3 a, Vector3 b, Vector3 point) =>
            point.x >= Mathf.Min(a.x, b.x) - Tolerance && point.x <= Mathf.Max(a.x, b.x) + Tolerance &&
            point.z >= Mathf.Min(a.z, b.z) - Tolerance && point.z <= Mathf.Max(a.z, b.z) + Tolerance;

        private static double Cross(Vector3 a, Vector3 b, Vector3 c) =>
            ((double)b.x - a.x) * ((double)c.z - a.z) - ((double)b.z - a.z) * ((double)c.x - a.x);

        private static double Length(Vector3 a, Vector3 b)
        {
            double dx = (double)b.x - a.x;
            double dz = (double)b.z - a.z;
            return Math.Sqrt(dx * dx + dz * dz);
        }

        private static double WallLength(WallData wall) => Length(wall.Start, wall.End);

        private static void RequireFinite(Vector3 value, string field)
        {
            if (!float.IsFinite(value.x) || !float.IsFinite(value.y) || !float.IsFinite(value.z))
                throw Invalid(field, "must contain finite coordinates");
        }

        private static void RequirePositive(float value, string field)
        {
            if (!float.IsFinite(value) || value <= 0) throw Invalid(field, "must be finite and positive");
        }

        private static RoomValidationException Invalid(string field, string reason) => new($"{field} {reason}.");
    }
}
