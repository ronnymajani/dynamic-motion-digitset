import logging
import time
import json

from Driver import Driver
from data.interface import DigitSet, DataSet
import config
from data.contract import DataSetContract


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

        self.driver = Driver(device)
        self.driver.start()  # Start Async Task
        self.dataSet = DataSet()
        self.digitSets = []

        # Externally set variables
        self.activeDrawingWindow = None
        self.activeDigitSet = None

        self.currentDigitPhase = 0
        self.count = 0

    # Support Functions
    def get_device_resolution_width(self):
        return self.dataSet.json[DataSetContract.METADATA]\
            [DataSetContract.Metadata.Device.RESOLUTION]\
            [DataSetContract.Metadata.Device.RESOLUTION_WIDTH]

    def get_device_resolution_height(self):
        return self.dataSet.json[DataSetContract.METADATA]\
            [DataSetContract.Metadata.Device.RESOLUTION]\
            [DataSetContract.Metadata.Device.RESOLUTION_HEIGHT]

    def get_device_pen_resolution(self):
        return self.dataSet.json[DataSetContract.METADATA]\
            [DataSetContract.Metadata.Device.PEN_PRESSURE]

    # Export Functions
    def export_digitset(self):
        """Export the current Digit Set
        The file will be named 17.49.01.12.2017_digitset.json"""
        filepath = config.Settings.EXPORT_DIRECTORY_PATH + time.strftime("%Y.%m.%d_%H.%M") + "_digitset.json"
        with open(filepath, "w") as fd:
            json.dump(self.activeDigitSet.as_json(), fd,
                      indent=config.Settings.JSON_INDENT_LEVEL,
                      separators=config.Settings.JSON_SEPARATORS)

    def export_dataset(self):
        """Export the current Data Set
        This will overwrite any previous dataset if it has the same name as specified in the config"""
        filepath = config.Settings.EXPORT_DIRECTORY_PATH + config.Settings.DATASET_FILENAME
        with open(filepath, "w") as fd:
            json.dump(self.dataSet.as_json(), fd,
                      indent=config.Settings.JSON_INDENT_LEVEL,
                      separators=config.Settings.JSON_SEPARATORS)

    # Setup Functions
    def set_active_user(self, user):
        """Sets the active user and creates a digitset for that user"""
        if self.activeDigitSet is not None:
            self.digitSets.append(self.activeDigitSet)
        # Create a new DigitSet for this user
        self.activeDigitSet = DigitSet(user)
        # Set the Driver to RUNNING
        self.driver.set_state_running()

    def attach_active_drawing_window(self, window):
        """Attach the Server to the currently active Drawing Window"""
        self.activeDrawingWindow = window

    def detach_active_drawing_window(self):
        """Detach the currently active Drawing Window from the Server"""
        self.activeDrawingWindow = None
        self.reset()

    def reset(self):
        """Resets the state of the server
        Does not detach drawing window"""
        # Set the Driver to IDLE
        self.driver.set_state_idle()
        # Reset phase and count
        self.currentDigitPhase = 0
        self.count = 0
        # Reset the digitset reference variable to indicate that there is no active user
        self.activeDigitSet = None

    # Other Operations
    def reset_digit(self):
        self.driver.clear_buffer()

    def undo_digit(self):
        self.__decrement_count()
        data = self.activeDigitSet.pop_last_digit_data(self.currentDigitPhase)
        self.driver.set_buffer(data)

    # State Functions
    def save_digit(self):
        """Save the drawn digit and increment the counter"""
        # Copy Driver buffer
        data = self.driver.get_buffer_copy()
        # Save copy to Digit Set
        self.activeDigitSet.add_digit_data(self.currentDigitPhase, data)
        # Clear Driver buffer
        self.driver.clear_buffer()
        # Update the counter
        self.__update_count()

        # Private Functions
    def __decrement_count(self):
        """Called when user undoes a drawn digit"""
        self.count -= 1
        if self.count < 0:
            self.__prev_digit_phase()
        # Update attached drawing window
        if self.activeDrawingWindow is not None:
            times_left = config.Settings.SAMPLE_COUNT_PER_DIGIT - self.count
            self.activeDrawingWindow.count_progress_bar.setValue(times_left)

    def __prev_digit_phase(self):
        """Called at the end of every phase"""
        self.count = config.Settings.SAMPLE_COUNT_PER_DIGIT - 1
        self.currentDigitPhase -= 1
        if self.currentDigitPhase < 0:
            self.currentDigitPhase = 0
            self.count = 0
        else:
            # Update attached drawing window
            if self.activeDrawingWindow is not None:
                self.activeDrawingWindow.phase_digit_label.setText(str(self.currentDigitPhase))

    def __update_count(self):
        """Called after user saves a drawn digit"""
        self.count += 1
        if self.count == config.Settings.SAMPLE_COUNT_PER_DIGIT:
            self.__next_digit_phase()
        # Update attached drawing window
        if self.activeDrawingWindow is not None:
            times_left = config.Settings.SAMPLE_COUNT_PER_DIGIT - self.count
            self.activeDrawingWindow.count_progress_bar.setValue(times_left)

    def __next_digit_phase(self):
        """Called at the end of every phase"""
        self.count = 0
        self.currentDigitPhase += 1
        if self.currentDigitPhase == 10:
            self.__finished_digit_phases()
        else:
            # Update attached drawing window
            if self.activeDrawingWindow is not None:
                self.activeDrawingWindow.phase_digit_label.setText(str(self.currentDigitPhase))

    def __finished_digit_phases(self):
        """Called when all phases are complete"""
        # Save the digitset to a file
        self.export_digitset()
        # Add the digitset to the dataset
        self.dataSet.add_digitset(self.activeDigitSet)
        # Reset Server's state
        self.reset()
        # Close Drawing Window
        self.activeDrawingWindow.close()

