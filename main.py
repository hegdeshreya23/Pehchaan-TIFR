import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
import cv2
import face_recognition

admin_verified = False
admin = "user"

class ImageScreen(QDialog):
    def __init__(self, filename):
        super(ImageScreen, self).__init__()
        loadUi("image.ui", self)
        self.filename = filename
        self.img = self.recogniser(filename)
        self.height, self.width, self.channel = self.img.shape
        self.bytesPerLine = 3 * self.width
        self.img = QtGui.QImage(self.img.data, self.width, self.height, self.bytesPerLine,
                                QtGui.QImage.Format_RGB888).rgbSwapped()
        # ---------------------------------------
        self.pixmap = QtGui.QPixmap.fromImage(self.img)
        self.pixmap4 = self.pixmap.scaled(761, 411, QtCore.Qt.KeepAspectRatio)
        # self.pic.setPixmap(QtGui.QPixmap.fromImage(self.pixmap4))
        self.pic.setPixmap(self.pixmap4)
        # ------------------------------------------
        self.home.clicked.connect(self.goto_landingpage)
        # self.color_button.clicked.connect(self.color_image)
        # self.grayscale_button.clicked.connect(self.grayscale_image)
        # self.face.clicked.connect(self.face_recog)
        self.get_desc(self.filename)

    def goto_landingpage(self):
        landingpage = LandingPage()
        widget.addWidget(landingpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def get_desc(self, filename):
        size = os.path.getsize(filename)
        size //= 1000
        print(size)
        im = Image.open(filename)
        dimensions = im.size
        file_format = im.format
        print(im.format, im.size, im.mode)
        desc_text = "Format: " + str(file_format) + "\nSize: " + str(size) + " kB \nPixels: " + str(dimensions)
        self.desc.setText(desc_text)

    def recogniser(self, filename):
        # Adding images
        numberOfImages = 1
        img = face_recognition.load_image_file(filename)
        # Scaling large images
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        scale_percent = 40
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        images = [img]

        # Images of the group members
        imgFriend1 = face_recognition.load_image_file("Images/muskan.jpg")
        imgFriend1 = cv2.cvtColor(imgFriend1, cv2.COLOR_BGR2RGB)

        imgFriend2 = face_recognition.load_image_file("Images/prerak.jpg")
        imgFriend2 = cv2.cvtColor(imgFriend2, cv2.COLOR_BGR2RGB)

        imgFriend3 = face_recognition.load_image_file("Images/garv.jpg")
        imgFriend3 = cv2.cvtColor(imgFriend3, cv2.COLOR_BGR2RGB)

        imgFriend4 = face_recognition.load_image_file("Images/shreya.jpg")
        imgFriend4 = cv2.cvtColor(imgFriend4, cv2.COLOR_BGR2RGB)
        # Creating face encodings of all friends
        friends = 4
        label = ["muskan", "prerak", "garv", "shreya"]
        encodeFriend1 = face_recognition.face_encodings(imgFriend1)[0]
        encodeFriend2 = face_recognition.face_encodings(imgFriend2)[0]
        encodeFriend3 = face_recognition.face_encodings(imgFriend3)[0]
        encodeFriend4 = face_recognition.face_encodings(imgFriend4)[0]
        encodedFriends = [encodeFriend1, encodeFriend2, encodeFriend3, encodeFriend4]

        # Creating face encoding of the test image
        encodedImages = []
        for i in range(0, 1):
            encodedImages.append(face_recognition.face_encodings(images[i]))

        # Creating a list of detected people
        name = []

        # Detecting the boundary box of face
        for i in range(0, numberOfImages):
            n = len(encodedImages[i])
            for j in range(0, n):
                if (face_recognition.face_distance([encodedFriends[0]], encodedImages[i][j])[0] < 0.45):
                    name.append(label[0])
                elif (face_recognition.face_distance([encodedFriends[1]], encodedImages[i][j])[0] < 0.45):
                    name.append(label[1])
                elif (face_recognition.face_distance([encodedFriends[2]], encodedImages[i][j])[0] < 0.45):
                    name.append(label[2])
                elif (face_recognition.face_distance([encodedFriends[3]], encodedImages[i][j])[0] < 0.45):
                    name.append(label[3])
                else:
                    name.append("Unknown")
                faceLocation = face_recognition.face_locations(images[i])
                faceLoc = faceLocation[i]
                cv2.rectangle(images[i], (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 0), 2)
                cv2.putText(images[i], f'{name[j]}', (faceLoc[3], faceLoc[2] + 25), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 0, 0), 1)
            # Displaying Image
            return img


class LandingPage(QDialog):
    def __init__(self):
        super(LandingPage, self).__init__()
        loadUi("landingPage.ui", self)
        self.browse_button.clicked.connect(self.browsefiles)
        self.open_button.clicked.connect(self.openfiles)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:\TIFR-Assignment-1\Images',
                                            'Images (*.png *.xmp *.PNG *.jpg *.jpeg *.gif)')
        self.browse_line.setText(fname[0])

    def openfiles(self):
        filename = self.browse_line.text()
        image_window = ImageScreen(filename)
        widget.addWidget(image_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        print(filename)


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
            self.success("Welcome "+ str(admin))
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
        self.ThreadActive = True
        global video_auth
        video_auth = cv2.VideoCapture(0)
        while self.ThreadActive:
            # start_time = time.time()
            ret, frame = video_auth.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                scale_percent = 40
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)
                img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                images = [img]

                # Images of the group members
                imgFriend1 = face_recognition.load_image_file("Images/muskan.jpg")
                imgFriend1 = cv2.cvtColor(imgFriend1, cv2.COLOR_BGR2RGB)

                imgFriend2 = face_recognition.load_image_file("Images/prerak.jpg")
                imgFriend2 = cv2.cvtColor(imgFriend2, cv2.COLOR_BGR2RGB)

                imgFriend3 = face_recognition.load_image_file("Images/garv.jpg")
                imgFriend3 = cv2.cvtColor(imgFriend3, cv2.COLOR_BGR2RGB)

                imgFriend4 = face_recognition.load_image_file("Images/shreya.jpg")
                imgFriend4 = cv2.cvtColor(imgFriend4, cv2.COLOR_BGR2RGB)
                # Creating face encodings of all friends
                friends = 4
                label = ["muskan", "prerak", "garv", "shreya"]
                encodeFriend1 = face_recognition.face_encodings(imgFriend1)[0]
                encodeFriend2 = face_recognition.face_encodings(imgFriend2)[0]
                encodeFriend3 = face_recognition.face_encodings(imgFriend3)[0]
                encodeFriend4 = face_recognition.face_encodings(imgFriend4)[0]
                encodedFriends = [encodeFriend1, encodeFriend2, encodeFriend3, encodeFriend4]

                # Creating face encoding of the test image
                encodedImages = []
                for i in range(0, 1):
                    encodedImages.append(face_recognition.face_encodings(images[i]))

                # Creating a list of detected people
                name = "Unknown"

                # Detecting the boundary box of face
                n = len(encodedImages[i])
                for j in range(0, n):
                    if (face_recognition.face_distance([encodedFriends[0]], encodedImages[i][j])[0] < 0.45):
                        name = label[0]
                    elif (face_recognition.face_distance([encodedFriends[1]], encodedImages[i][j])[0] < 0.45):
                        name = label[1]
                    elif (face_recognition.face_distance([encodedFriends[2]], encodedImages[i][j])[0] < 0.45):
                        name = label[2]
                    elif (face_recognition.face_distance([encodedFriends[3]], encodedImages[i][j])[0] < 0.45):
                        name = label[3]
                    

                    if name != "Unknown":
                        global admin_verified
                        admin_verified = True
                        global admin
                        admin = name
                    self.stop()

                    faceLocation = face_recognition.face_locations(images[i])
                    faceLoc = faceLocation[i]
                    cv2.rectangle(images[i], (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 0), 2)
                    cv2.putText(images[i], f'{name[j]}', (faceLoc[3], faceLoc[2] + 25), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 0, 0), 1)

                # print(time.time() - start_time)
                h, w, ch = img.shape
                bytesPerLine = ch * w
                ConvertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
                Video3Image = ConvertToQtFormat.scaled(height, width, Qt.KeepAspectRatio)
                self.Image3Update.emit(Video3Image)

    def stop(self):
        self.ThreadActive = False
        global video_auth
        video_auth.release()
        cv2.destroyAllWindows()
        self.quit()


class MySuccess(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("successful.ui", self)
        self.ok_btn.clicked.connect(self.goto_last_pg)

    def goto_last_pg(self):
        self.close()


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
