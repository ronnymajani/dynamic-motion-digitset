import json
import copy

from data.contract import DataSetContract
import config


class User(object):
    def __init__(self, age, sex, hand):
        if age <= 0:
            raise ValueError("Age should be > 0")

        self.age = age
        self.sex = sex
        self.hand = hand

    def as_json(self):
        return {
            DataSetContract.DigitSets.Metadata.USER_AGE: self.age,
            DataSetContract.DigitSets.Metadata.USER_SEX: self.sex,
            DataSetContract.DigitSets.Metadata.USER_HAND: self.hand
        }


class DigitSet(object):
    """
    Variables:
        - user: A User object to hold the information related to the user who produced this digitset
        - data: A tuple of 10 lists. Each element in the tuple corresponds to a digit
            (ie: element 0 corresponds to digit '0')
            each element itself is a list of data
            each 'data' is a list of tuples in the form (X, Y, P) which represent the captured frames
            in chronological order
        - json: a dictionary of the JSON data in this digitset
    """
    _TEMPLATE = None

    def __init__(self, user):
        """
        :param user: a User object representing the user that produced the data to be stored in this set
        """
        self.user = user
        self.data = ([], [], [], [], [], [], [], [], [], [])

        # If the template has not been loaded, load it from the JSON file specified by DataSetContract
        if DigitSet._TEMPLATE is None:
            DigitSet._import_template()

        self.json = DigitSet._TEMPLATE.copy()

    def add_digit_data(self, digit, data):
        """Add new recorded handwritten digit data to the digitset
        Data should be a list of 3d tuples in the form (X, Y, P)
        """
        if digit < 0 or digit > 9:
            raise ValueError("Digit should be in the range [0,9]")
        else:
            self.data[digit].append(data)

    def as_json(self):
        # Synchronize user data with JSON dictionary
        self.json[DataSetContract.DigitSets.METADATA] = self.user.as_json()

        # Synchronize digit data with JSON dictionary
        for i in range(10):
            key = str(i)
            self.json[DataSetContract.DigitSets.DIGITS][key] = self.data[i]

        return self.json

    @staticmethod
    def _import_template():
        """Creates a new JSON dictionary from a template file
        Saves this dictionary in the class's _TEMPLATE variable
        The template file is version specific, and is specified in the DataSetContract class
        """
        with open(DataSetContract.JSON_DIGITSET_TEMPLATE, "r") as fd:
            DigitSet._TEMPLATE = json.loads(fd.read())


class DataSet(object):
    """
    Variables:
        - digitSets: a list of digitsets in this dataset
        - metadata: metadata information about this dataset
        - json: a dictionary of the JSON data in this dataset
    """
    _TEMPLATE = None

    def __init__(self):
        # If the template has not been loaded, load it from the JSON file specified by DataSetContract
        self.json = DataSet._get_template()

        # Set metadata
        self.update_metadata_info(name=config.Settings.DEVICE_NAME,
                                  sampling_rate=config.Settings.SAMPLING_RATE,
                                  resolution_width=config.Settings.RESOLUTION_WIDTH,
                                  resolution_height=config.Settings.RESOLUTION_HEIGHT,
                                  pen_pressure=config.Settings.PEN_PRESSURE,
                                  misc=config.Settings.MISC)

    def update_metadata_info(self, name=None, sampling_rate=None,
                             resolution_width=None, resolution_height=None,
                             pen_pressure=None, misc=None):
        """Updates the specified fields of the dataset's metadata"""
        metadata = self.json[DataSetContract.METADATA]  # reference object to the metdata field in the dataset
        contract_metadata = DataSetContract.Metadata  # reference to the DataSetContract's Metadata class
        contract_device = contract_metadata.Device  # reference to the DataSetContract Metadata"s Device class
        if name is not None:
            metadata[contract_device.NAME] = name
        if sampling_rate is not None:
            metadata[contract_device.SAMPLING_RATE] = sampling_rate
        if resolution_width is not None:
            metadata[contract_device.RESOLUTION][contract_device.RESOLUTION_WIDTH] = resolution_width
        if resolution_height is not None:
            metadata[contract_device.RESOLUTION][contract_device.RESOLUTION_HEIGHT] = resolution_height
        if pen_pressure is not None:
            metadata[contract_device.PEN_PRESSURE] = pen_pressure
        if misc is not None:
            metadata[contract_metadata.MISC] = misc

    def as_json(self):
        """Returns this dataset's JSON dictionary"""
        return self.json

    def as_json_string(self):
        """Returns a string representation of this dataset in the JSON format"""
        return json.dumps(self.as_json(), indent=None, separators=(",", ":"), sort_keys=True)

    def add_digitset(self, digitset):
        """Add a digitset to the dataset"""
        self.json[DataSetContract.DIGITSETS].append(digitset.as_json())

    def merge_dataset(self, dataset):
        """Merge another dataset into this one"""
        for digitset in dataset.as_json()[DataSetContract.DIGITSETS]:
            self.json[DataSetContract.DIGITSETS].append(digitset)

    def clear_digitsets(self):
        """Delete all digitsets from this dataset"""
        self.json[DataSetContract.DIGITSETS] = []

    @staticmethod
    def _get_template():
        """Returns a copy of the Data Set template if it exists, otherwise loaded it from memory first"""
        if DataSet._TEMPLATE is None:
            DataSet._import_template()
        return copy.deepcopy(DataSet._TEMPLATE)

    @staticmethod
    def _import_template():
        """Creates a new JSON dictionary from a template file
        Saves this dictionary in the class's _TEMPLATE variable
        The template file is version specific, and is specified in the DataSetContract class
        """
        with open(DataSetContract.JSON_DATASET_TEMPLATE, "r") as fd:
            DataSet._TEMPLATE = json.load(fd)

    @staticmethod
    def import_dataset(filepath):
        ret = DataSet()
        with open(filepath, "r") as fd:
            ret.json = json.load(fd)
        return ret

