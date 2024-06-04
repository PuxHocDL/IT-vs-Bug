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
        super().__init__(x, y, speed=0.5, max_health=900, bug_size=150, rect_x=150, rect_y=150, name="NormalBug")
        
        self._images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","alive", f"pic_{i}.png")), (150, 150)) for i in range(9)]
        self._images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_1","dead", f"{i}.png")), (150, 150)) for i in range(12)]
        self._load_imgs()
