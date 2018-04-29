import sys
from Server import Server

# Global Constants
CONFIG_FILE_FOLDER = "../settings"  # The path to the configuration file to load on start
CONFIG_FILE_NAME = "config.json"  # The name of the configuration file
CONFIG_FILE = CONFIG_FILE_FOLDER + "/" + CONFIG_FILE_NAME
device_name = "/dev/input/event12"  # The path to the event device file representing the connected Wacom Tablet
keras_model_name = "prediction/model.hdf5"

# Global Objects
device_server = None  # An instance of the Server class that the program uses
keras_graph = None


def init_globals():
    """Initialize Global variables"""
    global device_name, device_server
    # Set Event Device name if specified as a command line argument
    if len(sys.argv) > 1:
        device_name = "/dev/input/event%d" % int(sys.argv[1])
    # Initialize Server
    device_server = Server(device_name)
