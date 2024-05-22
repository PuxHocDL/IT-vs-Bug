import os
import pygame
import math
from config import *
from bug import Bug
from interact import Interact
from bullet import Bullet
from tower import *
from grid import Grid
# Vòng lặp chính của game
slow_placed_time = 0
slow_placed = False
running = True
clock = pygame.time.Clock()

tile_imgs = [pygame.image.load(os.path.join("assets", "grass1.jpg")), pygame.image.load(os.path.join("assets", "grass2.jpg"))]

grid = Grid(WIDTH, HEIGHT, tile_imgs)
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    buy_tower_btn.change_color((mouse_x, mouse_y))
    buy_slow_btn.change_color((mouse_x, mouse_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == Bug.spawn_BUG_event:
            Bug.create_BUG(BUGs)
        elif event.type == Bug.spawn_big_BUG_event: 
            Bug.create_big_BUG(BUGs)
        elif event.type == Bug.spawn_triangle_BUG_event: 
            Bug.create_triangle_BUG(BUGs)
        elif event.type == Bug.spawn_hexagon_BUG_event:
            Bug.create_hexagon_BUG(BUGs)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if placing_tower:
                if gold.gold >= tower_cost:
                    grid_x, grid_y = grid.convert(mouse_x, mouse_y)
                    if (grid_x, grid_y) != (-1, -1):
                        BasicTower.create_basic_tower(mouse_x - TOWER_SIZE // 2, mouse_y - TOWER_SIZE // 2)
                        grid.add_object(grid_x, grid_y)
                        shoot_counters.append(0)
                        gold.gold -= tower_cost
                        placing_tower = False
            elif placing_slow:
                if gold.gold >= slow_cost:
                    Bug.apply_slow_effect(BUGs)  # Áp dụng hiệu ứng làm chậm cho tất cả quái vật
                    slow_placed_time = pygame.time.get_ticks()
                    slow_placed = True
                    slow_position = (mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
                    gold.gold -= slow_cost
                    placing_slow = False
            elif buy_tower_btn.check_for_input((mouse_x, mouse_y)):
                buy_tower_btn.click_color()
                placing_tower = True
                placing_slow = False
            elif buy_slow_btn.check_for_input((mouse_x, mouse_y)):
                buy_slow_btn.click_color()
                placing_slow = True
                placing_tower = False
            else:
                for i, tower in enumerate(towers):
                    tower_rect = pygame.Rect(tower.x, tower.y, TOWER_SIZE, TOWER_SIZE)
                    if tower_rect.collidepoint(mouse_x, mouse_y):
                        TowerGame.upgrade_tower(i)
                        break

    # Vẽ tháp
    #for tower in towers:
    #    tower.draw_tower()
    grid.draw(screen)
    
    # Tạo đạn từ các tháp với khoảng thời gian delay
    for i, tower in enumerate(towers):
        shoot_counters[i] += 1
        if shoot_counters[i] >= shoot_delay:
            tower.shoot()
            shoot_counters[i] = 0

    # Danh sách tạm thời để lưu các đạn và quái vật cần xóa
    bullets_to_remove = []
    BUGs_to_remove = []

    # Cập nhật vị trí và vẽ đạn
    for bullet in bullets:
        level = bullet[3]
        if level == 1:
            bullet[0] += bullet_speed
        elif level == 2:
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])
        elif level == 3:
            if BUGs:
                nearest_BUG = min(BUGs, key=lambda m: math.hypot(m.x - bullet[0], m.y - bullet[1]))
                bullet[2] = math.atan2(nearest_BUG.y - bullet[1], nearest_BUG.x - bullet[0])
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])

        bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE)
        Bullet.draw_bullet(bullet[0], bullet[1])

        # Kiểm tra va chạm giữa đạn và quái vật
        for BUG in BUGs:
            BUG_rect = pygame.Rect(BUG.x, BUG.y, BUG.BUG_SIZE, BUG.BUG_SIZE)
            if Interact.check_collision(bullet_rect, BUG_rect):
                bullets_to_remove.append(bullet)
                BUG.health -= 20  # Giảm máu quái vật mỗi khi bị bắn
                if BUG.health <= 0:
                    BUGs_to_remove.append(BUG)
                    gold .gold+= 10  # Nhận vàng khi tiêu diệt quái vật
                break

        # Xóa đạn nếu ra khỏi màn hình
        if bullet[0] < 10 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            bullets_to_remove.append(bullet)

    # Xóa các đạn và quái vật đã va chạm hoặc ra khỏi màn hình
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    for BUG in BUGs_to_remove:
        if BUG in BUGs:
            BUGs.remove(BUG)

    # Cập nhật vị trí và vẽ quái vật
    for BUG in BUGs:
        BUG_speed = BUG.speed  # Tốc độ hiện tại của quái vật
        BUG.update()
        Bug.draw_health_bar(BUG.x, BUG.y, BUG)

        # Kiểm tra nếu thời gian làm chậm đã kết thúc
        if BUG.slowed and pygame.time.get_ticks() > BUG.slow_timer:
            BUG.speed = 2  # Khôi phục tốc độ ban đầu
            BUG.slowed = False  # Hủy đánh dấu bị làm chậm

        BUG.x -= BUG_speed  # Di chuyển quái vật sang trái
        if BUG.x < 0:
            BUGs_to_remove.append(BUG)
        else:
            Bug.draw_BUG(BUG.x, BUG.y,BUG)


    # Hiển thị vị trí đặt tháp hoặc vật làm chậm nếu đang ở chế độ đặt
    if placing_tower:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        TowerGame.draw_tower(mouse_x - TOWER_SIZE // 2, mouse_y - TOWER_SIZE // 2, 1)
    elif placing_slow:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        TowerGame.draw_slow(mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
    
    # Vẽ vật làm chậm nếu đã được đặt và chỉ trong vòng 1 giây
    if slow_placed:
        if pygame.time.get_ticks() - slow_placed_time <= 1000:  # 1 giây
            TowerGame.draw_slow(*slow_position)
        else:
            slow_placed = False  # Reset flag sau 1 giây

    # Vẽ thông tin vàng và nút mua tháp
    TowerGame.draw_gold()
    buy_tower_btn.draw(screen)
    buy_slow_btn.draw(screen)

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát khỏi Pygame
pygame.quit()
