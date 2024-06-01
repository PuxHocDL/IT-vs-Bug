from bug import *
class TriangleBug(Bug):
    """
    A class representing a triangle bug in the game, inheriting from Bug.

    Methods:
        draw(self._ screen): Draws the triangle bug on the screen.
        draw_health_bar(self._ screen): Draws the health bar of the triangle bug.
        create_triangle_bug(bugs, grid): Static method to create and add a triangle bug to the game.
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
        super().__init__(x, y, speed=0.5, max_health=200, bug_size=50, rect_x=130, rect_y=150, name="TriangleBug")
        self._x = WIDTH
        self._y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + (grid.get_cell_size()+20)//2
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
        return(super().draw_dead(screen,dt,self.__triangle_bug_images_dead))

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