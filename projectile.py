import os
import pygame
import math
from vfx_manager import VFXManager

class Bullet:
    def __init__(self, x, y, reverse=False, angle=0.0):
        self._x = x
        self._y = y
        self._size = 32
        self._angle = angle
        self._damage = 50
        self._speed = 10
        self._slow = 1
        self._slow_time = 0
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "move", "Bullet", f"bullet{i}.png")).convert_alpha(), (self._size, self._size)) for i in range(8)]
        self._destroy_imgs = [os.path.join("assets", "Projectiles", "explode", "Bullet", f"bullet{i}.png") for i in range(8)]
        self._is_reverse = reverse
        self._current_time = 0
        self._img_index = 0
        self._ani_interval = 1000
        self._reverse()

    def _reverse(self):
        if self._is_reverse:
            self._speed *= -1

    def increase_damage(self, damage):
        self._damage += damage

    def increase_slow(self, slow):
        self._slow += slow

    def draw(self, screen, dt): 
        if self._current_time >= 1/(len(self._imgs))*self._ani_interval:
            self._img_index = (self._img_index + 1) % len(self._imgs)
            self._current_time = 0 
        screen.blit(self._imgs[self._img_index], (self._x, self._y))
        self._x += self._speed * math.cos(self._angle)
        self._y += self._speed * math.sin(self._angle)
        self._current_time += dt

    def draw_destroy(self):
        VFXManager.add_vfx(self._x, self._y, (self._size, self._size), 200, self._destroy_imgs)
        
    def get_rect(self):
        return pygame.mask.from_surface(self._imgs[self._img_index], threshold=255).to_surface()

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
    def __init__(self, x, y, reverse=False, angle=0.0):
        super().__init__(x, y, reverse, angle)
        self._damage = 30
        self._slow = 0.8
        self._slow_time = 2000
        self._imgs = [os.path.join("assets", "Projectiles", "ice_bullet.png")]
        self._reverse()

class FireBullet(Bullet):
    def __init__(self, x, y, reverse=False, angle=0.0):
        super().__init__(x, y, reverse, angle)
        self._damage = 100

class IceFireBullet(Bullet):
    def __init__(self, x, y, reverse=False, angle=0.0):
        super().__init__(x, y, reverse, angle)
        self._damage = 100
        self._slow = 2

class Skull(Bullet): 
    def __init__(self, x, y, reverse=True, angle=0.0):
        super().__init__(x, y, reverse, angle)
        self._size = 100
        self._damage = 30
        self._speed = 3
        self._imgs = [os.path.join("assets", "Monster_3","Skull_attack", f"{i}.png") for i in range(0, 8)]
        self._reverse()
