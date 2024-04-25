import pygame
import random

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

        self.action = ''
        self.flip = False
        self.animation = None
        self.set_action('idle_down')

        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0],
                          movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.animation.update()

    def render(self, surface):
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                     self.pos)


class Chicken(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'chicken', pos, size)

    def update(self, movement=(0, 0)):
        if movement[0] != 0:
            self.set_action('run_right')
        elif movement[1] > 0:
            self.set_action('run_down')
        elif movement[1] < 0:
            self.set_action('run_up')
        elif self.last_movement[0] != 0:
            self.set_action('idle_right')
        elif self.last_movement[1] > 0:
            self.set_action('idle_down')
        elif self.last_movement[1] < 0:
            self.set_action('idle_up')
        else:
            x = random.randint(1, 2000)
            if x == 1:
                self.set_action('idle_up')
            elif x == 2:
                self.flip = False
                self.set_action('idle_right')
            elif x == 3:
                self.flip = True
                self.set_action('idle_right')
            elif x == 4:
                self.set_action('idle_down')
        super().update(movement=movement)

