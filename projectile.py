import os
import pygame
import math
from vfx_manager import VFXManager


class Bullet:
    """
    Base class representing a bullet fired by towers.

    Attributes:
        _x (float): The x-coordinate of the bullet.
        _y (float): The y-coordinate of the bullet.
        _size (int): The size of the bullet.
        _angle (float): The angle of the bullet's trajectory.
        _damage (int): The damage inflicted by the bullet.
        _speed (float): The speed of the bullet.
        _slow (float): The slowing effect applied by the bullet.
        _slow_time (int): The duration of the slowing effect.
        _imgs (list): List of images representing the bullet.
        _destroy_imgs (list): List of images representing the bullet's destruction.
        _is_reverse (bool): Flag indicating if the bullet is moving in reverse.
        _current_time (int): The current time elapsed.
        _img_index (int): The index of the current image in _imgs.
        _ani_interval (int): The interval between animation frames.
        destroy_sound (pygame.mixer.Sound): Sound played upon bullet destruction.
        fire_sound (pygame.mixer.Sound): Sound played upon bullet firing.
    """

    def __init__(self, x, y, reverse=False, angle=0.0, extra_dmg=0):
        """
        Initializes a Bullet object.

        Parameters:
            x (float): The x-coordinate of the bullet.
            y (float): The y-coordinate of the bullet.
            reverse (bool, optional): Flag indicating if the bullet moves in reverse (default is False).
            angle (float, optional): The angle of the bullet's trajectory (default is 0.0).
            extra_dmg (int, optional): Additional damage inflicted by the bullet (default is 0).
        """
        pygame.mixer.init()
        self._x = x
        self._size = 32
        self._y = y - self._size // 2
        self._angle = angle
        self._damage = 100 + extra_dmg
        self._speed = 1000
        self._slow = 1
        self._slow_time = 0
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "move", "Bullet", f"bullet{i}.png")).convert_alpha(), (self._size, self._size)) for i in range(8)]
        self._destroy_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "explode", "Bullet", f"bullet{i}.png")).convert_alpha(), (self._size, self._size)) for i in range(8)]
        self._is_reverse = reverse
        self._current_time = 0
        self._img_index = 0
        self._ani_interval = 1000
        self._reverse()
        self.destroy_sound = pygame.mixer.Sound(os.path.join("assets", "music", "fire_destroy_sound.wav"))
        self.fire_sound = pygame.mixer.Sound(os.path.join("assets", "music", "posion.wav"))
        self.fire_sound.play()

    def _reverse(self):
        """Reverse the direction of the bullet if needed."""
        if self._is_reverse:
            self._speed *= -1

    def increase_damage(self, damage):
        """
        Increase the damage of the bullet.

        Parameters:
            damage (int): The amount of damage to increase.
        """
        self._damage += damage

    def increase_slow(self, slow):
        """
        Increase the slowing effect of the bullet.

        Parameters:
            slow (float): The amount by which to increase the slowing effect.
        """
        self._slow += slow

    def draw(self, screen, dt): 
        """
        Draw the bullet on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bullet.
            dt (int): The time elapsed since the last frame.
        """
        index_interval = self._ani_interval // len(self._imgs)
        self._current_time = self._current_time + dt
        additional_index = self._current_time // index_interval
        self._current_time %= index_interval

        self._img_index = (self._img_index + additional_index) % len(self._imgs)
        screen.blit(self._imgs[self._img_index], (self._x, self._y))

        self._x += self._speed * math.cos(self._angle) * dt / 1000
        self._y += self._speed * math.sin(self._angle) * dt / 1000

    def draw_destroy(self):
        """Draw the destruction animation of the bullet."""
        VFXManager.add_vfx(self._x, self._y, 200, self._destroy_imgs)
        self.destroy_sound.play()

    def get_rect(self):
        """
        Get the mask representing the collision rectangle of the bullet.

        Returns:
            pygame.mask.Mask: The mask representing the collision rectangle.
        """
        return pygame.mask.from_surface(self._imgs[0], threshold=254)

    def check_border(self, width, height):
        """
        Check if the bullet has reached the border of the screen.

        Parameters:
            width (int): The width of the screen.
            height (int): The height of the screen.

        Returns:
            bool: True if the bullet is out of the screen, False otherwise.
        """
        if 0 < self._x < width and 0 < self._y < height:
            return False
        return True

    def get_damage(self):
        """
        Get the damage inflicted by the bullet.

        Returns:
            int: The damage inflicted by the bullet.
        """
        return self._damage

    def get_slow(self):
        """
        Get the slowing effect applied by the bullet.

        Returns:
            float: The slowing effect applied by the bullet.
        """
        return self._slow

    def get_slow_time(self):
        """
        Get the duration of the slowing effect applied by the bullet.

        Returns:
            int: The duration of the slowing effect applied by the bullet.
        """
        return self._slow_time

    def get_pos(self):
        """
        Get the position of the bullet.

        Returns:
            tuple: A tuple containing the x and y coordinates of the bullet.
        """
        return self._x, self._y


class IceBullet(Bullet):
    """
    Class representing an ice bullet fired by towers.

    Inherits from Bullet class.

    Attributes:
        Inherits all attributes from the Bullet class.
    """

    def __init__(self, x, y, reverse=False, angle=0.0, extra_slow=0, extra_slow_time=0):
        """
        Initializes an IceBullet object.

        Parameters:
            x (float): The x-coordinate of the bullet.
            y (float): The y-coordinate of the bullet.
            reverse (bool, optional): Flag indicating if the bullet moves in reverse (default is False).
            angle (float, optional): The angle of the bullet's trajectory (default is 0.0).
            extra_slow (float, optional): Additional slowing effect applied by the bullet (default is 0).
            extra_slow_time (int, optional): Additional duration of the slowing effect (default is 0).
        """
        super().__init__(x, y, reverse, angle)
        self._speed = 800
        self._damage = 50
        self._slow = 0.2 + extra_slow
        self._slow_time = 2000 + extra_slow_time
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "ice_bullet.png")), (self._size, self._size)).convert_alpha()]
        self._destroy_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "explode", "IceBullet", f"bullet{i}.png")), (self._size, self._size)).convert_alpha() for i in range(12)]
        self.fire_sound = pygame.mixer.Sound(os.path.join("assets", "music", "ice_fire_sound.wav"))
        self.fire_sound.play()
        self.destroy_sound = pygame.mixer.Sound(os.path.join("assets", "music", "ice_destroy_sound.mp3"))
        self._reverse()


class FireBullet(Bullet):
    """
    Class representing a fire bullet fired by towers.

    Inherits from Bullet class.

    Attributes:
        Inherits all attributes from the Bullet class.
    """

    def __init__(self, x, y, reverse=False, angle=0.0, extra_dmg=0):
        """
        Initializes a FireBullet object.

        Parameters:
            x (float): The x-coordinate of the bullet.
            y (float): The y-coordinate of the bullet.
            reverse (bool, optional): Flag indicating if the bullet moves in reverse (default is False).
            angle (float, optional): The angle of the bullet's trajectory (default is 0.0).
            extra_dmg (int, optional): Additional damage inflicted by the bullet (default is 0).
        """
        super().__init__(x, y, reverse, angle)
        self._damage = 200 + extra_dmg
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "fire_bullet.png")), (self._size, self._size)).convert_alpha()]
        self.fire_sound = pygame.mixer.Sound(os.path.join("assets", "music", "fire_fire_sound.wav"))
        self.fire_sound.play()


class Skull(Bullet):
    """
    Class representing a skull projectile fired by towers.

    Inherits from Bullet class.

    Attributes:
        Inherits all attributes from the Bullet class.
    """

    def __init__(self, x, y, reverse=True, angle=0.0, extra_dmg=0):
        """
        Initializes a Skull object.

        Parameters:
            x (float): The x-coordinate of the bullet.
            y (float): The y-coordinate of the bullet.
            reverse (bool, optional): Flag indicating if the bullet moves in reverse (default is True).
            angle (float, optional): The angle of the bullet's trajectory (default is 0.0).
            extra_dmg (int, optional): Additional damage inflicted by the bullet (default is 0).
        """
        super().__init__(x, y, reverse, angle)
        self._size = 100
        self._damage = 80 + extra_dmg
        self._speed = 500
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3", "Skull_attack", f"{i}.png")), (self._size, self._size)).convert_alpha() for i in range(0, 8)]
        self._reverse()


class Winter(Bullet):
    """
    Class representing a winter projectile fired by towers.

    Inherits from Bullet class.

    Attributes:
        Inherits all attributes from the Bullet class.
    """

    def __init__(self, x, y, reverse=True, angle=0.0, extra_dmg=0):
        """
        Initializes a Winter object.

        Parameters:
            x (float): The x-coordinate of the bullet.
            y (float): The y-coordinate of the bullet.
            reverse (bool, optional): Flag indicating if the bullet moves in reverse (default is True).
            angle (float, optional): The angle of the bullet's trajectory (default is 0.0).
            extra_dmg (int, optional): Additional damage inflicted by the bullet (default is 0).
        """
        super().__init__(x, y, reverse, angle)
        self._size = 100
        self._damage = 30 + extra_dmg
        self._speed = 500
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Monster_3", "Winter_attack", f"0{i}.png")), (self._size, self._size)).convert_alpha() for i in range(0, 5)]
        self._destroy_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "explode", "Winter", f"{i}.png")).convert_alpha(), (130, 130)) for i in range(5)]
        self._reverse()
        self.fire_sound = pygame.mixer.Sound(os.path.join("assets", "music", "water_fire_sound.wav"))
        self.fire_sound.play()


class Bomb(Bullet):
    """
    Class representing a bomb projectile fired by towers.

    Inherits from Bullet class.

    Attributes:
        Inherits all attributes from the Bullet class.
    """

    def __init__(self, x, y, reverse=True, angle=0.0, extra_dmg=0):
        """
        Initializes a Bomb object.

        Parameters:
            x (float): The x-coordinate of the bullet.
            y (float): The y-coordinate of the bullet.
            reverse (bool, optional): Flag indicating if the bullet moves in reverse (default is True).
            angle (float, optional): The angle of the bullet's trajectory (default is 0.0).
            extra_dmg (int, optional): Additional damage inflicted by the bullet (default is 0).
        """
        super().__init__(x, y, reverse, angle)
        pygame.mixer.init()
        self._size = 200
        self._damage = 30
        self._speed = 700
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "Bomb", "Bomb", f"{i}.png")), (self._size, self._size)).convert_alpha() for i in range(0, 3)]
        self._destroy_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "Bomb", "Bomb_explotion", f"{i}.png")).convert_alpha(), (200, 200)) for i in range(11)]
        self._reverse()
        self.destroy_sound = pygame.mixer.Sound(os.path.join("assets", "music", "boom.wav"))


class SilverLining(Bullet):
    """
    Class representing a silver lining projectile fired by towers.

    Inherits from Bullet class.

    Attributes:
        Inherits all attributes from the Bullet class.
    """

    def __init__(self, x, y, reverse=False, angle=0.0, extra_dmg=0):
        """
        Initializes a SilverLining object.

        Parameters:
            x (float): The x-coordinate of the bullet.
            y (float): The y-coordinate of the bullet.
            reverse (bool, optional): Flag indicating if the bullet moves in reverse (default is False).
            angle (float, optional): The angle of the bullet's trajectory (default is 0.0).
            extra_dmg (int, optional): Additional damage inflicted by the bullet (default is 0).
        """
        super().__init__(x, y, reverse, angle)
        self._damage = 500 + extra_dmg
        self._imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "ice_bullet.png")), (self._size, self._size)).convert_alpha()]
        self._destroy_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "Projectiles", "explode", "Electricity", f"electricity{i}.png")), (4*self._size, 4*self._size)).convert_alpha() for i in range(16)]
        self._reverse()
        self.fire_sound = pygame.mixer.Sound(os.path.join("assets", "music", "thunder_fire_sound.wav"))
        self.fire_sound.play()
