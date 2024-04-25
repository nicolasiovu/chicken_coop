import pygame
import sys
import random

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Chicken
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('chicken game')
        self.screen = pygame.display.set_mode((1280, 720))
        self.game_display = pygame.Surface((60, 60), pygame.SRCALPHA)
        self.sidebar = pygame.Surface((560, 720), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        self.assets = {
            'grass': load_images('tiles/grass'),
            'chicken': load_image('entities/chicken.png'),
            'chicken/idle_down': Animation(load_images('entities/chicken/idle_down')),
            'chicken/idle_right': Animation(load_images('entities/chicken/idle_right')),
            'chicken/idle_up': Animation(load_images('entities/chicken/idle_up')),
            'chicken/run_right': Animation(load_images('entities/chicken/run_right')),
            'chicken/run_down': Animation(load_images('entities/chicken/run_down')),
            'chicken/run_up': Animation(load_images('entities/chicken/run_up'))
        }

        self.movement = [False, False, False, False]
        self.player = Chicken(self, (2, 2), (16, 16))

        self.tilemap = Tilemap(self, tile_size=20)

        self.level = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

    def run(self):
        pixels_moved = 0
        screen_w = 60
        screen_h = 60
        while True:
            self.screen.fill((0, 0, 0, 0))
            self.game_display.fill((0, 0, 0, 0))
            self.sidebar.fill((90, 0, 0))

            self.tilemap.render(self.game_display)

            self.player.update((self.movement[1] - self.movement[0],
                                self.movement[3] - self.movement[2]))

            if any(self.movement):
                pixels_moved += 1
            if pixels_moved == 20:
                self.movement = [False, False, False, False]
                pixels_moved = 0
            self.player.render(self.game_display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pass
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_n and pixels_moved == 0:
                        direction = random.randint(0, 3)
                        self.movement[direction] = True
                    if event.key == pygame.K_r:

                        if screen_w*2 < 960:
                            screen_w *= 2
                            screen_h *= 2
                            self.game_display = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
                            print(screen_w, screen_h)

            self.screen.blit(
                pygame.transform.scale(self.game_display, (720, 720)), (0, 0))
            self.screen.blit(self.sidebar, (720, 0))

            pygame.display.update()
            self.clock.tick(60)


Game().run()
