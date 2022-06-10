import math
import pygame


class strings_buttons:
    def __init__(self, string_focus):
        self.strings = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
        self.focused = string_focus[0]
        self.change_focus = string_focus[1]

        self.string_width = 250
        self.string_height = 75
        self.margin = 150
        self.margin_y = 20

        self.pressed = False

        self.start_y_point = 450

        self.font = pygame.font.SysFont('comicsans', 42)

    def draw(self, window, focused):
        for index, string in enumerate(self.strings):
            column = math.floor((index + 1) / 4)
            row = index % 3
            color = (255, 0, 255)

            # Draw the rect
            x = ((window.get_width() / 2) - (self.string_width + self.margin / 2)) + \
                (column * (self.string_width + self.margin))
            y = self.start_y_point + \
                (row * (self.string_height + self.margin_y))
            container = pygame.Rect(
                (x, y), (self.string_width, self.string_height))

            if focused == string:
                color = (255, 0, 0)

            pygame.draw.rect(window, color, container)

            self.check_for_click(container, string)

            # Draw the text
            text = self.font.render(string, 1, (0, 0, 0))
            text_rect = text.get_rect(center=container.center)
            window.blit(text, text_rect)

    def check_for_click(self, container, string):
        mouse_pos = list(pygame.mouse.get_pos())
        if container.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.change_focus(string)
                    self.pressed = False
