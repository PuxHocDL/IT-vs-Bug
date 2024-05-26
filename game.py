import os
import pygame
import math
from config import *
from bug import *
from interact import Interact
from bullet import Bullet
from tower import *

# Initialize pygame
pygame.init()

# Main game loop variables
slow_placed_time = 0
slow_placed = False
running = True
clock = pygame.time.Clock()


# A list to keep track of explosions
explosions = []

# Thêm nút mua tháp băng


while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    buy_tower_btn.change_color((mouse_x, mouse_y))
    buy_slow_btn.change_color((mouse_x, mouse_y))
    buy_ice_btn.change_color((mouse_x, mouse_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == spawn_bug_event:
            NormalBug.create_bug(bugs, grid)
        elif event.type == spawn_big_bug_event: 
            BigBug.create_big_bug(bugs, grid)
        elif event.type == spawn_triangle_bug_event: 
            TriangleBug.create_triangle_bug(bugs, grid)
        elif event.type == spawn_hexagon_bug_event:
            HexagonBug.create_hexagon_bug(bugs, grid)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rect_size = grid.get_cell_size()
            grid_x, grid_y = grid.convert_to_grid_pos(mouse_x, mouse_y)
            if (grid_x, grid_y) not in [(-1, -1), (-2, -2)]:
                screen_pos = grid.convert_to_screen_pos(grid_x, grid_y)
                upgrade_tower = False
                if placing_tower:
                    if gold.gold >= tower_cost:
                            grid.add_object(grid_x, grid_y, BasicTower(screen_pos[0] + rect_size // 2, screen_pos[1] + rect_size // 2), basic_tower_img)
                            shoot_counters.append(0)
                            gold.gold -= tower_cost
                            placing_tower = False
                elif placing_slow:
                    if gold.gold >= slow_cost:
                        Bug.apply_slow_effect(bugs)  # Apply slow effect to all bugs
                        slow_placed_time = pygame.time.get_ticks()
                        slow_placed = True
                        slow_position = (mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
                        gold.gold -= slow_cost
                        placing_slow = False
                elif placing_ice:
                    if gold.gold >= ice_cost:
                        grid_x, grid_y = grid.convert_to_grid_pos(mouse_x, mouse_y)
                        if (grid_x, grid_y) != (-1, -1):
                            grid.add_object(grid_x, grid_y, IceTower(screen_pos[0] + rect_size // 2, screen_pos[1] + rect_size // 2))
                            shoot_counters.append(0)
                            gold.gold -= ice_cost
                            placing_ice = False

            if (grid_x, grid_y) == (-2, -2) and not (placing_slow or placing_ice or placing_tower):
                for i, tower in enumerate(grid.get_objects()):
                    tower_rect = pygame.Rect(tower.x - rect_size//2, tower.y - rect_size//2, rect_size, rect_size)
                    if tower_rect.collidepoint(mouse_x, mouse_y):
                        tower.upgrade()
                        break

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

    grid.draw(screen)
    
    for i, tower in enumerate(grid.get_objects()):
        shoot_counters[i] += 1
        if shoot_counters[i] >= shoot_delay:
            tower.shoot()
            shoot_counters[i] = 0

    bullets_to_remove = []
    bugs_to_remove = []

    for bullet in bullets:
        level = bullet[3]
        if level == 1:
            bullet[0] += bullet_speed
        elif level == 2:
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])
        elif level == 3:
            if bugs:
                nearest_bug = min(bugs, key=lambda m: math.hypot(m.x - bullet[0], m.y - bullet[1]))
                bullet[2] = math.atan2(nearest_bug.y - bullet[1], nearest_bug.x - bullet[0])
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])

        bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE)
        if bullet[4] == "normal":
            Bullet.draw_normal_bullet(bullet[0], bullet[1])
        elif bullet[4] == "ice":
            Bullet.draw_ice_bullet(bullet[0], bullet[1])
        for bug in bugs:
            bug_rect = pygame.Rect(bug.x, bug.y, bug.bug_size, bug.bug_size)
            collision_coordinates = Interact.check_collision(bullet_rect, bug.get_rect())
            if collision_coordinates and not bug.death:
                explosions.append((collision_coordinates[0], collision_coordinates[1], pygame.time.get_ticks()))
                bullets_to_remove.append(bullet)
                bug.health -= 50
                if bullet[4] == "ice" and not bug.slowed_bullet:  # Xử lý đạn băng làm chậm quái vật
                    bug.speed *= 0.7  # Giảm tốc độ 50%
                    bug.slowed_bullet = True
                    bug.slow_timer_bullet = pygame.time.get_ticks() + 5000  # Thời gian làm chậm là 5 giây
                
                break

        if bullet[0] < 10 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            bullets_to_remove.append(bullet)

    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    for bug in bugs:
        if bug.health < 0:
            bug.death = True
            if bug.name == "NormalBug" or bug.name == "BigBug" or bug.name == "HexagonBug":
                if bug.draw_death(screen):
                    gold.gold +=30
                    bugs.remove(bug)  # Remove bug from list if death animation is complete
            else:
                gold.gold +=30 
                bugs.remove(bug)

        else:
            bug_speed = bug.speed
            bug.update()
            bug.draw_health_bar(screen)

            if bug.slowed and pygame.time.get_ticks() > bug.slow_timer:
                bug.speed = 2
                bug.slowed = False
            if bug.x < 0:
                bugs.remove(bug)
            else:
                bug.draw(screen)
            
            if bug.slowed_bullet and pygame.time.get_ticks() > bug.slow_timer_bullet:
                bug.speed /= 0.7  # Khôi phục tốc độ ban đầu
                bug.slowed_bullet = False
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

    TowerGame.draw_gold()
    buy_tower_btn.draw(screen)
    buy_slow_btn.draw(screen)
    buy_ice_btn.draw(screen)

    # Draw explosions and remove them after a short duration
    current_time = pygame.time.get_ticks()

    explosions_to_remove = []

    for explosion in explosions:
        x, y, start_time = explosion
        if current_time - start_time <= 100:  # Explosion lasts for 500ms
            Bullet.draw_bullet_with_collision(x, y)
        else:
            explosions_to_remove.append(explosion)

    for explosion in explosions_to_remove:
        if explosion in explosions:
            explosions.remove(explosion)

    pygame.display.flip()

pygame.quit()
