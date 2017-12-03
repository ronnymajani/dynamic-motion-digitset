from PyQt4 import QtCore, QtGui, uic
import logging
import os

import config
import globals
from data.interface import DataSet
from data.contract import DataSetContract

# Set Logging
logging.basicConfig(level=logging.DEBUG)
# Import QT Design
qtCreatorFile = "../Design/ExportWindow.ui"
UI_SettingsWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class ExportWindow(QtGui.QMainWindow, UI_SettingsWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self)
        UI_SettingsWindow.__init__(self)
        self.setupUi(self)

        self.parent = parent

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.load_dataset()
        self.register_buttons()

    def register_buttons(self):
        """Register the callback functions for the GUI buttons"""
        self.save_button.clicked.connect(self.save)

    def load_dataset(self):
        # Load Dataset file if it exists, otherwise initialize a new DataSet object
        filepath = config.Settings.EXPORT_DIRECTORY_PATH + config.Settings.DATASET_FILENAME
        self.filename_label.setText(filepath)  # display filename in GUI
        if os.path.isfile(filepath):
            self.logger.debug("Dataset File already exists. Importing it...")
            imported_dataset = DataSet.import_dataset(filepath)
            globals.device_server.dataSet.merge_dataset(imported_dataset)
        else:
            self.logger.debug("No Dataset File found.")
        # Load the DataSet metadata in GUI
        self.load_values()

    def load_values(self):
        self.logger.debug("Loading values")
        json = globals.device_server.dataSet.as_json()  # reference to the currently loaded dataset
        metadata = json[DataSetContract.METADATA]  # reference object to the metdata field in the dataset
        contract_metadata = DataSetContract.Metadata  # reference to the DataSetContract's Metadata class
        contract_device = contract_metadata.Device  # reference to the DataSetContract Metadata"s Device class
        self.device_name_value.setText(metadata[contract_device.NAME])
        self.misc_textEdit.setPlainText(metadata[contract_metadata.MISC])
        self.pressure_spinBox.setValue(metadata[contract_device.PEN_PRESSURE])
        self.sampling_rate_spinBox.setValue(metadata[contract_device.SAMPLING_RATE])
        self.resolution_width_spinBox.setValue(metadata[contract_device.RESOLUTION][contract_device.RESOLUTION_WIDTH])
        self.resolution_height_spinBox.setValue(metadata[contract_device.RESOLUTION][contract_device.RESOLUTION_HEIGHT])

    # Callback Functions
    def save(self):
        """Save the dataset"""
        self.logger.info("Saving Database...")
        # Get input values
        device_name = str(self.device_name_value.text())
        misc = str(self.misc_textEdit.toPlainText())
        pressure = int(self.pressure_spinBox.value())
        sampling_rate = int(self.sampling_rate_spinBox.value())
        resolution_width = int(self.resolution_width_spinBox.value())
        resolution_height = int(self.resolution_height_spinBox.value())
        # Update dataset metadata
        globals.device_server.dataSet.update_metadata_info(name=device_name,
                                                           sampling_rate=sampling_rate,
                                                           resolution_width=resolution_width,
                                                           resolution_height=resolution_height,
                                                           pen_pressure=pressure,
                                                           misc=misc)
        # Export metadata
        globals.device_server.export_dataset()
        # Reset loaded Data Set
        self.logger.debug("Resetting Data Set")
        globals.device_server.dataSet.clear_digitsets()
        # Close window
        self.close()

    # Qt Events
    def closeEvent(self, QCloseEvent):
        self.logger.debug("Closing Window...")
        self.parent.show()

