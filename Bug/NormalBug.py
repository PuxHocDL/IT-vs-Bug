from bug import *
class NormalBug(Bug):
    """
    A class representing a normal bug in the game, inheriting from Bug.

    Methods:
        draw(self._ screen): Draws the normal bug on the screen.
        draw_death(self._ screen): Draws the normal bug's death animation on the screen.
        create_bug(bugs, grid): Static method to create and add a normal bug to the game.
        draw_health_bar(self._ screen): Draws the health bar of the normal bug.
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
        super().__init__(x, y, speed=0.5, max_health=900, bug_size=50, rect_x=150, rect_y=150, name="NormalBug")
        self._x = WIDTH
        self._y =  random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + (grid.get_cell_size()-50)//2 + 50
        
        self.__normal_bug_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","alive", f"pic_{i}.png")), (150, 150)) for i in range(0, 9)]
        self.__normal_bug_images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","dead", f"{i}.png")), (150, 150)) for i in range(0, 12)]

    def draw(self,dt,screen): 
        super().draw_alive_no_attacking(screen,dt,self.__normal_bug_images)

    def draw_dead(self,dt,screen):
        return(super().draw_dead(screen,dt,self.__normal_bug_images_dead))

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