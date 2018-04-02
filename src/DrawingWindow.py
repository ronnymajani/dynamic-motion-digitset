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
        QtGui.QMainWindow.__init__(self)
        UI_DrawingWindow.__init__(self)
        self.setupUi(self)

        self.parent = parent

        self.canvas = Canvas.Canvas(self.drawing_panel)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.register_buttons()
        # set max counts in progresss bar
        self.count_progress_bar.setMaximum(config.Settings.SAMPLE_COUNT_PER_DIGIT)
        self.count_progress_bar.setValue(config.Settings.SAMPLE_COUNT_PER_DIGIT)
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
        self.button_undo.clicked.connect(self.event_undo_button_clicked)

    # Our Events (Callback Functions)
    def event_next_button_clicked(self):
        self.logger.debug("next button clicked")
        globals.device_server.save_digit()

    def event_reset_button_clicked(self):
        self.logger.debug("reset button clicked")
        globals.device_server.reset_digit()

    def event_undo_button_clicked(self):
        self.logger.debug("undo button clicked")
        globals.device_server.undo_digit()

    def event_cancel_button_clicked(self):
        self.logger.debug("cancel button clicked")
        globals.device_server.reset_digit()
        self.close()

    # Qt Events
    def closeEvent(self, event):
        self.logger.debug("Closing Window...")
        # Detach this window from the Server
        globals.device_server.detach_active_drawing_window()
        self.timer.stop()
        # Show the parent window
        self.parent.show()

    def keyPressEvent(self, QKeyEvent):
        """Handle Keypress"""
        if QKeyEvent.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Space):
            self.event_next_button_clicked()
        elif QKeyEvent.key() == QtCore.Qt.Key_R:
            self.event_reset_button_clicked()
        elif QKeyEvent.key() == QtCore.Qt.Key_U:
            self.event_undo_button_clicked()
        QtGui.QMainWindow.keyPressEvent(self, QKeyEvent)

    # Update Function
    def update_panel(self):
        """Refreshes and updates the GUI with new information"""
        self.logger.debug("Updating Panel")
        # The Driver connected to the device
        driver = globals.device_server.driver
        # update X, Y, P indicators
        self.data_x_value.setText(str(driver.x))
        self.data_y_value.setText(str(driver.y))
        self.data_p_value.setText(str(driver.p))
        self.data_dt_value.setText(str(driver.dt))
        # update Canvas
        # todo: make sure that directly passing the buffer doesn't cause a problem
        # todo: find a better way than to keep getting the device width and height on every call
        res_x = globals.device_server.get_device_resolution_width()
        res_y = globals.device_server.get_device_resolution_height()
        res_p = globals.device_server.get_device_pen_resolution()
        self.canvas.draw(driver.buffer, res_x, res_y, res_p)
        # force QT to repaint window
        self.repaint()

