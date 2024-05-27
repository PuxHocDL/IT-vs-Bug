import pygame
import random
import math
from config import *

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
        self._current_image_index_dead = 0
        self._slowed_bullet = False
        self._name = name
        self._death = False
        self._image_index = 0
        self._attacking = True
        self._image_attack = 0
        self._collision_with_tower = False

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

    def apply_slow(self):
        """
        Applies a slowing effect to the bug.
        """
        self._speed = self._original_speed * 0.5
        self._slowed = True
        self._slow_timer = pygame.time.get_ticks() + 10000

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

    @staticmethod
    def apply_slow_effect(bugs):
        for bug in bugs:
            bug.apply_slow()

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

class NormalBug(Bug):
    """
    A class representing a normal bug in the game, inheriting from Bug.

    Methods:
        draw(self._ screen): Draws the normal bug on the screen.
        draw_death(self._ screen): Draws the normal bug's death animation on the screen.
        create_bug(bugs, grid): Static method to create and add a normal bug to the game.
        draw_health_bar(self._ screen): Draws the health bar of the normal bug.
    """

    __normal_bug_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","alive", f"pic_{i}.png")), (150, 150)) for i in range(0, 9)]
    __normal_bug_images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","dead", f"{i}.png")), (150, 150)) for i in range(0, 60)]
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
        self._health = 1900
        self._max_health = 1900 
        self._bug_size = 50
        self._rect_x = 150
        self._rect_y = 150
        self._name = "NormalBug"
        self._current_time = 0

    def draw(self, screen, dt):
        """
        Draws the normal bug on the screen.
        
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        self._current_time += dt
        if self._current_time > 1/9*1000:
            self._image_index = (self._image_index+1) % len(NormalBug.__normal_bug_images)
            self._current_time = 0
        current_image = NormalBug.__normal_bug_images[self._image_index]
        screen.blit(current_image, (self._x, self._y))

    def draw_death(self, screen):
        """
        Draws the normal bug's death animation on the screen.
        
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug's death animation.
        
        Returns:
            bool: True if the death animation is complete, False otherwise.
        """
        if self._current_image_index_dead < len(NormalBug.__normal_bug_images_dead):
            self._x -= self._speed * 0.3
            current_image = NormalBug.__normal_bug_images_dead[self._current_image_index_dead]
            screen.blit(current_image, (self._x, self._y))
            self._current_image_index_dead += 1
        else:
            return True
        return False

    def draw_health_bar(self, screen):
        """
        Draws the health bar of the normal bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        """
        if self._x > 11:
            health_bar_length = self._bug_size
            health_bar_height = 5
            fill = (self._health / self._max_health) * health_bar_length
            rect = self.get_rect()
            outline_rect = pygame.Rect(rect[0]+40, self._y - 10, health_bar_length, health_bar_height)
            fill_rect = pygame.Rect(rect[0]+40, self._y - 10, fill, health_bar_height)
            pygame.draw.rect(screen, (152, 251, 152), fill_rect)
            pygame.draw.rect(screen, BLACK, outline_rect, 1)

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
    __big_bug_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","alive", f"{i}.png")), (150, 150)) for i in range(0, 8)]
    __big_bug_images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","dead", f"{i}.png")), (150, 150)) for i in range(0, 6)]
    expanded_big_bug_images = []
    expanded_big_bug_images_dead = []
    for image in __big_bug_images:
        expanded_big_bug_images.extend([image] * 8)
    for image in __big_bug_images_dead:
        expanded_big_bug_images_dead.extend([image] * 10)
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
        self._rect_x = 150
        self._rect_y = 150
        self._name = "BigBug"


    def draw(self, screen):
        """
        Draws the big bug on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        current_image_index = self._image_index % len(BigBug.expanded_big_bug_images)
        current_image = BigBug.expanded_big_bug_images[current_image_index]
        screen.blit(current_image, (self._x, self._y))
        self._image_index += 1

    def draw_death(self, screen):
        """
        Draws the big bug's death animation on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug's death animation.

        Returns:
            bool: True if the death animation is complete, False otherwise.
        """
        if self._current_image_index_dead < len(BigBug.expanded_big_bug_images_dead):
            self._x -= self._speed * 0.3
            current_image = BigBug.expanded_big_bug_images_dead[self._current_image_index_dead]
            screen.blit(current_image, (self._x, self._y))
            self._current_image_index_dead += 1
        else:
            return True
        return False

    def draw_health_bar(self, screen):
        """
        Draws the health bar of the big bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        """
        if self._x > 11:
            health_bar_length = self._bug_size
            health_bar_height = 5
            fill = (self._health / self._max_health) * health_bar_length
            rect = self.get_rect()
            outline_rect = pygame.Rect(rect[0], self._y - 10, health_bar_length, health_bar_height)
            fill_rect = pygame.Rect(rect[0], self._y - 10, fill, health_bar_height)
            pygame.draw.rect(screen, (152, 251, 152), fill_rect)
            pygame.draw.rect(screen, BLACK, outline_rect, 1)

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
        self._rect_x = 70
        self._rect_y = 70
        self._name = "TriangleBug"
    def draw(self, screen):
        """
        Draws the triangle bug on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        points = [(self._x - self._bug_size, self._y - self._bug_size // 2), (self._x, self._y - self._bug_size), (self._x, self._y)]
        pygame.draw.polygon(screen, (72, 61, 139), points)

    def draw_health_bar(self, screen):
        """
        Draws the health bar of the triangle bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        """
        health_bar_length = self._bug_size
        health_bar_height = 5
        fill = (self._health / self._max_health) * health_bar_length
        outline_rect = pygame.Rect(self._x - self._bug_size, self._y + self._bug_size // 3, health_bar_length, health_bar_height)
        fill_rect = pygame.Rect(self._x - self._bug_size, self._y + self._bug_size // 3, fill, health_bar_height)
        pygame.draw.rect(screen, (152, 251, 152), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)

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
    fly_bug_image = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","alive", f"{i}.png")), (400, 400)) for i in range(0, 6)]
    expanded_fly_bug_image = []
    for image in fly_bug_image:
        expanded_fly_bug_image.extend([image] * 10)

    fly_bug_image_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","attack", f"{i}.png")), (400, 400)) for i in range(0, 18)]
    expanded_fly_bug_image_attack = []
    for image in fly_bug_image_attack:
        expanded_fly_bug_image_attack.extend([image] * 4)

    fly_bug_image_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","dead", f"{i}.png")), (400, 400)) for i in range(0, 3)]
    expanded_fly_bug_image_dead = []
    for image in fly_bug_image_dead:
        expanded_fly_bug_image_dead.extend([image] * 15)
    expanded_fly_bug_image_dead.extend([fly_bug_image_dead[2]] * 15)
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

    def update(self):
        """
        Updates the bug's position and speed, including a flying effect.
        """
        super().update()
    def draw(self, screen):
        """
        Draws the hexagon bug on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        current_image_index = self._image_index % len(HexagonBug.expanded_fly_bug_image)
        current_image = HexagonBug.expanded_fly_bug_image[current_image_index]
        screen.blit(current_image, (self._x, self._y))
        self._image_index += 1

    def draw_health_bar(self, screen):
        """
        Draws the health bar of the hexagon bug.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the health bar.
        """
        health_bar_length = self._bug_size
        health_bar_height = 5
        fill = (self._health / self._max_health) * health_bar_length
        outline_rect = pygame.Rect(self._x + self._bug_size//3, self._y + self._bug_size//2-20, health_bar_length, health_bar_height)
        fill_rect = pygame.Rect(self._x + self._bug_size//3, self._y + self._bug_size//2-20, fill, health_bar_height)
        pygame.draw.rect(screen, (152, 251, 152), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)

    def draw_death(self, screen):
        """
        Draws the Haxegon 's death animation on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug's death animation.

        Returns:
            bool: True if the death animation is complete, False otherwise.
        """
        if self._current_image_index_dead < len(HexagonBug.expanded_fly_bug_image_dead):
            current_image = HexagonBug.expanded_fly_bug_image_dead[self._current_image_index_dead]
            screen.blit(current_image, (self._x, self._y))
            self._current_image_index_dead += 1
        else:
            return True
        return False
    
    def draw_attack(self, screen): 
        current_image_index = self._image_attack % len(HexagonBug.expanded_fly_bug_image_attack)
        current_image = HexagonBug.expanded_fly_bug_image_attack[current_image_index]
        screen.blit(current_image, (self._x, self._y))
        self._image_attack += 1

    def get_rect(self): 
        return pygame.Rect(self._x + 150, self._y+250, self._rect_x, self._rect_y)

# Timers to spawn bugs
spawn_bug_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_bug_event, 20000)

spawn_big_bug_event = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_big_bug_event, 13000000)

spawn_triangle_bug_event = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_triangle_bug_event, 1800000)

spawn_hexagon_bug_event = pygame.USEREVENT + 4
pygame.time.set_timer(spawn_hexagon_bug_event, 1000000)
