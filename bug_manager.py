from bug import *

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
        bug_y = random.choice(range(HEIGHT - 50 - grid.get_cell_size() * grid.get_rows(), HEIGHT - 50 - grid.get_cell_size(), grid.get_cell_size())) + (grid.get_cell_size()-80)//2 + 70
        self.__bugs.append(BugManager.__bug_types[name](bug_x, bug_y))

    def get_bugs(self):
        return self.__bugs

    def get_bugs_pos(self):
        return [[bug.get_x(), bug.get_y()] for bug in self.__bugs]

    def remove_bug(self, bug):
        self.__bugs.remove(bug)

    def apply_slow_effect(self):
        for bug in self.__bugs:
            bug.apply_slow()
