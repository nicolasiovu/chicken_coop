import pygame
import random
from typing import Optional


class Button:
    def __init__(self, game, button_type, moveable, x, y, length, height, img):
        self.moveable = moveable
        self.game = game
        self.rectangle = pygame.Rect(x, y, length, height)
        self.button_type = button_type
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        if img:
            if isinstance(img, str):
                self.img = self.game.assets[img]
            elif isinstance(img, list):
                self.img = img[0]
                self.current_image = 0
                self.images = img
        else:
            self.img = None

    def render(self, surface, v_displacement=0):
        self.y = v_displacement + self.y
        if self.img:
            surface.blit(self.img, (self.x, self.y))

    def is_within(self, mouse_pos):
        if not self.moveable:
            if (720 + self.x <= mouse_pos[0] <= self.x + 720 + self.length and
                    self.y <= mouse_pos[1] <= self.y + self.height):
                return True
            else:
                return False
        else:
            if 140 < mouse_pos[1] < 580:
                if (720 + self.x <= mouse_pos[0] <= self.x + 720 + self.length and
                        self.y <= mouse_pos[1] <= self.y + self.height):
                    return True
                else:
                    return False

    def next_img(self):
        length = len(self.images) - 1
        self.current_image += 1
        if self.current_image > length:
            self.current_image = 0
        self.img = self.images[self.current_image]
