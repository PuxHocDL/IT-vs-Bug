import pygame
import colors

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
        self.__size = (width - 150)//11
        self.__rows = 6
        self.__cols = 11
        self.__imgs = imgs
        self.__bg_img = bg_img
        self.__objects = []
        for _ in range(self.__rows):
            temp = []
            for _ in range(self.__cols):
                temp.append(None)
            self.__objects.append(temp)

    def reset(self):
        """
        Resets all the objects.
        """
        self.__objects = []

    def add_object(self, x, y, object):
        """
        Add an object to a Cell on the Grid.

        Parameters:
            x (int): the x position on the Grid.
            y (int): the y position on the Grid.
            image (pygame.Image): the image to be drawn.
        """
        self.__objects[x][y] = object

    def remove_objects(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__objects[i][j]:
                    if self.__objects[i][j].is_dead():
                        self.__objects[i][j] = None


    def convert_to_grid_pos(self, x, y):
        """
        Converts xy screen position to xy Grid position if possible.

        Parameters:
            x (int): the x position on the screen.
            y (int): the y position on the screen.

        Returns:
            (x, y): the xy position of the Grid. (-1, -1) if the passed position is beyond Grid's position or the Cell already has an object.
        """
        return (y - (self.__screen_height - 50 - self.__size*self.__rows))//self.__size, (x-50)//self.__size

    def is_inside_gird(self, i, j):
        if j in range(self.__cols) and i in range(self.__rows):
            return True
        return False
    
    def is_occupied(self, i, j):
        if not self.is_inside_gird(i, j):
            return False
        if self.__objects[i][j]:
            return True
        return False
    
    def convert_to_screen_pos(self, i, j):
        """
        Converts xy Grid position to xy screen position.

        Parameters:
            i (int): the row number in Grid.
            j (int): the column number in Grid.
        """
        x_offset = 50
        y_offset = self.__screen_height - 50 - self.__size*self.__rows
        x = x_offset + j*self.__size
        y = y_offset + i*self.__size
        return x, y

    def upgrade_tower(self, i, j):
        if self.is_occupied(i, j):
            self.__objects[i][j].upgrade()

    def draw(self, screen, dt):
        """
        Draws the Grid to the screen.

        Parameters:
            screen (pygame.Surface): the surface to be drawn on.

        Returns:
            projectiles: a List of Projectiles shot from towers.
        """
        projectiles = []
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

                if self.__objects[i][j]:
                    projectiles.extend(self.__objects[i][j].draw(screen, dt))
        return projectiles

    def draw_on_mouse_pos(self, screen, pos, img=None):
        """
        Draws the image on the mouse position.

        Parameters:
            screen (pygame.Surface): the surface to be drawn on.
            pos (tuple): xy mouse position.
        """
        if img:
            screen.blit(img, (pos[0], pos[1]))
        else:
            pygame.draw.rect(screen, colors.red, [pos[0]-self.__size//2, pos[1]-self.__size//2, self.__size, self.__size])

    def get_cell_size(self):
        return self.__size

    def get_objects(self):
        temp = []
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__objects[i][j]:
                    temp.append(self.__objects[i][j])
        return temp

    def get_objects_pos(self):
        poses = []
        for i in range(self.__rows):
            for j in range(self.__cols):
                poses.append((i, j))
        return poses

    def get_objs_in_row(self, row):
        temp = []
        if row in range(self.__rows):
            for obj in self.__objects[row]:
                if obj:
                    temp.append(obj)
        return temp

    def get_rows(self):
        return self.__rows
    
    def get_cols(self): 
        return self.__cols
