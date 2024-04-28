import json
import pygame

NEIGHBOR_TILES = [(0, 1), (-1, 0), (0, -1), (1, 0)]


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
            if tile['fence'][f_type] == 0:
                tile['fence'][f_type] = 1
                self.game.money -= 5

    def delete_fence(self, pos, f_type):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['fence'][f_type] == 1:
                tile['fence'][f_type] = 0
                self.game.money += 2

    def get_fences_on_tile(self, pos):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            return tile['fence'].copy()
        else:
            return []

    def get_fences_nearby(self, pos):
        fences = [0, 0, 0, 0]
        for i in range(len(NEIGHBOR_TILES)):
            loc = (str(pos[0] + NEIGHBOR_TILES[i][0]) + ';' +
                   str(pos[1] + NEIGHBOR_TILES[i][1]))
            if loc in self.tilemap:
                if self.tilemap[loc]['fence'][(i + 2) % 4] == 1:
                    fences[i] = 1
        return fences.copy()

    def get_eggs_nearby(self, pos):
        eggs = [0, 0, 0, 0]
        for i in range(len(NEIGHBOR_TILES)):
            loc = (str(pos[0] + NEIGHBOR_TILES[i][0]) + ';' +
                   str(pos[1] + NEIGHBOR_TILES[i][1]))
            if loc in self.tilemap:
                if self.tilemap[loc]['has_egg'] == 1:
                    eggs[i] = 1
        return eggs

    def chicken_here(self, pos, chicken):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            tile['chickens'].append(chicken)

    def remove_chicken(self, pos, chicken):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            tile['chickens'].remove(chicken)

    def check_overloaded_chickens(self, surface, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if len(tile['chickens']) >= 3:
                        print(len(tile['chickens']), len(self.game.chickens) + len(self.game.roosters))
                        for chicken in tile['chickens']:
                            if chicken.type == 'chicken':
                                if chicken in self.game.chickens:
                                    self.game.chickens.remove(chicken)
                            else:
                                if chicken in self.game.roosters:
                                    self.game.roosters.remove(chicken)
                        tile['chickens'] = []
                        print(len(tile['chickens']), len(self.game.chickens) + len(self.game.roosters))


