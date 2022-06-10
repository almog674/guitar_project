import librosa
from .Tuner_Proccesor import Tuner_Proccesor
import os
import numpy as np


class Auto_Tuner(Tuner_Proccesor):
    def __init__(self, S_rate=44100, WINDOW_SIZE=44100, WINDOW_STEP=12000, NUM_HPS=5, POWER_THRESH=0.000001, WHITE_NOISE_THRESH=0.2, update=lambda x: x):
        super().__init__(S_rate=S_rate, WINDOW_SIZE=WINDOW_SIZE, WINDOW_STEP=WINDOW_STEP,
                         NUM_HPS=NUM_HPS, POWER_THRESH=POWER_THRESH, WHITE_NOISE_THRESH=WHITE_NOISE_THRESH)
        self.update = update
        self.note = 'E2'

    def print_closest_note(self, max_freq):
        closest_note, closest_pitch = self.find_closest_note(max_freq)
        max_freq = round(max_freq, 1)
        closest_pitch = round(closest_pitch, 1)

        # note that this is a ringbuffer
        self.noteBuffer.insert(0, closest_note)
        self.noteBuffer.pop()

        note = self.find_closest_string(max_freq)
        tuned, direction, gap = self.check_if_note(
            max_freq, librosa.note_to_hz(note))
        self.update(note, gap, direction, tuned)

    def callback(self, indata, frames, time, status):
        max_freq, error = self.process_note(indata, status)
        if error:
            pass
        else:
            self.print_closest_note(max_freq)

    def find_closest_string(self, max_freq):
        strings = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
        notes = strings.copy()

        distance_list = []
        for string in strings:
            string = librosa.note_to_hz(string)
            string_distance = abs(max_freq - string)
            distance_list.append(string_distance)
        closest_freq_index = distance_list.index(min(distance_list))
        closest_string = notes[closest_freq_index]
        return closest_string
