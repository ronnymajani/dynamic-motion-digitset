import sys, os
from PyQt4 import QtCore, QtGui, uic
import logging

from prediction.PredictionWindow import PredictionWindow

import prediction.globals
import config


def load_config():
    """Load configuration if the file exists"""
    logger.info("Checking if config file exists")
    if os.path.isfile(prediction.globals.CONFIG_FILE):
        logger.info("Config file found, loading settings from [%s]" % prediction.globals.CONFIG_FILE)
        config.Settings.load_config_from_file(prediction.globals.CONFIG_FILE)
    else:  # create file
        # if the folder doesn't exist, create it
        if not os.path.exists(prediction.globals.CONFIG_FILE_FOLDER):
            logger.info("The folder [%s] doesn't exist. Creating it now" % prediction.globals.CONFIG_FILE_FOLDER)
            os.mkdir(prediction.globals.CONFIG_FILE_FOLDER)
        logger.info("No config file exists, creating one in [%s]" % prediction.globals.CONFIG_FILE)
        config.Settings.save_config_to_file(prediction.globals.CONFIG_FILE)
        config.Settings.initialize()


if __name__ == '__main__':
    # Create logger and set logging level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Initialize Global variables
    prediction.globals.init_globals()
    # Load Configuration
    load_config()
    # Create Qt Application
    logger.info("Creating App")
    app = QtGui.QApplication(sys.argv)
    # Create Start Window
    logger.info("Starting Prediction Window GUI")
    window = PredictionWindow()
    window.show()
    # Exit when window is closed
    sys.exit(app.exec_())
