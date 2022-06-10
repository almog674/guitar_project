import numpy as np
import os
import scipy.fftpack
import copy
import time

# Audio Packegas
import librosa
import librosa.display


class Tuner_Proccesor:
    def __init__(self, S_rate=44100, WINDOW_SIZE=44100, WINDOW_STEP=12000, NUM_HPS=5, POWER_THRESH=1e-6, WHITE_NOISE_THRESH=0.2):
        self.CONCERT_PITCH = 440
        self.ALL_NOTES = ["A", "A#", "B", "C", "C#",
                          "D", "D#", "E", "F", "F#", "G", "G#"]

        # General settings that can be changed by the user
        self.SAMPLE_FREQ = S_rate  # sample frequency in Hz
        self.WINDOW_SIZE = WINDOW_SIZE  # window size of the DFT in samples
        self.WINDOW_STEP = WINDOW_STEP  # step size of window
        self.NUM_HPS = NUM_HPS  # max number of harmonic product spectrums
        # tuning is activated if the signal power exceeds this threshold
        self.POWER_THRESH = POWER_THRESH
        self.CONCERT_PITCH = 440  # defining a1
        # everything under WHITE_NOISE_THRESH*avg_energy_per_freq is cut off
        self.WHITE_NOISE_THRESH = WHITE_NOISE_THRESH

        self.WINDOW_T_LEN = self.WINDOW_SIZE / \
            self.SAMPLE_FREQ  # length of the window in seconds
        # length between two samples in seconds
        self.SAMPLE_T_LENGTH = 1 / self.SAMPLE_FREQ
        # frequency step width of the interpolated DFT
        self.DELTA_FREQ = self.SAMPLE_FREQ / self.WINDOW_SIZE
        self.OCTAVE_BANDS = [50, 100, 200, 400,
                             800, 1600, 3200, 6400, 12800, 25600]
        self.HANN_WINDOW = np.hanning(self.WINDOW_SIZE)

    def find_closest_note(self, pitch):
        i = int(np.round(np.log2(pitch/self.CONCERT_PITCH)*12))
        closest_note = self.ALL_NOTES[i % 12] + str(4 + (i + 9) // 12)
        closest_pitch = self.CONCERT_PITCH*2**(i/12)
        return closest_note, closest_pitch

    def get_frequency(self, audio):
        # avoid spectral leakage by multiplying the signal with a hann window
        hann_samples = self.window_samples * self.HANN_WINDOW
        magnitude_spec = abs(scipy.fftpack.fft(
            hann_samples)[:len(hann_samples)//2])

        # supress mains hum, set everything below 62Hz to zero
        for i in range(int(62/self.DELTA_FREQ)):
            magnitude_spec[i] = 0

        # calculate average energy per frequency for the octave bands
        # and suppress everything below it
        for j in range(len(self.OCTAVE_BANDS)-1):
            ind_start = int(self.OCTAVE_BANDS[j]/self.DELTA_FREQ)
            ind_end = int(self.OCTAVE_BANDS[j+1]/self.DELTA_FREQ)
            ind_end = ind_end if len(
                magnitude_spec) > ind_end else len(magnitude_spec)
            avg_energy_per_freq = (np.linalg.norm(
                magnitude_spec[ind_start:ind_end], ord=2)**2) / (ind_end-ind_start)
            avg_energy_per_freq = avg_energy_per_freq**0.5
            for i in range(ind_start, ind_end):
                magnitude_spec[i] = magnitude_spec[i] if magnitude_spec[i] > self.WHITE_NOISE_THRESH * \
                    avg_energy_per_freq else 0

        # interpolate spectrum
        mag_spec_ipol = np.interp(np.arange(0, len(magnitude_spec), 1/self.NUM_HPS), np.arange(0, len(magnitude_spec)),
                                  magnitude_spec)
        mag_spec_ipol = mag_spec_ipol / \
            np.linalg.norm(mag_spec_ipol, ord=2)  # normalize it

        hps_spec = copy.deepcopy(mag_spec_ipol)

        # calculate the HPS
        for i in range(self.NUM_HPS):
            tmp_hps_spec = np.multiply(
                hps_spec[:int(np.ceil(len(mag_spec_ipol)/(i+1)))], mag_spec_ipol[::(i+1)])
            if not any(tmp_hps_spec):
                break
            hps_spec = tmp_hps_spec

        max_ind = np.argmax(hps_spec)
        # The frequency
        max_freq = max_ind * \
            (self.SAMPLE_FREQ/self.WINDOW_SIZE) / self.NUM_HPS
        return max_freq

    def check_signal_power(self):
        # skip if signal power is too low
        signal_power = (np.linalg.norm(self.window_samples,
                                       ord=2)**2) / len(self.window_samples)
        if signal_power < self.POWER_THRESH:
            # os.system('cls' if os.name == 'nt' else 'clear')
            # print("Closest note: ...")
            return False
        return True

    def define_static_variables(self):
        # define static variables
        if not hasattr(self, "window_samples"):
            self.window_samples = [0 for _ in range(self.WINDOW_SIZE)]
        if not hasattr(self, "noteBuffer"):
            self.noteBuffer = ["1", "2"]

    def get_new_samples(self, samples):
        # define static variables
        self.window_samples = np.concatenate(
            (self.window_samples, samples[:, 0]))  # append new samples
        self.window_samples = self.window_samples[len(
            samples[:, 0]):]  # remove old samples

    def check_if_note(self, max_freq, ideal_freq):
        # Check if the gap betwwen them is more than 1.5Hz
        gap = abs(max_freq - ideal_freq)

        if max_freq > ideal_freq:
            direction = 'down'
        else:
            direction = 'up'

        if gap < 1:
            tuned = True
        else:
            tuned = False

        return (tuned, direction, gap)

    def process_note(self, indata, status):
        self.define_static_variables()
        if status:
            return 0, status
        if any(indata):
            self.get_new_samples(indata)
            if self.check_signal_power() == False:
                return 0, 'no note is playing'
            max_freq = self.get_frequency(indata)
            return max_freq, None
        else:
            0, 'no input'
