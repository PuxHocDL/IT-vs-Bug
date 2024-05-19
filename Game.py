import pygame
import math
from config import *
from Bug import Bug
from Interact import Interact
from Bullet import Bullet
from Tower import tower_game
# Vòng lặp chính của game
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == Bug.spawn_monster_event:
                Bug.create_monster(100,100)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if placing_tower:
                if gold >= tower_cost:
                    towers.append((mouse_x - TOWER_SIZE // 2, mouse_y - TOWER_SIZE // 2, 1))  # Thêm cấp độ của tháp
                    shoot_counters.append(0)
                    gold -= tower_cost
                    placing_tower = False
            elif placing_slow:
                if gold >= slow_cost:
                    Bug.apply_slow_effect()  # Áp dụng hiệu ứng làm chậm cho tất cả quái vật
                    slow_placed_time = pygame.time.get_ticks()
                    slow_placed = True
                    slow_position = (mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
                    gold -= slow_cost
                    placing_slow = False
            elif 10 <= mouse_x <= 240 and HEIGHT - 60 <= mouse_y <= HEIGHT - 10:
                placing_tower = True
                placing_slow = False
            elif 250 <= mouse_x <= 480 and HEIGHT - 60 <= mouse_y <= HEIGHT - 10:
                placing_slow = True
                placing_tower = False
            else:
                for i, tower in enumerate(towers):
                    tower_rect = pygame.Rect(tower[0], tower[1], TOWER_SIZE, TOWER_SIZE)
                    if tower_rect.collidepoint(mouse_x, mouse_y):
                        tower_game.upgrade_tower(i)
                        break
    # Vẽ tháp
    for tower in towers:
        tower_game.draw_tower(tower[0], tower[1], tower[2])
    # Tạo đạn từ các tháp với khoảng thời gian delay
    for i, tower in enumerate(towers):
        shoot_counters[i] += 1
        if shoot_counters[i] >= shoot_delay:
            bullet_x = tower[0] + TOWER_SIZE // 2 - BULLET_SIZE // 2
            bullet_y = tower[1] + TOWER_SIZE // 2 - BULLET_SIZE // 2
            if tower[2] == 1:  # Basic tower
                bullets.append([bullet_x, bullet_y, 0, tower[2]])  # Thêm cấp độ của đạn
            elif tower[2] == 2:  # Advanced tower
                for angle in [-0.2, 0, 0.2]:  # Bắn ra 3 viên đạn tỏa ra 3 hướng
                    bullets.append([bullet_x, bullet_y, angle, tower[2]])
            elif tower[2] == 3:  # Elite tower
                if monsters:
                    nearest_monster = min(monsters, key=lambda m: math.hypot(m[0] - bullet_x, m[1] - bullet_y))
                    angle = math.atan2(nearest_monster[1] - bullet_y, nearest_monster[0] - bullet_x)
                else:
                    angle = 0
                bullets.append([bullet_x, bullet_y, angle, tower[2]])  # Đạn đuổi
            shoot_counters[i] = 0

    # Danh sách tạm thời để lưu các đạn và quái vật cần xóa
    bullets_to_remove = []
    monsters_to_remove = []

    # Cập nhật vị trí và vẽ đạn
    for bullet in bullets:
        level = bullet[3]
        if level == 1:
            bullet[0] += bullet_speed
        elif level == 2:
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])
        elif level == 3:
            if monsters:
                nearest_monster = min(monsters, key=lambda m: math.hypot(m[0] - bullet[0], m[1] - bullet[1]))
                bullet[2] = math.atan2(nearest_monster[1] - bullet[1], nearest_monster[0] - bullet[0])
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])

        bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE)
        Bullet.draw_bullet(bullet[0], bullet[1])

       # Kiểm tra va chạm giữa đạn và quái vật
        for monster in monsters:
            
            monster_rect = pygame.Rect(monster[0], monster[1], MONSTER_SIZE, MONSTER_SIZE)
            if Interact.check_collision(bullet_rect, monster_rect):
                bullets_to_remove.append(bullet)
                monster[3]-= 10  # Giảm máu quái vật mỗi khi bị bắn
                if monster[3] <= 0:
                    monsters_to_remove.append(monster)
                    gold += 10  # Nhận vàng khi tiêu diệt quái vật
                break

        # Xóa đạn nếu ra khỏi màn hình
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            bullets_to_remove.append(bullet)

    # Xóa các đạn và quái vật đã va chạm hoặc ra khỏi màn hình
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    for monster in monsters_to_remove:
        if monster in monsters:
            monsters.remove(monster)

    # Cập nhật vị trí và vẽ quái vật
    for monster in monsters:
        monster_speed = monster[2]  # Tốc độ hiện tại của quái vật
        monster_x, monster_y, monster_speed, monster_health, max_health, slowed, slow_timer = monster
        Bug.draw_health_bar(monster[0],monster[1],monster[3],monster[4])

        # Kiểm tra nếu thời gian làm chậm đã kết thúc
        if slowed and pygame.time.get_ticks() > slow_timer:
            monster[2] = 2  # Khôi phục tốc độ ban đầu
            monster[4] = False  # Hủy đánh dấu bị làm chậm

        monster[0] -= monster_speed  # Di chuyển quái vật sang trái
        if monster[0] < 0:
            monsters_to_remove.append(monster)
        else:
            Bug.draw_monster(monster[0], monster[1])

    # Vẽ thông tin vàng và nút mua tháp
    tower_game.draw_gold()
    tower_game.draw_buy_tower_button()
    tower_game.draw_buy_slow_button()

    # Hiển thị vị trí đặt tháp hoặc vật làm chậm nếu đang ở chế độ đặt
    if placing_tower:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tower_game.draw_tower(mouse_x - TOWER_SIZE // 2, mouse_y - TOWER_SIZE // 2, 1)
    elif placing_slow:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tower_game.draw_slow(mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
    
    # Vẽ vật làm chậm nếu đã được đặt và chỉ trong vòng 1 giây
    if slow_placed:
        if pygame.time.get_ticks() - slow_placed_time <= 1000:  # 1 giây
            tower_game.draw_slow(*slow_position)
        else:
            slow_placed = False  # Reset flag sau 1 giây

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát khỏi Pygame
pygame.quit()
