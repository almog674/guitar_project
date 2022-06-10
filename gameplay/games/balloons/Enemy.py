import pygame
import random
from music.Music_converter import Music_Converter


class Enemy:
    def __init__(self, pos, vel, enemy_len, converter,  is_boss=False):
        self.pos = pos
        self.vel = vel
        self.is_boss = is_boss
        self.converter = converter

        self.picture = self.initialize_picture()
        self.enemy_len = enemy_len
        self.tab_list, self.notes_list = self.get_tabs(enemy_len)

        self.tab_width = 20
        self.tab_height = 40
        self.tab_margin = 5
        self.tab_font = pygame.font.SysFont('comicsans', 18)

        self.neck_x = self.pos[0] - 35
        self.neck_width = 125
        self.get_neck_height()

        self.strings_x = [self.neck_x + (i * (self.neck_width / 7))
                          for i in range(1, 7)]

        self.cursor = 0
        self.active = True

    def initialize_picture(self):
        if self.is_boss:
            url = 'gameplay\games\\balloons\\assets\enemies\\10.png'
        else:
            picture_number = random.randint(1, 3)
            url = f'gameplay\games\\balloons\\assets\enemies\\{picture_number}.png'

        picture = pygame.transform.scale(
            pygame.image.load(url), (60, 100)).convert()
        picture.set_colorkey((255, 255, 255))
        return picture

    def get_neck_height(self):
        base_height = len(self.tab_list) * \
            (self.tab_height + self.tab_margin)
        additional_height = 20
        self.neck_height = base_height + additional_height

    def draw(self, screen):
        # 1) Draw the picture
        screen.blit(self.picture, self.pos)

        # 2) Draw the neck
        self.draw_neck(screen)

    def draw_neck(self, screen):
        y_pos = self.pos[1] - self.neck_height + 15
        # Draw empty neck accourding to the lenght
        neck_rect = pygame.Rect(
            self.neck_x, y_pos, self.neck_width, self.neck_height)
        pygame.draw.rect(screen, (50, 50, 50), neck_rect)

        for i in range(1, 7):
            pygame.draw.line(
                screen, (200, 200, 200), (self.strings_x[i - 1], self.pos[1] + 15), (self.strings_x[i - 1], y_pos), 2)

        # Fill the neck with tabs
        # draw_tab_list = reversed(self.tab_list)
        for i, tab in enumerate(self.tab_list):
            tab_x_pos = self.strings_x[int(
                tab[1]) - 1] - self.tab_width / 2
            tab_y_pos = y_pos + ((len(self.tab_list) - i) * self.tab_height +
                                 (len(self.tab_list) - i) * self.tab_margin) - self.tab_height

            tab_color = (255, 0, 0)
            # if self.cursor > i:
            #     tab_color = (0, 255, 0)

            pygame.draw.rect(screen, tab_color, (tab_x_pos,
                             tab_y_pos, self.tab_width, self.tab_height))

            tab_label = self.tab_font.render(tab[2], 1, (255, 255, 255))
            label_x = tab_x_pos + (self.tab_width / 2 -
                                   tab_label.get_width() / 2)
            label_y = tab_y_pos + \
                (self.tab_height / 2 - tab_label.get_height() / 2)
            screen.blit(tab_label, (label_x, label_y))

    def get_tabs(self, lenght):
        tab_list = []
        for i in range(lenght):
            string = random.randint(1, 6)
            part = random.randint(1, 10)
            tab_list.append([f'{string}-{part}', string, str(part)])
        # Takes each tab and convert to note
        note_list = list(map(self.converter.tab_to_note,
                             [tab[0] for tab in tab_list]))
        return tab_list, note_list

    def move_tab(self):
        # if self.cursor == len(self.notes_list) - 1:
        #     self.active = False
        # else:
        #     self.cursor += 1
        if len(self.notes_list) == 1:
            self.active = False
        else:
            self.notes_list.pop(0)
            self.tab_list.pop(0)
            self.get_neck_height()
            if self.is_boss:
                self.pos[1] -= (self.vel * 20)

    def move(self, dt):
        self.pos[1] += self.vel * dt
