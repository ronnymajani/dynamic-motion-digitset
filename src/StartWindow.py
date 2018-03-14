from PyQt4 import QtCore, QtGui, uic
import logging

import globals
import data.interface
from data.contract import DataSetContract

from DrawingWindow import DrawingWindow
from ExportWindow import ExportWindow

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
        self.export_window = None

        self.register_buttons()

    def register_buttons(self):
        """Register the callback functions for the GUI buttons"""
        self.Start_pushButton.clicked.connect(self.event_start_button_clicked)
        self.actionExport.triggered.connect(self.event_export_action_button_clicked)

    def get_user_info(self):
        age = self.Age_spinBox.value()

        # todo: make sure that the UI file always coincides with this part of the code
        # we assume that the first dropdown option is Male, and the second is Female for sex
        # and for hand we assume the first to be Right, and the second to be Left
        sex = self.Sex_comboBox.currentIndex()
        if sex == 0:
            sex = DataSetContract.DigitSet.Metadata.USER_SEX_MALE
        else:
            sex = DataSetContract.DigitSet.Metadata.USER_SEX_FEMALE

        hand = self.Hand_comboBox.currentIndex()
        if hand == 0:
            hand = DataSetContract.DigitSet.Metadata.USER_HAND_RIGHT
        else:
            hand = DataSetContract.DigitSet.Metadata.USER_HAND_LEFT

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

    def event_export_action_button_clicked(self):
        """Export action button was clicked"""
        self.logger.debug("export action button clicked")
        self.export_window = ExportWindow(self)
        self.export_window.show()
        self.hide()

    # Main Events
    def closeEvent(self, event):
        self.logger.debug("Window Closed")
