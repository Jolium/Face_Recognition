import face_recognition
import cv2
import numpy as np
import os.path

import encoder
import settings as sets
import hash_sha1


# Get a reference to webcam
video_capture = cv2.VideoCapture(0)         # '0' is the standard webcam
video_capture.set(3, sets.frame_width)      # Width of the frames in the video stream
video_capture.set(4, sets.frame_height)     # Height of the frames in the video stream
# video_capture.set(5, sets.frame_rate)       # Frame rate
# video_capture.set(10, sets.brightness)      # Brightness of the image
# video_capture.set(11, sets.contrast)        # Contrast of the image
# video_capture.set(12, sets.saturation)      # Saturation of the image
# video_capture.set(13, sets.hue)             # Hue of the image
# video_capture.set(14, sets.gain)            # Gain of the image
# video_capture.set(15, sets.exposure)        # Exposure

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
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
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

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), frame_color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), frame_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Camera', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
