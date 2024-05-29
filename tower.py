from config import *
from collections import defaultdict
from projectile import *

class BasicTower:
    """Tháp cơ bản, bắn đạn gây sát thương lên quái vật"""
    def __init__(self, x, y, size):
        self._x = x
        self._y = y
        self._level = 1
        self._cost = 50  # Giá mua tháp
        self._color_for_levels = {1: BLUE, 2: YELLOW, 3: RED}
        self._health = 100
        self._size = size
        self._idle_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "idle", "BasicTower", f"tower{i}.png")), (size, size)) for i in range(6)]
        self._atk_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Towers", "shoot", "BasicTower", f"tower{i}.png")), (size, size)) for i in range(16)]
        self._destroy_imgs = []
        self._img_mode = {0: self._idle_imgs, 1: self._atk_imgs, 2: self._destroy_imgs}
        self._animate_time = {0: 200, 1: 1000, 2: 500}
        self._mode = 0
        self._img_index = 0
        self._current_time = 0
        
    def upgrade(self):
        global gold
        if gold.gold >= upgrade_cost and self._level < 3:
            self._level += 1
            gold.gold -= upgrade_cost
            
    def __shoot(self):
        """Tháp bắn đạn"""
        bullet_x = self._x - BULLET_SIZE // 2
        bullet_y = self._y - BULLET_SIZE // 2
        
        if self._level == 1:
            return [Bullet(self._x, self._y)]
        elif self._level == 2:
            return [Bullet(self._x, self._y, -0.2), Bullet(self._x, self._y, 0), Bullet(self._x, self._y, 0.2)]
            
        else:
           # if bugs:
           #     nearest_bug = min(bugs, key=lambda m: math.hypot(m.get_x() - bullet_x, m.get_y() - bullet_y))
           #     angle = math.atan2(nearest_bug.get_y() - bullet_y, nearest_bug.get_x() - bullet_x)
           # else:
           #     angle = 0
           # bullets.append([bullet_x, bullet_y, angle, self._level, "normal"])  # Đạn đuổi
           # bullets.append([bullet_x, bullet_y, angle, self._level, "normal"])  # Đạn đuổi
           # bullets.append([bullet_x, bullet_y, angle, self._level, "normal"])  # Đạn đuổi
            return []

    def draw(self, screen, dt):
        proj = []
        current_imgs = self._img_mode[self._mode]
        if self._current_time > self._animate_time[self._mode]/len(current_imgs):
            self._img_index = (self._img_index + 1) % len(current_imgs)
            self._current_time = 0
        screen.blit(current_imgs[self._img_index], (self._x - self._size // 2, self._y - self._size // 2))
        self._current_time += dt
        if self._mode == 1 and self._img_index == len(current_imgs)-1:
            proj = self.__shoot()
            self.set_mode(0)
        return proj

    def set_mode(self, mode):
        if mode != self._mode:
            self._mode = mode
            self._img_index = 0

    def damage(self, val):
        self._health -= val

    def get_pos(self):
        return self._x, self._y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


class SlowTower(BasicTower):
    """Tháp làm chậm, kế thừa từ basic_tower, làm chậm tốc độ di chuyển của quái"""
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self._cost = 100
        self._color_for_levels = defaultdict(lambda: PURPLE)  # Màu là PURPLE cho mọi cấp
        self._tower_type = "Slow"
    def shoot(self):
        """Làm chậm tốc độ quái trên sân"""
        for bug in bugs:
            bug.speed = 1  # Giảm tốc độ quái vật
            bug.slowed = True  # Đánh dấu bị làm chậm
            bug.slow_timer = pygame.time.get_ticks() + 10000  # Thiết lập thời gian kết thúc làm chậm

class TowerGame:
    """Các chức năng liên quan đến game tháp"""
    def draw_gold():
        """Vẽ thông tin vàng"""
        gold_text = font.render(f"Gold: {gold.gold}", True, BLACK)
        screen.blit(gold_text, (10, 10))
    
    def draw_slow(x, y):
        """Vẽ vật làm chậm ở vị trí x, y"""
        pygame.draw.rect(screen, PURPLE, (x, y, TOWER_SIZE, TOWER_SIZE))
        
class IceTower(BasicTower):
    """Tháp băng, bắn đạn gây sát thương và làm chậm kẻ địch"""
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self._cost = 150
        self._color_for_levels = {1: LIGHT_BLUE, 2: ICE_BLUE, 3: DARK_BLUE}
        self._tower_type = "Ice"

    def shoot(self):
        """Tháp băng bắn đạn làm chậm kẻ địch"""

        if self._level == 1:
             return [IceBullet(self._x, self._y)]
        elif self._level == 2:
             return [IceBullet(self._x, self._y, -0.2), IceBullet(self._x, self._y, 0), IceBullet(self._x, self._y, 0.2)]
        else:
           # if bugs:
           #     nearest_bug = min(bugs, key=lambda m: math.hypot(m.x - bullet_x, m.y - bullet_y))
           #     angle = math.atan2(nearest_bug.y - bullet_y, nearest_bug.x - bullet_x)
           # else:
           #     angle = 0
           # bullets.append([bullet_x, bullet_y, angle, self._level, "ice"])
           # bullets.append([bullet_x, bullet_y, angle, self._level, "ice"])
           # bullets.append([bullet_x, bullet_y, angle, self._level, "ice"])  # Đạn băng đuổi
            return []
