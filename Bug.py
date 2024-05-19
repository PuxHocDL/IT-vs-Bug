import pygame
import random
from config import *
class Bug:
    def __init__(self, x, y, speed, health):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.slowed = False
        self.slow_timer = 0

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, MONSTER_SIZE, MONSTER_SIZE))

    def update(self):
        if self.slowed and pygame.time.get_ticks() > self.slow_timer:
            self.speed = 2
            self.slowed = False
        self.x -= self.speed

    def apply_slow(self):
        self.speed = 1
        self.slowed = True
        self.slow_timer = pygame.time.get_ticks() + 10000 
    
    # Hàm tạo quái vật mới
    def create_monster():
        monster_x = WIDTH
        monster_y = random.randint(0, HEIGHT - MONSTER_SIZE)
        monsters.append([monster_x, monster_y, 2, 100, False, 0])  # Tốc độ ban đầu của quái vật là 2, máu của quái vật là 100, thêm flag bị làm chậm và thời gian hết hiệu lực

        # Khởi tạo bộ đếm thời gian để tạo quái vật mới
    spawn_monster_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_monster_event, 1000)  # Tạo quái vật mới mỗi giây
    
    # Hàm vẽ quái vật
    def draw_monster(x, y):
        pygame.draw.rect(screen, RED, (x, y, MONSTER_SIZE, MONSTER_SIZE))

    # Hàm áp dụng hiệu ứng làm chậm cho tất cả quái vật
    def apply_slow_effect():
        for monster in monsters:
            monster[2] = 1  # Giảm tốc độ quái vật
            monster[4] = True  # Đánh dấu bị làm chậm
            monster[5] = pygame.time.get_ticks() + 10000  # Thiết lập thời gian kết thúc làm chậm
