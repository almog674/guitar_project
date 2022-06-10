from .Tuner_Proccesor import Tuner_Proccesor
from .Auto_Tuner import Auto_Tuner
import librosa


class Tab_Player_Proccesor(Tuner_Proccesor):
    def __init__(self, S_rate=44100, WINDOW_SIZE=44100, WINDOW_STEP=12000, NUM_HPS=5, POWER_THRESH=0.000001, WHITE_NOISE_THRESH=0.2):
        super().__init__(S_rate=S_rate, WINDOW_SIZE=WINDOW_SIZE, WINDOW_STEP=WINDOW_STEP,
                         NUM_HPS=NUM_HPS, POWER_THRESH=POWER_THRESH, WHITE_NOISE_THRESH=WHITE_NOISE_THRESH)

        self.closest_note = None

    def callback(self, indata, frames, time, status):
        max_freq, error = self.process_note(indata, status)
        if error:
            self.closest_note = None
        else:
            closest_note, closest_pitch = self.find_closest_note(max_freq)
            self.closest_note = closest_note

    def change_note(self, new_note):
        self.freq = round(librosa.note_to_hz(new_note), 1)
        self.note = new_note
        self.detected = False
