import pygame
from global_state import Global_State


class Base_Widget:
    def __init__(self, height, width, pos, foucs_number=-1):
        self.height = height
        self.width = width
        self.pos = pos
        self.focus_number = foucs_number

        self.rect = pygame.Rect(pos[0], pos[1], width, height)

        self.onFocus = False
        self.onHover = False
        self.onClick = False
        self.pressed = False

    def check_focus(self):
        if self.focus_number == Global_State.FOCUS:
            self.onFocus = True
        else:
            self.onFocus = False

    def check_hover(self):
        mouse_pos = list(pygame.mouse.get_pos())
        if self.rect.collidepoint(mouse_pos):
            self.onHover = True
        else:
            self.onHover = False

    def check_click(self):
        # Important! need to call "check_hover" to make it works
        if self.onHover:
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.onClick = False
            else:
                self.onClick = False
                if self.pressed == True:
                    self.onClick = True
                    self.pressed = False
        else:
            self.onClick = False

    def check_guitar_click(self):
        # Important! need to call "check_focus" to make it works
        if self.onFocus:
            if Global_State.ENTER_PRESSED:
                self.pressed = True
                self.onClick = False
            else:
                self.onClick = False
                if self.pressed == True:
                    self.onClick = True
                    self.pressed = False
        else:
            self.onClick = False
