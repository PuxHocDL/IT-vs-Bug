from config import *
from collections import defaultdict
class basic_tower:
    """tháp cơ bản, bắn đạn gây sát thương ln quái"""
    def __init__(self,x,y):
        """x,y: tọa độ tháp, level: cấp tháp, color_for_levels: màu ứng với từng cấp"""
        global gold
        self.x=x
        self.y=y
        self.level=1
        self.cost=50   # giá mua tháp
        self.buy_button=[GREEN,(10,HEIGHT-60,230,50)]#[màu tháp, hình chữ nhật tháp]
        self.color_for_levels={1: BLUE, 2: YELLOW, 3: RED}
        self.tower_type="Tower"
        gold-=self.cost
    def draw_tower(self):
        """vẽ tháp"""
        pygame.draw.rect(screen, self.color_for_levels[self.level], (self.x, self.y, TOWER_SIZE, TOWER_SIZE))
    def draw_buy_button(self):
        """vẽ nút mua tháp"""
        """        pygame.draw.rect(screen, GREEN, (10, HEIGHT - 60, 230, 50))
        buy_text = font.render("Buy Tower - $50", True, BLACK)
        screen.blit(buy_text, (20, HEIGHT - 50))"""
        pygame.draw.rect(screen, *self.buy_button)
        buy_text = font.render("Buy {} - ${}".format(self.tower_type,self.cost), True, WHITE)
        screen.blit(buy_text, (self.buy_button[1][0]+10,self.buy_button[1][1]+10))
    # Hàm nâng cấp tháp
    def upgrade(index):
        global gold
        if gold >= upgrade_cost and towers[index][2] < 3:
            towers[index] = (towers[index][0], towers[index][1], towers[index][2] + 1)
            gold -= upgrade_cost
    def shoot(self):
        """tháp bắn đạn"""
        bullet_x = self.x + TOWER_SIZE // 2 - BULLET_SIZE // 2
        bullet_y = self.y + TOWER_SIZE // 2 - BULLET_SIZE // 2
        if(self.level==1):
            bullets.append([bullet_x, bullet_y, 0, self.level]) # đạn bình thường
        elif(self.level==2):
            bullets.extend([[bullet_x, bullet_y, angle, self.level] for angle in [-0.2,0,0.2]])# đạn cuồng cung
        else:
            if monsters:
                nearest_monster = min(monsters, key=lambda m: math.hypot(m[0] - bullet_x, m[1] - bullet_y))
                angle = math.atan2(nearest_monster[1] - bullet_y, nearest_monster[0] - bullet_x)
            else:
                angle = 0
            bullets.append([bullet_x, bullet_y, angle, self.level])  # Đạn đuổi
class slow_tower(basic_tower):
    """tháp làm chậm, được kế thừa từ basic_tower, làm chậm tốc độ di chuyển của quái"""
    def __init__(self,x,y):
        """tạo tháp làm chậm"""
        global gold
        super().__init__(x,y)
        self.cost=100
        self.buy_button=[PURPLE,(250, HEIGHT - 60, 230, 50)]
        self.tower_type="Slow"
        gold-=self.cost-100 # vì hàm super đã trừ gold đi 100 rồi nên phải cộng lại
        self.color=defaultdict(lambda: PURPLE) # màu là PURPLE cho mọi cấp
    def shoot(self):
        """làm chậm tốc độ quái trên sân"""
        for monster in monsters:
            monster.speed = 1  # Giảm tốc độ quái vật
            monster.slowed = True  # Đánh dấu bị làm chậm
            monster.slow_timer = pygame.time.get_ticks() + 10000  # Thiết lập thời gian kết thúc làm chậm
    # Hàm vẽ nút mua vật làm chậm
    def draw_buy_slow_button():
        pygame.draw.rect(screen, PURPLE, (250, HEIGHT - 60, 230, 50))
        buy_text = font.render("Buy Slow - $100", True, WHITE)
        screen.blit(buy_text, (260, HEIGHT - 50))
    # Hàm vẽ vật làm chậm
    def draw_slow(x, y):
        pygame.draw.rect(screen, PURPLE, (x, y, SLOW_SIZE, SLOW_SIZE))
class tower_game: 
    # Hàm vẽ thông tin vàng
    def draw_gold():
        gold_text = font.render(f"Gold: {gold}", True, BLACK)
        screen.blit(gold_text, (10, 10))
