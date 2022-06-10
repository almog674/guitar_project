from threading import Thread

from global_state import Global_State
from .tuner_scene_ui import tuner_scene_ui

from music.tuner.Manuel_Tuner import Manuel_Tuner
from music.tuner.Auto_Tuner import Auto_Tuner
from music.tuner.Live_recorder import Live_Recorder

from ...pygame_functions import quit_scene, quit_game


class Tuner_scene:
    def __init__(self, screen, type='regular'):
        self.screen = screen
        self.auto = False
        self.type = type
        self.finish = True
        if self.type == 'regular':
            self.focused = 'E2'
        else:
            self.notes = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
            self.cursor = 0
            self.focused = self.notes[self.cursor]

        self.direction = 'up'
        self.abs_diffrent = 0
        self.tuned = False
        self.new_tuned = 0

        self.manuel_tuner = Manuel_Tuner(
            self.focused, WINDOW_SIZE=48000, WINDOW_STEP=12000, S_rate=48000, update=self.update_parameters)
        self.auto_tuner = Auto_Tuner(
            WINDOW_SIZE=48000, WINDOW_STEP=12000, S_rate=48000, update=self.update_parameters)

        self.initialize_recorder()

        self.ui = tuner_scene_ui(self.screen,
                                 (self.focused, self.change_focuse), self.change_to_auto, self)

    def initialize_recorder(self):
        self.recorder = Live_Recorder(
            function=self.process_sound, blocksize=self.manuel_tuner.WINDOW_SIZE, samplerate=self.manuel_tuner.SAMPLE_FREQ, delay=0.05)
        self.recording_thread = Thread(target=self.recorder.start_recording)
        self.recording_thread.start()

    def process_sound(self, indata, *args):
        if self.auto == True:
            self.auto_tuner.callback(indata, *args)
        else:
            self.manuel_tuner.callback(indata, *args)

    def update_focus(self):
        if self.tuned:
            if (len(self.notes) - 1) > self.cursor:
                self.cursor += 1
                self.change_focuse(self.notes[self.cursor])
            else:
                self.finish = True
            self.tuned = False

    def render(self):
        if self.type != 'regular':
            self.update_focus()
        self.ui.draw(self.focused, (self.abs_diffrent,
                     self.direction, self.tuned), self.finish)

    def change_focuse(self, new_focus):
        self.focused = new_focus
        self.manuel_tuner.change_note(new_focus)

    def update_parameters(self, note, abs_different, direction, tuned):
        if note:
            self.focused = note
        self.abs_diffrent = abs_different
        self.direction = direction
        self.tuned = tuned

    def change_to_auto(self):
        self.auto = not self.auto

    def exit_tuner(self):
        self.recorder.stop = True

    def exit_start_tuner_scene(self, scene):
        self.exit_tuner()
        quit_scene(scene)
        Global_State.NEED_TUNING = False

    def exit_tuner_to_app(self):
        self.exit_tuner()
        quit_game()
