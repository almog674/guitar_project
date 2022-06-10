import pyaudio
import time
import numpy as np

from .Live_recorder import Live_Recorder
from .Auto_Tuner import Auto_Tuner
from .Manuel_Tuner import Manuel_Tuner

notes = ['E2', 'A3', 'F#2', 'C#4']

# Parameters that icorilated with speed = Window_size and window_step


class Tuner:
    def __init__(self, note):
        self.note = note
        self.proccesor = Auto_Tuner(
            WINDOW_SIZE=12000, WINDOW_STEP=12000, S_rate=48000)
        self.recorder = Live_Recorder(
            function=self.proccesor.callback, blocksize=self.proccesor.WINDOW_SIZE, samplerate=self.proccesor.SAMPLE_FREQ, delay=0.05)
        self.recorder.start_recording()


tuni = Tuner('E4')
