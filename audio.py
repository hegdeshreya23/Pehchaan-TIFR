import socket
import time
import wave

HOST = '172.20.10.2'
PORT = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

data = b''
elapsed = 0
seconds = 8
start = time.time()
while True:
    elapsed = time.time() - start
    print(elapsed)
    chunk = sock.recv(4096)
    if not chunk:
        break
    elif elapsed > seconds:
        break
    data += chunk

with wave.open('audio.wav', 'wb') as wavfile:
    wavfile.setnchannels(1)
    wavfile.setsampwidth(2)
    wavfile.setframerate(16000)
    wavfile.writeframes(data)
