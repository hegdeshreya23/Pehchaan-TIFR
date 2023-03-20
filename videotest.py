import cv2
vcap = cv2.VideoCapture("rtsp://192.168.69.152:8554/mjpeg/1")
while(1):
    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)