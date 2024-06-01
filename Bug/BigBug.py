from bug import *

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
    def __init__(self, x, y):
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
        super().__init__(x, y, speed=3, max_health=1000, bug_size=80, rect_x=100, rect_y=100, name="BigBug")
        self._x = WIDTH
        self._y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + (grid.get_cell_size()-80)//2 + 70
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
        return(super().draw_dead(screen,dt,self.__big_bug_images_dead))

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