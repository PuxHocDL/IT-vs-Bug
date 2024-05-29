import os
import pygame
import colors
from button import Button
import colors
from button import Button
from grid import Grid
from projectile_manager import ProjectileManager
# Kích thước màn hình
pygame.init()
WIDTH, HEIGHT = 1300, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Màu sắc
LIGHT_BLUE = (173, 216, 230)
ICE_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
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
BULLET_SIZE = 16
TOWER_SIZE = 50
SLOW_SIZE = 50
# Tốc độ đạn
bullet_speed = 5
# Giá tiền mua tháp và vật làm chậm
tower_cost = 50
slow_cost = 100
slow_placed = False
ice_cost = 300
count = 0
# Giá nâng cấp tháp
upgrade_cost = 200
class gold:
    gold = 3000
gold = gold()
# Tần suất bắn đạn (tính bằng khung hình)
shoot_delay = 60
shoot_counters = []

# Phông chữ
font = pygame.font.Font(os.path.join("assets", "vinque.otf"), 36)

buy_tower_btn = Button((10, HEIGHT - 50), "Buy Tower - $50", font, colors.black, colors.lime, colors.red)

buy_slow_btn = Button((350, HEIGHT - 50), "Buy Slow - $100", font, colors.black, colors.dark_yellow, colors.red)

buy_ice_btn = Button((700, HEIGHT - 50), "Buy Ice - $300", font, colors.black, colors.dark_yellow, colors.red)
# Chế độ đặt tháp hoặc vật làm chậm
placing_tower = False
placing_slow = False
placing_ice = False
upgrade_tower = True
# Tạo danh sách chứa các quái vật, đạn, tháp, và vật làm chậm
bullets = []


tile_imgs = [
    pygame.image.load(os.path.join("assets", "grass1.jpg")), 
    pygame.image.load(os.path.join("assets", "grass2.jpg"))
]
grid = Grid(WIDTH, HEIGHT, tile_imgs)

projectiles = ProjectileManager()
bug_projectiles = ProjectileManager()
