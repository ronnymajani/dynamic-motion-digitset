import threading
import logging
import evdev
import copy

import config


class Driver(threading.Thread):
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
        self.state = Driver.STATE_IDLE

        self.isButtonDown = 0

        self.x = 0
        self.y = 0
        self.p = 0
        self.t = 0.0

        self._prev_time = 0.0

    def run(self):
        while True:
            for event in self.device.read_loop():
                # Only Run if the Task is in the RUNNING state
                if self.state == Driver.STATE_RUNNING:
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
                        if self.p > config.Settings.PEN_PRESSURE_MIN_THRESHOLD:  # Is pen tip on pad?
                            curr_time = event.timestamp()
                            if self._prev_time == 0.0:
                                self.t = 0.0
                            else:
                                self.t = round((curr_time - self._prev_time) * 1000.0, 3)
                            self.buffer.append((self.x, self.y, self.p, self.t))
                            self.logger.info("(%d, %d, %d, %.3f)" % (self.x, self.y, self.p, self.t))
                            self._prev_time = curr_time

    # Support Functions
    def clear_buffer(self):
        self.buffer = []
        self._prev_time = 0.0

    def get_buffer_copy(self):
        return copy.copy(self.buffer)

    def set_state_running(self):
        self.state = Driver.STATE_RUNNING

    def set_state_idle(self):
        self.state = Driver.STATE_IDLE


