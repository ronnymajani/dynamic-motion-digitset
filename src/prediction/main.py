import sys, os
from PyQt4 import QtCore, QtGui, uic
import logging

from PredictionWindow import PredictionWindow

import globals


if __name__ == '__main__':
    # Create logger and set logging level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Initialize Global variables
    globals.init_globals()
    # Create Qt Application
    logger.info("Creating App")
    app = QtGui.QApplication(sys.argv)
    # Create Start Window
    logger.info("Starting Prediction Window GUI")
    window = PredictionWindow()
    window.show()
    # Exit when window is closed
    sys.exit(app.exec_())
