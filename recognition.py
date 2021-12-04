# from pathlib import Path

import face_recognition
from cv2 import cv2
import numpy as np
import os.path
from playsound import playsound
# from play_sounds import play_file, DEFAULT_SOUND

import encoder
import settings as sets
import hash_sha1
# import prints

# Get a reference to webcam
video_capture = cv2.VideoCapture(0)  # '0' is the standard webcam

# print(video_capture.get(cv2.CAP_PROP_FPS))

video_capture.set(3, sets.frame_width)  # Width of the frames in the video stream
video_capture.set(4, sets.frame_height)  # Height of the frames in the video stream
# video_capture.set(5, sets.frame_rate)       # Frame rate
# video_capture.set(10, sets.brightness)      # Brightness of the image
# video_capture.set(11, sets.contrast)        # Contrast of the image
# video_capture.set(12, sets.saturation)      # Saturation of the image
# video_capture.set(13, sets.hue)             # Hue of the image
# video_capture.set(14, sets.gain)            # Gain of the image
# video_capture.set(15, sets.exposure)        # Exposure
# video_capture.set(20, sets.sharpness)       # sharpness
# video_capture.set(21, sets.auto_exposure)   # auto_exposure
# video_capture.set(22, sets.gamma)           # gamma
# video_capture.set(23, sets.temperature)     # temperature
# video_capture.set(28, sets.focus)           # focus
# video_capture.set(32, sets.backlight)       # backlight
# video_capture.set(39, sets.auto_focus)      # auto_focus
# video_capture.set(42, sets.backend)         # backend
# video_capture.set(44, sets.auto_wb)         # auto_wb
# video_capture.set(42, sets.wb_temperature)  # wb_temperature

# prints.prints(video_capture)

# Rectangle frame color when unknown
frame_color = (0, 0, 255)  # Red

# Delay sound when find known person
delay_sound = 0

# Create database if it does not exist
if not os.path.isfile(sets.database):
    encoder.create_database()

# Create folder 'images' if it does not exist
if not os.path.isdir(sets.folder_path):
    os.mkdir(sets.folder_path)

# Check if are changes in the folder 'images'
hash_sha1.compare_hashes()

# Import encodings and names from json files
known_face_encodings, known_face_names = encoder.import_from_database()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_colors = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    if delay_sound > 0:
        delay_sound -= 1

    # Only process every other frame of video to save time
    if process_this_frame:
    # if delay_sound - (sets.delay_sound / 2) <= 0:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        frame_colors = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            frame_color = (0, 0, 255)  # Red

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                frame_color = (0, 255, 0)  # Green

                if delay_sound <= 0 and sets.play_sound:
                    print('Play sound!')
                    delay_sound = sets.delay_sound
                    # Play sound
                    playsound(sets.sound_file, block=False)
                    # play_file(DEFAULT_SOUND, block=False)
                    # play_file(Path('sounds/beep.mp3'), block=False)

            face_names.append(name)
            frame_colors.append(frame_color)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name, color in zip(face_locations, face_names, frame_colors):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        if name is 'Unknown':
            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, bottom), (right, bottom), color, cv2.FILLED)

        else:
            # Draw a label with a name below the face
            rect = cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            # get boundary of this text
            text_size = cv2.getTextSize(name, font, 0.8, 1)[0]

            align_center = int((right - left - text_size[0]) / 2)

            cv2.putText(frame, name, (left + align_center, bottom - 6), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

    # resize image
    percent = sets.scale_percent
    width = int(sets.frame_width * percent / 100)
    height = int(sets.frame_height * percent / 100)
    # ratio = sets.ratio
    # width = round(sets.frame_width * ratio)
    # height = round(sets.frame_height * ratio)
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    # Display the resulting image
    if sets.gray_scale:
        grayFrame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Gray scale
        cv2.imshow(sets.win_name, grayFrame)  # Gray scale
    else:
        cv2.imshow(sets.win_name, resized)  # Color

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Close window when close button is pressed
    if cv2.getWindowProperty(sets.win_name, cv2.WND_PROP_VISIBLE) < 1:
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
