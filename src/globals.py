from driver.Server import Server

# Global Constants
CONFIG_FILE = "../temp/config.json"  # The path to the configuration file to load on start
device_name = "/dev/input/event12"  # The path to the event device file representing the connected Wacom Tablet

# Global Objects
device_server = Server(device_name)  # An instance of the Server class that the program uses
