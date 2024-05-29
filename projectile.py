import os
import pygame
import math

class Bullet:
    def __init__(self, x, y, reverse=False, angle=0.0):
        self._x = x
        self._y = y
        self._size = 16
        self._angle = angle
        self._damage = 50
        self._speed = 10
        self._slow = 1
        self._slow_time = 0
        self._img_path = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "fire_bullet.png")), (30, 30)) for i in range(0, 1)]
        self._destroy_img_path = os.path.join("assets", "PeaNormalExplode_0.png")
        self._is_reverse = reverse
        self._current_time_alive = 0
        self._image_index_alive = -1
        self._reverse()

    def _reverse(self):
        if self._is_reverse:
            self._speed *= -1

    def increase_damage(self, damage):
        self._damage += damage

    def increase_slow(self, slow):
        self._slow += slow

    def draw(self, screen):
        img = pygame.transform.scale(pygame.image.load(self._img_path).convert_alpha(), (self._size, self._size))
        screen.blit(img, (self._x, self._y))
        self._x += self._speed * math.cos(self._angle)
        self._y += self._speed * math.sin(self._angle)

    def draw_ani(self, screen, dt, image): 
        self._current_time_alive += dt
        if self._current_time_alive >= 1/(len(image))*1000:
            self._image_index_alive = (self._image_index_alive +1) % len(image)
            self._current_time_alive = 0 
        current_image = image[self._image_index_alive]
        screen.blit(current_image, (self._x, self._y))
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
    
    def get_img_path(self): 
        return self._img_path

class IceBullet(Bullet):
    def __init__(self, x, y, reverse=False, angle=0.0):
        super().__init__(x, y, reverse, angle)
        self._damage = 30
        self._slow = 0.8
        self._slow_time = 20000
        self._img_path = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "ice_bullet.png")), (30, 30)) for i in range(0, 1)]
        self._reverse()

class FireBullet(Bullet):
    def __init__(self, x, y, angle=0.0):
        super().__init__(x, y, angle)
        self._damage = 100

class IceFireBullet(Bullet):
    def __init__(self, x, y, angle=0.0):
        super().__init__(x, y, angle)
        self._damage = 100
        self._slow = 2

class Skull_attack(Bullet): 
    def __init__(self, x, y, reverse = True, angle=0.0):
        super().__init__(x, y, reverse, angle)
        self._damage = 30
        self._is_reverse = reverse
        self._img_path = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3","Skull_attack", f"{i}.png")), (100, 100)) for i in range(0, 8)]
        self.speed = -3
        
