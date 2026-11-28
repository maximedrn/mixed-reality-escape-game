using System;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEngine;

namespace RoomGeneration
{
    public static class RoomJson
    {
        public static RoomData Deserialize(string json)
        {
            if (string.IsNullOrWhiteSpace(json)) throw new FormatException("Room JSON is empty.");

            JObject root;
            try
            {
                using var reader = new JsonTextReader(new StringReader(json))
                {
                    DateParseHandling = DateParseHandling.None
                };
                root = JObject.Load(reader, new JsonLoadSettings
                {
                    DuplicatePropertyNameHandling = DuplicatePropertyNameHandling.Error
                });
                while (reader.Read())
                    if (reader.TokenType != JsonToken.Comment)
                        throw new JsonReaderException("Unexpected content after the room object.");
            }
            catch (JsonException error)
            {
                throw new FormatException($"Invalid room JSON: {error.Message}", error);
            }

            JToken version = Require(root, "schemaVersion");
            if (version.Type != JTokenType.Integer || version.ToString(Formatting.None) != "1")
                throw new FormatException("schemaVersion must be 1.");

            return new RoomData
            {
                Name = ReadString(Require(root, "name")),
                Floor = ReadSurface(Require(root, "floor")),
                Ceiling = ReadSurface(Require(root, "ceiling")),
                Walls = ReadArray(Require(root, "walls"), ReadWall),
                Openings = ReadArray(Require(root, "openings"), ReadOpening),
                Furniture = ReadArray(Require(root, "furniture"), ReadFurniture)
            };
        }

        private static RoomSurfaceData ReadSurface(JToken token) => new()
        {
            Contour = ReadArray(Require(token, "contour"), ReadVector),
            Labels = ReadLabels(token)
        };

        private static WallData ReadWall(JToken token) => new()
        {
            Start = ReadVector(Require(token, "start")),
            End = ReadVector(Require(token, "end")),
            Height = ReadNumber(Require(token, "height")),
            Labels = ReadLabels(token)
        };

        private static OpeningData ReadOpening(JToken token) => new()
        {
            Kind = ReadKind(Require(token, "kind")),
            WallIndex = ReadIndex(Require(token, "wallIndex")),
            Offset = ReadNumber(Require(token, "offset")),
            Bottom = ReadNumber(Require(token, "bottom")),
            Width = ReadNumber(Require(token, "width")),
            Height = ReadNumber(Require(token, "height")),
            Labels = ReadLabels(token)
        };

        private static FurnitureData ReadFurniture(JToken token) => new()
        {
            Center = ReadVector(Require(token, "center")),
            RotationDegrees = ReadVector(Require(token, "rotationDegrees")),
            Size = ReadVector(Require(token, "size")),
            Labels = ReadLabels(token)
        };

        private static Vector3 ReadVector(JToken token) => new(
            ReadNumber(Require(token, "x")), ReadNumber(Require(token, "y")), ReadNumber(Require(token, "z")));

        private static OpeningKind ReadKind(JToken token) => ReadString(token) switch
        {
            "door" => OpeningKind.Door,
            "window" => OpeningKind.Window,
            _ => throw new FormatException($"{token.Path} must be 'door' or 'window'.")
        };

        private static string[] ReadLabels(JToken token) => token["labels"] is JToken labels
            ? ReadArray(labels, ReadString)
            : Array.Empty<string>();

        private static T[] ReadArray<T>(JToken token, Func<JToken, T> read)
        {
            if (token is not JArray array) throw Unexpected(token, "an array");
            var result = new T[array.Count];
            for (int i = 0; i < result.Length; i++) result[i] = read(array[i]);
            return result;
        }

        private static JToken Require(JToken token, string key)
        {
            if (token is not JObject obj) throw Unexpected(token, "an object");
            string field = string.IsNullOrEmpty(obj.Path) ? key : $"{obj.Path}.{key}";
            return obj[key] ?? throw new FormatException($"Missing required field {field}.");
        }

        private static string ReadString(JToken token)
        {
            if (token.Type != JTokenType.String || string.IsNullOrWhiteSpace((string)token))
                throw Unexpected(token, "a nonempty string");
            return (string)token;
        }

        private static float ReadNumber(JToken token)
        {
            if (token.Type != JTokenType.Integer && token.Type != JTokenType.Float)
                throw Unexpected(token, "a number");
            return (float)token;
        }

        private static int ReadIndex(JToken token)
        {
            if (token.Type != JTokenType.Integer || !int.TryParse(token.ToString(Formatting.None), out int index))
                throw Unexpected(token, "a 32-bit integer");
            return index;
        }

        private static FormatException Unexpected(JToken token, string expected) => new($"{token.Path} must be {expected}.");
    }
}
