using System;
using System.IO;
using NUnit.Framework;
using UnityEngine;

namespace RoomGeneration.Tests
{
    public sealed class RoomDataTests
    {
        private static string SamplePath(string file) =>
            Path.Combine(Application.streamingAssetsPath, "Rooms", file);

        [TestCase("rectangle.json", 4)]
        [TestCase("polygon.json", 6)]
        public void LoadsExamplesAndPreservesUnityCoordinates(string file, int cornerCount)
        {
            RoomData room = RoomLoader.Load(SamplePath(file));

            Assert.That(room.Floor.Contour.Length, Is.EqualTo(cornerCount));
            Assert.That(room.Floor.Contour[0], Is.EqualTo(new Vector3(-4, 0, -3)));
            Assert.That(room.Floor.Contour[1], Is.EqualTo(new Vector3(4, 0, -3)));
            Assert.That(room.Ceiling.Contour[0], Is.EqualTo(new Vector3(-4, 2.8f, -3)));
            Assert.That(room.Walls.Length, Is.EqualTo(cornerCount));
            Assert.That(room.Openings[0].Kind, Is.EqualTo(OpeningKind.Door));
            Assert.That(room.Openings[1].Kind, Is.EqualTo(OpeningKind.Window));
            Assert.That(room.Furniture[0].Center, Is.EqualTo(new Vector3(-2, 0.45f, 1)));
            Assert.That(room.Furniture[0].RotationDegrees.y, Is.EqualTo(25));
            Assert.That(room.Furniture[0].Labels, Does.Contain("table"));
        }

        [TestCase("{")]
        [TestCase("[]")]
        [TestCase("{\"schemaVersion\": 2}")]
        public void RejectsInvalidJson(string json)
        {
            Assert.Throws<FormatException>(() => RoomJson.Deserialize(json));
        }

        [Test]
        public void RejectsMissingCoordinateInsteadOfDefaultingToZero()
        {
            string json = File.ReadAllText(SamplePath("rectangle.json")).Replace("\"z\": -3", "\"unused\": -3");
            Assert.That(Assert.Throws<FormatException>(() => RoomJson.Deserialize(json)).Message,
                Does.Contain("floor.contour[0].z"));
        }

        [Test]
        public void InvalidFileMentionsFileAndJsonField()
        {
            string path = Path.GetTempFileName();
            try
            {
                File.WriteAllText(path, "{\"schemaVersion\": 1, \"name\": \"Room\"}");
                Assert.That(Assert.Throws<FormatException>(() => RoomLoader.Load(path)).Message,
                    Does.Contain(path).And.Contain("floor"));
            }
            finally
            {
                File.Delete(path);
            }
        }

        [Test]
        public void PreservesIsoDateTextAsNameAndLabel()
        {
            const string text = "2026-11-27T16:00:00Z";
            string json = File.ReadAllText(SamplePath("rectangle.json"))
                .Replace("Rectangular room", text).Replace("\"table\"", $"\"{text}\"");
            RoomData room = RoomJson.Deserialize(json);
            Assert.That(room.Name, Is.EqualTo(text));
            Assert.That(room.Furniture[0].Labels, Does.Contain(text));
            Assert.Throws<FormatException>(() => RoomJson.Deserialize(json + "{}"));
        }

        [Test]
        public void ReportsUnreadableFileWithItsPath()
        {
            string path = Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString("N"), "room.json");
            Assert.That(Assert.Throws<IOException>(() => RoomLoader.Load(path)).Message, Does.Contain(path));
        }

        [Test]
        public void RejectsSelfIntersectingContourWithNonzeroSignedArea()
        {
            RoomData room = RoomLoader.Load(SamplePath("rectangle.json"));
            room.Floor.Contour = new[]
            {
                new Vector3(0, 0, 0), new Vector3(4, 0, 4),
                new Vector3(0, 0, 3), new Vector3(3, 0, 0)
            };
            Assert.That(Assert.Throws<RoomValidationException>(() => RoomValidator.Validate(room)).Message,
                Does.Contain("floor.contour"));
        }

        [Test]
        public void RejectsOpeningOutsideItsWall()
        {
            RoomData room = RoomLoader.Load(SamplePath("rectangle.json"));
            room.Openings[0].Width = 12;
            Assert.That(Assert.Throws<RoomValidationException>(() => RoomValidator.Validate(room)).Message,
                Does.Contain("openings[0]"));
        }

        [Test]
        public void RejectsNonHorizontalSurfaceAndZeroSizeFurniture()
        {
            RoomData room = RoomLoader.Load(SamplePath("rectangle.json"));
            room.Ceiling.Contour[0] += Vector3.up;
            Assert.That(Assert.Throws<RoomValidationException>(() => RoomValidator.Validate(room)).Message,
                Does.Contain("ceiling.contour"));
            room.Ceiling.Contour[0] -= Vector3.up;
            room.Furniture[0].Size = Vector3.zero;
            Assert.That(Assert.Throws<RoomValidationException>(() => RoomValidator.Validate(room)).Message,
                Does.Contain("furniture[0].size"));
        }

        [Test]
        public void PlaceholderReturnsEmptyEnvironment()
        {
            EnvironmentData result = new ProceduralGenerator().Generate(RoomLoader.Load(SamplePath("polygon.json")));
            Assert.That(result.Meshes, Is.Empty);
            Assert.That(result.Instances, Is.Empty);
        }
    }
}
