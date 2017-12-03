import sys
from PyQt4 import QtCore, QtGui, uic
import logging

import globals
import Canvas
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

        self.canvas = Canvas.Canvas(self.drawing_panel)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.register_buttons()
        # Attach this window to the Server
        globals.device_server.attach_active_drawing_window(self)

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
        self.logger.debug("next button clicked")
        globals.device_server.save_digit()

    def event_reset_button_clicked(self):
        self.logger.debug("reset button clicked")
        globals.device_server.reset_digit()

    def event_cancel_button_clicked(self):
        self.logger.debug("cancel button clicked")
        globals.device_server.reset_digit()
        self.close()

    # Main Events
    def closeEvent(self, event):
        self.logger.debug("Closing Window...")
        # Detach this window from the Server
        globals.device_server.detach_active_drawing_window()
        self.timer.stop()
        # Show the parent window
        self.parent.show()

    # Update Function
    def update_panel(self):
        """Refreshes and updates the GUI with new information"""
        self.logger.debug("Updating Panel")
        # The AsyncTask connected to the device
        async_task = globals.device_server.asyncTask
        # update X, Y, P indicators
        self.data_x_value.setText(str(async_task.x))
        self.data_y_value.setText(str(async_task.y))
        self.data_p_value.setText(str(async_task.p))
        # todo: make sure that directly passing the buffer doesn't cause a problem
        self.canvas.draw(async_task.buffer)
        self.repaint()

