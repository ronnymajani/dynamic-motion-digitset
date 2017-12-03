import sys
from PyQt4 import QtCore, QtGui, uic
import logging

# Set Logging
logging.basicConfig(level=logging.DEBUG)
# Import QT Design
qtCreatorFile = "../Design/StartWindow.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class StartWindow(QtGui.QMainWindow, UI_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        UI_MainWindow.__init__(self)
        self.setupUi(self)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.register_buttons()

    def register_buttons(self):
        """Register the callback functions for the GUI buttons"""
        self.Start_pushButton.clicked.connect(self.event_start_button_clicked)

    # Our Events
    def event_start_button_clicked(self):
        print("start button clicked")

    # Main Events
    def closeEvent(self, event):
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
