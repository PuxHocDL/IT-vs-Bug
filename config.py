import os
import pygame
import Colors
from Button import Button
# Kích thước màn hình
pygame.init()
WIDTH, HEIGHT = 1300, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Màu sắc
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)  # Màu của vật làm chậm
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
mediumaquamarine = (102, 205, 170)
# Tốc độ khung hình
FPS = 60

# Kích thước quái vật và đạn
BULLET_SIZE = 10
TOWER_SIZE = 50
SLOW_SIZE = 50
# Tốc độ đạn
bullet_speed = 5
# Giá tiền mua tháp và vật làm chậm
tower_cost = 50
slow_cost = 100
slow_placed = False
# Giá nâng cấp tháp
upgrade_cost = 200
class gold:
    gold = 3000

# Tần suất bắn đạn (tính bằng khung hình)
shoot_delay = 60
shoot_counters = []

# Phông chữ
font = pygame.font.Font(os.path.join("assets", "vinque.otf"), 36)

buy_tower_btn = Button((10, HEIGHT - 50), "Buy Tower - $50", font, Colors.black, Colors.lime, Colors.red)
buy_slow_btn = Button((350, HEIGHT - 50), "Buy Slow - $100", font, Colors.black, Colors.dark_yellow, Colors.red)

# Chế độ đặt tháp hoặc vật làm chậm
placing_tower = False
placing_slow = False
# Tạo danh sách chứa các quái vật, đạn, tháp, và vật làm chậm
BUGs = []
bullets = []
towers = []

