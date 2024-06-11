import pygame
from projectile import *
from vfx_manager import VFXManager
from bar import Bar

class Bug:
    """
    A base class for all types of bugs in the game.

    Methods:
        __init__(self x, y, speed, health, max_health, bug_size, rect_x, rect_y, name): Initializes a Bug instance with its properties.
        get_rect(self): Returns the rectangular area of the bug for collision detection.
        update(self): Updates the bug's position and speed based on its current state.
        apply_slow(self): Applies a slowing effect to the bug.
        draw(self._ screen): Abstract method to draw the bug on the screen.
        draw_death(self._ screen): Abstract method to draw the bug's death animation on the screen.
    """
    def __init__(self, x, y, speed, max_health, bug_size, rect_x, rect_y, name):
        """
        Initializes a Bug instance with the given parameters.
        
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
        pygame.mixer.init()
        self._x = x
        self._y = y
        self._original_y = y
        self._speed = speed
        self._original_speed = speed
        self._max_health = max_health
        self._health = max_health
        self._slowed = False
        self._slow_timer = 0
        self._bug_size = bug_size
        self._rect_x = rect_x
        self._rect_y = rect_y
        self._slowed_bullet = False
        self.name = name
        self._death = False
        self.attacking = False
        self._collision_with_tower = False
        self._current_time_dead = 0 
        self._image_index_dead = 0
        self._current_time = 0
        self._img_index = 0
        self._image_index_attack = -1
        self._current_time_attack = 0
        self._current_atk_interval = 0
        self._attack_times = 0
        self._bullet_check = False
        self._current_atk_collision = -1
        self._ban = False
        self._modifiled = 0

        self._atk_index = -1
        self._shoot_index = -1
        self._atk_interval = 0
        self._mode = 0
        self._animate_time = {0: 1000, 1: 1000, 2: 1500, 3: 1500, 4: 1500, 5:2000}    # 0: Move, 1: Attack, 2: Dead, 3: Shoot, 4: Jump

        self._images = []
        self._images_attack = []
        self._images_dead = []
        self._images_shoot = []
        self._jump_images = []  
        self._images_healing = []
        self.jumping = False
        self._jump_height = 0
        self._jump_speed = 0
        self._jump_duration = 0
        self._jump_start_time = 0
       
        self._current_jump_frame = 0  
        self._jump_frame_duration = 100
        self._current_jump_time = 0  
        self.fix_coli = 50
        self.fix_thunder = 0
        self.monster_attacking_sound = pygame.mixer.Sound(os.path.join("assets", "music", "monster_attack.wav"))
        self.turn = 0 
        self._load_imgs()

    def _load_imgs(self):
        self._img_mode = {0: self._images, 1: self._images_attack, 2: self._images_dead, 3: self._images_shoot, 4: self._jump_images, 5: self._images_healing}
    def get_bug_pos(self):
        return [self.get_x(), self.get_y()]

    def get_bug_size(self): 
        return self._bug_size
    
    def jump(self):
        """
        Makes the bug jump over an object.

        Parameters:
            height (int): The height of the jump.
            speed (int): The speed of the jump.
            duration (int): The duration of the jump in milliseconds.
        """
        if not self.jumping:
            self.set_mode(4)
            self.jumping = True
            self._jump_start_time = pygame.time.get_ticks()
            
    

    def draw(self, screen, dt):
        """
        Draws the bug on the screen.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        proj = []
        if self._current_atk_interval > self._atk_interval * len(self._images) and self._atk_interval:
            if self.attacking:
                self.set_mode(3)
            elif self.attacking == False and self.name == "BossBug": 
                if self.turn%2==0: 
                    self.set_mode(5)
                    self.turn +=1
                else: 
                    self.set_mode(3)
                    self.turn +=1
            self._current_atk_interval = 0
        images = self._img_mode[self._mode]
        self._current_time += dt
        if self._mode !=4:
            if self._current_time >= self._animate_time[self._mode] / len(images):
                self._img_index = (self._img_index + 1) % len(images)
                self._current_time = 0
                proj = self._shoot()
                self._current_atk_interval += 1
            screen.blit(images[self._img_index], (self._x, self._y - self._modifiled))
        if self._mode == 4:
            self._current_jump_time += dt
            if self._current_jump_time >= self._jump_frame_duration:
                self._current_jump_frame = (self._current_jump_frame + 1) % len(self._jump_images)
                self._current_jump_time = 0
            screen.blit(self._jump_images[self._current_jump_frame], (self._x, self._y - self._modifiled))

        if self._img_index == len(images) - 1:
            self.set_mode(0)
        if self._mode not in [1, 3]:
            self.update(dt)

        if self.name == "BossBug":
            health_bar = Bar(self._x + self.get_size()//2, self._y + 30, 200, 10, "green", "white", self._max_health)
            health_bar.set_val(self._health)
            health_bar.draw(screen)
        return proj
    def get_img_index(self): 
        return self._img_index
    def _shoot(self):
        proj = []
        if self._mode == 3 and self._img_index == self._shoot_index:
            if self.name == "BigBug":
                proj = [Winter(self._x, self._y+self._rect_y//2+30, reverse=True)]
            if self.name == "TriangleBug": 
                proj = [Skull(self._x, self._y+self._rect_y//2, reverse=True)]
            if self.name == "HexagonBug": 
                proj = [Bomb(self._x, self._y+self._rect_y//2, reverse=True)]
            if self.name == "BossBug":
                proj = [Skull(self._x, 750 - 50 - 100 *i + 30, reverse=True, extra_dmg=120)for i in range(1,7)]
        return proj
        
    def draw_dead(self):
        """
        Draws the normal bug on the screen.
        Parameters:
            screen (pygame.Surface): The surface on which to draw the bug.
        """
        VFXManager.add_vfx(self._x, self._y - self._modifiled, self._animate_time[2], self._img_mode[2])

    def set_mode(self, mode):
        if mode != self._mode:
            self._mode = mode
            self._img_index = 0

    def get_rect(self):
        """
        Returns the rectangular area of the bug for collision detection.
        
        Returns:
            pygame.Rect: The rectangle representing the bug's area.
        """
        return pygame.mask.from_surface(self._images[0], threshold=5)

    def update(self, dt):
        if self._slowed and pygame.time.get_ticks() > self._slow_timer:
            self._speed = self._original_speed
            self._slowed = False

        if self.jumping:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self._jump_start_time
            jump_progress = elapsed_time / self._jump_duration

            if jump_progress <= 1.0:
                self._y = self._original_y - self._jump_height * (4 * jump_progress * (1 - jump_progress))
            else:
                self.jumping = None
                self._y = self._original_y
                self.set_mode(0)
        if not self.jumping:
            self._x -= self._speed * dt / 1000 
        else: 
            self._x -= self._speed * (dt / 1000)*5

    def apply_slow(self, slow, slow_time):
        """
        Applies a slowing effect to the bug.
        """
        self._speed = self._original_speed * (1-slow)
        self._slowed = True
        self._slow_timer = slow_time + pygame.time.get_ticks()

    def damage(self, dmg):
        self._health -= dmg
    
    def is_dead(self):
        return self._health <= 0
    
    def get_current_speed(self):
        return self._speed

    def is_slowed(self):
        return self._slowed 

    def get_pos(self):
        return self._x, self._y - self.fix_coli
    
    def get_x(self):
        return self._x + self.fix_thunder 

    def get_y(self):
        return self._y + self._bug_size//2

    def get_name(self):
        return self._name

    def get_check_bullet(self): 
        return self._bullet_check
    
    def get_atk_index(self):
        return self._atk_index

    def get_size(self):
        return self._bug_size

    def get_health(self):
        return self._health
        

monster_schedule = [
    {"time": 1, "name": "BigBug"},
    {"time": 1, "name": "TriangleBug"},
    {"time": 1, "name": "BigBug"},
    {"time": 1, "name": "HexagonBug"},
]
