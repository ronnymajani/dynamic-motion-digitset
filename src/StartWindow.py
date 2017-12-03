import sys
from PyQt4 import QtCore, QtGui, uic
import logging

import globals
import data.interface

from DrawingWindow import DrawingWindow

# Set Logging
logging.basicConfig(level=logging.DEBUG)
# Import QT Design
qtCreatorFile = "../Design/StartWindow.ui"
UI_StartWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class StartWindow(QtGui.QMainWindow, UI_StartWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        UI_StartWindow.__init__(self)
        self.setupUi(self)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.drawing_window = None

        self.register_buttons()

    def register_buttons(self):
        """Register the callback functions for the GUI buttons"""
        self.Start_pushButton.clicked.connect(self.event_start_button_clicked)

    def get_user_info(self):
        age = self.Age_spinBox.value()

        sex = self.Sex_comboBox.currentIndex()
        if sex == 0:
            sex = "male"
        else:
            sex = "female"

        hand = self.Hand_comboBox.currentIndex()
        if hand == 0:
            hand = "right"
        else:
            hand = "left"

        return age, sex, hand

    # Our Events
    def event_start_button_clicked(self):
        """Start Button was clicked"""
        self.logger.debug("start button clicked")

        user = data.interface.User(*self.get_user_info())  # Get user info
        globals.device_server.set_active_user(user)  # Set active user
        self.drawing_window = DrawingWindow(self)  # Create Drawing Window
        self.drawing_window.show()  # Show Drawing Window
        self.hide()  # Close this Window

    # Main Events
    def closeEvent(self, event):
        self.logger.debug("Window Closed")


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
