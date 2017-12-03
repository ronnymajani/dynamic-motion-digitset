import sys
from PyQt4 import QtCore, QtGui, uic
import logging

import Panel
import config

# Set Logging
logging.basicConfig(level=logging.DEBUG)
# Import QT Design
qtCreatorFile = "../Design/DrawingWindow.ui"
UI_DrawingWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class DrawingWindow(QtGui.QMainWindow, UI_DrawingWindow):
    def __init__(self, parent):
        self.parent = parent

        QtGui.QMainWindow.__init__(self)
        UI_DrawingWindow.__init__(self)
        self.setupUi(self)

        self.panel = Panel.Panel(self.drawing_panel)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.register_buttons()

        # Panel Updater timer
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(config.Settings.REFRESH_INTERVAL)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update_panel)
        self.timer.start()

    def register_buttons(self):
        """Register the callback functions for the GUI buttons"""
        self.button_next.clicked.connect(self.event_next_button_clicked)
        self.button_reset.clicked.connect(self.event_reset_button_clicked)
        self.button_cancel.clicked.connect(self.event_cancel_button_clicked)

    # Our Events
    def event_next_button_clicked(self):
        self.logger.info("next button clicked")

    def event_reset_button_clicked(self):
        self.logger.info("reset button clicked")

    def event_cancel_button_clicked(self):
        self.logger.info("cancel button clicked")
        self.close()

    # Main Events
    def closeEvent(self, event):
        self.parent.show()
        self.logger.info("Window Closed")

    # Update Function
    def update_panel(self):
        """Refreshes and updates the GUI with new information"""
        # todo: update X, Y, P
        # todo: update drawing panel
        pass

