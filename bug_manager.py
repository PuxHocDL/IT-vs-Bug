import random
from config import WIDTH, HEIGHT
from Bug.BigBug import *
from Bug.HexagonBug import *
from Bug.NormalBug import *
from Bug.TriangleBug import *
from interact import *

class BugManager:
    __bug_types = {"NormalBug": NormalBug, "BigBug": BigBug, "TriangleBug": TriangleBug, "HexagonBug": HexagonBug}
    def __init__(self):
        self.__bugs = []

    def add_bug(self, grid, name):
        """
        Static method to create and add a big bug to the game.

        Parameters:
            grid (Grid): The grid object to determine the bug's starting position.
            name (string): Name of the bug.
        """
        bug_x = WIDTH
        bug_y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + 20 
        self.__bugs.append(BugManager.__bug_types[name](bug_x, bug_y))

    def get_bugs(self):
        return self.__bugs

    def get_bugs_pos(self):
        return [[bug.get_x(), bug.get_y()] for bug in self.__bugs]
    def remove_bug(self, bug):
        self.__bugs.remove(bug)

    def apply_slow_effect(self):
        for bug in self.__bugs:
            bug.apply_slow(0.5, 3)

    def check_collision(self, grid):
        for bug in self.__bugs:
            bug_rect = bug.get_rect()
            bug_pos = bug.get_bug_pos()
            if grid.get_objs_in_row(grid.convert_to_grid_pos(bug_pos[0], bug_pos[1])[0]):
                bug.attacking = True
                for obj in grid.get_objs_in_row(grid.convert_to_grid_pos(bug_pos[0], bug_pos[1])[0]):
                    obj_rect = obj.get_rect()
                    collision_coordinates = Interact.collide_mask(bug_rect, obj_rect, bug.get_pos(), obj.get_pos())
                    if collision_coordinates:
                        if bug.get_img_index() == bug.get_atk_index():
                            obj.damage(10)
                        if not obj.is_dead():
                            bug.set_mode(1)
            else: 
                bug.attacking = False
