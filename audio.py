
import pyaudio
import socket
import threading
import wave

buffer = []
buffering = False
buffer_audio = True

url_mic = '192.168.176.39'

def read_audio_from_socket():
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


def save_esp():
    global buffer, buffering, buffer_audio
    # initiaslise pyaudio
    p = pyaudio.PyAudio()
    # kick off the audio buffering thread
    thread = threading.Thread(target=read_audio_from_socket())
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



if __name__ == "__main__":
    save_esp()