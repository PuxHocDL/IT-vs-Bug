import os
import pygame
import math

class Bullet:
    def __init__(self, x, y, angle=0.0):
        self._x = x
        self._y = y
        self._size = 16
        self._angle = angle
        self._damage = 50
        self._speed = 5
        self._slow = 1
        self._slow_time = 0
        self._img_path = os.path.join("assets", "PeaNormal_0.png")
        self._destroy_img_path = os.path.join("assets", "PeaNormalExplode_0.png")

    def increase_damage(self, damage):
        self._damage += damage

    def increase_slow(self, slow):
        self._slow += slow

    def draw(self, screen):
        img = pygame.transform.scale(pygame.image.load(self._img_path).convert_alpha(), (self._size, self._size))
        screen.blit(img, (self._x, self._y))
        self._x += self._speed * math.cos(self._angle)
        self._y += self._speed * math.sin(self._angle)

    def draw_destroy(self, screen):
        img = pygame.transform.scale(pygame.image.load(self._destroy_img_path).convert_alpha(), (self._size, self._size))
        screen.blit(img, (self._x, self._y))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._size, self._size)

    def check_border(self, width, height):
        if 0 < self._x < width or 0 < self._y < height:
            return False
        return True

    def get_damage(self):
        return self._damage

    def get_slow(self):
        return self._slow

    def get_slow_time(self):
        return self._slow_time

class IceBullet(Bullet):
    def __init__(self, x, y, angle=0.0):
        super().__init__(x, y, angle)
        self._damage = 30
        self._slow = 0.8
        self._slow_time = 20000

class FireBullet(Bullet):
    def __init__(self, x, y, angle=0.0):
        super().__init__(x, y, angle)
        self._damage = 100

class IceFireBullet(Bullet):
    def __init__(self, x, y, angle=0.0):
        super().__init__(x, y, angle)
        self._damage = 100
        self._slow = 2
