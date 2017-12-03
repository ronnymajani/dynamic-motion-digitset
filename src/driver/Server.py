import logging
import time
import json

from AsyncTask import AsyncTask
from data.interface import DigitSet, DataSet
import config


class Server(object):
    """This class is the interface between the async task
    that collects the raw data from the Wacom tablet and the GUI.
    It handles managing the data, triggering events, updating the GUI with new information,
    controlling the async task, etc.
    More specifically:
    - Creating the async process
    - Getting the raw data from the async process
    - Clearing the async process's buffer
    - Dealing with save, reset, and cancel operations
    - Managing the different phases of the drawing part
    """
    def __init__(self, device):
        """
        :param device: the linux event file of the Wacom device to connect to (eg: /dev/input/event12)
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.async_task = AsyncTask(device)
        self.dataSet = DataSet()
        self.digitSets = []
        self.digitSet = None

        self.current_digit_phase = 0
        self.count = 0

    def export_digitset(self):
        """Export the current Digit Set
        The file will be named 17.49.01.12.2017_digitset.json"""
        filepath = config.Settings.EXPORT_LOCATION + time.strftime("%H.%M_%d.%m.%Y") + "_digitset.json"
        with open(filepath, "w") as fd:
            json.dump(self.digitSet.as_json(), fd,
                      indent=config.Settings.JSON_INDENT_LEVEL,
                      separators=config.Settings.JSON_SEPARATORS)

    def export_dataset(self):
        """Export the current Data Set
        This will overwrite any previous dataset if it has the same name as specified in the config"""
        filepath = config.Settings.EXPORT_LOCATION + config.Settings.DATASET_FILENAME
        with open(filepath, "w") as fd:
            json.dump(self.dataSet.as_json(), fd,
                      indent=config.Settings.JSON_INDENT_LEVEL,
                      separators=config.Settings.JSON_SEPARATORS)

    def set_activate_user(self, user):
        """Sets the active user and creates a digitset for that user"""
        if self.digitSet is not None:
            self.digitSets.append(self.digitSet)
        # Create a new DigitSet for this user
        self.digitSet = DigitSet(user)
        # Set the AsyncTask to RUNNING
        self.async_task.set_state_running()

    def save_digit(self):
        """Save the drawn digit and increment the counter"""
        # Copy AsyncTask buffer
        data = self.async_task.get_buffer_copy()
        # Save copy to Digit Set
        self.digitSet.add_digit_data(self.current_digit_phase, data)
        # Clear AsyncTask buffer
        self.async_task.clear_buffer()
        # Update the counter
        self.__update_count()

    def __update_count(self):
        """Called after user saves a drawn digit"""
        self.count += 1
        if self.count == config.Settings.SAMPLE_COUNT_PER_DIGIT:
            self.__next_digit_phase()
        # todo: update GUI

    def __next_digit_phase(self):
        """Called at the end of every phase"""
        self.count = 0
        self.current_digit_phase += 1
        if self.current_digit_phase == 10:
            self.__finished_digit_phases()
        else:
            # todo: update GUI
            pass

    def __finished_digit_phases(self):
        """Called when all phases are complete"""
        # Save the digitset to a file
        self.export_digitset()
        # Add the digitset to the dataset
        self.dataSet.add_digitset(self.digitSet)
        # Reset the digitset reference variable to indicate that there is no active user
        self.digitSet = None
        # Set the AsyncTask to IDLE
        self.async_task.set_state_idle()
        # todo: close Drawing Window

