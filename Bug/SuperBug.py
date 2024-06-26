from bug import *
class SuperBug(Bug):
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
        super().__init__(x, y, speed=20, max_health=3000, bug_size=400, rect_x=120, rect_y=100, name="SuperBug")
        pygame.mixer.init()
        self._animate_time = {0: 1500, 1: 2000, 2: 1000, 3: 2000, 4: 1500}
        self._atk_index = [6, 14, 31, 39]
        self._modifiled = 120
        self.fix_coli = 100
        self._jump_height = 100
        self._jump_duration = 2400
        self.jump_sound = pygame.mixer.Sound(os.path.join("assets", "music", "jump.wav"))
        self.damaged= 20
        self.fix_thunder = 100

        self._images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_7","run", f"{i}.png")), (400, 400)) for i in range(8)]
        self._images_dead = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_7","dead", f"{i}.png")), (400, 400)) for i in range(16)]
        self._images_attack = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_7","attack", f"{i}.png")), (400, 400)) for i in range(40)]
        self._jump_images = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_7","run", f"{i}.png")), (400, 400)) for i in range(8)]
        self._load_imgs()
