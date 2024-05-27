import os
import math
import pygame

class Bullet:
    def __init__(self, x, y, angle=0):
        self._x = x
        self._y = y
        self._angle = angle
        self._damage = 50
        self._speed = 5
        self._slow = 0
        self._img = None
        self._destroy_img = None

    def increase_damage(self, damage):
        self._damage += damage

    def increase_slow(self, slow):
        self._slow += slow

    def draw(self, screen):
        screen.blitz(self._img, self._x, self._y)
        self._x += self._speed * math.cos(self._angle)
        self._x += self._speed * math.sin(self._angle)

    def draw_destroy(self, screen):
        screen.blitz(self._destroy_img, self._x, self._y)

class IceBullet(Bullet):
    def __init__(self, x, y, angle=0):
        super().__init__(x, y, angle)
        self._damage = 30
        self._slow = 2

class FireBullet(Bullet):
    def __init__(self, x, y, angle=0):
        super().__init__(x, y, angle)
        self._damage = 100

class IceFireBullet(Bullet):
    def __init__(self, x, y, angle=0):
        super().__init__(x, y, angle)
        self._damage = 100
        self._slow = 2
