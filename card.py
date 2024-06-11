import pygame
import os
from tower import *


class Card:
    price = 0
    def __init__(self, x, y, size, img=pygame.image.load(os.path.join("assets", "UI", "unknown.png")), time=1, init_time=0, name=""):
        self.__font = pygame.font.Font(os.path.join("assets", "vinque.otf"), 10)
        self.__name = self.__font.render(name, True, "black")
        self.__name_rect = self.__name.get_rect()
        self._price = Card.price
        self.__price_text = self.__font.render(str(self._price), True, "black")
        self.__price_rect = self.__price_text.get_rect()

        self._tower = None
        self._avatar = None
        self.__x = x
        self.__y = y
        self.__size = size
        self.__img = pygame.transform.scale(img, (size, 1.5*size))
        self.__timer_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "timer_img.png")), (size, 1.5*size))
        self.__current_time = init_time
        self.__time = time
        self.__selected = False

    def _load_price(self):
        self.__price_text = self.__font.render(str(self._price), True, "black")
        self.__price_rect = self.__price_text.get_rect()

    def draw(self, screen, dt):
        screen.blit(self.__img, (self.__x, self.__y))
        screen.blit(self.__name, (self.__x+(self.__size-self.__name_rect.w)/2, self.__y+self.__name_rect.h/2))
        screen.blit(self.__price_text, (self.__x+(self.__size-self.__price_rect.w)/2, self.__y + 1.2*self.__size))
        timer_img = pygame.transform.scale(self.__timer_img, (self.__size, 1.5*self.__size*(1-(self.__current_time/self.__time))))
        if self.__selected:
            screen.blit(self.__timer_img, (self.__x, self.__y))
        else:
            screen.blit(timer_img, (self.__x, self.__y))

        self.__current_time = min(self.__current_time + dt, self.__time)

    def check_avail(self):
        return self.__current_time == self.__time

    def check_input(self, mouse_x, mouse_y):
        return mouse_x in range(self.__x, self.__x+self.__size) and mouse_y in range(self.__y, int(self.__y+1.5*self.__size))

    def toggle_select(self):
        self.__selected = not self.__selected

    def reset_time(self):
        self.__current_time = 0

    def add_tower(self, grid, grid_x, grid_y):
        screen_pos = grid.convert_to_screen_pos(grid_x, grid_y)
        rect_size = grid.get_cell_size()
        grid.add_object(grid_x, grid_y, self._tower(screen_pos[0] + rect_size // 2, screen_pos[1] + rect_size // 2, rect_size, self._price))

    def get_price(self):
        return self.__price

    def get_img(self):
        return self._avatar

    def set_affordable(self, value):
        if value < self._price:
            self.__price_text = self.__font.render(str(self._price), True, "red")
        else:
            self.__price_text = self.__font.render(str(self._price), True, "black")


class BasicTowerCard(Card):
    price = 300
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "basic_tower_card.png")), 10000, 3000, "Basic Tower")
        self._price = BasicTowerCard.price
        self._tower = BasicTower
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "basic_tower.png")), (size, size))
        self._load_price()


class IceTowerCard(Card):
    price = 500
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "ice_tower_card.png")), 15000, 0, "Ice Tower")
        self._price = IceTowerCard.price
        self._tower = IceTower
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "ice_tower.png")), (size, size))
        self._load_price()

class FireTowerCard(Card):
    price = 800
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "fire_tower_card.png")), 20000, 10000, "Fire Tower")
        self._price = FireTowerCard.price
        self._tower = FireTower
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "fire_tower.png")), (size, size))
        self._load_price()

class TheWallCard(Card):
    price = 100
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "the_wall_card.png")), 10000, 10000, "The Wall")
        self._price = TheWallCard.price
        self._tower = TheWall
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "the_wall.png")), (size, size))
        self._load_price()

class TheRookCard(Card):
    price = 1200
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "the_rook_card.png")), 30000, 30000, "The Rook")
        self._price = TheRookCard.price
        self._tower = TheRook
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "the_rook.png")), (size, size))
        self._load_price()

class ObeliskCard(Card):
    price = 500
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "obelisk_card.png")), 20000, 15000, "Obelisk")
        self._price = ObeliskCard.price
        self._tower = Obelisk
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "obelisk.png")), (size, size))
        self._load_price()

class HealingTowerCard(Card):
    price = 300
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "healing_tower_card.png")), 20000, 20000, "Healing Tower")
        self._price = HealingTowerCard.price
        self._tower = HealingTower
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "healing_tower.png")), (size, size))
        self._load_price()

class TheBombCard(Card):
    price = 500
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "the_bomb_card.png")), 2000, 2000, "The Bomb")
        self._price = TheBombCard.price
        self._tower = TheBomb
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "the_bomb.png")), (size, size))
        self._load_price()

class GoldenRookCard(Card):
    price = 1000
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "golden_rook_card.png")), 5000, 40000, "Golden Rook")
        self._price = GoldenRookCard.price
        self._tower = GoldenRook
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "golden_rook.png")), (size, size))
        self._load_price()
