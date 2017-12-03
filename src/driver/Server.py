import logging
import time
import json

from AsyncTask import AsyncTask
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

        self.asyncTask = AsyncTask(device)
        self.asyncTask.start()  # Start Async Task
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
        filepath = config.Settings.EXPORT_LOCATION + time.strftime("%H.%M_%d.%m.%Y") + "_digitset.json"
        with open(filepath, "w") as fd:
            json.dump(self.activeDigitSet.as_json(), fd,
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

    # Setup Functions
    def set_active_user(self, user):
        """Sets the active user and creates a digitset for that user"""
        if self.activeDigitSet is not None:
            self.digitSets.append(self.activeDigitSet)
        # Create a new DigitSet for this user
        self.activeDigitSet = DigitSet(user)
        # Set the AsyncTask to RUNNING
        self.asyncTask.set_state_running()

    def attach_active_drawing_window(self, window):
        """Attach the Server to the currently active Drawing Window"""
        self.activeDrawingWindow = window

    def detach_active_drawing_window(self):
        """Detach the currently active Drawing Window from the Server"""
        self.activeDrawingWindow = None

    # Other Operations
    def reset_digit(self):
        self.asyncTask.clear_buffer()

    # State Functions
    def save_digit(self):
        """Save the drawn digit and increment the counter"""
        # Copy AsyncTask buffer
        data = self.asyncTask.get_buffer_copy()
        # Save copy to Digit Set
        self.activeDigitSet.add_digit_data(self.currentDigitPhase, data)
        # Clear AsyncTask buffer
        self.asyncTask.clear_buffer()
        # Update the counter
        self.__update_count()

        # Private Functions
    def __update_count(self):
        """Called after user saves a drawn digit"""
        self.count += 1
        if self.count == config.Settings.SAMPLE_COUNT_PER_DIGIT:
            self.__next_digit_phase()
        # Update attached drawing window
        if self.activeDrawingWindow is not None:
            self.activeDrawingWindow.count_progress_bar.setValue(self.count+1)

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
        # Reset the digitset reference variable to indicate that there is no active user
        self.activeDigitSet = None
        # Set the AsyncTask to IDLE
        self.asyncTask.set_state_idle()
        # Close Drawing Window
        self.activeDrawingWindow.close()

