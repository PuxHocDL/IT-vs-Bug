import pygame
from config import *

class Bullet:
    
    normal_bullet_image = pygame.image.load(os.path.join("assets", "PeaNormal_0.png"))

    break_bullet_image = pygame.image.load(os.path.join("assets", "PeaNormalExplode_0.png"))

    ice_bullet_image = pygame.image.load(os.path.join("assets", "PeaIce_0.png"))

    @staticmethod
    def draw_normal_bullet(x, y):
            screen.blit(Bullet.normal_bullet_image, (x, y))     

    def draw_ice_bullet(x, y):
            screen.blit(Bullet.ice_bullet_image, (x, y))

    def draw_bullet_with_collision(x,y): 
            screen.blit(Bullet.break_bullet_image, (x, y))
    
