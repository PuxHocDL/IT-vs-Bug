import pygame
import colors
from projectile import *
from bar import Bar


class BasicTower:
    """Tháp cơ bản, bắn đạn gây sát thương lên quái vật"""

    def __init__(self, x, y, size):
        self._x = x
        self._y = y
        self._level = 1
        self._cost = 50  # Giá mua tháp
        self._max_health = 500
        self._health = self._max_health
        self._size = size
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "BasicTower", f"tower{i}.png")).convert_alpha(), (size, size)) for i in range(8)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "BasicTower", f"tower{i}.png")).convert_alpha(), (size, size)) for i in range(16)]
        self._destroy_imgs = []
        self._animate_time = {0: 200, 1: 2000, 2: 500}
        self._mode = 0
        self._img_index = 0
        self._current_time = 0
        self._load_imgs()
        self._health_bar = Bar(self._x - self._size//4, self._y - self._size//2, self._size//2, 5, colors.green, colors.gray, self._max_health)

    def _load_imgs(self):
        self._img_mode = {0: self._idle_imgs, 1: self._atk_imgs, 2: self._destroy_imgs}

    def upgrade(self):
        self._level = min(self.__level + 1, 3)

    def _shoot(self):
        """Tháp bắn đạn"""
        if self._level == 1:
            return [Bullet(self._x, self._y)]
        else:
            return [Bullet(self._x, self._y, angle=-0.2), Bullet(self._x, self._y, angle=0), Bullet(self._x, self._y, angle=0.2)]

    def draw(self, screen, dt):
        proj = []
        current_imgs = self._img_mode[self._mode]
        if self._current_time > self._animate_time[self._mode]/len(current_imgs):
            self._img_index = (self._img_index + 1) % len(current_imgs)
            self._current_time = 0
        screen.blit(current_imgs[self._img_index], (self._x - self._size // 2, self._y - self._size // 2))
        self._current_time += dt
        if self._mode == 1 and self._img_index == len(current_imgs)-1:
            proj = self._shoot()
            self.set_mode(0)

        if self._health < self._max_health:
            self._health_bar.draw(screen)
        return proj

    def damage(self, val):
        self._health -= val
        self._health_bar.set_val(self._health)

    def apply_slow(self, slow, slow_time):
        return

    def get_health(self):
        return self._health

    def is_dead(self):
        return self._health <= 0

    def set_mode(self, mode):
        if mode != self._mode:
            self._mode = mode
            self._img_index = 0

    def get_rect(self):
        return pygame.mask.from_surface(self._idle_imgs[0], threshold=244)

    def get_pos(self):
        return self._x - self._size//2, self._y - self._size//2

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


class SlowTower(BasicTower):
    """Tháp làm chậm, kế thừa từ basic_tower, làm chậm tốc độ di chuyển của quái"""

    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self._cost = 100
        self._tower_type = "Slow"


class IceTower(BasicTower):
    """Tháp băng, bắn đạn gây sát thương và làm chậm kẻ địch"""
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self._cost = 150
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "IceTower", f"tower{i}.png")), (size, size)) for i in range(1, 7)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "IceTower", f"tower{i}.png")), (size, size)) for i in range(1, 17)]
        self._load_imgs()

    def _shoot(self):
        if self._level == 1:
            return [IceBullet(self._x, self._y)]
        else:
            return [IceBullet(self._x, self._y, angle=-0.2), IceBullet(self._x, self._y, angle=0), IceBullet(self._x, self._y, angle=0.2)]
