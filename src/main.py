import sys, os
from PyQt4 import QtCore, QtGui, uic
import logging

from StartWindow import StartWindow

import globals
import config


def load_config():
    """Load configuration if the file exists"""
    logger.info("Checking if config file exists")
    if os.path.isfile(globals.CONFIG_FILE):
        logger.info("Config file found, loading settings from [%s]" % globals.CONFIG_FILE)
        config.Settings.load_config_from_file(globals.CONFIG_FILE)
    else:  # create file
        logger.info("No config file exists, creating one in [%s]" % globals.CONFIG_FILE)
        config.Settings.save_config_to_file(globals.CONFIG_FILE)


if __name__ == '__main__':
    # Create logger and set logging level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Initialize Global variables
    globals.init_globals()
    # Load Configuration
    load_config()
    # Create Qt Application
    logger.info("Creating App")
    app = QtGui.QApplication(sys.argv)
    # Create Start Window
    logger.info("Starting GUI")
    window = StartWindow()
    window.show()
    # Exit when window is closed
    sys.exit(app.exec_())
