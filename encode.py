#Server side

import pickle
import face_recognition
import glob

imdir = 'Images/'
ext = ['png', 'jpg', 'gif']    # Add image formats here
#add only non existing image encode functionality
files = []
[files.extend(glob.glob(imdir + '*.' + e)) for e in ext]
for i in range(0,len(files) -1):
    image = face_recognition.load_image_file(files[i])

    encodings = face_recognition.face_encodings(image)[0]
    face_encodings = dict()
    face_encodings[files[i][7:-4]] = [encodings]
    file = open('new_encodings.dat', 'wb')
    pickle.dump(face_encodings, file)
    file.close()
    print(face_encodings)