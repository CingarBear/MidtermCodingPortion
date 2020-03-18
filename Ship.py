############################################################
# Author:       Michael Cingari
# CWID:         889574562
# ---------------------------------------------------------
# ASSIGNMENT:   CPSC 386 Midterm Coding Portion
# DOS:          3 / 18 / 2020
# ---------------------------------------------------------
# NOTES:
#       - The class 'Laser' was also implemented in this
#       file so that Ship.py would be able to run properly
#        even though it was not required.
#
#       - The reason that the green check mark in
#       the upper right hand corner is because pycharm
#       doesnt recognize the earlier deceleration of the
#       variable 'alien' in the for-loop above. All other
#       style requirement checks were satisfied.
############################################################
import pygame as pg
from Vector import *
# from game import Laser

from pygame.sprite import Sprite


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __rmul__(self, k: float):
        return Vector(self.x * k, self.y * k)

    def __mul__(self, k: float):
        return self.__rmul__(k)

    def __truediv__(self, k: float):
        return self.__rmul__(1.0/k)

    def __neg__(self, k: float):
        self.x *= -1
        self.y *= -1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def test():  # feel free to change the test code
        v = Vector(x=5, y=5)
        u = Vector(x=4, y=4)
        print("v is {}".format(v))
        print("u is {}".format(u))
        print("uplusv is {}".format(u + v))
        # print("uminusv is {}".format(u - v)
        # print("ku is {}".format(3 * u))
        print("-u is {}".format(-1 * u))


class Laser(Sprite):
    SPEED = 5
    WIDTH = 400
    HEIGHT = 15
    COLOR = (200, 0, 0)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.color = Laser.COLOR
        self.rect = pg.Rect(0, 0, Laser.WIDTH, Laser.HEIGHT)
        self.rect.midtop = self.game.ship.rect.midtop
        self.velocity = Vector(0, -Laser.SPEED)
        self.y = float(self.rect.y)

    def move(self):
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y

    def draw(self): pg.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        self.move()
        self.draw()


class Ship:
    def __init__(self, game, vector=Vector()):
        self.game = game
        self.screen = game.screen
        self.velocity = vector
        self.screen_rect = game.screen.get_rect()
        self.image = pg.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.lasers = pg.sprite.Group()

    def __repr__(self):
        r = self.rect
        return "ship({},{}), v = {}".format(r.x, r.y, self.velocity)

    def fire(self):
        laser = Laser(game=self.game)
        self.lasers.add(laser)

    def remove_lasers(self):
        self.lasers.remove()

    def move(self):
        if self.velocity == Vector():
            return
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.game.limit_on_screen(self.rect)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        fleet = self.game.fleet

        self.move()
        self.draw()
        for laser in self.lasers.sprites():
            laser.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        aliens_hit = pg.sprite.groupcollide(fleet.aliens, self.lasers, False, True)
        if len(aliens_hit.keys()) > 0:
            print('{} aliens hit'.format(len(aliens_hit.keys())))
        for alien in aliens_hit:
            alien.hit()
        if alien.health <= 0:
            fleet.aliens.remove(alien)
        if not fleet.aliens:
            self.game.restart()
