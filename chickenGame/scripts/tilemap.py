import json
import pygame

NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0),
                   (0, 0), (-1, 1), (0, 1), (1, 1)]


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

    def tiles_around(self, position):
        tiles = []
        tile_loc = (int(position[0] // self.tile_size),
                    int(position[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = (str(tile_loc[0] + offset[0]) + ';'
                         + str(tile_loc[1] + offset[1]))
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

