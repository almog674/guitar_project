from tkinter.tix import Tree
import pygame
from global_state import Global_State
from .pygame_functions import quit_game

from .scenes.welcome_scene.welcome_scene import Welcome_Scene
from .scenes.tuner_scene.tuner_scene import Tuner_scene

from .games.balloons.main_loop import ballon_game


class GamePlay:
    def __init__(self):
        WINDOW_WIDTH = Global_State.WIDTH
        WINDOW_HEIGTH = Global_State.HEIGHT

        self.fps = 60
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
        pygame.display.set_caption('Prevent collider')

        # Scenes
        self.welcome_scene = None
        self.tuner_scene = None
        self.tuner_reg_scene = None

        # Games
        self.ballon_game = None

    def main_loop(self):
        finish = False
        while not finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                if event.type == pygame.KEYDOWN and event.unicode == 'c':
                    if not Global_State.USE_GUITAR:
                        Global_State.USE_GUITAR = True
                    else:
                        Global_State.USE_GUITAR = False

            if Global_State.SCENE == 'welcome':
                if not self.welcome_scene:
                    self.welcome_scene = Welcome_Scene(
                        self.screen)
                else:
                    self.welcome_scene.render()
            elif Global_State.NEED_TUNING:
                if not self.tuner_scene:
                    self.tuner_scene = Tuner_scene(
                        self.screen, type='no')
                else:
                    self.tuner_scene.render()
            elif Global_State.SCENE == 'tuner':
                if not self.tuner_reg_scene:
                    self.tuner_reg_scene = Tuner_scene(
                        self.screen)
                else:
                    self.tuner_reg_scene.render()
            elif Global_State.SCENE == 'balloon game':
                if not self.ballon_game:
                    self.ballon_game = ballon_game(
                        self.screen)
                else:
                    self.ballon_game.render()

            pygame.display.flip()
            self.clock.tick(self.fps)
        quit_game()


def run_game():
    gameplay = GamePlay()
    gameplay.main_loop()
