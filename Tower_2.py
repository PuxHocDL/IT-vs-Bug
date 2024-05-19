from config import *
from collections import defaultdict

class basic_tower:
    """Tháp cơ bản, bắn đạn gây sát thương lên quái vật"""
    def __init__(self, x, y):
        global gold
        self.x = x
        self.y = y
        self.level = 1
        self.cost = 50  # Giá mua tháp
        self.color_for_levels = {1: BLUE, 2: YELLOW, 3: RED}
        self.tower_type = "Tower"
        gold -= self.cost
    
    def draw_tower(self):
        """Vẽ tháp"""
        pygame.draw.rect(screen, self.color_for_levels[self.level], (self.x, self.y, TOWER_SIZE, TOWER_SIZE))
    
    def create_basic_tower(x, y): 
        towers.append(basic_tower(x, y))
    
    def draw_buy_button():
        """Vẽ nút mua tháp"""
        pygame.draw.rect(screen, GREEN, (10, HEIGHT - 60, 230, 50))
        buy_text = font.render("Buy Tower - $50", True, WHITE)
        screen.blit(buy_text, (20, HEIGHT - 50))
    
    def upgrade(index):
        """Nâng cấp tháp"""
        global gold
        if gold >= upgrade_cost and towers[index].level < 3:
            towers[index].level += 1
            gold -= upgrade_cost
    
    def shoot(self):
        """Tháp bắn đạn"""
        bullet_x = self.x + TOWER_SIZE // 2 - BULLET_SIZE // 2
        bullet_y = self.y + TOWER_SIZE // 2 - BULLET_SIZE // 2
        if self.level == 1:
            bullets.append([bullet_x, bullet_y, 0, self.level])  # Đạn bình thường
        elif self.level == 2:
            bullets.extend([[bullet_x, bullet_y, angle, self.level] for angle in [-0.2, 0, 0.2]])  # Đạn cuồng cung
        else:
            if monsters:
                nearest_monster = min(monsters, key=lambda m: math.hypot(m.x - bullet_x, m.y - bullet_y))
                angle = math.atan2(nearest_monster.y - bullet_y, nearest_monster.x - bullet_x)
            else:
                angle = 0
            bullets.append([bullet_x, bullet_y, angle, self.level])  # Đạn đuổi

class slow_tower(basic_tower):
    """Tháp làm chậm, kế thừa từ basic_tower, làm chậm tốc độ di chuyển của quái"""
    def __init__(self, x, y):
        global gold
        super().__init__(x, y)
        self.cost = 100
        self.color_for_levels = defaultdict(lambda: PURPLE)  # Màu là PURPLE cho mọi cấp
        self.tower_type = "Slow"
        gold -= self.cost - 50  # Vì hàm super đã trừ gold đi 50 rồi nên phải cộng lại
    
    def shoot(self):
        """Làm chậm tốc độ quái trên sân"""
        for monster in monsters:
            monster.speed = 1  # Giảm tốc độ quái vật
            monster.slowed = True  # Đánh dấu bị làm chậm
            monster.slow_timer = pygame.time.get_ticks() + 10000  # Thiết lập thời gian kết thúc làm chậm
    
    def draw_buy_slow_button():
        """Vẽ nút mua vật làm chậm"""
        pygame.draw.rect(screen, PURPLE, (250, HEIGHT - 60, 230, 50))
        buy_text = font.render("Buy Slow - $100", True, WHITE)
        screen.blit(buy_text, (260, HEIGHT - 50))
    
    def draw_slow(x, y):
        """Vẽ vật làm chậm"""
        pygame.draw.rect(screen, PURPLE, (x, y, SLOW_SIZE, SLOW_SIZE))

class tower_game:
    """Các chức năng liên quan đến game tháp"""
    def draw_gold():
        """Vẽ thông tin vàng"""
        gold_text = font.render(f"Gold: {gold}", True, BLACK)
        screen.blit(gold_text, (10, 10))
    
    def draw_tower(x, y, level):
        """Vẽ tháp ở vị trí x, y với cấp độ level"""
        color_for_levels = {1: BLUE, 2: YELLOW, 3: RED}
        pygame.draw.rect(screen, color_for_levels[level], (x, y, TOWER_SIZE, TOWER_SIZE))
    
    def upgrade_tower(index):
        """Nâng cấp tháp tại vị trí index"""
        basic_tower.upgrade(index)
    
    def draw_buy_tower_button():
        """Vẽ nút mua tháp"""
        basic_tower.draw_buy_button()
    
    def draw_buy_slow_button():
        """Vẽ nút mua vật làm chậm"""
        slow_tower.draw_buy_slow_button()
    
    def draw_slow(x, y):
        """Vẽ vật làm chậm ở vị trí x, y"""
        slow_tower.draw_slow(x, y)
