import pickle
import sys, os

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
import cv2
import face_recognition
from essential_generators import DocumentGenerator

from threading import Timer
from scipy.io import wavfile
import sounddevice as sd
import time
import pickle
from speaker_verification.model_evaluation import run_user_evaluation
from speaker_verification.deep_speaker.audio import NUM_FRAMES, SAMPLE_RATE, read_mfcc, sample_from_mfcc

filename = ""
admin_verified = False
admin = "user"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MySAdminLogin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("preview_img.ui", self)
        self.Worker3 = Worker3()
        self.Worker3.finished.connect(self.verify)
        self.Worker3.start()
        self.Worker3.Image3Update.connect(self.Image3UpdateSlot)
        global height, width
        height = 800
        width = 800
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.close)

    def Image3UpdateSlot(self, Image):
        self.pic.setPixmap(QPixmap.fromImage(Image))

    def verify(self):
        global admin_verified
        self.ok_btn.setEnabled(True)
        if admin_verified:
            gen = DocumentGenerator()
            input_str = gen.sentence()
            print(input_str)
            result_list = input_str.split()[:9]
            phrase = " ".join(result_list)
            rstr = "Welcome "+ str(admin)+"\n \n"+ "Please say this phrase: \n"+phrase
            self.success(rstr)
        # self.close()

        else:
            # self.close()
            self.goto_alert("Authentication Failed.")
            cv2.destroyAllWindows()

    def success(self, message):
        self.w = MySuccess()
        self.w.label.setText(message)
        self.w.setWindowTitle("UpAIsthiti")
        self.w.show()

    def goto_alert(self, message):
        self.w = MyAlert()
        self.w.label.setText(message)
        self.w.setWindowTitle("UpAIsthiti")
        self.w.show()


class Worker3(QThread):
    Image3Update = pyqtSignal(QImage)

    def run(self):
        global attendance_entry, id_name_mapping, id_status_mapping
        self.ThreadActive = True
        global video_auth
        video_auth = cv2.VideoCapture(0)
        while self.ThreadActive:
            # start_time = time.time()
            ret, frame = video_auth.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # scale_percent = 40
                # width = int(img.shape[1] * scale_percent / 100)
                # height = int(img.shape[0] * scale_percent / 100)
                # dim = (width, height)
                # img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                images = [img]

                # Creating a list of detected people
                name = "Unknown"

                #detection code here
                try:
                    with open(os.path.join(BASE_DIR, 'new_encodings.dat'), 'rb') as f:
                        all_face_encodings = pickle.load(f)
                except:
                    all_face_encodings = {}
                face_ids = list(all_face_encodings.keys())
                print(face_ids)
                known_face_encodings = np.array(list(value[0] for value in all_face_encodings.values()))
                check_frame = True
                while self.ThreadActive:
                    try:
                        # video_work = cv2.VideoCapture('')
                        video_work = cv2.VideoCapture(0)
                        ret, frame = video_work.read()
                        Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        if check_frame:
                            face_locations = face_recognition.face_locations(Image)
                            
                            if (len(face_locations) > 0):
                                face_encodings = face_recognition.face_encodings(Image, face_locations)
                                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                                    # See if the face is a match for the known face(s)
                                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding,
                                                                             tolerance=0.45)
                                    if True in matches:
                                        name = face_ids[matches.index(True)]
                                        cv2.rectangle(Image, (left, top), (right, bottom), (0, 255, 0), 1)
                                        y = top - 15 if top - 15 > 15 else top + 15
                                        cv2.putText(Image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    except:
                        print("Error")
                    if name != "Unknown":
                        global admin_verified
                        admin_verified = True
                        global admin
                        admin = name
                    self.stop()

                    # faceLoc = face_locations[0]
                    # cv2.rectangle(Image, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 0), 2)
                    # cv2.putText(Image, f'{name}', (faceLoc[3], faceLoc[2] + 25), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                    #             (255, 0, 0), 1)

                # print(time.time() - start_time)
                h, w, ch = Image.shape
                bytesPerLine = ch * w
                ConvertToQtFormat = QImage(Image.data, w, h, bytesPerLine, QImage.Format_RGB888)
                Video3Image = ConvertToQtFormat.scaled(height, width, Qt.KeepAspectRatio)
                self.Image3Update.emit(Video3Image)

    def stop(self):
        print("Stopping")
        self.ThreadActive = False
        global video_auth
        video_auth.release()
        cv2.destroyAllWindows()
        self.quit()


class MySuccess(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("successful.ui", self)
        #self.ok_btn.clicked.connect(self.goto_last_pg)
        self.sr = 44100
        self.max_duration = 600
        self.ch = 1
        self.save_num = 0
        self.audio = np.array([])
        self.input_device = sd.query_devices(kind='input')
        self.output_device = sd.query_devices(kind='output')
        self.time = 0
        self.status = 0
        self.rec()
        t = Timer(5, self.stop)
        t.start()

    def rec(self):
        self.audio = sd.rec(frames=self.max_duration*self.sr, samplerate=self.sr, channels=self.ch, dtype='float32',
                            device=self.input_device['name'])
        self.time = time.time()
        self.status = 'rec'
        self.label1.setText('REC')

    def stop(self):
        sd.stop()
        if self.status == 'rec':
            s_time = time.time() - self.time
            self.audio = self.audio[:int(round(s_time, 0)*self.sr)]
            global file_name
            file_name = 'rec_audio'+str(self.save_num)+'.wav'
            wavfile.write(file_name, self.sr, self.audio)
            print(file_name)
            self.status = 'stop'
            self.label1.setText('stop')
            try:
                with open(os.path.join(BASE_DIR, 'audio_encodings.dat'), 'rb') as f:
                    audio_encodings = pickle.load(f)
            except:
                audio_encodings = {}
            global admin
            print(admin)
            mfcc = audio_encodings[admin]
            score = run_user_evaluation(mfcc, file_name)
            result = round(score[0] * 100, 2)
            print(result)
            if result > 55.0:
                self.label1.setText('verified')
            else:
                self.label1.setText('not verified')
        # self.label.setText('no')

    # def save(self):
    #     if len(self.audio) != 0:
    #         file_name = 'rec_audio'+str(self.save_num)+'.wav'
    #         wavfile.write(file_name, self.sr, self.audio)
    #         self.save_num += 1
    #         self.label.setText(str(self.save_num)+'_SAVE')
    #     else:
    #         self.label.setText('None')


class MyAlert(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("alert.ui", self)
        self.ok_btn.clicked.connect(self.goto_last_pg)

    def goto_last_pg(self):
        self.close()


app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()

landingpage = MySAdminLogin()
widget.addWidget(landingpage)
widget.setFixedWidth(962)
widget.setFixedHeight(730)
widget.show()
sys.exit(app.exec_())

# if path is empty display msg
# bg set
# grayscale
# disable text writing in labels
