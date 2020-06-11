"""
Encode and Decode NumPy array to and from JSON file
"""

import face_recognition
import json
import numpy as np
import os

import settings as sets


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


def importFromJson():
    """Import all data from .json files"""

    # Deserialization (JSON file into Numpy Array)
    with open('database.json', 'r', encoding='utf-8') as db:
        data = json.load(db)
        encodings = np.asarray(data["array"])

    with open('known_faces.json', 'r', encoding='utf-8') as db:
        data = json.load(db)
        names = np.asarray(data["names"])

    return encodings, names


def _exportToJson(face_encodings, names):
    """Export all data to .json files"""

    # Serialization (NumPy Array into JSON file)
    data = {"array": face_encodings}
    with open('database.json', 'w', encoding='utf-8') as db:
        json.dump(data, db, cls=NumpyArrayEncoder, ensure_ascii=False, indent=2)

    # Creates a file with all names of known faces
    data = {"names": names}
    with open('known_faces.json', 'w', encoding='utf-8') as db:
        json.dump(data, db, cls=NumpyArrayEncoder, ensure_ascii=False, indent=2)


def createData(path=sets.path):
    """Create lists to be exported to .json files"""

    images = os.listdir(path)
    formats = sets.allowed_formats
    known_face_encodings = []
    known_face_names = []
    for i in images:
        if i.endswith(formats):
            # Create arrays of known face encodings
            known_image = face_recognition.load_image_file(path + i)
            known_face_encoding = face_recognition.face_encodings(known_image)
            known_face_encodings.extend(known_face_encoding)

            # Creates a list with all names of known faces
            name = os.path.splitext(i)
            known_face_names.append(name[0])

    if path == sets.path:
        _exportToJson(known_face_encodings, known_face_names)
    else:
        return known_face_encodings, known_face_names


def updateData(path):
    """Append/update new entries to .json files"""

    face_encodings, names = createData(path=path)

    # Append to database.json
    with open('database.json', encoding='utf-8') as db:
        data = json.load(db)
        temp_face_encodings = data['array']
        temp_face_encodings.extend(face_encodings)

    # Append to known_faces.json
    with open('known_faces.json', encoding='utf-8') as db:
        data = json.load(db)
        temp_name = data['names']
        temp_name.extend(names)

    _exportToJson(temp_face_encodings, temp_name)


if __name__ == '__main__':
    # # Create database
    # createData()

    # # Update database ( path='folder/with/new_pictures/' )
    # updateData(path='img/')
    pass
