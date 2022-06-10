from ast import Global
import pygame
import time

from global_state import Global_State

from ...pygame_functions import get_exact_middle, quit_scene, quit_game
from .auto_button import auto_button
from .strings_buttons import strings_buttons
from .display_tuning import display_tuning

from ...components.Button import Button


class tuner_scene_ui:
    def __init__(self, screen, string_focus, change_to_auto, parent):
        self.title_font = pygame.font.SysFont('arial', 62)
        self.screen = screen
        self.parent = parent
        self.type = parent.type
        if self.type == 'regular':
            self.text = 'Tuner'
            self.auto_button = auto_button('A',
                                           self.screen, 50, 50, (self.screen.get_width() - 85, 35), change_to_auto)
            self.exit_button = auto_button('X',
                                           self.screen, 50, 50, (35, 35), lambda: quit_scene('balloon game'), animation=False)
        else:
            self.focused = string_focus[0]
            self.text = f'Please tuner {self.focused}'
            button_width = 200
            button_height = 50
            self.tuner_button = Button(
                'Go to tuner', button_width, button_height, (Global_State.WIDTH / 2 - button_width - 100, Global_State.HEIGHT - 100), 8, lambda: parent.exit_start_tuner_scene('tuner'), 0)
            self.login_button = Button(
                'Go to login', button_width, button_height, (Global_State.WIDTH / 2 + 100, Global_State.HEIGHT - 100), 8, lambda: parent.exit_tuner_to_app(), 1)

        self.srings_buttons = strings_buttons(string_focus)
        self.display_tuning = display_tuning()

    def draw(self, string_focus, tune_args, finish=False):
        self.screen.fill((30, 30, 30))
        # Draw the title
        title = self.title_font.render(
            self.text, 1, (255, 255, 255))
        self.screen.blit(
            title, (get_exact_middle(self.screen, title)[0], 20))

        # Draw the auto_button & exit_button
        if self.type == 'regular':
            self.auto_button.draw()
            self.exit_button.draw()
            self.srings_buttons.draw(self.screen, string_focus)
        elif finish:
            self.text = f'Guitar tuned successfuly!'
            self.tuner_button.draw(self.screen)
            self.login_button.draw(self.screen)
        else:
            self.text = f'Please tuner {string_focus}'
            self.srings_buttons.draw(self.screen, string_focus)

        # Draw the display
        self.display_tuning.draw(
            self.screen, tune_args[0], tune_args[1], tune_args[2])
