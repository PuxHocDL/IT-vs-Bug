from config import *
import math
from collections import defaultdict

class BasicTower:
    """Tháp cơ bản, bắn đạn gây sát thương lên quái vật"""
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._level = 1
        self._cost = 50  # Giá mua tháp
        self._color_for_levels = {1: BLUE, 2: YELLOW, 3: RED}
        self._tower_type = "Tower"
        self._health=100
        self._image=None
        self._idle_imgs = []
        self._atk_imgs = []
        self._destroy_imgs = []
        self._img_mode = {0: self._idle_imgs, 1: self._atk_imgs, 2: self._destroy_imgs}
        self._animate_time = {0: 200, 1: 500, 2: 500}
        self._mode = 0
        self._img_index = 0
        self._current_time = 0
        
    def upgrade(self):
        global gold
        if gold.gold >= upgrade_cost and self._level < 3:
            self._level += 1
            gold.gold -= upgrade_cost
            
    def shoot(self):
        """Tháp bắn đạn"""
        bullet_x = self._x - BULLET_SIZE // 2
        bullet_y = self._y - BULLET_SIZE // 2
        
        if self._level == 1:
             bullets.append([bullet_x, bullet_y, 0, self._level, "normal"])  # Đạn bình thường

        elif self._level == 2:
             bullets.extend([[bullet_x, bullet_y, angle, self._level, "normal"] for angle in [-0.2, 0, 0.2]])  # Đạn cuồng cung
            
        else:
            if bugs:
                nearest_bug = min(bugs, key=lambda m: math.hypot(m.get_x() - bullet_x, m.get_y() - bullet_y))
                angle = math.atan2(nearest_bug.get_y() - bullet_y, nearest_bug.get_x() - bullet_x)
            else:
                angle = 0
            bullets.append([bullet_x, bullet_y, angle, self._level, "normal"])  # Đạn đuổi
            bullets.append([bullet_x, bullet_y, angle, self._level, "normal"])  # Đạn đuổi
            bullets.append([bullet_x, bullet_y, angle, self._level, "normal"])  # Đạn đuổi

    def draw(self, dt):
        current_imgs = self._img_mode[self._mode]
        if self._current_time > self._animate_time[self._mode]:
            self._img_index = (self._img_index + 1) % len(current_imgs)
        screen.blit(current_imgs[self._img_index], (self._x, self._y))
        self._current_time += dt

    def set_mode(self, mode):
        self._mode = mode
        self._img_index = 0


class SlowTower(BasicTower):
    """Tháp làm chậm, kế thừa từ basic_tower, làm chậm tốc độ di chuyển của quái"""
    def __init__(self x, y):
        super().__init__(x, y)
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
    
    def draw_tower(x, y, level):
        """Vẽ tháp ở vị trí x, y với cấp độ level"""
        color_for_levels = {1: BLUE, 2: YELLOW, 3: RED}
        pygame.draw.rect(screen, color_for_levels[level], (x, y, TOWER_SIZE, TOWER_SIZE))
    def upgrade_tower(index):
        """Nâng cấp tháp tại vị trí index"""
        BasicTower.upgrade(index)
    
    def draw_slow(x, y):
        """Vẽ vật làm chậm ở vị trí x, y"""
        pygame.draw.rect(screen, PURPLE, (x, y, TOWER_SIZE, TOWER_SIZE))
        
class IceTower(BasicTower):
    """Tháp băng, bắn đạn gây sát thương và làm chậm kẻ địch"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self._cost = 150
        self._color_for_levels = {1: LIGHT_BLUE, 2: ICE_BLUE, 3: DARK_BLUE}
        self._tower_type = "Ice"

    def shoot(self):
        """Tháp băng bắn đạn làm chậm kẻ địch"""
        bullet_x = self._x - BULLET_SIZE // 2
        bullet_y = self._y - BULLET_SIZE // 2
        if self._level == 1:
            bullets.append([bullet_x, bullet_y, 0, self._level, "ice"])  # Đạn băng bình thường
        elif self._level == 2:
            bullets.extend([[bullet_x, bullet_y, angle, self._level, "ice"] for angle in [-0.2, 0, 0.2]])  # Đạn băng cuồng cung
        else:
            if bugs:
                nearest_bug = min(bugs, key=lambda m: math.hypot(m.x - bullet_x, m.y - bullet_y))
                angle = math.atan2(nearest_bug.y - bullet_y, nearest_bug.x - bullet_x)
            else:
                angle = 0
            bullets.append([bullet_x, bullet_y, angle, self._level, "ice"])
            bullets.append([bullet_x, bullet_y, angle, self._level, "ice"])
            bullets.append([bullet_x, bullet_y, angle, self._level, "ice"])  # Đạn băng đuổi
            
    def upgrade(self):
        """Nâng cấp tháp"""
        if gold.gold >= upgrade_cost and self._level < 3:
            self._level += 1
            gold.gold -= upgrade_cost
