import pygame
import random
import math

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)  # Màu của vật làm chậm

# Tốc độ khung hình
FPS = 60

# Kích thước quái vật và đạn
MONSTER_SIZE = 50
BULLET_SIZE = 10
TOWER_SIZE = 50
SLOW_SIZE = 50

# Tốc độ đạn
bullet_speed = 5

# Tạo danh sách chứa các quái vật, đạn, tháp, và vật làm chậm
monsters = []
bullets = []
towers = []

# Giá tiền mua tháp và vật làm chậm
tower_cost = 50
slow_cost = 100

# Giá nâng cấp tháp
upgrade_cost = 200

# Số lượng vàng ban đầu
gold = 3000

# Tần suất bắn đạn (tính bằng khung hình)
shoot_delay = 60
shoot_counters = []

# Phông chữ
font = pygame.font.SysFont(None, 36)

# Chế độ đặt tháp hoặc vật làm chậm
placing_tower = False
placing_slow = False

# Hàm tạo quái vật mới
def create_monster():
    monster_x = WIDTH
    monster_y = random.randint(0, HEIGHT - MONSTER_SIZE)
    monsters.append([monster_x, monster_y, 2, 100, False, 0])  # Tốc độ ban đầu của quái vật là 2, máu của quái vật là 100, thêm flag bị làm chậm và thời gian hết hiệu lực

# Khởi tạo bộ đếm thời gian để tạo quái vật mới
spawn_monster_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_monster_event, 1000)  # Tạo quái vật mới mỗi giây

# Hàm vẽ quái vật
def draw_monster(x, y):
    pygame.draw.rect(screen, RED, (x, y, MONSTER_SIZE, MONSTER_SIZE))

# Hàm vẽ tháp
def draw_tower(x, y, level):
    if level == 1:
        color = BLUE
    elif level == 2:
        color = YELLOW
    elif level == 3:
        color = RED
    pygame.draw.rect(screen, color, (x, y, TOWER_SIZE, TOWER_SIZE))

# Hàm vẽ đạn
def draw_bullet(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, BULLET_SIZE, BULLET_SIZE))

# Hàm vẽ vật làm chậm
def draw_slow(x, y):
    pygame.draw.rect(screen, PURPLE, (x, y, SLOW_SIZE, SLOW_SIZE))

# Hàm kiểm tra va chạm
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Hàm vẽ thông tin vàng
def draw_gold():
    gold_text = font.render(f"Gold: {gold}", True, BLACK)
    screen.blit(gold_text, (10, 10))

# Hàm vẽ nút mua tháp
def draw_buy_tower_button():
    pygame.draw.rect(screen, GREEN, (10, HEIGHT - 60, 230, 50))
    buy_text = font.render("Buy Tower - $50", True, BLACK)
    screen.blit(buy_text, (20, HEIGHT - 50))

# Hàm vẽ nút mua vật làm chậm
def draw_buy_slow_button():
    pygame.draw.rect(screen, PURPLE, (250, HEIGHT - 60, 230, 50))
    buy_text = font.render("Buy Slow - $100", True, WHITE)
    screen.blit(buy_text, (260, HEIGHT - 50))

# Hàm nâng cấp tháp
def upgrade_tower(index):
    global gold
    if gold >= upgrade_cost and towers[index][2] < 3:
        towers[index] = (towers[index][0], towers[index][1], towers[index][2] + 1)
        gold -= upgrade_cost

# Hàm áp dụng hiệu ứng làm chậm cho tất cả quái vật
def apply_slow_effect():
    for monster in monsters:
        monster[2] = 1  # Giảm tốc độ quái vật
        monster[4] = True  # Đánh dấu bị làm chậm
        monster[5] = pygame.time.get_ticks() + 10000  # Thiết lập thời gian kết thúc làm chậm

# Vòng lặp chính của game
running = True
clock = pygame.time.Clock()

# Biến để lưu thời gian hiện tại và thời gian đặt vật làm chậm
slow_placed_time = 0
slow_placed = False

while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == spawn_monster_event:
            create_monster()
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
                    apply_slow_effect()  # Áp dụng hiệu ứng làm chậm cho tất cả quái vật
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
                        upgrade_tower(i)
                        break

    # Vẽ tháp
    for tower in towers:
        draw_tower(tower[0], tower[1], tower[2])

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
        draw_bullet(bullet[0], bullet[1])

        # Kiểm tra va chạm giữa đạn và quái vật
        for monster in monsters:
            monster_rect = pygame.Rect(monster[0], monster[1], MONSTER_SIZE, MONSTER_SIZE)
            if check_collision(bullet_rect, monster_rect):
                bullets_to_remove.append(bullet)
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
        monster_x, monster_y, monster_speed, monster_health, slowed, slow_timer = monster

        # Kiểm tra nếu thời gian làm chậm đã kết thúc
        if slowed and pygame.time.get_ticks() > slow_timer:
            monster[2] = 2  # Khôi phục tốc độ ban đầu
            monster[4] = False  # Hủy đánh dấu bị làm chậm

        monster[0] -= monster_speed  # Di chuyển quái vật sang trái
        if monster[0] < 0:
            monsters_to_remove.append(monster)
        else:
            draw_monster(monster[0], monster[1])

    # Vẽ thông tin vàng và nút mua tháp
    draw_gold()
    draw_buy_tower_button()
    draw_buy_slow_button()

    # Hiển thị vị trí đặt tháp hoặc vật làm chậm nếu đang ở chế độ đặt
    if placing_tower:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        draw_tower(mouse_x - TOWER_SIZE // 2, mouse_y - TOWER_SIZE // 2, 1)
    elif placing_slow:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        draw_slow(mouse_x - SLOW_SIZE // 2, mouse_y - SLOW_SIZE // 2)
    
    # Vẽ vật làm chậm nếu đã được đặt và chỉ trong vòng 1 giây
    if slow_placed:
        if pygame.time.get_ticks() - slow_placed_time <= 1000:  # 1 giây
            draw_slow(*slow_position)
        else:
            slow_placed = False  # Reset flag sau 1 giây

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát khỏi Pygame
pygame.quit()
