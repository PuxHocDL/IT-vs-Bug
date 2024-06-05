from config import *
from bug import *
from interact import Interact
from bug_manager import BugManager
from vfx_manager import VFXManager
import time
# Initialize pygame
pygame.init()

bug_manager = BugManager()
clock = pygame.time.Clock()
dt = 0 
# Main game loop variables
slow_placed_time = 0
slow_placed = False
running = True
rect_size = grid.get_cell_size()
start_time = time.time()

option = -1

while running:
    dt = clock.tick(FPS)
    screen.fill(WHITE)

    current_time = time.time() - start_time

    for schedule in monster_schedule[:]:
        if current_time >= schedule["time"]:
            bug_manager.add_bug(grid, schedule["name"])
            monster_schedule.remove(schedule)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid_x, grid_y = grid.convert_to_grid_pos(mouse_x, mouse_y)
            if option != -1:
                if not grid.is_occupied(grid_x, grid_y) and grid.is_inside_gird(grid_x, grid_y):
                    hand.add_tower(grid, grid_x, grid_y)
                    hand.reset_time(option)
                hand.toggle_select(option)
            else:
                pass

            option = hand.select(mouse_x, mouse_y)

    projectiles.add_projectiles(grid.draw(screen, dt))
    # Towers shoot
    for bug_pos in bug_manager.get_bugs_pos():
        for tower in grid.get_objs_in_row(grid.convert_to_grid_pos(bug_pos[0], bug_pos[1])[0]):
            tower.set_mode(1)

    # Check bullet-bug collision
    projectiles.check_collision(bug_manager.get_bugs(), WIDTH, HEIGHT)
    projectiles.remove_projectiles()
    projectiles.draw(screen,dt)

    grid.remove_objects()

    bug_manager.check_collision(grid) 


    # Update bugs
    for bug in bug_manager.get_bugs():
        if bug.is_dead():
            gold.gold +=30
            bug.draw_dead()
            bug_manager.remove_bug(bug)  
        else:
            bug_projectiles.add_projectiles(bug.draw(screen, dt))
        if bug.get_x() <= 0:
            bug_manager.remove_bug(bug)

    # Check bullet-tower collision
    bug_projectiles.check_collision(grid.get_objects(), WIDTH, HEIGHT)
    bug_projectiles.remove_projectiles()
    bug_projectiles.draw(screen,dt)

    # Draw vfx
    VFXManager.draw(screen, dt)
    hand.draw(screen, dt)

    pygame.display.flip()

pygame.quit()
