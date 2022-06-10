import pyaudio
import time
import numpy as np
import sounddevice as sd


class Live_Recorder:
    def __init__(self, function, blocksize, samplerate, delay=0.05):
        self.function = function
        self.blocksize = blocksize
        self.samplerate = samplerate
        self.delay = delay
        self.stop = False

    def start_recording(self):
        self.stop = False
        try:
            print("Starting to record frequencies")
            with sd.InputStream(channels=1, callback=self.function, blocksize=self.blocksize, samplerate=self.samplerate):
                while True:
                    if self.stop == True:
                        break
                    time.sleep(self.delay)

        except Exception as exc:
            print(str(exc))
