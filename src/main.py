import sys, os
from PyQt4 import QtCore, QtGui, uic
import logging

from StartWindow import StartWindow

import config

CONFIG_FILE = "../temp/config.json"

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.info("Checking if config file exists")
    if os.path.isfile(CONFIG_FILE):
        logger.info("Config file found, loading settings from [%s]" % CONFIG_FILE)
        config.Settings.load_config_from_file(CONFIG_FILE)
    else:  # create file
        logger.info("No config file exists, creating one in [%s]" % CONFIG_FILE)
        config.Settings.save_config_to_file(CONFIG_FILE)

    logger.info("Creating App")
    app = QtGui.QApplication(sys.argv)
    window = StartWindow()
    logger.info("Starting GUI")
    window.show()
    sys.exit(app.exec_())
