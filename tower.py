from config import *
import math
from collections import defaultdict

class BasicTower:
    """Tháp cơ bản, bắn đạn gây sát thương lên quái vật"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.level = 1
        self.cost = 50  # Giá mua tháp
        self.color_for_levels = {1: BLUE, 2: YELLOW, 3: RED}
        self.tower_type = "Tower"
        self.health=100
        self.image=None

    def upgrade(self):
        global gold
        """Nâng cấp tháp"""
        if gold.gold >= upgrade_cost and self.level < 3:
            self.level += 1
            gold.gold -= upgrade_cost

    def shoot(self):
        """Tháp bắn đạn"""
        bullet_x = self.x - BULLET_SIZE // 2
        bullet_y = self.y - BULLET_SIZE // 2
        if self.level == 1:
            bullets.append([bullet_x, bullet_y, 0, self.level])  # Đạn bình thường
        elif self.level == 2:
            bullets.extend([[bullet_x, bullet_y, angle, self.level] for angle in [-0.2, 0, 0.2]])  # Đạn cuồng cung
        else:
            if BUGs:
                nearest_BUG = min(BUGs, key=lambda m: math.hypot(m.x - bullet_x, m.y - bullet_y))
                angle = math.atan2(nearest_BUG.y - bullet_y, nearest_BUG.x - bullet_x)
            else:
                angle = 0
            bullets.append([bullet_x, bullet_y, angle, self.level])  # Đạn đuổi

class SlowTower(BasicTower):
    """Tháp làm chậm, kế thừa từ basic_tower, làm chậm tốc độ di chuyển của quái"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = 100
        self.color_for_levels = defaultdict(lambda: PURPLE)  # Màu là PURPLE cho mọi cấp
        self.tower_type = "Slow"
    def shoot(self):
        """Làm chậm tốc độ quái trên sân"""
        for BUG in BUGs:
            BUG.speed = 1  # Giảm tốc độ quái vật
            BUG.slowed = True  # Đánh dấu bị làm chậm
            BUG.slow_timer = pygame.time.get_ticks() + 10000  # Thiết lập thời gian kết thúc làm chậm

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
