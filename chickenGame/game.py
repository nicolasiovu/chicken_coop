import pygame
import sys
import random

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Chicken, Rooster
from scripts.ui import Button
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('chicken game')
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 100)
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
            'redfence': load_images('tiles/redplaceable'),
            'timer': load_image('entities/timer.png'),
            'hungerbar': load_images('entities/hungerbar'),
            'hunger': load_image('entities/hunger.png'),
            'feed': load_image('entities/feed.png'),
            'redfeed': load_image('entities/redfeed.png'),
            'chicken': load_image('entities/chicken.png'),
            'chicken/idle_down': Animation(
                load_images('entities/chicken/idle_down')),
            'chicken/idle_right': Animation(
                load_images('entities/chicken/idle_right')),
            'chicken/idle_up': Animation(
                load_images('entities/chicken/idle_up')),
            'chicken/run_right': Animation(
                load_images('entities/chicken/run_right')),
            'chicken/run_down': Animation(
                load_images('entities/chicken/run_down')),
            'chicken/run_up': Animation(load_images('entities/chicken/run_up')),
            'rooster': load_image('entities/chicken.png'),
            'rooster/idle_down': Animation(
                load_images('entities/rooster/idle_down')),
            'rooster/idle_right': Animation(
                load_images('entities/rooster/idle_right')),
            'rooster/idle_up': Animation(
                load_images('entities/rooster/idle_up')),
            'rooster/run_right': Animation(
                load_images('entities/rooster/run_right')),
            'rooster/run_down': Animation(
                load_images('entities/rooster/run_down')),
            'rooster/run_up': Animation(load_images('entities/rooster/run_up')),
            'egg/0': load_image('entities/egg/0.png'),
            'timers/timer': load_images('entities/timers/timer')
        }

        self.selected_fence = 0

        self.movement = [False, False, False, False]

        self.chickens = []
        self.roosters = []
        self.eggs = []

        self.buttons = []
        self.v_displacement = 0

        self.mode = 'select'
        self.money = 100

        self.tilemap = Tilemap(self, tile_size=20)

        self.level = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

    def run(self):
        time_to_move = False
        pixels_moved = 0
        size_factor = 720 / self.resolution
        b = Button(self, "toggle", True, 150, 150, 100, 100)
        c = Button(self, "toggle", False, 160, 600, 100, 100)
        self.buttons.append(b)
        self.buttons.append(c)
        mouse_timer = 0
        while True:

            self.screen.fill((0, 0, 0, 0))
            self.game_display.fill((0, 0, 0, 0))
            self.sidebar.fill((90, 0, 0))

            self.tilemap.render(self.game_display)
            self.tilemap.render_fences(self.game_display)

            # BUTTONS

            if mouse_timer > 0:

                mouse_timer -= 1
                print(mouse_timer)
            else:
                self.v_displacement = 0

                self.v_displacement = 0
            for button in self.buttons:
                if button.moveable:
                    button.render(self.sidebar, self.v_displacement)
                else:
                    button.render(self.sidebar, 0)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / size_factor, mouse_pos[1] / size_factor)
            tile_pos = (int((mouse_pos[0]) // self.tilemap.tile_size),
                        int((mouse_pos[1]) // self.tilemap.tile_size))

            # outlines for button implementation
            # next button
            pygame.draw.rect(self.sidebar, (255, 0, 0),
                             (25, 600, 200, 100), 2)
            # buy rooster/chicken button (split in half)
            pygame.draw.rect(self.sidebar, (255, 0, 0),
                             (250, 600, 287.5, 100), 2)

            # stats box (like how many roosters you have and chickens)
            pygame.draw.rect(self.sidebar, (255, 0, 0),
                             (25, 25, 287.5, 100), 2)

            # money
            pygame.draw.rect(self.sidebar, (255, 0, 0),
                             (337.5, 25, 200, 100), 2)

            if time_to_move:
                pixels_moved += 1
                for chicken in self.chickens:
                    chicken.update(chicken.movement)
                for rooster in self.roosters:
                    rooster.update(rooster.movement)
            else:
                for chicken in self.chickens:
                    chicken.update()
                    if (0 > chicken.pos[0] or 0 > chicken.pos[1]) or \
                            (chicken.pos[0] > self.stages[self.stage] or
                             chicken.pos[1] > self.stages[self.stage]):
                        self.chickens.remove(chicken)
                for rooster in self.roosters:
                    rooster.update()
                    if (0 > rooster.pos[0] or 0 > rooster.pos[1]) or \
                            (rooster.pos[0] > self.stages[self.stage] or
                             rooster.pos[1] > self.stages[self.stage]):
                        self.roosters.remove(rooster)
            if pixels_moved == 20:
                pixels_moved = 0
                time_to_move = False
                for chicken in self.chickens:
                    chicken.movement = [0, 0]
                    if not chicken.hunger_bar.next_img():
                        self.chickens.remove(chicken)
                        continue
                    if chicken.fertile:
                        if chicken.timer.progress != 3:
                            chicken.timer.next_img()
                    pos = (int(chicken.pos[0] // self.tilemap.tile_size),
                           int(chicken.pos[1] // self.tilemap.tile_size))
                    self.tilemap.chicken_here(pos, chicken)
                    if any(self.tilemap.get_feeders_nearby(pos)):
                        chicken.eat()

                for rooster in self.roosters:
                    rooster.movement = [0, 0]
                    if not rooster.hunger_bar.next_img():
                        self.roosters.remove(rooster)
                        continue
                    if not rooster.fertile:
                        rooster.timer.next_img()
                    if rooster.timer.progress == 3:
                        rooster.fertile = True
                    pos = (int(rooster.pos[0] // self.tilemap.tile_size),
                           int(rooster.pos[1] // self.tilemap.tile_size))
                    self.tilemap.chicken_here(pos, rooster)
                    if any(self.tilemap.get_feeders_nearby(pos)):
                        rooster.eat()
                    for chicken in self.chickens:
                        if rooster.pos == chicken.pos:
                            if rooster.fertile and not chicken.fertile:
                                rooster.fertilize()
                                chicken.fertilized()
                self.tilemap.check_overloaded_chickens(self.game_display)

            self.tilemap.render_feeders(self.game_display)
            if self.mode == 'fence':
                if pygame.mouse.get_pressed()[2]:
                    current_tile_img = self.assets['redfence'][self.selected_fence].copy()
                else:
                    current_tile_img = self.assets['fence'][self.selected_fence].copy()
            else:
                if pygame.mouse.get_pressed()[2]:
                    current_tile_img = self.assets['redfeed'].copy()
                else:
                    current_tile_img = self.assets['feed'].copy()
            current_tile_img.set_alpha(100)
            if self.mode == 'fence':
                if self.selected_fence != 0:
                    self.game_display.blit(current_tile_img,
                                           (tile_pos[0] * self.tilemap.tile_size,
                                            tile_pos[1] * self.tilemap.tile_size))
            elif self.mode == 'feed':
                self.game_display.blit(current_tile_img,
                                       (tile_pos[0] * self.tilemap.tile_size,
                                        tile_pos[1] * self.tilemap.tile_size))
            for chicken in self.chickens:
                chicken.render(self.game_display)
            for rooster in self.roosters:
                rooster.render(self.game_display)
            for egg in self.eggs:
                egg.render(self.game_display)
                egg.timer.update()
                egg.timer.render(self.game_display)
            self.tilemap.render_front_fences(self.game_display)
            for chicken in self.chickens:
                chicken.timer.render(self.game_display)
                chicken.hunger_bar.render(self.game_display)
            for rooster in self.roosters:
                rooster.timer.render(self.game_display)
                rooster.hunger_bar.render(self.game_display)
            if self.mode == 'fence' and self.selected_fence == 0:
                self.game_display.blit(current_tile_img,
                                       (tile_pos[0] * self.tilemap.tile_size,
                                        tile_pos[1] * self.tilemap.tile_size))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEWHEEL:
                    if mouse_pos[0] <= self.stages[self.stage] and self.mode == 'fence':
                        if event.y > 0:
                            self.selected_fence -= 1
                            if self.selected_fence == -1:
                                self.selected_fence = 3
                        elif event.y < 0:
                            self.selected_fence += 1
                            if self.selected_fence == 4:
                                self.selected_fence = 0

                    elif mouse_pos[0] > self.stages[self.stage]:
                        if event.y > 0:

                            mouse_timer = 30
                            self.v_displacement = -4
                        elif event.y < 0:
                            mouse_timer = 30
                            self.v_displacement = 4

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.mode == 'fence':
                        if event.button == 1:
                            pos = (int(mouse_pos[0] // self.tilemap.tile_size),
                                   int(mouse_pos[1] // self.tilemap.tile_size))
                            self.tilemap.place_fence(pos, self.selected_fence)
                        if event.button == 3:
                            pos = (int(mouse_pos[0] // self.tilemap.tile_size),
                                   int(mouse_pos[1] // self.tilemap.tile_size))
                            self.tilemap.delete_fence(pos, self.selected_fence)
                    elif self.mode == 'feed':
                        if event.button == 1:
                            pos = (int(mouse_pos[0] // self.tilemap.tile_size),
                                   int(mouse_pos[1] // self.tilemap.tile_size))
                            self.tilemap.place_feeder(pos)
                        if event.button == 3:
                            pos = (int(mouse_pos[0] // self.tilemap.tile_size),
                                   int(mouse_pos[1] // self.tilemap.tile_size))
                            self.tilemap.delete_feeder(pos)
                    elif self.mode == 'select':
                        if event.button == 1:
                            pos = (int(mouse_pos[0]),
                                   int(mouse_pos[1]))
                            for egg in self.eggs:
                                if pos[0] in range(egg.pos[0], egg.pos[0] + 16) and \
                                        pos[1] in range(egg.pos[1], egg.pos[1] + 16):
                                    egg.sell()
                if event.type == pygame.KEYUP and pixels_moved == 0:
                    if event.key == pygame.K_n:
                        time_to_move = True
                        for egg in self.eggs:
                            if egg.timer.progress == 3:
                                egg.hatch()
                            else:
                                egg.timer.next_img()
                        for chicken in self.chickens:
                            chicken.movement = self.move_chicken(chicken)
                            if chicken.movement != (0, 0):
                                pos = (int(chicken.pos[0] // self.tilemap.tile_size),
                                       int(chicken.pos[1] // self.tilemap.tile_size))
                                self.tilemap.remove_chicken(pos, chicken)
                            if chicken.fertile and chicken.timer.progress == 3:
                                chicken.lay_egg()
                        for rooster in self.roosters:
                            rooster.movement = self.move_chicken(rooster)
                            if rooster.movement != (0, 0):
                                pos = (int(rooster.pos[0] // self.tilemap.tile_size),
                                       int(rooster.pos[1] // self.tilemap.tile_size))
                                self.tilemap.remove_chicken(pos, rooster)
                    if event.key == pygame.K_s:
                        if self.money - 8 >= 0:
                            possible_places = self.tilemap.spawn_chicken(self.game_display)
                            if possible_places:
                                selected_place = possible_places[random.randint(0, len(possible_places) -1)]
                                coordinates = (2 + 20 * selected_place['pos'][0],
                                               2 + 20 * selected_place['pos'][1])
                                new_chicken = Chicken(self, coordinates, (16, 16))
                                self.chickens.append(new_chicken)
                                self.tilemap.chicken_here(selected_place['pos'], new_chicken)
                                self.money -= 8
                    if event.key == pygame.K_a:
                        if self.money - 12 >= 0:
                            possible_places = self.tilemap.spawn_chicken(self.game_display)
                            if possible_places:
                                selected_place = possible_places[random.randint(0, len(possible_places) -1)]
                                coordinates = (2 + 20 * selected_place['pos'][0],
                                               2 + 20 * selected_place['pos'][1])
                                new_rooster = Rooster(self, coordinates, (16, 16))
                                self.roosters.append(new_rooster)
                                self.tilemap.chicken_here(selected_place['pos'], new_rooster)
                                self.money -= 12
                    if event.key == pygame.K_r:
                        self.stage += 1
                        if self.stage > len(self.stages) - 1:
                            self.stage = 0
                        self.resolution = self.stages[self.stage]
                        size_factor = 720 / self.resolution
                        self.game_display = pygame.Surface(
                            (self.resolution, self.resolution))

                    # CHANGE MODE TO FENCE or SELECT or FEED: temp actuation,
                    # will be a button
                    if event.key == pygame.K_k:
                        self.mode = 'fence'
                    elif event.key == pygame.K_l:
                        self.mode = 'select'
                    elif event.key == pygame.K_f:
                        self.mode = 'feed'

            text_surface = self.my_font.render(str(self.money), False, (0, 0, 0))
            self.sidebar.blit(text_surface, (100, 50))
            self.screen.blit(
                pygame.transform.scale(self.game_display, (720, 720)), (0, 0))
            self.screen.blit(self.sidebar, (720, 0))

            pygame.display.update()
            self.clock.tick(60)

    def move_chicken(self, chicken: Chicken) -> tuple[int, int]:
        pos = (int(chicken.pos[0] // self.tilemap.tile_size),
               int(chicken.pos[1] // self.tilemap.tile_size))
        fences = self.tilemap.get_fences_on_tile(pos)
        nearby_fences = self.tilemap.get_fences_nearby(pos)
        nearby_eggs = self.tilemap.get_eggs_nearby(pos)
        nearby_feeders = self.tilemap.get_feeders_nearby(pos)
        for i in range(len(fences)):
            if nearby_fences[i] == 1 or nearby_eggs[i] == 1 or nearby_feeders[i] == 1:
                fences[i] = 1
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
