import socket
import pyaudio

# Set up socket connection to the ESP32
serverIP = '192.168.176.39' # replace with the IP address of your ESP32
serverPort = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((serverIP, serverPort))

# Set up PyAudio to play audio data
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

# Receive and play audio data over WiFi
while True:
    data, addr = sock.recvfrom(1024)
    stream.write(data)


# import socket
# import numpy as np
# import wave

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect the socket to the port where the server is listening
# server_address = ('192.168.0.161', 1234)
# print(f"connecting to {server_address[0]} port {server_address[1]}")
# sock.connect(server_address)

# # Open a WAV file for writing
# filename = "recording.wav"
# nchannels = 1
# sampwidth = 2  # 16-bit audio data
# framerate = 44100
# nframes = 0
# comptype = "NONE"
# compname = "not compressed"
# wave_file = wave.open(filename, "wb")
# wave_file.setnchannels(nchannels)
# wave_file.setsampwidth(sampwidth)
# wave_file.setframerate(framerate)
# wave_file.setnframes(nframes)
# wave_file.setcomptype(comptype, compname)

# # Receive and write audio data to the WAV file
# while True:
#     data = sock.recv(1024)
#     if not data:
#         break
#     wave_file.writeframes(data)

# # Close the WAV file and the socket
# wave_file.close()
# sock.close()

# print("Recording saved to recording.wav.")


# import socket

# HOST = '192.168.0.161'  # Replace with your ESP32's IP address
# PORT = 1234

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT))

# while True:
#     data = sock.recv(1024)
#     print(data)
#     # Process audio data as needed