import pygame
# Kích thước màn hình
pygame.init()
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)  # Màu của vật làm chậm

# Tốc độ khung hình
FPS = 60

# Kích thước quái vật và đạn
MONSTER_SIZE = 50
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
font = pygame.font.SysFont(None, 36)

# Chế độ đặt tháp hoặc vật làm chậm
placing_tower = False
placing_slow = False
# Tạo danh sách chứa các quái vật, đạn, tháp, và vật làm chậm
monsters = []
bullets = []
towers = []
