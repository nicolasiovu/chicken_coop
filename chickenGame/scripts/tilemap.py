import json
import pygame

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0),
                   (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'wall'}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap,
                   'tile_size': self.tile_size,
                   'offgrid': self.offgrid_tiles
                   }, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def render(self, surface, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']],
                         (tile['pos'][0] - offset[0],
                          tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surface.blit(self.game.assets[tile['type']][tile['variant']],
                                 (tile['pos'][0] * self.tile_size - offset[0],
                                  tile['pos'][1] * self.tile_size - offset[1]))

    def render_fences(self, surface, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    for i in range(1, len(tile['fence'])):
                        if tile['fence'][i] == 1:
                            surface.blit(self.game.assets['fence'][i],
                                         (tile['pos'][0] * self.tile_size - offset[0],
                                          tile['pos'][1] * self.tile_size - offset[1]))

    def render_front_fences(self, surface, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if tile['fence'][0] == 1:
                        surface.blit(self.game.assets['fence'][0],
                                     (tile['pos'][0] * self.tile_size - offset[0],
                                      tile['pos'][1] * self.tile_size - offset[1]))

    def place_fence(self, pos, f_type):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            tile['fence'][f_type] = 1

    def get_fences_on_tile(self, pos):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            return tile['fence']
        else:
            return []
