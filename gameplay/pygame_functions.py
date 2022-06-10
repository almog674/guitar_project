from global_state import Global_State
import pygame


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def get_exact_middle(sur1, sur2):
    width = (sur1.get_width() / 2) - (sur2.get_width() / 2)
    height = (sur1.get_height() / 2) - (sur2.get_height() / 2)
    return width, height


def change_app_scene(scene):
    quit_game()
    Global_State.APP_SCENE = scene


def quit_scene(scene):
    Global_State.FOCUS = 0
    Global_State.SCENE = scene


def quit_game():
    # Quit the game and move to the Qt app
    Global_State.FOCUS = 0
    Global_State.APP = 'APP'
    pygame.quit()
