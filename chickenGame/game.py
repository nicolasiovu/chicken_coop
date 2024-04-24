import pygame
import sys

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Chicken


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('chicken game')
        self.screen = pygame.display.set_mode((1280, 720))
        self.game_display = pygame.Surface((120, 90), pygame.SRCALPHA)
        self.sidebar = pygame.Surface((320, 720), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        self.assets = {
            'trampled_grass': load_images('tiles/grass'),
            'chicken': load_image('entities/chicken.png'),
            'chicken/idle_down': Animation(load_images('entities/chicken/idle_down')),
            'chicken/idle_right': Animation(load_images('entities/chicken/idle_right')),
            'chicken/idle_up': Animation(load_images('entities/chicken/idle_up')),
            'chicken/run_right': Animation(load_images('entities/chicken/run_right')),
            'chicken/run_down': Animation(load_images('entities/chicken/run_down')),
            'chicken/run_up': Animation(load_images('entities/chicken/run_up'))
        }

        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.player = Chicken(self, (0, 0), (16, 16))

    def run(self):
        while True:
            self.screen.fill((0, 0, 0, 0))
            self.game_display.fill((0, 0, 0, 0))
            self.sidebar.fill((90, 0, 0))

            self.player.update((self.movement_x[1] - self.movement_x[0],
                                self.movement_y[1] - self.movement_y[0]))
            self.player.render(self.game_display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_x[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement_x[1] = True
                    if event.key == pygame.K_UP:
                        self.movement_y[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement_y[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_x[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement_x[1] = False
                    if event.key == pygame.K_UP:
                        self.movement_y[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement_y[1] = False

            print(self.player.action)

            self.screen.blit(
                pygame.transform.scale(self.game_display, (960, 720)), (0, 0))
            self.screen.blit(self.sidebar, (960, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().run()
