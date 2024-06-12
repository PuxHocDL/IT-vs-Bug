import random
from config import WIDTH, HEIGHT
from Bug.BigBug import *
from Bug.HexagonBug import *
from Bug.NormalBug import *
from Bug.TriangleBug import *
from Bug.SuperBug import *
from interact import *
from Bug.BossBug import *

class BugManager:
    """
    A class to manage the bugs in the game.

    Attributes:
        __bug_types (dict): A dictionary mapping bug names to their corresponding classes.
        __bugs (list): A list to store instances of bugs in the game.

    Methods:
        __init__(self):
            Initializes the BugManager with an empty list of bugs.
        add_bug(self, grid, name):
            Creates and adds a bug to the game.
        get_bugs(self):
            Returns the list of bugs.
        get_bugs_pos(self):
            Returns a list of positions of all the bugs.
        remove_bug(self, bug):
            Removes a bug from the list of bugs.
        apply_slow_effect(self):
            Applies a slow effect to all bugs.
        check_collision(self, grid):
            Checks and handles collisions between bugs and objects in the grid.
    """
    
    __bug_types = {
        "NormalBug": NormalBug, 
        "BigBug": BigBug, 
        "TriangleBug": TriangleBug, 
        "HexagonBug": HexagonBug, 
        "SuperBug": SuperBug, 
        "BossBug": BossBug
    }

    def __init__(self):
        """
        Initializes the BugManager with an empty list of bugs.
        """
        self.__bugs = []

    def add_bug(self, grid, name):
        """
        Creates and adds a bug to the game.

        Parameters:
            grid (Grid): The grid object to determine the bug's starting position.
            name (string): The name of the bug to add.
        """
        bug_x = WIDTH - 50
        if name != "SuperBug":
            bug_y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * (grid.get_rows()+1), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + 20
        else:
            bug_y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * (grid.get_rows()+2), HEIGHT - 50 - grid.get_cell_size()*2 , grid.get_cell_size())) + 20
        self.__bugs.append(BugManager.__bug_types[name](bug_x, bug_y))

    def get_bugs(self):
        """
        Returns the list of bugs.

        Returns:
            list: A list of bug instances.
        """
        return self.__bugs

    def get_bugs_pos(self):
        """
        Returns a list of positions of all the bugs.

        Returns:
            list: A list of [x, y] positions for each bug.
        """
        return [[bug.get_x(), bug.get_y()] for bug in self.__bugs]

    def remove_bug(self, bug):
        """
        Removes a bug from the list of bugs.

        Parameters:
            bug (Bug): The bug instance to remove.
        """
        self.__bugs.remove(bug)

    def check_collision(self, grid):
        """
        Checks and handles collisions between bugs and objects in the grid.

        Parameters:
            grid (Grid): The grid object containing objects to check for collisions.
        """
        for bug in self.__bugs:
            if bug.name != "BossBug":
                bug_rect = bug.get_rect()
                bug_pos = bug.get_bug_pos()
                grid_pos = grid.convert_to_grid_pos(bug_pos[0], bug_pos[1])
                if grid.get_objs_in_row(grid_pos[0]):
                    bug.attacking = True
                    for obj in grid.get_objs_in_row(grid_pos[0]):
                        obj_rect = obj.get_rect()
                        collision_coordinates = Interact.collide_mask(bug_rect, obj_rect, bug.get_pos(), obj.get_pos())
                        if collision_coordinates:
                            if bug.jumping == False:
                                bug.jump_sound.play()
                                bug.jump()
                            else:
                                if bug.get_img_index() in bug.get_atk_index():
                                    obj.damage(bug.damaged)
                                    bug.monster_attacking_sound.play()
                                if not obj.is_dead() and bug.jumping == None:
                                    bug.set_mode(1)
                else:
                    bug.attacking = False
            else: 
                pass
