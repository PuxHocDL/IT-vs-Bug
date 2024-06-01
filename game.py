import pygame
from config import *
from bug import *
from interact import Interact
from tower import *
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

# A list to keep track of explosions
explosions = []

# Thêm nút mua tháp băng

def collision_all(bug): 
    for tower in grid.get_objects():
        tower_rect = pygame.Rect(tower.get_x() - rect_size // 2, tower.get_y() - rect_size // 2, rect_size, rect_size)
        bug.collision_with_tower = Interact.check_collision_2(bug.get_rect(), tower_rect)
        if bug.collision_with_tower: 
            return True
    return False
start_time = time.time()

while running:
    dt = clock.tick(FPS)
    screen.fill(WHITE)

    current_time = time.time() - start_time

    for schedule in monster_schedule[:]:
        if current_time >= schedule["time"]:
            bug_manager.add_bug(grid, schedule["name"])
            monster_schedule.remove(schedule)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    buy_tower_btn.change_color((mouse_x, mouse_y))
    buy_slow_btn.change_color((mouse_x, mouse_y))
    buy_ice_btn.change_color((mouse_x, mouse_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid_x, grid_y = grid.convert_to_grid_pos(mouse_x, mouse_y)
            if not grid.is_occupied(grid_x, grid_y):
                screen_pos = grid.convert_to_screen_pos(grid_x, grid_y)
                upgrade_tower = False
                if placing_tower:
                    if gold.gold >= tower_cost:
                        grid.add_object(grid_x, grid_y, BasicTower(screen_pos[0] + rect_size // 2, screen_pos[1] + rect_size // 2, grid.get_cell_size()))
                        gold.gold -= tower_cost
                        placing_tower = False
                elif placing_slow:
                    if gold.gold >= slow_cost:
                        bug_manager.apply_slow_effect()  # Apply slow effect to all bugs
                        slow_placed_time = pygame.time.get_ticks()
                        slow_placed = True
                        slow_position = (mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
                        gold.gold -= slow_cost
                        placing_slow = False
                elif placing_ice:
                    if gold.gold >= ice_cost:
                        grid.add_object(grid_x, grid_y, IceTower(screen_pos[0] + rect_size // 2, screen_pos[1] + rect_size // 2, grid.get_cell_size()))
                        gold.gold -= ice_cost
                        placing_ice = False
            else:
                upgrade_tower = True

            if upgrade_tower and not (placing_tower or placing_slow or placing_ice):
                grid.upgrade_tower(grid_x, grid_y)
                upgrade_tower = False
            
            if buy_tower_btn.check_for_input((mouse_x, mouse_y)) and not placing_tower:
                buy_tower_btn.click_color()
                placing_tower = True
                placing_slow = False
                placing_ice = False
            elif buy_slow_btn.check_for_input((mouse_x, mouse_y)) and not placing_slow:
                buy_slow_btn.click_color()
                placing_slow = True
                placing_tower = False
                placing_ice = False
            elif buy_ice_btn.check_for_input((mouse_x, mouse_y)) and not placing_ice:
                buy_ice_btn.click_color()
                placing_ice = True
                placing_tower = False
                placing_slow = False

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

    # Spawn bugs
    for bug in bug_manager.get_bugs():
            if bug.attacking == True: 
                 bug_projectiles.add_projectiles(bug.draw_attack(screen,dt))
            else: 
                if bug.is_dead():
                        if bug.draw_dead(dt,screen):
                            gold.gold +=30
                            bug_manager.remove_bug(bug)  

                else:
                    bug_rect = bug.get_rect()
                    pygame.draw.rect(screen, (255, 0, 0), bug_rect, 2)  
                    bug_speed = bug.get_current_speed()
                    bug.update()
                    bug.draw(dt,screen)
            if bug.get_x() <= 0:
                bug_manager.remove_bug(bug)
            """else: 
                if not collision_all(bug) or bug.get_name()!="HexagonBug" : 
                    bug.update()
                    bug.draw(dt,screen)
                elif collision_all(bug) and bug.get_name()=="HexagonBug": 
                    bug.draw_attack(dt,screen)"""
            if bug._slowed_bullet and pygame.time.get_ticks() > bug._slow_timer_bullet:
                bug._speed /= 0.7  # Khôi phục tốc độ ban đầu
                bug._slowed_bullet = False
    # Check bullet-tower collision
    bug_projectiles.check_collision(grid.get_objects(), WIDTH, HEIGHT)
    bug_projectiles.remove_projectiles()
    bug_projectiles.draw(screen,dt)

    if placing_tower:
        grid.draw_on_mouse_pos(screen, (mouse_x, mouse_y))
    elif placing_slow:
        grid.draw_on_mouse_pos(screen, (mouse_x, mouse_y))
    elif placing_ice:
        grid.draw_on_mouse_pos(screen, (mouse_x, mouse_y))
    
    if slow_placed:
        if pygame.time.get_ticks() - slow_placed_time <= 1000:
            TowerGame.draw_slow(*slow_position)
        else:
            slow_placed = False

    print(projectiles.get_projectiles())
    
    TowerGame.draw_gold()
    buy_tower_btn.draw(screen)
    buy_slow_btn.draw(screen)
    buy_ice_btn.draw(screen)

    # Draw vfx
    VFXManager.draw(screen, dt)

    pygame.display.flip()

pygame.quit()
