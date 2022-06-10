from .Tuner_Proccesor import Tuner_Proccesor
import librosa


class Manuel_Tuner(Tuner_Proccesor):
    def __init__(self, note='E2', S_rate=44100, WINDOW_SIZE=44100, WINDOW_STEP=12000, NUM_HPS=5, POWER_THRESH=0.000001, WHITE_NOISE_THRESH=0.2, update=lambda x: x):
        super().__init__(S_rate=S_rate, WINDOW_SIZE=WINDOW_SIZE, WINDOW_STEP=WINDOW_STEP,
                         NUM_HPS=NUM_HPS, POWER_THRESH=POWER_THRESH, WHITE_NOISE_THRESH=WHITE_NOISE_THRESH)

        self.update = update
        if note:
            self.freq = round(librosa.note_to_hz(note), 1)
            self.note = note

    def callback(self, indata, frames, time, status):
        max_freq, error = self.process_note(indata, status)
        if error:
            pass
        else:
            tuned, direction, gap = self.check_if_note(max_freq, self.freq)
            self.update(None, gap, direction, tuned)

    def change_note(self, new_note):
        self.freq = round(librosa.note_to_hz(new_note), 1)
        self.note = new_note
