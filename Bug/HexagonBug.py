from bug import *
class HexagonBug(Bug):
    """
    A class representing a hexagon bug in the game, inheriting from Bug.

    Attributes:
        fly_bug_image (list): Class attribute containing the loaded images for a hexagon bug.
        expanded_fly_bug_image (list): Expanded list of images for smoother animation.

    Methods:
        __init__(self._ x, y, speed, health, max_health, bug_size, rect_x, rect_y, name): Initializes a HexagonBug instance with its properties.
        update(self): Updates the bug's position and speed, including a flying effect.
        draw(self, screen): Draws the hexagon bug on the screen.
        draw_health_bar(self, screen): Draws the health bar of the hexagon bug.
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
        super().__init__(x, y, speed=100, max_health=1000, bug_size=200, rect_x=120, rect_y=100, name="HexagonBug")
        self._atk_interval = 3
        self._shoot_index = 9
        self._atk_index = 6

        self._images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_5","alive", f"{i}.png")), (200, 200)) for i in range(10)]
        self._images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_5","dead", f"{i}.png")), (200, 200)) for i in range(10)]
        self._images_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_5","attack", f"{i}.png")), (400, 400)) for i in range(8)]
        self._images_shoot = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_5","shoot", f"{i}.png")), (200,200)) for i in range(12)]
        self._load_imgs()
