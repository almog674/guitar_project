from librosa.core.convert import hz_to_note
import numpy as np
import librosa
from music21.note import Note, Rest


class Music_Converter:
    def __init__(self):
        self.tabs_map = self.get_tab_map()
        self.tab_map_keys = list(self.tabs_map.keys())
        self.tab_map_values = list(self.tabs_map.values())

    def get_tab_map(self):
        tab_map = {}
        base_tones = dict(
            zip(range(1, 7), [82.4, 110, 146.8, 196, 246.9, 329.6]))

        for i in range(1, 7):
            for j in range(13):
                tab_map[f'{i}-{j}'] = round(2**(j / 12) * base_tones[i], 1)

        return tab_map

    def note_to_tab(self, note, Low=True):
        if note == '':
            return note

        # convert note to freq
        freq = round(librosa.note_to_hz(note), 1)

        # find key of the frequency in tab map
        index = self.tab_map_values.index(freq)
        tab = self.tab_map_keys[index]

        # Try to find the same freq in lower part of the guitar
        if Low:
            string, part = tab.split('-')
            string, part = int(string), int(part)
            if part >= 5:
                string += 1
                part -= 5
            tab = f'{string}-{part}'
        return tab

    def tab_to_note(self, tab):
        if tab == '':
            return tab

        # Get the freq related to the tab
        index = self.tab_map_keys.index(tab)
        freq = self.tab_map_values[index]

        # Get the note
        note = librosa.hz_to_note(freq)

        if '♯' in note:
            print('yes')
            note = note.replace('♯', '#')
        return note

    def format_stream(self, stream):
        notes_list = []
        for note in stream:
            if isinstance(note, Note):
                full_note = note.name + str(note.octave)
                notes_list.append(
                    {'tab': self.note_to_tab(full_note), 'duration': note.duration.quarterLength})
            elif isinstance(note, Rest):
                notes_list.append(
                    {'tab': '', 'duration': note.duration.quarterLength})
        return notes_list
