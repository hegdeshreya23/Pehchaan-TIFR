import pickle
import sys, os

import pyaudio
import socket
import threading
import wave

import urllib

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
import cv2
import face_recognition
from essential_generators import DocumentGenerator
from PyQt5.QtCore import QTimer
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
new_user = "user"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# url_cam = 'http://192.168.176.152/cam-hi.jpg'
url_mic = '192.168.0.161'

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
        # admin_verified = True
        if admin_verified:
            gen = DocumentGenerator()
            input_str = gen.sentence()
            print(input_str)
            result_list = input_str.split()[:12]
            phrase = " ".join(result_list)
            rstr = "Welcome "+ str(admin)+"\n \n"+ "Please say this phrase: \n"+phrase
            self.success(rstr)
        # self.close()

        else:
            # self.close()
            self.goto_alert("Authentication Failed.")
            cv2.destroyAllWindows()

    def success(self, message):
        self.w = MyVoice()
        self.w.label.setText(message)
        self.w.label.setWordWrap(True)
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
        # for webcam
        video_auth = cv2.VideoCapture(0)
        # for esp32
        # imgResp=urllib.request.urlopen(url_cam)

        while self.ThreadActive:
            # start_time = time.time()
            # for webcam
            ret, frame = video_auth.read()
            # for esp32
            # imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
            # frame = cv2.imdecode(imgNp,-1)
            # ret = True
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


class MyVoice(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("successful.ui", self)
        #self.ok_btn.clicked.connect(self.goto_last_pg)
        self.label1.setStyleSheet('background-color: none')
        self.sr = 44100
        self.max_duration = 600
        self.ch = 1
        self.save_num = 0
        self.audio = np.array([])
        self.input_device = sd.query_devices(kind='input')
        self.time = 0
        self.status = 0
        self.rec()
        t = Timer(5, self.stop)
        t.start()

    def read_audio_from_socket(self):
        global buffering, buffer, buffer_audio
        # connect to the esp32 socket
        sock = socket.socket()
        sock.connect((url_mic, 1234))
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        while buffer_audio:
            data = sock.recv(4096)
            if data == b"":
                raise RuntimeError("Lost connection")
            buffer.append(data)
            if len(buffer) > 50 and buffering:
                print("Finished buffering")
                buffering = False

    def save_esp(self):
        global buffer, buffering, buffer_audio
        # initiaslise pyaudio
        p = pyaudio.PyAudio()
        # kick off the audio buffering thread
        thread = threading.Thread(target=self.read_audio_from_socket(self))
        thread.daemon = True
        thread.start()
        if True:
            input("Recording to output.wav - hit any key to stop")
            buffer_audio = False
            # write the buffered audio to a wave file
            with wave.open("output.wav", "wb") as wave_file:
                wave_file.setnchannels(1)
                wave_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wave_file.setframerate(16000)
                wave_file.writeframes(b"".join(buffer))

    def rec(self):
        self.audio = sd.rec(frames=self.max_duration*self.sr, samplerate=self.sr, channels=self.ch, dtype='float32',
                            device=self.input_device['name'])
        self.time = time.time()
        self.status = 'rec'
        self.label1.setText('REC')
        self.label1.setStyleSheet('background-color: orange; font-size: 40px')
    #     self.flag = True
    #     timer = QTimer(self, interval=500)
    #     timer.timeout.connect(self.flashing)
    #     timer.start()

    # def flashing(self):
    #     if self.flag:
    #         self.label1.setStyleSheet('background-color: none; font-size: 40px')
    #     else:
    #         self.label1.setStyleSheet('background-color: orange; font-size: 40px')
    #     self.flag = not self.flag

    def stop(self):
        sd.stop()
        if self.status == 'rec':
            s_time = time.time() - self.time
            self.audio = self.audio[:int(round(s_time, 0)*self.sr)]
            global file_name
            file_name = 'rec_audio'+str(self.save_num)+'.wav'
            wavfile.write(file_name, self.sr, self.audio)
            self.status = 'stop'
            self.label1.setText('STOP')
            self.label1.setStyleSheet('background-color: none; font-size: 40px')
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


class MyAlert(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("alert.ui", self)
        self.ok_btn.clicked.connect(self.goto_last_pg)

    def goto_last_pg(self):
        self.close()


class MySuccess(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("successpop.ui", self)
        self.ok_btn.clicked.connect(self.goto_last_pg)

    def goto_last_pg(self):
        self.close()

class Enroll(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("landingPage.ui", self)
        self.browse_button.clicked.connect(self.browsefiles)
        self.open_button.clicked.connect(self.goto_insert_user)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', BASE_DIR, 'Images (*.png *.jpeg *.xmp *.PNG *.jpg)')
        if fname[0]:
            self.image_url_text.setText(fname[0])
        else:
            self.goto_alert("No file selected")

    def goto_alert(self, message):
        self.w = MyAlert()
        self.w.label.setText(message)
        self.w.show()
    
    def record(self):
        self.w = Record()
        self.w.show()

    def goto_insert_user(self):
        self.user_name = self.name_text.text()
        self.user_photo_url = self.image_url_text.text()
        image = face_recognition.load_image_file(self.user_photo_url)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if (len(face_recognition.face_locations(image)) > 1):
            self.goto_alert("Upload an individual image")
            return
        elif (len(face_recognition.face_locations(image)) == 0):
            self.goto_alert("Upload an image of your face")
            return
        try:
            with open(os.path.join(BASE_DIR, 'new_encodings.dat'), 'rb') as f:
                all_face_encodings = pickle.load(f)
        except:
            all_face_encodings = {}
        all_face_encodings[self.user_name] = [face_recognition.face_encodings(image)[0]]
        with open(os.path.join(BASE_DIR, 'new_encodings.dat'), 'wb') as f:
            pickle.dump(all_face_encodings, f)
    
        global new_user
        new_user = self.user_name
        self.record()
        self.name_text.setText("")
        self.image_url_text.setText("")

class Record(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("record.ui", self)
        self.input_device = sd.query_devices(kind='input')
        self.rec = 1
        self.audio = np.array([])
        self.time = 0
        self.sr = 44100
        self.max_duration = 600
        self.ch = 1
        self.save_num = 0
        self.enroll.clicked.connect(self.goto_enroll)
        self.start.clicked.connect(self.goto_start)
        self.stop.clicked.connect(self.goto_stop)
    
    def goto_enroll(self):
        if self.rec == "saved":
            try:
                with open(os.path.join(BASE_DIR, 'audio_encodings.dat'), 'rb') as f:
                    audio_encodings = pickle.load(f)
            except:
                audio_encodings = {}
            mfcc = sample_from_mfcc(read_mfcc("D:/tifr pehchaan/"+file_name, SAMPLE_RATE), NUM_FRAMES)
            global new_user
            audio_encodings[new_user] = mfcc    
            with open(os.path.join(BASE_DIR, 'audio_encodings.dat'), 'wb') as f:
                pickle.dump(audio_encodings, f)
            self.rec = "enrolled"
            self.success("Person successfully inserted")
        else:
            self.goto_alert("Please record audio again")
            return


    def goto_start(self):
        self.start.setStyleSheet('background-color: orange')
        self.audio = sd.rec(frames=self.max_duration*self.sr, samplerate=self.sr, channels=self.ch, dtype='float32',
                            device=self.input_device['name'])
        self.time = time.time()
        self.rec = "rec"

    def goto_stop(self):
        self.start.setStyleSheet('background-color: none')
        sd.stop()
        if self.rec == 'rec':
            s_time = time.time() - self.time
            self.audio = self.audio[:int(round(s_time, 0)*self.sr)]
            global file_name
            file_name = 'rec_audio'+str(self.save_num)+'.wav'
            wavfile.write(file_name, self.sr, self.audio)
            print(file_name)
            self.rec = "saved"

    def success(self, message):
        self.w = MySuccess()
        self.w.label.setText(message)
        self.w.show()

    def goto_alert(self, message):
        self.w = MyAlert()
        self.w.label.setText(message)
        self.w.show()


class LandingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("gui.ui", self)
        self.enroll.clicked.connect(self.goto_enroll)
        self.attend.clicked.connect(self.goto_attend)

    def goto_enroll(self):
        enroll = Enroll()
        widget.addWidget(enroll)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_attend(self):
        attend = MySAdminLogin()
        widget.addWidget(attend)
        widget.setCurrentIndex(widget.currentIndex() + 1)

        
app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()

landingpage = LandingPage()
widget.addWidget(landingpage)
widget.setFixedWidth(962)
widget.setFixedHeight(730)
widget.show()
sys.exit(app.exec_())

