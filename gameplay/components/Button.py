import pygame
from global_state import Global_State


class Button:
    def __init__(self, text, width, height, pos, elevetion, function, focus_number=-1):
        # Core attrebutes
        self.pressed = False
        self.elevation = elevetion
        self.dynamic_elevation = elevetion
        self.original_y_pos = pos[1]
        self.function = function

        self.focus_number = focus_number

        # Top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475f77'

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevetion))
        self.bottom_color = '#354B5E'

        # Text
        font = pygame.font.SysFont(None, 28)
        self.text = font.render(text, 1, '#ffffff')
        self.text_rect = self.text.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # Elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color,
                         self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color,
                         self.top_rect, border_radius=12)
        screen.blit(self.text, self.text_rect)

        if Global_State.USE_GUITAR:
            self.check_guitar_click()
        else:
            self.check_click()

    def check_guitar_click(self):
        if self.focus_number == Global_State.FOCUS:
            self.top_color = '#d74b4b'
            if Global_State.ENTER_PRESSED:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.function()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475f77'

    def check_click(self):
        mouse_pos = list(pygame.mouse.get_pos())
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#d74b4b'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.function()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475f77'
