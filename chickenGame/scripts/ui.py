import pygame
import random


class Button:
    def __init__(self, game, button_type, moveable, x, y, length, height):
        self.moveable = moveable
        self.game = game
        self.rectangle = pygame.Rect(x, y, length, height)
        self.button_type = button_type
        self.x = x
        self.y = y
        self.img = self.game.assets['timers/timer'][0]

    def render(self, surface, v_displacement=0):
        self.y = v_displacement + self.y
        surface.blit(self.img, (self.x, self.y))




