using RoomGeneration;
using UnityEngine;
using UnityEngine.Rendering;

namespace EnvironmentSandbox
{
    internal static class SandboxPhysics
    {
        public static GameObject Create(RoomData room, Transform parent, Material material)
        {
            var root = new GameObject("SandboxPhysics");
            root.transform.SetParent(parent, false);

            // A flat test platform provides ground contact while the room itself is a wireframe.
            var bounds = new Bounds(room.Floor.Contour[0], Vector3.zero);
            foreach (Vector3 point in room.Floor.Contour) bounds.Encapsulate(point);
            float floorY = room.Floor.Contour[0].y;
            GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Cube);
            ground.name = "Test Platform";
            ground.transform.SetParent(root.transform, false);
            ground.transform.localPosition = new Vector3(bounds.center.x, floorY - 0.11f, bounds.center.z);
            ground.transform.localScale = new Vector3(bounds.size.x + 6f, 0.2f, bounds.size.z + 6f);
            var renderer = ground.GetComponent<MeshRenderer>();
            renderer.sharedMaterial = material;
            renderer.shadowCastingMode = ShadowCastingMode.Off;
            var properties = new MaterialPropertyBlock();
            properties.SetColor("_BaseColor", new Color(0.14f, 0.18f, 0.23f));
            renderer.SetPropertyBlock(properties);

            for (int i = 0; i < room.Furniture.Length; i++)
            {
                FurnitureData furniture = room.Furniture[i];
                var obstacle = new GameObject($"Furniture Collider {i}");
                obstacle.transform.SetParent(root.transform, false);
                obstacle.transform.SetLocalPositionAndRotation(furniture.Center, Quaternion.Euler(furniture.RotationDegrees));
                obstacle.AddComponent<BoxCollider>().size = furniture.Size;
            }
            return root;
        }
    }
}
