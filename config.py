import os
import pygame
import colors
from button import Button
import colors
from button import Button
from grid import Grid
from projectile_manager import ProjectileManager
from hand import Hand
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



projectiles = ProjectileManager()
bug_projectiles = ProjectileManager()

brightness = 1
