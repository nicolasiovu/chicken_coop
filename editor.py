import sys
import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap


class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('editor')

        self.screen = pygame.display.set_mode((720, 720))
        self.display = pygame.Surface((180, 180))
        self.clock = pygame.time.Clock()

        self.size_factor = 4

        self.assets = {
            'grass': load_images('tiles/grass'),
            'spawners': load_images('tiles/spawners')
        }

        self.movement = [False, False, False, False]
        self.tilemap = Tilemap(self, tile_size=20)

        try:
            self.tilemap.load('0.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        self.rect_width = 60

    def run(self):
        resolutions = [60, 80, 100, 140, 180, 240, 300, 400, 500, 600, 720]
        counter = 0
        while True:

            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / self.size_factor, mouse_pos[1] / self.size_factor)
            tile_pos = (int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                     tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mouse_pos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group],
                    'variant': self.tile_variant,
                    'pos': tile_pos,
                    'fence': [0, 0, 0, 0],
                    'has_egg': 0,
                    'has_feeder': 0,
                    'chickens': []
                }
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0],
                                         tile['pos'][1] - self.scroll[1],
                                         tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({
                                'type': self.tile_list[self.tile_group],
                                'variant': self.tile_variant,
                                'pos': (mouse_pos[0] + self.scroll[0],
                                        mouse_pos[1] + self.scroll[1])
                            })

                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = ((self.tile_variant - 1)
                                                 % len(self.assets[self.tile_list[self.tile_group]]))
                        if event.button == 5:
                            self.tile_variant = ((self.tile_variant + 1)
                                                 % len(self.assets[self.tile_list[self.tile_group]]))
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('0.json')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_r:
                        self.size_factor -= 1
                        if self.size_factor == 0:
                            self.size_factor = 4
                        self.display = pygame.Surface((720 / self.size_factor, 720 / self.size_factor))
                    if event.key == pygame.K_c:
                        counter += 1
                        if counter > len(resolutions)-1:
                            counter = 0
                        self.rect_width = resolutions[counter]

                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            pygame.draw.rect(self.display, (255, 0, 0), (0 - render_scroll[0], 0 - render_scroll[1], self.rect_width, self.rect_width), 2)
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0))
            self.screen.blit(current_tile_img, (5, 5))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()
