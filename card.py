import pygame
import os
from tower import *


class Card:
    def __init__(self, x, y, size, img=pygame.image.load(os.path.join("assets", "UI", "unknown.png")), time=1, name="", price=""):
        self.__font = pygame.font.Font(os.path.join("assets", "vinque.otf"), 10)
        self.__name = self.__font.render(name, True, "black")
        self.__name_rect = self.__name.get_rect()
        self.__price = price
        self.__price_text = self.__font.render(str(price), True, "black")
        self.__price_rect = self.__price_text.get_rect()

        self._tower = None
        self._avatar = None
        self.__x = x
        self.__y = y
        self.__size = size
        self.__img = pygame.transform.scale(img, (size, 1.5*size))
        self.__timer_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "timer_img.png")), (size, 1.5*size))
        self.__current_time = 0
        self.__time = time
        self.__selected = False

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
        grid.add_object(grid_x, grid_y, self._tower(screen_pos[0] + rect_size // 2, screen_pos[1] + rect_size // 2, rect_size))

    def get_ID(self):
        return self.__id

    def get_price(self):
        return self.__price

    def get_img(self):
        return self._avatar


class BasicTowerCard(Card):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "basic_tower_card.png")), 10000, "Basic Tower", 300)
        self._tower = BasicTower
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "basic_tower.png")), (size, size))


class IceTowerCard(Card):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "ice_tower_card.png")), 30000, "Ice Tower", 500)
        self._tower = IceTower
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "ice_tower.png")), (size, size))

class FireTowerCard(Card):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, pygame.image.load(os.path.join("assets", "UI", "fire_tower_card.png")), 10000, "Fire Tower", 800)
        self._tower = FireTower
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "fire_tower.png")), (size, size))