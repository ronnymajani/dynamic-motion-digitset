import json


class Defaults(object):
    EXPORT_DIRECTORY_PATH = "../temp/"
    DATASET_FILENAME = "dataset.json"
    SAMPLE_COUNT_PER_DIGIT = 5
    REFRESH_INTERVAL = 15
    JSON_INDENT_LEVEL = None
    JSON_SEPARATORS = (",", ":")
    PEN_PRESSURE_MIN_THRESHOLD = 5

    DEVICE_NAME = "Wacom Volito2 CTF-420/G tablet"
    SAMPLING_RATE = 100
    RESOLUTION_WIDTH = 5105
    RESOLUTION_HEIGHT = 3713
    PEN_PRESSURE = 512
    MISC = "Pen (model FP-410-0G)"


class Settings(Defaults):
    """
    Static Class to hold the global configuration of the application
    Variables:
        :var EXPORT_DIRECTORY_PATH the path to the directory where exported files should be saved
        :var DATASET_SAVE_LOCATION the filename and path where the current dataset will be saved
        :var SAMPLE_COUNT_PER_DIGIT the number of repetitions per digit to collect from the user
            (eg: the number of times a user will enter the digit "1")
        :var REFRESH_INTERVAL the refresh interval in miliseconds at which a drawing panel is updated
        :var JSON_INDENT_LEVEL the indent level to use when saving JSON files
        :var JSON_SEPARATORS the separators to use when saving JSON files
        :var PEN_PRESSURE_MIN_THRESHOLD the minimum pressure value that must be exceeded for the pen to be considered
            'touching' the drawing pad. Needed because sometime small vibrations or rebound can cause a small pressure
            reading which can lead to noisy readings
    """

    @staticmethod
    def as_json():
        """Return a JSON dictionary of the current settings"""
        return {
            "DATASET_FILENAME": Settings.DATASET_FILENAME,
            "SAMPLE_COUNT_PER_DIGIT": Settings.SAMPLE_COUNT_PER_DIGIT,
            "REFRESH_INTERVAL": Settings.REFRESH_INTERVAL,
            "EXPORT_DIRECTORY_PATH": Settings.EXPORT_DIRECTORY_PATH,
            "JSON_INDENT_LEVEL": Settings.JSON_INDENT_LEVEL,
            "JSON_SEPARATORS": Settings.JSON_SEPARATORS,
            "PEN_PRESSURE_MIN_THRESHOLD": Settings.PEN_PRESSURE_MIN_THRESHOLD
        }

    @staticmethod
    def from_json(config):
        """Load settings from a given JSON dictionary"""
        Settings.DATASET_FILENAME = config["DATASET_FILENAME"]
        Settings.SAMPLE_COUNT_PER_DIGIT = config["SAMPLE_COUNT_PER_DIGIT"]
        Settings.REFRESH_INTERVAL = config["REFRESH_INTERVAL"]
        Settings.EXPORT_DIRECTORY_PATH = config["EXPORT_DIRECTORY_PATH"]
        Settings.JSON_INDENT_LEVEL = config["JSON_INDENT_LEVEL"]
        Settings.JSON_SEPARATORS = config["JSON_SEPARATORS"]
        Settings.PEN_PRESSURE_MIN_THRESHOLD = config["PEN_PRESSURE_MIN_THRESHOLD"]

    @staticmethod
    def save_config_to_file(filename):
        """Save the current settings to the specified JSON file"""
        with open(filename, "w") as fd:
            json.dump(Settings.as_json(), fd, indent=2)

    @staticmethod
    def load_config_from_file(filename):
        """Load settings from the specified JSON file"""
        with open(filename, "r") as fd:
            Settings.from_json(json.load(fd))


