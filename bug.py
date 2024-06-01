import pygame
import random
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

    def __init__(self, x, y, speed, max_health, bug_size, rect_x, rect_y, name):
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
        self._max_health = max_health
        self._health = max_health
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
    def draw_alive_no_attacking(self, screen, dt, image):
        """
        Draws the normal bug on the screen.
        
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
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
            projectile = [Skull(self._x, self._y+self._rect_y//2 - 20, reverse=True)]
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
        if not self._slowed and pygame.time.get_ticks() > self._slow_timer:
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

monster_schedule = [
    {"time": 5, "name": "HexagonBug"},
    {"time": 15, "name": "TriangleBug"},
    {"time": 20, "name": "BigBug"},
    {"time": 25, "name": "HexagonBug"},
]