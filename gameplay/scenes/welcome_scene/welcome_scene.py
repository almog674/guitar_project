from gameplay.components.Button import Button
from ...pygame_functions import quit_scene
import pygame


class Welcome_Scene:
    def __init__(self, screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.title_font = pygame.font.SysFont('comicsans', 64)
        self.button = Button('Start Here', 200, 50, (self.width / 2 -
                                                     100, self.height - 100), 8, lambda: quit_scene('tuner'))

    def render(self):
        font_label = self.title_font.render(
            'Welcome to the game!', 1, (255, 255, 255))

        self.screen.blit(font_label, (self.width / 2 -
                         font_label.get_width() / 2, 50))
        self.button.draw(self.screen)
