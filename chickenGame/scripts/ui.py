import pygame
import random


class Button:
    def __init__(self, game, button_type, x, y, length, height, v_displacement):
        self.game = game
        self.rectangle = pygame.Rect(x, y, length, height)
        self.button_type = button_type
        self.x = x
        self.y = y + v_displacement
        self.img = self.game.assets['timers/timer'][0]

    def render(self, surface):
        surface.blit(self.img, (self.x, self.y))




