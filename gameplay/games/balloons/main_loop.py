import pygame
import time
from .Game import Game
from global_state import Global_State
from music.Music_converter import Music_Converter


class ballon_game:
    def __init__(self, screen, player=Global_State.PLAYER, difficulty=2):
        self.music_converter = Music_Converter()
        self.game = Game(self.music_converter, player, difficulty)
        self.screen = screen
        # initialize the recorder

    def render(self):
        if self.game.active:
            # render game
            self.game.render_game(self.screen)
        else:
            pass
        # Go to end scene

    def finish_game(self):
        pass
