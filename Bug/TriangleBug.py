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
        self._animate_time = {0: 1000, 1: 1000, 2: 1000, 3: 2000}
        self._atk_interval = 7
        self._shoot_index = 7

        self._images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3","alive", f"{i}.png")), (180, 180)) for i in range(7)]
        self._images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3","dead", f"{i}.png")), (180, 180)) for i in range(7)]
        self._images_shoot = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3","attack", f"{i}.png")), (180, 180)) for i in range(10)]
        self._load_imgs()
