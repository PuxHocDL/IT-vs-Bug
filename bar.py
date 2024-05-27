import pygame
class Bar:
    """
    Class for Bar object.
    """
    def __init__(self, x, y, w, h, color, bg_color, max_val):
        """
        Initializes the Bar object.

        Parameters:
            x (int): the x position of the Bar on the screen.
            y (int): the y position of the Bar on the screen.
            w (int): the width of the Bar (in pixels).
            h (int): the height of the Bar (in pixels).
            color (tuple): RGB color code of the Bar.
            bg_color (tuple): RGB color code for the background of the Bar.
            max_val (int): the value in which the Bar is full.
        """
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__color = color
        self.__bg_color = bg_color
        self.__max_val = max_val
        self.__val = max_val

    def set_val(self, val):
        """
        Sets the current value of the Bar.

        Parameters:
            val (int): value to be set.
        """
        self.__val = val

    def draw(self, screen):
        """
        Draws the bar to the screen.

        Parameters:
            screen (pygame.Surface): the surface in which the Bar is drawn.
        """
        pygame.draw.rect(screen, self.__bg_color, [self.__x, self.__y, self.__w, self.__h])
        pygame.draw.rect(screen, self.__color, [self.__x, self.__y, self.__w*self.__val/self.__max_val, self.__h])
        pygame.draw.rect(screen, "black", [self.__x, self.__y, self.__w, self.__h], 1)
