import json


class Defaults(object):
    EXPORT_DIRECTORY_PATH = "../temp/"
    DATASET_FILENAME = "dataset.json"
    SAMPLE_COUNT_PER_DIGIT = 5

    DEVICE_NAME = "Wacom Volito2 CTF-420/G tablet"
    SAMPLING_RATE = 100
    RESOLUTION_WIDTH = 5105
    RESOLUTION_HEIGHT = 3713
    PEN_PRESSURE = 512
    MISC = "Pen (model FP-410-0G)"


class Settings(object):
    """
    Static Class to hold the global configuration of the application
    Variables:
        :var DATASET_SAVE_LOCATION the filename and path where the current dataset will be saved
        :var SAMPLE_COUNT_PER_DIGIT the number of repetitions per digit to collect from the user
            (eg: the number of times a user will enter the digit "1")
        :var REFRESH_INTERVAL the refresh interval in miliseconds at which a drawing panel is updated
    """
    EXPORT_LOCATION = Defaults.EXPORT_DIRECTORY_PATH
    DATASET_FILENAME = Defaults.DATASET_FILENAME
    SAMPLE_COUNT_PER_DIGIT = Defaults.SAMPLE_COUNT_PER_DIGIT
    REFRESH_INTERVAL = 250
    JSON_INDENT_LEVEL = None
    JSON_SEPARATORS = (",", ":")

    @staticmethod
    def as_json():
        """Return a JSON dictionary of the current settings"""
        return {
            "DATASET_FILENAME": Settings.DATASET_FILENAME,
            "SAMPLE_COUNT_PER_DIGIT": Settings.SAMPLE_COUNT_PER_DIGIT,
            "REFRESH_INTERVAL": Settings.REFRESH_INTERVAL,
            "EXPORT_LOCATION": Settings.EXPORT_LOCATION,
            "JSON_INDENT_LEVEL": Settings.JSON_INDENT_LEVEL,
            "JSON_SEPARATORS": Settings.JSON_SEPARATORS
        }

    @staticmethod
    def from_json(config):
        """Load settings from a given JSON dictionary"""
        Settings.DATASET_FILENAME = config["DATASET_FILENAME"]
        Settings.SAMPLE_COUNT_PER_DIGIT = config["SAMPLE_COUNT_PER_DIGIT"]
        Settings.REFRESH_INTERVAL = config["REFRESH_INTERVAL"]
        Settings.EXPORT_LOCATION = config["EXPORT_LOCATION"],
        Settings.JSON_INDENT_LEVEL = config["JSON_INDENT_LEVEL"],
        Settings.JSON_SEPARATORS = config["JSON_SEPARATORS"]

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


