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

        self.movement = [0, 0]
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


class Timer:
    def __init__(self, game, pos, img, size):
        self.game = game
        self.img = img
        self.size = size
        self.pos = list(pos)
        self.progress = 0

    def update(self, movement=(0, 0)):
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]

    def next_img(self):
        self.progress += 1
        if self.progress == 4:
            self.progress = 0
        self.img = self.game.assets['timers/timer'][self.progress]

    def render(self, surface):
        surface.blit(self.img, self.pos)


class Chicken(PhysicsEntity):
    def __init__(self, game, pos, size, fertile=False):
        super().__init__(game, 'chicken', pos, size)
        self.timer = Timer(game, (pos[0] - 2, pos[1] - 2),
                           game.assets['timer'], (20, 20))
        self.fertile = fertile

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

    def fertilized(self):
        self.fertile = True

    def lay_egg(self):
        self.game.eggs.append(Egg(self.game, '0', self.pos, (16, 16),
                                  self.game.assets['egg/0']))
        self.timer.next_img()
        self.fertile = False


class Rooster(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'rooster', pos, size)
        self.timer = Timer(game, (pos[0] - 2, pos[1] - 2),
                           game.assets['timer'], (20, 20))
        self.fertile = False

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

    def fertilize(self):
        self.fertile = False
        self.timer.next_img()


class Egg:
    def __init__(self, game, e_type, pos, size, img):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.img = img
        self.timer = Timer(game, (pos[0] - 2, pos[1] - 2), game.assets['timer'], (20, 20))

    def render(self, surface):
        surface.blit(self.img, self.pos)

    def hatch(self):
        self.game.eggs.remove(self)
        self.game.chickens.append(Chicken(self.game, self.pos, (16, 16)))
