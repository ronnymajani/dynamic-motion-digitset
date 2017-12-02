class DataSetContract:
    VERSION = "0.2"
    METADATA = "dataset_metadata"
    DIGITSETS = "digitsets"

    class Metadata:
        MISC = "misc"

        class Device:
            NAME = "device_name"
            SAMPLING_RATE = "sampling_rate"
            RESOLUTION = "device_resolution"
            PEN_PRESSURE = "pressure_resolution"

            RESOLUTION_WIDTH = "W"
            RESOLUTION_HEIGHT = "H"

    class DigitSets:
        METADATA = "digitset_metadata"
        DIGITS = "digits"
        Digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        class Metadata:
            USER_AGE = "user_age"
            USER_SEX = "user_gender"
            USER_HAND = "user_hand"