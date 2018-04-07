import logging

import globals
from config import Settings
from driver.Driver import Driver
import numpy as np
import preprocessing

from keras.models import load_model


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

        self.driver.set_state_running()

        # Externally set variables
        self.activeDrawingWindow = None

        # load keras model
        self.model = load_model(globals.keras_model_name)

    def predict(self):
        digit = self.driver.get_buffer_copy()
        digit = preprocessing.apply_mean_centering(digit)
        digit = preprocessing.apply_unit_distance_normalization(digit)
        digit = preprocessing.normalize_pressure_value(digit)
        digit = preprocessing.spline_interpolate_and_resample(digit, 200)
        digit = np.array([digit])
        return self.model.predict_classes(digit, verbose=1)[0]

    # Support Functions
    def get_device_resolution_width(self):
        return Settings.RESOLUTION_WIDTH

    def get_device_resolution_height(self):
        return Settings.RESOLUTION_HEIGHT

    def get_device_pen_resolution(self):
        return Settings.PEN_PRESSURE

    def attach_active_drawing_window(self, window):
        """Attach the Server to the currently active Drawing Window"""
        self.activeDrawingWindow = window
        self.driver.set_state_running()

    def detach_active_drawing_window(self):
        """Detach the currently active Drawing Window from the Server"""
        self.activeDrawingWindow = None
        self.driver.set_state_idle()

    # Other Operations
    def reset_digit(self):
        self.driver.clear_buffer()
