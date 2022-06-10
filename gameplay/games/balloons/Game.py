import pygame
import random
import time
import threading

from gameplay.games.balloons.Enemy import Enemy
from gameplay.games.balloons.Player import Player
from global_state import Global_State
from music.tuner.Tab_Player_Proccesor import Tab_Player_Proccesor
from music.tuner.Live_recorder import Live_Recorder


class Game:
    difficulty_map = {0: ['Easy', (0, 255, 0)], 1: [
        'Medium', (255, 255, 0)], 2: ['Hard', (255, 255, 0)]}

    def __init__(self, music_converter, player, difficulty):
        self.music_converter = music_converter
        self.difficulty = difficulty
        self.player = player

        # Remove after authentication is okay
        if not player:
            self.player = Player()

        self.enemies_list = []
        self.note_detector = None
        self.boss_exist = False
        self.pause = False
        self.points = 0
        self.active = True

        self.font = pygame.font.SysFont('comicsans', 24)
        self.last_time = time.time()

        self.level = 0
        self.max_enemies = 3 + difficulty
        self.enemy_vel = 0.5 + self.level

        self.min_enemy_len = 1 + (difficulty * self.level)
        self.max_enemy_len = 3 + (difficulty * self.level)

        self.note_detector = Tab_Player_Proccesor(
            WINDOW_SIZE=12000, WINDOW_STEP=12000, S_rate=48000, NUM_HPS=3)
        self.initialize_recorder()
        self.recorder_thread.start()

    def initialize_recorder(self):
        self.recorder = Live_Recorder(
            function=self.note_detector.callback, blocksize=self.note_detector.WINDOW_SIZE, samplerate=self.note_detector.SAMPLE_FREQ, delay=0.05)
        self.recorder_thread = threading.Thread(
            target=self.recorder.start_recording)

    def initialize_game(self, difficulty):
        self.difficulty = difficulty
        self.enemies_list = []
        self.note_detector = None
        self.boss_exist = False
        self.pause = False
        self.points = 0
        self.last_time = time.time()
        self.initialize_recorder()
        self.recorder_thread.start()

    def render_game(self, screen):
        # 1) Draw the game
        self.draw(screen)

        # 2) Get time delta
        dt = time.time() - self.last_time
        dt *= 60
        self.last_time = time.time()

        if not self.pause:
            # 3) Enemies loop
            for enemy in self.enemies_list:
                # 2.1 Check if hit the floor
                if enemy.pos[1] >= Global_State.HEIGHT - 30:
                    self.active = False
                    self.recorder.stop = True

                if not enemy.active:
                    print('inactive')
                    if enemy.is_boss:
                        self.points += 5
                        self.level += 1
                        self.boss_exist = False
                    else:
                        self.points += 1
                    self.enemies_list.remove(enemy)

                # 2.2 Check if current tab == enemy.tab_list[cursor]
                if self.note_detector.closest_note == enemy.notes_list[0]:
                    enemy.move_tab()

                # 2.3 move the enemy
                enemy.move(dt)

                # 2.4 draw the enemy
                enemy.draw(screen)

            # 4) Generation loop
            self.generate_enemies(dt)
        else:
            pass
            # Go to pause scene

    def draw(self, screen):
        # Draw the background
        background_url = 'gameplay\games\\balloons\\assets\\background.png'
        background_image = pygame.transform.scale(
            pygame.image.load(background_url), (Global_State.WIDTH, Global_State.HEIGHT)).convert()
        screen.blit(background_image, (0, 0))

        # Draw the labels
        self.draw_labels(screen)

    def generate_enemies(self, dt):
        if self.boss_exist:
            return
        if len(self.enemies_list) >= self.max_enemies:
            return
        if self.points % 1 == 0 and self.points > 0:
            # Generate boss
            self.generate_boss()
            self.boss_exist = True
        if random.randint(1, 1.5 * 60) == 1:
            # Generate Enemy
            self.generate_enemy()

    def generate_enemy_pos(self):
        return random.randint(15, Global_State.WIDTH - 50), -random.randint(0, 200)

    def generate_enemy(self):
        x_pos, y_pos = self.generate_enemy_pos()
        enemy_len = random.randint(self.min_enemy_len, self.max_enemy_len)
        enemy = Enemy([x_pos, y_pos], self.enemy_vel,
                      enemy_len, self.music_converter)
        self.enemies_list.append(enemy)

    def generate_boss(self):
        x_pos, y_pos = self.generate_enemy_pos()
        enemy_len = random.randint(
            self.min_enemy_len * 5, self.max_enemy_len * 5)
        enemy = Enemy([x_pos, y_pos], self.enemy_vel / 2,
                      enemy_len, self.music_converter, True)
        self.enemies_list.append(enemy)

    def draw_labels(self, screen):
        # Draw the difficulty
        difficulty_text = f'Difficulty: {self.difficulty_map[self.difficulty][0]}'
        difficulty_color = self.difficulty_map[self.difficulty][1]
        difficulty_label = self.font.render(
            difficulty_text, 1, difficulty_color)
        # Draw the score
        score_label = self.font.render(
            f'Score: {self.points}', 1, difficulty_color)
        # Draw the name
        name_label = self.font.render(
            f'Name: {self.player.name}', 1, (255, 0, 0))
        # Draw the best score
        best_score_label = self.font.render(
            f'Best Score: {self.player.best_score}', 1,  (255, 0, 0))

        screen.blit(name_label, (10, 10))
        screen.blit(best_score_label, (10, name_label.get_height() + 10))

        screen.blit(difficulty_label, (Global_State.WIDTH -
                    difficulty_label.get_width() - 10, 10))
        screen.blit(score_label, (Global_State.WIDTH -
                    best_score_label.get_width() - 10, difficulty_label.get_height() + 10))
