import pygame
import sys
import random

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Chicken, Rooster
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('chicken game')
        self.screen = pygame.display.set_mode((1280, 720))
        self.game_display = pygame.Surface((60, 60), pygame.SRCALPHA)
        self.sidebar = pygame.Surface((560, 720), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        self.stages = [60, 80, 100, 140, 180, 240, 300, 400, 500, 600, 720]
        self.stage = 0

        self.resolution = 60

        self.assets = {
            'grass': load_images('tiles/grass'),
            'fence': load_images('tiles/placeable'),
            'chicken': load_image('entities/chicken.png'),
            'chicken/idle_down': Animation(load_images('entities/chicken/idle_down')),
            'chicken/idle_right': Animation(load_images('entities/chicken/idle_right')),
            'chicken/idle_up': Animation(load_images('entities/chicken/idle_up')),
            'chicken/run_right': Animation(load_images('entities/chicken/run_right')),
            'chicken/run_down': Animation(load_images('entities/chicken/run_down')),
            'chicken/run_up': Animation(load_images('entities/chicken/run_up')),
            'rooster': load_image('entities/chicken.png'),
            'rooster/idle_down': Animation(load_images('entities/rooster/idle_down')),
            'rooster/idle_right': Animation(load_images('entities/rooster/idle_right')),
            'rooster/idle_up': Animation(load_images('entities/rooster/idle_up')),
            'rooster/run_right': Animation(load_images('entities/rooster/run_right')),
            'rooster/run_down': Animation(load_images('entities/rooster/run_down')),
            'rooster/run_up': Animation(load_images('entities/rooster/run_up'))
        }

        self.selected_fence = 0

        self.movement = [False, False, False, False]

        self.chickens = []

        self.tilemap = Tilemap(self, tile_size=20)

        self.level = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

    def run(self):
        pixels_moved = 0
        size_factor = 720 / self.resolution
        chicken_movement = []

        while True:
            self.screen.fill((0, 0, 0, 0))
            self.game_display.fill((0, 0, 0, 0))
            self.sidebar.fill((90, 0, 0))

            self.tilemap.render(self.game_display)
            self.tilemap.render_fences(self.game_display)

            current_tile_img = self.assets['fence'][self.selected_fence].copy()
            current_tile_img.set_alpha(100)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / size_factor, mouse_pos[1] / size_factor)
            tile_pos = (int((mouse_pos[0]) // self.tilemap.tile_size),
                        int((mouse_pos[1]) // self.tilemap.tile_size))

            self.game_display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size,
                                                      tile_pos[1] * self.tilemap.tile_size))

            if chicken_movement:
                pixels_moved += 1
                for i in range(len(self.chickens)):
                    self.chickens[i].update(chicken_movement[i])
            else:
                for chicken in self.chickens:
                    chicken.update()
            if pixels_moved == 20:
                chicken_movement = []
                pixels_moved = 0
            for chicken in self.chickens:
                chicken.render(self.game_display)
            self.tilemap.render_front_fences(self.game_display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.selected_fence -= 1
                        if self.selected_fence == -1:
                            self.selected_fence = 3
                    elif event.y < 0:
                        self.selected_fence += 1
                        if self.selected_fence == 4:
                            self.selected_fence = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = (int(mouse_pos[0] // self.tilemap.tile_size),
                               int(mouse_pos[1] // self.tilemap.tile_size))
                        self.tilemap.place_fence(pos, self.selected_fence)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_n and pixels_moved == 0:
                        for chicken in self.chickens:
                            movement = self.move_chicken(chicken)
                            chicken_movement.append(movement)
                    if event.key == pygame.K_s:
                        x = int(self.game_display.get_width() / 20)
                        coordinates = (2 + 20 * random.randint(0, x-1), 2 + 20 * random.randint(0, x-1))
                        self.chickens.append(Chicken(self, coordinates, (16, 16)))
                    if event.key == pygame.K_r:
                        self.stage += 1
                        if self.stage > len(self.stages) - 1:
                            self.stage = 0
                        self.resolution = self.stages[self.stage]
                        size_factor = 720 / self.resolution
                        self.game_display = pygame.Surface((self.resolution, self.resolution))

            self.screen.blit(
                pygame.transform.scale(self.game_display, (720, 720)), (0, 0))
            self.screen.blit(self.sidebar, (720, 0))

            pygame.display.update()
            self.clock.tick(60)

    def move_chicken(self, chicken: Chicken) -> tuple[int, int]:
        pos = (int(chicken.pos[0] // self.tilemap.tile_size),
               int(chicken.pos[1] // self.tilemap.tile_size))
        fences = self.tilemap.get_fences_on_tile(pos)
        if all([fence == 1 for fence in fences]):
            return 0, 0
        direction = random.randint(0, 3)
        unseen = [0, 1, 2, 3]
        while fences[direction] != 0:
            direction = unseen[random.randint(0, len(unseen) - 1)]
            unseen.remove(direction)
        if direction == 0:
            return 0, 1
        elif direction == 1:
            return -1, 0
        elif direction == 2:
            return 0, -1
        else:
            return 1, 0



Game().run()
