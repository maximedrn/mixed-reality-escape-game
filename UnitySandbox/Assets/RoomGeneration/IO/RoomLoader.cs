using System;
using System.IO;

namespace RoomGeneration
{
    public static class RoomLoader
    {
        public static RoomData Load(string path)
        {
            string json;
            try
            {
                json = File.ReadAllText(path);
            }
            catch (Exception error) when (error is IOException or UnauthorizedAccessException or ArgumentException)
            {
                throw new IOException($"Cannot read room file '{path}': {error.Message}", error);
            }

            try
            {
                RoomData room = RoomJson.Deserialize(json);
                RoomValidator.Validate(room);
                return room;
            }
            catch (FormatException error)
            {
                throw new FormatException($"Invalid format in room file '{path}': {error.Message}", error);
            }
            catch (RoomValidationException error)
            {
                throw new RoomValidationException($"Invalid geometry in room file '{path}': {error.Message}", error);
            }
        }
    }
}
