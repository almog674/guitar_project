from os import access
import pygame


class auto_button:
    def __init__(self, text, window, width, height, pos, function, animation=True):
        self.window = window
        self.active = False
        self.pressed = False
        self.function = function
        self.radius = int(width / 2)
        self.animation = animation

        # The button itself
        self.rect = pygame.Rect(pos, (width, height))
        self.rect_color = '#efefef'

        # Text
        font = pygame.font.SysFont(None, 42)
        self.text = font.render(text, 1, '#000000')
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self):
        circle = pygame.draw.rect(self.window, self.rect_color,
                                  self.rect, border_radius=self.radius)

        self.check_click()

        if self.animation:
            if self.active:
                self.rect_color = '#ff0000'
            else:
                self.rect_color = '#efefef'

        self.window.blit(self.text, self.text_rect)

    def check_click(self):
        mouse_pos = list(pygame.mouse.get_pos())
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.function()
                    self.active = not self.active
                    self.pressed = False
