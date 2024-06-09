from config import *

class Bulldozer:
    def __init__(self, grid, row):
        self.active = False
        self.used = False
        self.x = 0
        self.grid = grid
        self.row = row
        self.y = HEIGHT - 50- ((6-self.row) * self.grid.get_cell_size()) + (self.grid.get_cell_size()-50)//2
        self.speed = 10

    def activate(self):
        if not self.used:
            self.active = True
            self.x = 0

    def update(self, bug_manager):
        if self.active:
            self.x += self.speed
            if self.x >= WIDTH:
                self.reset()
            else:
                self.clear_row(bug_manager)

    def clear_row(self, bug_manager):
        bugs_to_remove = [bug for bug in bug_manager.get_bugs() if 
                          self.grid.convert_to_grid_pos(bug.get_x(), bug.get_y())[0] == self.row and 
                          bug.get_x() <= self.x + 25]
        for bug in bugs_to_remove:
            bug.draw_dead()
            bug_manager.remove_bug(bug)

    def reset(self):
        self.active = False
        self.used = True

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 50))
        elif not self.used:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 50, 50))  
