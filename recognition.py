import face_recognition
import cv2
import numpy as np
import os


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Global vars
path = 'images/'
allowed_formats = ('.jpg', '.png')

# webcam vars
frame_width = 640
frame_height = 480

# Get a reference to webcam
video_capture = cv2.VideoCapture(0)  # '0' is the standard webcam
video_capture.set(3, frame_width)  # Width of the frames in the video stream
video_capture.set(4, frame_height)  # Height of the frames in the video stream
# video_capture.set(5, 30) # Frame rate
# video_capture.set(10, 150)  # Brightness of the image
# video_capture.set(11, 150)  # Contrast of the image
# video_capture.set(12, 150)  # Saturation of the image
# video_capture.set(13, 150)  # Hue of the image
# video_capture.set(14, 150)  # Gain of the image
# video_capture.set(15, 150)  # Exposure

#########################################################################

# Create arrays of known face encodings
img_list = os.listdir(path)
known_face_encodings = []
for i in img_list:
    known_image = face_recognition.load_image_file(path + i)
    known_face_encoding = face_recognition.face_encodings(known_image)
    known_face_encodings.extend(known_face_encoding)

##########################################################################

# # Create arrays of known face names
# known_face_names = [os.path.splitext(i)[0] for i in img_list]

known_face_names = []
for item in img_list:
    name = os.path.splitext(item)
    known_face_names.append(name[0])

############################################################################

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
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
