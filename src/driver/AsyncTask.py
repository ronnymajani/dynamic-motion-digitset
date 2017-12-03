import threading
import logging
import evdev


class AsyncTask(threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.setName("Async Task")
        self.daemon = True

        self.device = evdev.InputDevice(device)
        self.buffer = []
