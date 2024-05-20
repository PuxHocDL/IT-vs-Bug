import pygame
from config import *
class Bullet:
     # Hàm vẽ đạn
    def draw_bullet(x, y):
        pygame.draw.rect(screen, BLACK, (x, y, BULLET_SIZE, BULLET_SIZE))
