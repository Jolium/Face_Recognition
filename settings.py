"""
Settings of recognition.py
"""

# Global vars
folder_path = 'images/'  # Path to standard folder
allowed_formats = ('.jpg', '.png')  # Allowed pictures formats
database = 'database.json'  # Database file
auto_check = False  # Checks each start for changes in standard folder

# Sound
# to play when found known person
play_sound = False
sound_file = 'sounds/beep.mp3'
delay_sound = 40

# window
win_name = 'Camera'
scale_percent = 100
# ratio = 1

# webcam vars
webcam = 0  # '0' is the standard webcam                    default = 0
frame_width = 640  # Width of the frames in the video stream       default = 640 / 640
frame_height = 360  # Height of the frames in the video stream      default = 480 / 360
gray_scale = False  # Gray scale vs color

# To activate these settings, first uncheck it on 'recognition.py'
frame_rate = 30  # Frame rate                            default = 30
brightness = 0  # Brightness of the image (-64, 64)     default = 0
contrast = 4  # Contrast of the image (0, 92)         default = 4
saturation = 67  # Saturation of the image (0, 67)       default = 67
hue = 0  # Hue of the image (-2000, 2000)        default = 0
gain = 0  # Gain of the image (0, 100)            default = 0
exposure = 0  # Exposure (-7, 0)                      default = 78
sharpness = 2  # Sharpness (1, 7)                      default = 2

dict_properties = {
    'POS_MSEC': 0,
    'POS_FRAMES': 1,
    'POS_AVI_RATIO': 2,
    'FRAME_WIDTH': 3,
    'FRAME_HEIGHT': 4,
    'FPS': 5,
    'FOURCC': 6,
    'FRAME_COUNT': 7,
    'FORMAT': 8,
    'MODE': 9,
    'BRIGHTNESS': 10,
    'CONTRAST': 11,
    'SATURATION': 12,
    'HUE': 13,
    'GAIN': 14,
    'EXPOSURE': 15,
    'CONVERT_RGB': 16,
    'WHITE_BALANCE_BLUE_U': 17,
    'RECTIFICATION': 18,
    'MONOCHROME': 19,
    'SHARPNESS': 20,
    'AUTO_EXPOSURE': 21,
    'GAMMA': 22,
    'TEMPERATURE': 23,
    'TRIGGER': 24,
    'TRIGGER_DELAY': 25,
    'WHITE_BALANCE_RED_V': 26,
    'ZOOM': 27,
    'FOCUS': 28,
    'GUID': 29,
    'ISO_SPEED': 30,
    'BACKLIGHT': 32,
    'PAN': 33,
    'TILT': 34,
    'ROLL': 35,
    'IRIS': 36,
    'SETTINGS': 37,
    'BUFFERSIZE': 38,
    'AUTOFOCUS': 39,
    'SAR_NUM': 40,
    'SAR_DEN': 41,
    'BACKEND': 42,
    'CHANNEL': 43,
    'AUTO_WB': 44,
    'WB_TEMPERATURE': 45,
    'CODEC_PIXEL_FORMAT': 46,
    'BITRATE': 47,
    'ORIENTATION_META': 48,
    'ORIENTATION_AUTO': 49,
    'OPEN_TIMEOUT_MSEC': 53,
    'READ_TIMEOUT_MSEC': 54
}
