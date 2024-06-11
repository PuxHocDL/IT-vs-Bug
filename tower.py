import pygame
import colors
from projectile import *
from bar import Bar
from vfx_manager import VFXManager


class Tower:
    """Tháp cơ bản, bắn đạn gây sát thương lên quái vật"""

    def __init__(self, x, y, size, price, max_health=500):
        self._x = x
        self._y = y
        self._level = 1
        self._max_health = max_health
        self._health = self._max_health
        self._size = size
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "BasicTower", f"tower{i}.png")).convert_alpha(), (size, size)) for i in range(8)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "BasicTower", f"tower{i}.png")).convert_alpha(), (size, size)) for i in range(16)]
        self._animate_time = {0: 200, 1: 2000}
        self._mode = 0
        self._img_index = 0
        self._current_time = 0
        self._load_imgs()
        self._health_bar = Bar(self._x - self._size//4, self._y - self._size//2, self._size//2, 5, colors.green, colors.gray, self._max_health)

        self.__price = price

    def _load_imgs(self):
        self._img_mode = {0: self._idle_imgs, 1: self._atk_imgs}

    def upgrade(self):
        if self._level < 3:
            self._level += 1
            return True
        return False

    def _shoot(self):
        """Tháp bắn đạn"""
        if self._level == 1:
            return [Bullet(self._x, self._y)]
        elif self._level == 2:
            return [Bullet(self._x, self._y, angle=-0.2), Bullet(self._x, self._y, angle=0.0), Bullet(self._x, self._y, angle=0.2)]
        else:
            self._animate_time[1] = 1500
            return [Bullet(self._x, self._y, angle=-0.2, extra_dmg=30), Bullet(self._x, self._y, angle=0, extra_dmg=30), Bullet(self._x, self._y, angle=0.2, extra_dmg=30)]

    def draw(self, screen, dt):
        proj = []
        current_imgs = self._img_mode[self._mode]

        index_interval = self._animate_time[self._mode]//len(current_imgs)
        self._current_time = self._current_time + dt
        additional_index = self._current_time // index_interval
        self._current_time %= index_interval

        if self._mode == 1 and self._img_index + additional_index > len(current_imgs)-1:
            proj = self._shoot()
            self.set_mode(0)

        self._img_index = (self._img_index + additional_index) % len(current_imgs)
        screen.blit(current_imgs[self._img_index], (self._x - self._size // 2, self._y - self._size // 2))

        if self._health < self._max_health:
            self._health_bar.draw(screen)
        return proj

    def damage(self, val):
        self._health -= val
        self._health_bar.set_val(self._health)

    def heal(self, val):
        self._health = min(self._health + val, self._max_health)
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

    def get_name(self):
        return "Tower"

    def get_price(self):
        return self.__price

    def get_max_health(self):
        return self._max_health

class BasicTower(Tower):
    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price)

class SlowTower(Tower):
    """Tháp làm chậm, kế thừa từ basic_tower, làm chậm tốc độ di chuyển của quái"""

    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price)
        self._tower_type = "Slow"


class IceTower(Tower):
    """Tháp băng, bắn đạn gây sát thương và làm chậm kẻ địch"""
    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price)
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "IceTower", f"tower{i}.png")), (size, size)) for i in range(1, 7)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "IceTower", f"tower{i}.png")), (size, size)) for i in range(16)]
        self._load_imgs()

    def _shoot(self):
        if self._level == 1:
            return [IceBullet(self._x, self._y)]
        elif self._level == 2:
            return [IceBullet(self._x, self._y, extra_slow=0.3)]
        else:
            self._animate_time[1] = 1200
            return [IceBullet(self._x, self._y, extra_slow=0.3, extra_slow_time=1000)]

class FireTower(Tower):
    """Tháp băng, bắn đạn gây sát thương và làm chậm kẻ địch"""
    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price)
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "FireTower", f"tower{i}.png")), (size, size)) for i in range(8)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "FireTower", f"tower{i}.png")), (size, size)) for i in range(16)]
        self._load_imgs()

    def _shoot(self):
        if self._level == 1:
            return [FireBullet(self._x, self._y)]
        elif self._level == 2:
            return [FireBullet(self._x, self._y, extra_dmg=50)]
        else:
            self._animate_time[1] = 1200
            return [FireBullet(self._x, self._y, extra_dmg=80)]

class TheWall(Tower):
    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price, 5000)
        self._idle_imgs = self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "TheWall", f"wall.png")), (size, size))]
        self._load_imgs()
        self._animate_time = {0: 5000, 1: 5000}

    def _shoot(self):
        if self._level == 1:
            pass
        elif self._level == 2:
            self._max_health = 5300
        else:
            self._max_health = 5500
            self.heal(100)

        return []

class TheRook(Tower):
    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price, 1000)
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "TheRook", f"the_rook{i}.png")), (size, size)) for i in range(8)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "TheRook", f"the_rook{i}.png")), (size, size)) for i in range(8)]
        self._load_imgs()
        self._vfx_added = False
        self._animate_time = {0: 200, 1: 4000, 2: 500}

    def utility(self, screen, dt, towers, bugs):
        proj = []
        if bugs:
            self.set_mode(1)

        current_imgs = self._img_mode[self._mode]
        index_interval = self._animate_time[self._mode]//len(current_imgs)
        self._current_time = self._current_time + dt
        additional_index = self._current_time // index_interval
        self._current_time %= index_interval

        if self._mode == 1:
            if self._img_index <= 3 and self._img_index + additional_index > 3 and not self._vfx_added:
                pos = self.get_pos()
                VFXManager.add_vfx(pos[0], 0, 1800, [pygame.transform.scale(pygame.image.load(os.path.join("assets", "VFX", "SilverLining", f"silver_lining{i}.png")), (self._size, pos[1]+20)) for i in range(8)])
                self._vfx_added = True
            elif self._img_index + additional_index >= len(current_imgs)-1:
                if bugs:
                    proj = self._utility(bugs[0])
                self.set_mode(0)
                self._vfx_added = False

        self._img_index = (self._img_index + additional_index) % len(current_imgs)
        screen.blit(current_imgs[self._img_index], (self._x - self._size // 2, self._y - self._size // 2))

        if self._health < self._max_health:
            self._health_bar.draw(screen)
        return proj

    def _utility(self, obj):
        VFXManager.add_vfx(obj.get_x() + obj.get_size()//4, 0, 500, [pygame.transform.scale(pygame.image.load(os.path.join("assets", "VFX", "SilverLining", f"silver_lining{i}.png")), (self._size, obj.get_y())) for i in range(8)])
        return [SilverLining(obj.get_x() + obj.get_size()//4, obj.get_y())]

    def get_name(self):
        return "Utility"

class Obelisk(Tower):
    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price, 1000)
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "Obelisk", f"obelisk{i}.png")), (size, size)) for i in range(14)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "Obelisk", f"obelisk{i}.png")), (size, 19/12*size)) for i in range(14)]
        self._animate_time = 2000
        self._load_imgs()
        self.__energy_interval = 0
        self._vfx_added = False

    def utility(self, screen, dt):
        energy = 0
        current_imgs = self._img_mode[0]

        if self.__energy_interval > len(current_imgs)*5:
            self.set_mode(1)
            self.__energy_interval = 0

        index_interval = self._animate_time//len(current_imgs)
        self._current_time = self._current_time + dt
        additional_index = self._current_time // index_interval
        self._current_time %= index_interval

        if self._mode == 1:
            if not self._vfx_added:
                pos = self.get_pos()
                VFXManager.add_vfx(pos[0], pos[1] - 7/12*self._size, self._animate_time, self._img_mode[1][self._img_index + additional_index:])
                self._vfx_added = True
            if self._img_index <= 11 and self._img_index + additional_index > 11:
                energy = self._utility()
            elif self._img_index + additional_index >= len(current_imgs)-1:
                self.set_mode(0)
                self.__energy_interval = 0
                self._vfx_added = False
        else:
            self.__energy_interval += additional_index

        self._img_index = (self._img_index + additional_index) % len(current_imgs)
        screen.blit(current_imgs[self._img_index], (self._x - self._size // 2, self._y - self._size // 2))
        self.__update_speed()

        if self._health < self._max_health:
            self._health_bar.draw(screen)
        return energy

    def _utility(self):
        if self._level == 1:
            return 50
        elif self._level == 2:
            return 100
        else:
            return 150

    def __update_speed(self):
        if self._level == 3:
            self._animate_time = 1000

    def get_name(self):
        return "Obelisk"

class HealingTower(TheRook):
    def __init__(self, x, y, size, price):
        super().__init__(x, y, size, price)
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "HealingTower", f"tower{i}.png")), (size, size)) for i in range(14)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "HealingTower", f"tower{i}.png")), (size, 39/32*size)) for i in range(14)]
        self._load_imgs()
        self._vfx_added = False
        self._animate_time = 2000
        self.__heal_interval = 0
        self._vfx_added = False

    def utility(self, screen, dt, towers, bugs):
        current_imgs = self._img_mode[0]

        if self.__heal_interval > len(current_imgs)*5:
            self.set_mode(1)
            self.__heal_interval = 0

        index_interval = self._animate_time//len(current_imgs)
        self._current_time = self._current_time + dt
        additional_index = self._current_time // index_interval
        self._current_time %= index_interval

        if self._mode == 1:
            if not self._vfx_added:
                pos = self.get_pos()
                VFXManager.add_vfx(pos[0], pos[1] - 7/32*self._size, self._animate_time, self._img_mode[1][self._img_index + additional_index:])
                self._vfx_added = True
            if self._img_index <= 11 and self._img_index + additional_index > 11:
                if towers:
                    self._utility(towers)
            elif self._img_index + additional_index > len(current_imgs)-1:
                self.set_mode(0)
                self.__heal_interval = 0
                self._vfx_added = False
        else:
            self.__heal_interval += additional_index

        self._img_index = (self._img_index + additional_index) % len(current_imgs)
        screen.blit(current_imgs[self._img_index], (self._x - self._size // 2, self._y - self._size // 2))

        if self._health < self._max_health:
            self._health_bar.draw(screen)
        return []

    def _utility(self, obj):
        print("Lmao")
        if self._level == 1:
            healing_power = 100
            healing_number = 1
        elif self._level == 2:
            healing_power = 200
            healing_number = 2
        else:
            healing_power = 500
            healing_number = 3
        for o in sorted(obj, key=lambda o: o.get_health()):
            o.heal(healing_power)
            healing_number -= 1
            if healing_number == 0:
                break
