"""
Settings of recognition.py
"""

# Global vars
folder_path = 'images/'                 # Path to standard folder
allowed_formats = ('.jpg', '.png')      # Allowed pictures formats
database = 'database.json'              # Database file
auto_check = True                       # Checks each start for changes in standard folder

# webcam vars
webcam = 0          # '0' is the standard webcam                    default = 0
frame_width = 640   # Width of the frames in the video stream       default = 640
frame_height = 480  # Height of the frames in the video stream      default = 480

# To activate this settings, first uncheck it on 'recognition.py'
frame_rate = 30     # Frame rate                            default = 30
brightness = 0      # Brightness of the image (-64, 64)     default = 0
contrast = 4        # Contrast of the image (0, 92)         default = 4
saturation = 67     # Saturation of the image (0, 67)       default = 67
hue = 0             # Hue of the image (-2000, 2000)        default = 0
gain = 0            # Gain of the image (0, 100)            default = 0
exposure = 0        # Exposure (-7, 0)                      default = 0
