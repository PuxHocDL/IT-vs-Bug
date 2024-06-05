import pygame

class Card:
    def __init__(self, x, y, img, size, time):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__bg_img = None
        self.__img = img
        self.__timer_img = None
        self.__current_time = 0
        self.__time = time
        self.__selected = False

    def draw(self, screen, dt):
        screen.blit(self.__bg_img, (self.__x, self.__y))
        screen.blit(self.__img, (self.__x, self.__y))
        timer_img = pygame.transform.scale(self.__timer_img, (self.__size, 2*self.__size*(self.__current_time/self.__time)))

        
        self.__current_time = min(self.__current_time + dt, self.__time)
