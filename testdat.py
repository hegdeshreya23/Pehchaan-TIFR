import os
import pickle

import cv2
import face_recognition

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image = face_recognition.load_image_file("D:\TIFR-Assignment-1\Images\prerak.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

try:
    with open(os.path.join(BASE_DIR, 'new_encodings.dat'), 'rb') as f:
        all_face_encodings = pickle.load(f)
except:
    all_face_encodings = {}
print(all_face_encodings)
# all_face_encodings["prerak"] = [face_recognition.face_encodings(image)[0]]
# with open(os.path.join(BASE_DIR, 'new_encodings.dat'), 'wb') as f:
#     pickle.dump(all_face_encodings, f)

#print(face_recognition.face_encodings(image)[0])