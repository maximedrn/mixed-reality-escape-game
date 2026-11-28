using UnityEngine;
using UnityEngine.InputSystem;

namespace EnvironmentSandbox
{
    [RequireComponent(typeof(CharacterController))]
    internal sealed class SandboxFps : MonoBehaviour
    {
        private const float LookSensitivity = 0.11f;
        private const float Speed = 3.5f;
        private CharacterController controller;
        private Transform cameraPivot;
        private float pitch;
        private float verticalSpeed;
        private Vector3 spawnPosition;
        private float spawnYaw;

        public void Configure(Camera camera)
        {
            controller = GetComponent<CharacterController>();
            controller.height = 1.8f;
            controller.center = Vector3.up * 0.9f;
            controller.radius = 0.28f;
            controller.stepOffset = 0.22f;
            controller.minMoveDistance = 0f;
            cameraPivot = camera.transform;
            cameraPivot.SetParent(transform, false);
            cameraPivot.localPosition = Vector3.up * 1.62f;
            camera.nearClipPlane = 0.04f;
            camera.clearFlags = CameraClearFlags.SolidColor;
            camera.backgroundColor = new Color(0.065f, 0.09f, 0.13f);
        }

        public void ResetPose(Vector3 position, float yaw)
        {
            spawnPosition = position;
            spawnYaw = yaw;
            controller.enabled = false;
            transform.SetPositionAndRotation(position, Quaternion.Euler(0f, yaw, 0f));
            pitch = 4f;
            verticalSpeed = 0f;
            cameraPivot.localRotation = Quaternion.Euler(pitch, 0, 0);
            controller.enabled = true;
        }

        private void Update()
        {
            if (!controller) return;

            Keyboard keyboard = Keyboard.current;
            Mouse mouse = Mouse.current;
            if (keyboard != null && keyboard.escapeKey.wasPressedThisFrame) LockCursor(false);
            else if (mouse != null && mouse.leftButton.wasPressedThisFrame) LockCursor(true);

            Vector3 move = Vector3.zero;
            if (Cursor.lockState == CursorLockMode.Locked)
            {
                if (mouse != null)
                {
                    Vector2 delta = mouse.delta.ReadValue() * LookSensitivity;
                    pitch = Mathf.Clamp(pitch - delta.y, -85f, 85f);
                    cameraPivot.localRotation = Quaternion.Euler(pitch, 0, 0);
                    transform.Rotate(Vector3.up, delta.x);
                }
                if (keyboard != null) move = ReadMovement(keyboard) * Speed;
            }

            if (controller.isGrounded && verticalSpeed < 0f) verticalSpeed = -2f;
            verticalSpeed += Physics.gravity.y * Time.deltaTime;
            controller.Move((transform.TransformDirection(move) + Vector3.up * verticalSpeed) * Time.deltaTime);
            if (transform.position.y < spawnPosition.y - 10f) ResetPose(spawnPosition, spawnYaw);
        }

        private static Vector3 ReadMovement(Keyboard keyboard)
        {
            bool forward = keyboard.wKey.isPressed || keyboard.zKey.isPressed || keyboard.upArrowKey.isPressed;
            bool back = keyboard.sKey.isPressed || keyboard.downArrowKey.isPressed;
            bool left = keyboard.aKey.isPressed || keyboard.qKey.isPressed || keyboard.leftArrowKey.isPressed;
            bool right = keyboard.dKey.isPressed || keyboard.rightArrowKey.isPressed;
            return Vector3.ClampMagnitude(new Vector3((right ? 1 : 0) - (left ? 1 : 0), 0,
                (forward ? 1 : 0) - (back ? 1 : 0)), 1f);
        }

        private static void LockCursor(bool locked)
        {
            Cursor.lockState = locked ? CursorLockMode.Locked : CursorLockMode.None;
            Cursor.visible = !locked;
        }

        private void OnApplicationFocus(bool focused)
        {
            if (!focused) LockCursor(false);
        }

        private void OnDisable() => LockCursor(false);
    }
}
