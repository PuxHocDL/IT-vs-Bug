import pygame
from config import *
# Hàm vẽ tháp
class tower_game:
    def __init__(self,x,y,level):
        self.x = x
        self.y = y
        self.level = 1 
    def draw_tower(x, y, level):
        if level == 1:
            color = BLUE
        elif level == 2:
            color = YELLOW
        elif level == 3:
            color = RED
        pygame.draw.rect(screen, color, (x, y, TOWER_SIZE, TOWER_SIZE))
    # Hàm vẽ vật làm chậm
    def draw_slow(x, y):
        pygame.draw.rect(screen, PURPLE, (x, y, SLOW_SIZE, SLOW_SIZE))

    # Hàm vẽ thông tin vàng
    def draw_gold():
        gold_text = font.render(f"Gold: {gold}", True, BLACK)
        screen.blit(gold_text, (10, 10))

    # Hàm vẽ nút mua tháp
    def draw_buy_tower_button():
        pygame.draw.rect(screen, GREEN, (10, HEIGHT - 60, 230, 50))
        buy_text = font.render("Buy Tower - $50", True, BLACK)
        screen.blit(buy_text, (20, HEIGHT - 50))

    # Hàm vẽ nút mua vật làm chậm
    def draw_buy_slow_button():
        pygame.draw.rect(screen, PURPLE, (250, HEIGHT - 60, 230, 50))
        buy_text = font.render("Buy Slow - $100", True, WHITE)
        screen.blit(buy_text, (260, HEIGHT - 50))

    # Hàm nâng cấp tháp
    def upgrade_tower(index):
        global gold
        if gold >= upgrade_cost and towers[index][2] < 3:
            towers[index] = (towers[index][0], towers[index][1], towers[index][2] + 1)
            gold -= upgrade_cost
