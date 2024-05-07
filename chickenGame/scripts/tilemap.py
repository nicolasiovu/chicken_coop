import json
import pygame
import random

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

    def render_feeders(self, surface, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if tile['has_feeder'] == 1:
                        surface.blit(self.game.assets['feed'],
                                     (tile['pos'][0] * self.tile_size - offset[0],
                                      tile['pos'][1] * self.tile_size - offset[1]))

    def place_fence(self, pos, f_type):
        if self.game.money >= 5:
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
                self.game.money += 3

    def place_feeder(self, pos):
        if self.game.money >= 15:
            loc = str(pos[0]) + ';' + str(pos[1])
            if loc in self.tilemap:
                tile = self.tilemap[loc]
                if tile['has_feeder'] == 0 and not tile['chickens'] and tile['has_egg'] == 0:
                    tile['has_feeder'] = 1
                    self.game.money -= 15

    def delete_feeder(self, pos):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['has_feeder'] == 1:
                tile['has_feeder'] = 0
                self.game.money += 10

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

    def get_feeders_nearby(self, pos):
        feeders = [0, 0, 0, 0]
        for i in range(len(NEIGHBOR_TILES)):
            loc = (str(pos[0] + NEIGHBOR_TILES[i][0]) + ';' +
                   str(pos[1] + NEIGHBOR_TILES[i][1]))
            if loc in self.tilemap:
                if self.tilemap[loc]['has_feeder'] == 1:
                    feeders[i] = 1
        return feeders

    def spawn_chicken(self, surface, offset=(0, 0)) -> list:
        possible_tiles = []
        for x in range(0, surface.get_width(), 20):
            x //= self.tile_size
            for y in range(0, surface.get_height(), 20):
                y //= self.tile_size
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if tile['has_egg'] == 0 and tile['has_feeder'] == 0 and not tile['chickens']:
                        possible_tiles.append(tile)
        return possible_tiles

    def chicken_here(self, pos, chicken):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            if chicken not in tile['chickens']:
                tile['chickens'].append(chicken)

    def remove_chicken(self, pos, chicken):
        loc = str(pos[0]) + ';' + str(pos[1])
        if loc in self.tilemap:
            tile = self.tilemap[loc]
            if chicken in tile['chickens']:
                tile['chickens'].remove(chicken)

    def check_overloaded_chickens(self, surface, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    if len(tile['chickens']) > 3:
                        for chicken in tile['chickens']:
                            if chicken.type == 'chicken':
                                if chicken in self.game.chickens:
                                    self.game.chickens.remove(chicken)
                            else:
                                if chicken in self.game.roosters:
                                    self.game.roosters.remove(chicken)
                        tile['chickens'] = []


