import logging

import data.interface


class Server(object):
    """This class is the interface between the async task
    that collects the raw data from the Wacom tablet and the GUI.
    It handles managing the data, triggering events, updating the GUI with new information,
    controlling the async task, etc.
    More specifically:
    - Creating the async process
    - Getting the raw data from the async process
    - Clearing the async process's buffer
    - Dealing with save, reset, and cancel operations
    """
    def __init__(self):
        self.async_task = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)



