import threading
import logging
import evdev
import copy


class AsyncTask(threading.Thread):
    STATE_IDLE = 0
    STATE_RUNNING = 1

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.setName("Async Task")
        self.daemon = True

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.device = evdev.InputDevice(device)
        self.buffer = []
        self.state = AsyncTask.STATE_IDLE

        self.isButtonDown = 0

        self.x = 0
        self.y = 0
        self.p = 0

    def run(self):
        while True:
            for event in self.device.read_loop():
                # Only Run if the Task is in the RUNNING state
                if self.state == AsyncTask.STATE_RUNNING:
                    # Coordinate Data Events (X, Y, P)
                    if event.type == evdev.ecodes.EV_ABS:
                        if event.code == evdev.ecodes.ABS_X:
                            self.x = event.value
                        elif event.code == evdev.ecodes.ABS_Y:
                            self.y = event.value
                        elif event.code == evdev.ecodes.ABS_PRESSURE:
                            self.p = event.value
                    # Synchronization Events
                    elif event.type == evdev.ecodes.EV_SYN and event.code == evdev.ecodes.SYN_REPORT:
                        if self.p != 0:
                            self.buffer.append((self.x, self.y, self.p))
                            self.logger.debug("(%d, %d, %d)" % (self.x, self.y, self.p))  # todo: delete this line

    # Support Functions
    def clear_buffer(self):
        self.buffer = []

    def get_buffer_copy(self):
        return copy.copy(self.buffer)

    def set_state_running(self):
        self.state = AsyncTask.STATE_RUNNING

    def set_state_idle(self):
        self.state = AsyncTask.STATE_IDLE


