from projectile import *
from interact import Interact

class ProjectileManager:
    """
    Manages projectiles in the game, including adding, removing, drawing, and checking collisions.

    Attributes:
        __projectiles (list): A list of active projectiles.
        __remove_projectiles (list): A list of projectiles to be removed.
    """

    def __init__(self):
        """
        Initializes the ProjectileManager with empty lists for projectiles and projectiles to be removed.
        """
        self.__projectiles = []
        self.__remove_projectiles = []

    def add_projectiles(self, projectiles):
        """
        Adds a list of projectiles to the manager.

        Parameters:
            projectiles (list): A list of projectiles to add.
        """
        self.__projectiles.extend(projectiles)

    def add_remove_projectile(self, proj):
        """
        Adds a single projectile to the list of projectiles to be removed.

        Parameters:
            proj (Projectile): The projectile to be removed.
        """
        self.__remove_projectiles.append(proj)

    def get_projectiles(self):
        """
        Returns the list of active projectiles.

        Returns:
            list: The list of active projectiles.
        """
        return self.__projectiles

    def remove_projectiles(self):
        """
        Removes projectiles marked for removal from the list of active projectiles and resets the removal list.
        """
        for p in self.__remove_projectiles:
            p.draw_destroy()
            self.__projectiles.remove(p)
        self.__remove_projectiles = []

    def draw(self, screen, dt):
        """
        Draws all active projectiles on the screen.

        Parameters:
            screen (pygame.Surface): The surface to draw on.
            dt (int): The delta time since the last frame.
        """
        for projectile in self.__projectiles:
            projectile.draw(screen, dt)

    def check_collision(self, objects, width, height):
        """
        Checks for collisions between projectiles and other objects, and removes projectiles that go out of bounds.

        Parameters:
            objects (list): A list of objects to check for collisions with.
            width (int): The width of the game screen.
            height (int): The height of the game screen.
        """
        for projectile in self.__projectiles:
            proj_rect = projectile.get_rect()
            removed = False
            for obj in objects:
                obj_rect = obj.get_rect()
                collision_coordinates = Interact.collide_mask(proj_rect, obj_rect, projectile.get_pos(), obj.get_pos())
                if collision_coordinates and not obj.is_dead():
                    self.add_remove_projectile(projectile)
                    obj.damage(projectile.get_damage())
                    obj.apply_slow(projectile.get_slow(), projectile.get_slow_time())
                    removed = True
                    break

            if projectile.check_border(width, height) and not removed:
                self.add_remove_projectile(projectile)
