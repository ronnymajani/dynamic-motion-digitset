import evdev
import json

FILENAME = "temp/dataset.json"
JSON_DATASET_TEMPLATE = "Templates/data_v0.2_template_dataset.json"
JSON_DIGITSET_TEMPLATE = "Templates/data_v0.2_template_digitset.json"
SAMPLE_COUNT_PER_DIGIT = 5


#%%
device = evdev.InputDevice('/dev/input/event12')

#%%
x = 0
y = 0
p = 0
btn_down = 0
data = []
digits = []

# initialize digits
for i in range(10):
    digits.append([])


#%%
phase = 0
count = 0

print("\nDigit [%d] (%d/%d)"%(phase, count, SAMPLE_COUNT_PER_DIGIT))
for event in device.read_loop():
#    print(evdev.categorize(event))
    if event.type == evdev.ecodes.EV_KEY:
        # Stylus is now touching or has stopped touching the pad
        if event.code == evdev.ecodes.BTN_TOUCH:
            btn_down = event.value
            print()
            
        # Save Current Digit
        elif event.code == evdev.ecodes.BTN_STYLUS2 and event.value == 1:
            digits[phase].append(data)
            data = []
            print("Digit Saved")
            
            count += 1
            if count == SAMPLE_COUNT_PER_DIGIT:
                count = 0
                phase += 1
                if phase == 10:
                    break
                
            print("\nDigit [%d] (%d/%d)"%(phase, count, SAMPLE_COUNT_PER_DIGIT))
            
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
            data.append((x, y, p))
            print("(%d, %d, %d)"%(x, y, p))
            
#%%
with open(JSON_DATASET_TEMPLATE, "r") as fd:
    dataset = json.loads(fd.read())

with open(JSON_DIGITSET_TEMPLATE, "r") as fd:
    digitset = json.loads(fd.read())

# create digitset
    # metadata
digitset["digitset_metadata"]["user_age"] = 20
digitset["digitset_metadata"]["user_gender"] = "male"
digitset["digitset_metadata"]["user_hand"] = "right"
    # digits
for i in range(10):
    digitset["digits"][str(i)] = digits[i]
    
# append digitset to dataset
dataset["digitsets"].append(digitset)

# Save dataset to JSON file with no indentation and no separators for most efficient memory usage
with open(FILENAME, "w") as fd:
    json.dump(dataset, fd, indent=None, separators=(",",":"))