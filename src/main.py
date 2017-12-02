import evdev
import json
import data.contract
from data.interface import *
import config


#%%
device = evdev.InputDevice('/dev/input/event12')

#%%
x = 0
y = 0
p = 0
btn_down = 0

# initialize dataset
user = User(20, User.SEX_MALE, User.HAND_RIGHT)
dataset = DataSet()
digitset = DigitSet(user)
raw_data = []

#%%
phase = 0
count = 0

print("\nDigit [%d] (%d/%d)" % (phase, count, config.Defaults.SAMPLE_COUNT_PER_DIGIT))
for event in device.read_loop():
    #    print(evdev.categorize(event))
    if event.type == evdev.ecodes.EV_KEY:
        # Stylus is now touching or has stopped touching the pad
        if event.code == evdev.ecodes.BTN_TOUCH:
            btn_down = event.value
            print()

        # Save Current Digit
        elif event.code == evdev.ecodes.BTN_STYLUS2 and event.value == 1:
            digitset.add_digit_data(phase, raw_data)
            raw_data = []
            print("Digit Saved")

            count += 1
            if count == config.Defaults.SAMPLE_COUNT_PER_DIGIT:
                count = 0
                phase += 1
                if phase == 10:
                    break

            print("\nDigit [%d] (%d/%d)" % (phase, count, config.Defaults.SAMPLE_COUNT_PER_DIGIT))

        # Stop Loop
        elif event.code == evdev.ecodes.BTN_STYLUS:
            print("Stopping Loop")
            break

    if event.type == evdev.ecodes.EV_ABS:
        if event.code == evdev.ecodes.ABS_X:
            x = event.value
        elif event.code == evdev.ecodes.ABS_Y:
            y = event.value
        elif event.code == evdev.ecodes.ABS_PRESSURE:
            p = event.value

    if btn_down == 1:
        if event.type == evdev.ecodes.EV_SYN and event.code == evdev.ecodes.SYN_REPORT:
            raw_data.append((x, y, p))
            print("(%d, %d, %d)" % (x, y, p))

#%%
# append digitset to dataset
dataset.add_digitset(digitset)

# Save dataset to JSON file with no indentation and no separators for most efficient memory usage
with open(config.Defaults.DATASET_FILENAME, "w") as fd:
    json.dump(dataset.as_json(), fd, indent=None, separators=(",", ":"))
