from bug import *
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
        super().__init__(x, y, speed=0.5, max_health=1000, bug_size=100, rect_x=120, rect_y=100, name="HexagonBug")
        self._x = WIDTH
        self._y = random.choice(range(HEIGHT  - grid.get_cell_size() * grid.get_rows(), HEIGHT  , grid.get_cell_size())) + (grid.get_cell_size()-50)//2 - 350
        self.__fly_bug_image = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","alive", f"{i}.png")), (400, 400)) for i in range(0, 6)]
        self.__fly_bug_image_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","dead", f"{i}.png")), (400, 400)) for i in range(0, 3)]
        self.__fly_bug_image_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_4","attack", f"{i}.png")), (400, 400)) for i in range(0, 18)]
    def update(self):
        """
        Updates the bug's position and speed, including a flying effect.
        """
        super().update()
    def draw(self, dt, screen):
        super().draw_alive_no_attacking(screen,dt,self.__fly_bug_image)

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
        return(super().draw_dead(screen,dt,self.__fly_bug_image_dead))
    
    def draw_attack(self,dt, screen): 
        super().draw_attack(screen,dt,self.__fly_bug_image_attack)

    def get_rect(self): 
        return pygame.Rect(self._x + 150, self._y+250, self._rect_x, self._rect_y)
