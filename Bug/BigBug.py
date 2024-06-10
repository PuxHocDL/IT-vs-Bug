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
        super().__init__(x, y, speed=15, max_health=1000, bug_size=200, rect_x=100, rect_y=100, name="BigBug")
        self._atk_interval = 7
        self._shoot_index = 7
        self._atk_index = [7]
        self.damaged = 20
        self.jumping = None

        self._images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","alive", f"{i}.png")), (200, 200)) for i in range(8)]
        self._images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","dead", f"{i}.png")), (200, 200)) for i in range(14)]
        self._images_shoot = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","attack", f"{i}.png")), (200, 200)) for i in range(10)]
        self._images_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_2","attack", f"{i}.png")), (200, 200)) for i in range(10)]
        self._load_imgs()
