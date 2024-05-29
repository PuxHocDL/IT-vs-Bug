import pygame
import random
import math
from config import *
from projectile import *

class Bug:
    """
    A base class for all types of bugs in the game.

    Methods:
        __init__(self x, y, speed, health, max_health, bug_size, rect_x, rect_y, name): Initializes a Bug instance with its properties.
        get_rect(self): Returns the rectangular area of the bug for collision detection.
        update(self): Updates the bug's position and speed based on its current state.
        apply_slow(self._: Applies a slowing effect to the bug.
        draw(self._ screen): Abstract method to draw the bug on the screen.
        draw_death(self._ screen): Abstract method to draw the bug's death animation on the screen.
    """

    def __init__(self, x, y, speed, health, max_health, bug_size, rect_x, rect_y, name):
        """
        Initializes a Bug instance with the given parameters.
        
        Parameters:
            x (int): The x-coordinate of the bug.
            y (int): The y-coordinate of the bug.
            speed (float): The speed of the bug.
            health (int): The current health of the bug.
            max_health (int): The maximum health of the bug.
            bug_size (int): The size of the bug.
            rect_x (int): The width of the bug's rectangle.
            rect_y (int): The height of the bug's rectangle.
            name (str): The name of the bug.
        """
        self._x = x
        self._y = y
        self._speed = speed
        self._original_speed = speed
        self._health = health
        self._max_health = max_health
        self._slowed = False
        self._slow_timer = 0
        self._bug_size = bug_size
        self._rect_x = rect_x
        self._rect_y = rect_y
        self._slowed_bullet = False
        self._name = name
        self._death = False
        self._image_index_alive = 0
        self.attacking = False
        self._collision_with_tower = False
        self._current_time_dead = 0 
        self._image_index_dead = 0
        self._current_time_alive = 0
        self._image_index_alive = 0
        self._image_index_attack = -1
        self._current_time_attack = 0
        self._time_actions_alive = 0
        self._attack_times = 0
        self._bullet_check = False
    
    def draw_alive(self, screen, dt, image):
        """
        Draws the normal bug on the screen.
        
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        if self._time_actions_alive > 7*len(image): 
            self.attacking = True
            self._time_actions_alive = 0
        self._current_time_alive += dt
        if self._current_time_alive >= 1/(len(image))*1000:
            self._image_index_alive = (self._image_index_alive +1) % len(image)
            self._current_time_alive = 0
            self._time_actions_alive +=1 
        current_image = image[self._image_index_alive]
        screen.blit(current_image, (self._x, self._y))
        

    def draw_dead(self, screen, dt, image):
        """
        Draws the normal bug on the screen.
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        if self._image_index_dead < len(image):
            self._current_time_dead += dt
            current_image = image[self._image_index_dead]
            screen.blit(current_image, (self._x, self._y))
            if self._current_time_dead >= 1/(len(image))*1000:
                self._current_time_dead = 0 
                self._image_index_dead = (self._image_index_dead +1)
        else: 
            return True
        return False
            
    def draw_attack(self,screen,dt,image,time): 
        projectile = []
        self._current_time_attack += dt
        if self._attack_times > len(image):
            self.attacking = False
            self._attack_times = 0
        elif self._attack_times == 7:
            projectile = [Skull_attack(self._x, self._y+self._rect_y//2 - 20, reverse=True)]
            self._attack_times +=1
        else:
            if self._current_time_attack >= time/(len(image))*1000:
                self._image_index_attack = (self._image_index_attack +1) % len(image)
                self._current_time_attack = 0
                self._attack_times +=1
            current_image = image[self._image_index_attack]
            screen.blit(current_image, (self._x, self._y))
        return projectile
        

    def get_rect(self):
        """
        Returns the rectangular area of the bug for collision detection.
        
        Returns:
            pygame.Rect: The rectangle representing the bug's area.
        """
        return pygame.Rect(self._x, self._y, self._rect_x, self._rect_y)

    def update(self):
        """
        Updates the bug's position and speed based on its current state.
        """
        if self._slowed and pygame.time.get_ticks() > self._slow_timer:
            self._speed = self._original_speed
            self._slowed = False

        self._x -= self._speed

    def apply_slow(self, slow, slow_time):
        """
        Applies a slowing effect to the bug.
        """
        self._speed = self._original_speed * slow
        self._slowed = True
        self._slow_timer = slow_time + pygame.time.get_ticks()

    def draw(self, screen):
        """
        Abstract method to draw the bug on the screen.
        
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        pass

    def draw_death(self, screen) -> bool:
        """
        Abstract method to draw the bug's death animation on the screen.
        
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug's death animation.
        """
        pass

    def damage(self, dmg):
        self._health -= dmg
    
    def is_dead(self):
        return self._health <= 0
    
    def get_current_speed(self):
        return self._speed

    def is_slowed(self):
        return self._slowed 
    
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_name(self):
        return self._name
    def get_check_bullet(self): 
        return self._bullet_check
class NormalBug(Bug):
    """
    A class representing a normal bug in the game, inheriting from Bug.

    Methods:
        draw(self._ screen): Draws the normal bug on the screen.
        draw_death(self._ screen): Draws the normal bug's death animation on the screen.
        create_bug(bugs, grid): Static method to create and add a normal bug to the game.
        draw_health_bar(self._ screen): Draws the health bar of the normal bug.
    """
    def __init__(self, x, y, speed, health, max_health, bug_size, rect_x, rect_y, name):
        """
        Initializes a HexagonBug instance with the given parameters.
        
        Parameters:
            x (int): The x-coordinate of the bug.
            y (int): The y-coordinate of the bug.
            speed (float): The speed of the bug.
            health (int): The current health of the bug.
            max_health (int): The maximum health of the bug.
            bug_size (int): The size of the bug.
            rect_x (int): The width of the bug's rectangle.
            rect_y (int): The height of the bug's rectangle.
            name (str): The name of the bug.
        """
        super().__init__(x, y, speed, health, max_health, bug_size, rect_x, rect_y, name)
        self._x = WIDTH
        self._y =  random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + (grid.get_cell_size()-50)//2 + 50
        self._speed = 0.5
        self._health = 900
        self._max_health = 900 
        self._bug_size = 50
        self._rect_x = 150
        self._rect_y = 150
        self._name = "NormalBug"
        
        
        self.__normal_bug_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","alive", f"pic_{i}.png")), (150, 150)) for i in range(0, 9)]
        self.__normal_bug_images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","dead", f"{i}.png")), (150, 150)) for i in range(0, 12)]

    def draw(self,dt,screen): 
        super().draw_alive(screen,dt,self.__normal_bug_images)

    def draw_dead(self,dt,screen):
        super().draw_dead(screen,dt,self.__normal_bug_images_dead)

    """def draw_health_bar(self, screen):
        
        Draws the health bar of the normal bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        
        if self._x > 11:
            health_bar_length = self._bug_size
            health_bar_height = 5
            fill = (self._health / self._max_health) * health_bar_length
            rect = self.get_rect()
            outline_rect = pygame.Rect(rect[0]+40, self._y - 10, health_bar_length, health_bar_height)
            fill_rect = pygame.Rect(rect[0]+40, self._y - 10, fill, health_bar_height)
            pygame.draw.rect(screen, (152, 251, 152), fill_rect)
            pygame.draw.rect(screen, BLACK, outline_rect, 1)"""

class BigBug(Bug):
    """
    A class representing a big bug in the game, inheriting from Bug.

    Attributes:
        big_bug_images (list): Class attribute containing the loaded images for a big bug in an alive state.
        big_bug_images_dead (list): Class attribute containing the loaded images for a big bug in a dead state.
        expanded_big_bug_images (list): Expanded list of images for smoother animation.
        expanded_big_bug_images_dead (list): Expanded list of dead images for smoother animation.

    Methods:
        draw(self._ screen): Draws the big bug on the screen.
        draw_death(self._ screen): Draws the big bug's death animation on the screen.
        create_big_bug(bugs, grid): Static method to create and add a big bug to the game.
        draw_health_bar(self._ screen): Draws the health bar of the big bug.
    """
    def __init__(self, x, y, speed, health, max_health, bug_size, rect_x, rect_y, name):
        """
        Initializes a HexagonBug instance with the given parameters.
        
        Parameters:
            x (int): The x-coordinate of the bug.
            y (int): The y-coordinate of the bug.
            speed (float): The speed of the bug.
            health (int): The current health of the bug.
            max_health (int): The maximum health of the bug.
            bug_size (int): The size of the bug.
            rect_x (int): The width of the bug's rectangle.
            rect_y (int): The height of the bug's rectangle.
            name (str): The name of the bug.
        """
        super().__init__(x, y, speed, health, max_health, bug_size, rect_x, rect_y, name)
        self._x = WIDTH
        self._y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + (grid.get_cell_size()-80)//2 + 70
        self._speed = 0.5
        self._health = 1000
        self._max_health = 1000 
        self._bug_size = 80
        self._rect_x = 100
        self._rect_y = 100
        self._name = "BigBug"
        self.__big_bug_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","alive", f"{i}.png")), (150, 150)) for i in range(0, 8)]
        self.__big_bug_images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","dead", f"{i}.png")), (150, 150)) for i in range(0, 6)]
        self.__big_bug_images_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","attack", f"{i}.png")), (150, 150)) for i in range(0, 10)]

    def draw(self,dt,screen):
        """
        Draws the big bug on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        super().draw_alive(screen,dt,self.__big_bug_images)
    def draw_dead(self, dt,screen):
        """
        Draws the big bug's death animation on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug's death animation.

        Returns:
            bool: True if the death animation is complete, False otherwise.
        """
        super().draw_dead(screen,dt,self.__big_bug_images_dead)

    def draw_attack(self, screen, dt):
        return super().draw_attack(screen, dt, self.__big_bug_images_attack,1)
    
    """ def draw_health_bar(self, screen):
        
        Draws the health bar of the big bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        
        if self._x > 11:
            health_bar_length = self._bug_size
            health_bar_height = 5
            fill = (self._health / self._max_health) * health_bar_length
            rect = self.get_rect()
            outline_rect = pygame.Rect(rect[0], self._y - 10, health_bar_length, health_bar_height)
            fill_rect = pygame.Rect(rect[0], self._y - 10, fill, health_bar_height)
            pygame.draw.rect(screen, (152, 251, 152), fill_rect)
            pygame.draw.rect(screen, BLACK, outline_rect, 1)"""
    def get_rect(self): 
        return pygame.Rect(self._x + 25, self._y + 25, self._rect_x, self._rect_y)
class TriangleBug(Bug):
    """
    A class representing a triangle bug in the game, inheriting from Bug.

    Methods:
        draw(self._ screen): Draws the triangle bug on the screen.
        draw_health_bar(self._ screen): Draws the health bar of the triangle bug.
        create_triangle_bug(bugs, grid): Static method to create and add a triangle bug to the game.
    """
    def __init__(self, x, y, speed, health, max_health, bug_size, rect_x, rect_y, name):
        """
        Initializes a HexagonBug instance with the given parameters.
        
        Parameters:
            x (int): The x-coordinate of the bug.
            y (int): The y-coordinate of the bug.
            speed (float): The speed of the bug.
            health (int): The current health of the bug.
            max_health (int): The maximum health of the bug.
            bug_size (int): The size of the bug.
            rect_x (int): The width of the bug's rectangle.
            rect_y (int): The height of the bug's rectangle.
            name (str): The name of the bug.
        """
        super().__init__(x, y, speed, health, max_health, bug_size, rect_x, rect_y, name)
        self._x = WIDTH
        self._y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + (grid.get_cell_size()+20)//2
        self._speed = 0.5
        self._health = 200
        self._max_health = 200 
        self._bug_size = 50
        self._rect_x = 130
        self._rect_y = 150
        self._name = "TriangleBug"
        self.__triangle_bug_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3","alive", f"{i}.png")), (180, 180)) for i in range(0, 7)]
        self.__triangle_bug_images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3","dead", f"{i}.png")), (180, 180)) for i in range(0, 7)]
        self.__triangle_bug_images_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3","attack", f"{i}.png")), (180, 180)) for i in range(0, 10)]

    def draw(self,dt,screen):
        """
        Draws the big bug on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        super().draw_alive(screen,dt,self.__triangle_bug_images)
    def draw_dead(self, dt,screen):
        """
        Draws the big bug's death animation on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug's death animation.

        Returns:
            bool: True if the death animation is complete, False otherwise.
        """
        super().draw_dead(screen,dt,self.__triangle_bug_images_dead)

    def draw_attack(self, screen, dt):
        return super().draw_attack(screen, dt, self.__triangle_bug_images_attack,2)
    
    """ def draw_health_bar(self, screen):
        
        Draws the health bar of the big bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        
        if self._x > 11:
            health_bar_length = self._bug_size
            health_bar_height = 5
            fill = (self._health / self._max_health) * health_bar_length
            rect = self.get_rect()
            outline_rect = pygame.Rect(rect[0], self._y - 10, health_bar_length, health_bar_height)
            fill_rect = pygame.Rect(rect[0], self._y - 10, fill, health_bar_height)
            pygame.draw.rect(screen, (152, 251, 152), fill_rect)
            pygame.draw.rect(screen, BLACK, outline_rect, 1)"""
    def get_rect(self): 
        return pygame.Rect(self._x +20 , self._y + 15, self._rect_x, self._rect_y)


class HexagonBug(Bug):
    """
    A class representing a hexagon bug in the game, inheriting from Bug.

    Attributes:
        fly_bug_image (list): Class attribute containing the loaded images for a hexagon bug.
        expanded_fly_bug_image (list): Expanded list of images for smoother animation.

    Methods:
        __init__(self._ x, y, speed, health, max_health, bug_size, rect_x, rect_y, name): Initializes a HexagonBug instance with its properties.
        update(self._: Updates the bug's position and speed, including a flying effect.
        draw(self._ screen): Draws the hexagon bug on the screen.
        draw_health_bar(self._ screen): Draws the health bar of the hexagon bug.
        create_hexagon_bug(bugs, grid): Static method to create and add a hexagon bug to the game.
    """

    def __init__(self, x, y, speed, health, max_health, bug_size, rect_x, rect_y, name):
        """
        Initializes a HexagonBug instance with the given parameters.
        
        Parameters:
            x (int): The x-coordinate of the bug.
            y (int): The y-coordinate of the bug.
            speed (float): The speed of the bug.
            health (int): The current health of the bug.
            max_health (int): The maximum health of the bug.
            bug_size (int): The size of the bug.
            rect_x (int): The width of the bug's rectangle.
            rect_y (int): The height of the bug's rectangle.
            name (str): The name of the bug.
        """
        super().__init__(x, y, speed, health, max_health, bug_size, rect_x, rect_y, name)
        self._x = WIDTH
        self._y = random.choice(range(HEIGHT  - grid.get_cell_size() * grid.get_rows(), HEIGHT  , grid.get_cell_size())) + (grid.get_cell_size()-50)//2 - 350
        self._speed = 0.5
        self._health = 1000
        self._max_health = 1000 
        self._bug_size = 100
        self._rect_x = 120
        self._rect_y = 100
        self._name = "HexagonBug"

        self.__fly_bug_image = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","alive", f"{i}.png")), (400, 400)) for i in range(0, 6)]
        self.__fly_bug_image_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","dead", f"{i}.png")), (400, 400)) for i in range(0, 3)]
        self.__fly_bug_image_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","attack", f"{i}.png")), (400, 400)) for i in range(0, 18)]
    def update(self):
        """
        Updates the bug's position and speed, including a flying effect.
        """
        super().update()
    def draw(self, dt, screen):
        super().draw_alive(screen,dt,self.__fly_bug_image)

    """def draw_health_bar(self, screen):
        
        Draws the health bar of the hexagon bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        
        health_bar_length = self._bug_size
        health_bar_height = 5
        fill = (self._health / self._max_health) * health_bar_length
        outline_rect = pygame.Rect(self._x + self._bug_size//3, self._y + self._bug_size//2-20, health_bar_length, health_bar_height)
        fill_rect = pygame.Rect(self._x + self._bug_size//3, self._y + self._bug_size//2-20, fill, health_bar_height)
        pygame.draw.rect(screen, (152, 251, 152), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)"""

    def draw_dead(self, dt,screen):
        """
        Draws the Haxegon 's death animation on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug's death animation.

        Returns:
            bool: True if the death animation is complete, False otherwise.
        """
        super().draw_dead(screen,dt,self.__fly_bug_image_dead)
    
    def draw_attack(self,dt, screen): 
        super().draw_attack(screen,dt,self.__fly_bug_image_attack)

    def get_rect(self): 
        return pygame.Rect(self._x + 150, self._y+250, self._rect_x, self._rect_y)

# Timers to spawn bugs
spawn_bug_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_bug_event, 2000000)

spawn_big_bug_event = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_big_bug_event, 3000)

spawn_triangle_bug_event = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_triangle_bug_event, 3000)

spawn_hexagon_bug_event = pygame.USEREVENT + 4
pygame.time.set_timer(spawn_hexagon_bug_event, 1000000)
