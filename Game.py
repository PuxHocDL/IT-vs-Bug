import pygame
import math
from config import *
from Bug import Bug
from Interact import Interact
from Bullet import Bullet
from Tower_2 import *
# Vòng lặp chính của game
slow_placed_time = 0
slow_placed = False
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == Bug.spawn_monster_event:
            Bug.create_monster(monsters)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if placing_tower:
                if gold.gold >= tower_cost:
                    basic_tower.create_basic_tower(mouse_x - TOWER_SIZE // 2, mouse_y - TOWER_SIZE // 2)
                    shoot_counters.append(0)
                    gold.gold -= tower_cost
                    placing_tower = False
            elif placing_slow:
                if gold.gold >= slow_cost:
                    Bug.apply_slow_effect(monsters)  # Áp dụng hiệu ứng làm chậm cho tất cả quái vật
                    slow_placed_time = pygame.time.get_ticks()
                    slow_placed = True
                    slow_position = (mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
                    gold.gold -= slow_cost
                    placing_slow = False
            elif 10 <= mouse_x <= 240 and HEIGHT - 60 <= mouse_y <= HEIGHT - 10:
                placing_tower = True
                placing_slow = False
            elif 250 <= mouse_x <= 480 and HEIGHT - 60 <= mouse_y <= HEIGHT - 10:
                placing_slow = True
                placing_tower = False
            else:
                for i, tower in enumerate(towers):
                    tower_rect = pygame.Rect(tower.x, tower.y, TOWER_SIZE, TOWER_SIZE)
                    if tower_rect.collidepoint(mouse_x, mouse_y):
                        tower_game.upgrade_tower(i)
                        break

    # Vẽ tháp
    for tower in towers:
        tower.draw_tower()
    
    # Tạo đạn từ các tháp với khoảng thời gian delay
    for i, tower in enumerate(towers):
        shoot_counters[i] += 1
        if shoot_counters[i] >= shoot_delay:
            tower.shoot()
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
                nearest_monster = min(monsters, key=lambda m: math.hypot(m.x - bullet[0], m.y - bullet[1]))
                bullet[2] = math.atan2(nearest_monster.y - bullet[1], nearest_monster.x - bullet[0])
            bullet[0] += bullet_speed * math.cos(bullet[2])
            bullet[1] += bullet_speed * math.sin(bullet[2])

        bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE)
        Bullet.draw_bullet(bullet[0], bullet[1])

        # Kiểm tra va chạm giữa đạn và quái vật
        for monster in monsters:
            monster_rect = pygame.Rect(monster.x, monster.y, MONSTER_SIZE, MONSTER_SIZE)
            if Interact.check_collision(bullet_rect, monster_rect):
                bullets_to_remove.append(bullet)
                monster.health -= 10  # Giảm máu quái vật mỗi khi bị bắn
                if monster.health <= 0:
                    monsters_to_remove.append(monster)
                    gold .gold+= 10  # Nhận vàng khi tiêu diệt quái vật
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
        monster_speed = monster.speed  # Tốc độ hiện tại của quái vật
        Bug.draw_health_bar(monster.x, monster.y, monster.health, monster.max_health)

        # Kiểm tra nếu thời gian làm chậm đã kết thúc
        if monster.slowed and pygame.time.get_ticks() > monster.slow_timer:
            monster.speed = 2  # Khôi phục tốc độ ban đầu
            monster.slowed = False  # Hủy đánh dấu bị làm chậm

        monster.x -= monster_speed  # Di chuyển quái vật sang trái
        if monster.x < 0:
            monsters_to_remove.append(monster)
        else:
            Bug.draw_monster(monster.x, monster.y)

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
