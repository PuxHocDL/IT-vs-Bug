import pygame
import colors

class Cell:
    """
    Class for Cell object.
    """
    def __init__(self, x, y, image=None):
        """
        Initializes the Cell object.

        Parameters:
            image (pygame.Image): Image to be displayed.
        """
        self.__x = x
        self.__y = y
        self.__image = image

    def get_image(self):
        """
        Returns Image to be drawn.
        """
        return self.__image

    def get_pos(self):
        """
        Returns Cell's position on the Grid.
        """
        return self.__x, self.__y


class Grid:
    """
    Class for Grid object.
    """
    def __init__(self, width, height, imgs, bg_img=None):
        """
        Initializes the Grid object.

        Parameters:
            width (int): the width of the screen.
            height (int): the height of the screen.
            imgs (list): a list of tile images.
            bg_img (python.Image): Image object for the background.
        """
        self.__screen_width = width
        self.__screen_height = height
        self.__size = (width - 150)//10
        self.__rows = 7
        self.__cols = 9
        self.__imgs = imgs
        self.__bg_img = bg_img
        self.__cells = [[None for _ in range(self.__cols)] for _ in range(self.__rows)]

    def reset(self):
        """
        Resets all the objects.
        """
        self.__cells = []

    def add_object(self, x, y, image=None):
        """
        Add an object to a Cell on the Grid.

        Parameters:
            x (int): the x position on the Grid.
            y (int): the y position on the Grid.
            image (pygame.Image): the image to be drawn.
        """
        self.__cells[x][y] = Cell(x, y, image)

    def convert(self, x, y):
        """
        Converts xy screen position to xy Grid position if possible.

        Parameters:
            x (int): the x position on the screen.
            y (int): the y position on the screen.

        Returns:
            (x, y): the xy position of the Grid. (-1, -1) if the passed position is beyond Grid's position or the Cell already has an object.
        """
       # if x < 50 or x > 50 + self.__size*self.__cols or y > self.__screen_height - 50 or y < self.__screen_height - 50 - self.__size*self.__rows:
       #     return -1, -1
        x, y = (y - (self.__screen_height - 50 - self.__size*self.__rows))//self.__size, (x-50)//self.__size
        if x in range(self.__cols) and y in range(self.__rows) and not self.__cells[x][y]:
            return x, y
        return -1, -1


    def draw(self, screen):
        """
        Draws the Grid to the screen.

        Parameters:
            screen (pygame.Surface): the surface to be drawn on.
        """
        x_offset = 50
        y_offset = self.__screen_height - 50 - self.__size*self.__rows
        img_counter = 0
        for i in range(self.__rows):
            for j in range(self.__cols):
                x = x_offset + j*self.__size
                y = y_offset + i*self.__size
                screen.blit(pygame.transform.scale(self.__imgs[img_counter%len(self.__imgs)], (self.__size, self.__size)), (x, y))
                pygame.draw.rect(screen, colors.gray, [x, y, self.__size, self.__size], 1)
                img_counter += 1

                if self.__cells[i][j] is not None:
                    cell_img = self.__cells[i][j].get_image()
                    if cell_img:
                        screen.blit(cell_img, (x, y))
                    else:
                        pygame.draw.rect(screen, colors.red, [x, y, self.__size, self.__size])
