import pygame
from global_state import Global_State


class display_tuning:
    def __init__(self):
        self.width = 650
        self.height = 300

        self.currect_x = 0

    def draw(self, window, abs_diffrent, direction, tuned):
        self.rect = pygame.Rect(
            Global_State.WIDTH / 2 - self.width / 2, 125, self.width, self.height)
        pygame.draw.rect(window, (0, 0, 0), self.rect, border_radius=2)
        self.draw_circle(window, self.rect.centerx,
                         self.rect.centery, abs_diffrent, direction, tuned)

    def draw_circle(self, window,  middle_x, middle_y, abs_diffrent, direction, tuned):
        radius = 30
        color = (255, 0, 0)

        if tuned:
            color = (0, 255, 0)
        if direction == 'up':
            abs_diffrent = -abs_diffrent

        target_x = middle_x + (abs_diffrent * 4)
        if abs_diffrent > 50:
            target_x = middle_x + (67 * 4)
        elif abs_diffrent < -50:
            target_x = middle_x + (-67 * 4)

        if target_x > self.currect_x:
            self.currect_x += 0.2 * abs(target_x - self.currect_x)
        else:
            self.currect_x -= 0.2 * abs(target_x - self.currect_x)

        center_points = (self.currect_x, middle_y)

        pygame.draw.rect(window, (255, 255, 255),
                         ((center_points[0] - 2.5, center_points[1]), (5, self.height / 2)))

        pygame.draw.circle(window, color, center_points, radius)
        pygame.draw.circle(window, (255, 255, 255), center_points, radius, 4)

        font = pygame.font.SysFont('arial', 24)
        label = font.render(str(round(abs_diffrent, 1)), 1, (0, 0, 0))
        window.blit(label, (center_points[0] - label.get_width() /
                    2, center_points[1] - label.get_height() / 2))
