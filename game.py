import pygame
from config import *
from bug import *
from interact import Interact
from bug_manager import BugManager
from vfx_manager import VFXManager
import time
import os
import sys

def initialize_game(x, y):
    global screen, WIDTH, HEIGHT, tile_imgs, grid, projectiles, bug_projectiles, hand, \
           game_screen_width, game_screen_height, play_button_img, exit_button_img, help_button_img, \
           play_button_choose_img, exit_button_choose_img, help_button_choose_img, background_img, \
           menu_screen_width, menu_screen_height, level_buttons, level_buttons_choose, white, black, green, blue, \
           FPS, BULLET_SIZE, TOWER_SIZE, SLOW_SIZE, bullet_speed, tower_cost, slow_cost, ice_cost, count, \
           upgrade_cost, gold, shoot_delay, shoot_counters, pause_button_img, pause_button_choose_img, \
           continue_button_img, continue_button_choose_img, exit_game_button_img, exit_game_button_choose_img

    pygame.init()
    WIDTH, HEIGHT = 1300, 800
    screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Tower Defense Game")



    # Load button images
    pause_button_img = pygame.image.load(os.path.join("assets", "menu", "Pause.png"))
    pause_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Pause_choose.png"))
    continue_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
    continue_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
    exit_game_button_img = pygame.image.load(os.path.join("assets", "menu", "exit.png"))
    exit_game_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "exit_choose.png"))



    # Màu sắc
    LIGHT_BLUE = (173, 216, 230)
    ICE_BLUE = (135, 206, 235)
    DARK_BLUE = (0, 0, 139)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)  # Màu của vật làm chậm
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)
    mediumaquamarine = (102, 205, 170)

    # Tốc độ khung hình
    FPS = 60

    # Kích thước quái vật và đạn
    BULLET_SIZE = 16
    TOWER_SIZE = 50
    SLOW_SIZE = 50
    # Tốc độ đạn
    bullet_speed = 5
    # Giá tiền mua tháp và vật làm chậm
    tower_cost = 50
    slow_cost = 100
    slow_placed = False
    ice_cost = 300
    count = 0
    # Giá nâng cấp tháp
    upgrade_cost = 200

    class gold:
        gold = 3000

    gold = gold()
    # Tần suất bắn đạn (tính bằng khung hình)
    shoot_delay = 60
    shoot_counters = []

    tile_imgs = [
        pygame.image.load(os.path.join("assets", "grass1.jpg")), 
        pygame.image.load(os.path.join("assets", "grass2.jpg"))
    ]
    grid = Grid(WIDTH, HEIGHT, tile_imgs)

    projectiles = ProjectileManager()
    bug_projectiles = ProjectileManager()

    hand = Hand(100, 0, 80)

    # Thiết lập kích thước cửa sổ cho màn hình game
    game_screen_width = 1300
    game_screen_height = 800

    # Tải hình ảnh nút và hình nền
    play_button_img = pygame.image.load(os.path.join("assets", "menu", "Play.png"))
    exit_button_img = pygame.image.load(os.path.join("assets", "menu", "exit.png"))
    help_button_img = pygame.image.load(os.path.join("assets", "menu", "Option.png"))
    play_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Play_choose.png"))
    exit_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "exit_choose.png"))
    help_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Option_choose.png"))
    background_img = pygame.image.load(os.path.join("assets", "menu", "background.png"))

    # Thiết lập kích thước cửa sổ cho màn hình menu
    menu_screen_width = 1080
    menu_screen_height = 607

    # Tải hình ảnh các nút chọn level
    level_buttons = [pygame.image.load(os.path.join("assets", "menu", f"level_{i}.png")) for i in range(0, 6)]
    level_buttons_choose = [pygame.image.load(os.path.join("assets", "menu", f"level_{i}_choose.png")) for i in range(0, 6)]

    # Thiết lập màu sắc
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

# Initialize Pygame
initialize_game(1080,607)

# Trạng thái của màn hình
current_screen = "main_menu"
button_pressed = False  # Biến theo dõi trạng thái nhấn nút

def draw_pause_screen(mouse_pos):
    screen.fill(white)
    center_x = WIDTH // 2
    if draw_button(continue_button_img, continue_button_choose_img, center_x - continue_button_img.get_width() // 2, 300, continue_button_img.get_width(), continue_button_img.get_height(), mouse_pos):
        return "game_resume"
    if draw_button(exit_game_button_img, exit_game_button_choose_img, center_x - exit_game_button_img.get_width() // 2, 400, exit_game_button_img.get_width(), exit_game_button_img.get_height(), mouse_pos):
        return "main_menu"
    return "pause_screen"



# Hàm vẽ nút với hình ảnh và hiệu ứng khi rê chuột qua
def draw_button(image, image_choose, x, y, w, h, mouse_pos):
    global button_pressed
    button_rect = pygame.Rect(x, y, w, h)
    if button_rect.collidepoint(mouse_pos):
        screen.blit(image_choose, button_rect.topleft)
        if pygame.mouse.get_pressed()[0] == 1:
            button_pressed = True
        elif button_pressed and pygame.mouse.get_pressed()[0] == 0:
            button_pressed = False
            return True
    else:
        screen.blit(image, button_rect.topleft)
    return False

# Hàm vẽ màn hình chính
def draw_main_menu(mouse_pos):
    screen.blit(background_img, (0, 0))
    center_x = menu_screen_width // 2
    if draw_button(play_button_img, play_button_choose_img, center_x - play_button_img.get_width() // 2, 300, play_button_img.get_width(), play_button_img.get_height(), mouse_pos):
        return "level_select"
    if draw_button(help_button_img, help_button_choose_img, center_x - help_button_img.get_width() // 2, 400, help_button_img.get_width(), help_button_img.get_height(), mouse_pos):
        print("Display help instructions here")
        return "main_menu"
    if draw_button(exit_button_img, exit_button_choose_img, center_x - exit_button_img.get_width() // 2, 500, exit_button_img.get_width(), exit_button_img.get_height(), mouse_pos):
        pygame.quit()
        sys.exit()
    return "main_menu"

# Hàm vẽ màn hình chọn level
def draw_level_select(mouse_pos):
    screen.fill(white)
    for i, (button_img, button_choose_img) in enumerate(zip(level_buttons, level_buttons_choose)):
        x = (i % 3) * (button_img.get_width() + 20) + (menu_screen_width - 3 * button_img.get_width() - 40) // 2
        y = (i // 3) * (button_img.get_height() + 20) + 200
        if draw_button(button_img, button_choose_img, x, y, button_img.get_width(), button_img.get_height(), mouse_pos):
            return f"game_screen_{i+1}"
    return "level_select"
def game_loop(level):
    global screen, current_screen
    initialize_game(1300, 800)  

    bug_manager = BugManager()
    clock = pygame.time.Clock()
    dt = 0 
    # Main game loop variables
    slow_placed_time = 0
    slow_placed = False
    paused = False
    running = True
    rect_size = grid.get_cell_size()
    start_time = time.time()

    option = -1

    while running:
        if not paused:
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
                        hand.toggle_select(option)
                    else:
                        pass

                    option = hand.select(mouse_x, mouse_y)

            projectiles.add_projectiles(grid.draw(screen, dt, grid.get_objects(), bug_manager.get_bugs()))
            # Towers shoot
            for bug_pos in bug_manager.get_bugs_pos():
                for tower in grid.get_objs_in_row(grid.convert_to_grid_pos(bug_pos[0], bug_pos[1])[0]):
                    if tower.get_name() == "Tower":
                        tower.set_mode(1)

            # Check bullet-bug collision
            projectiles.check_collision(bug_manager.get_bugs(), WIDTH, HEIGHT)
            projectiles.remove_projectiles()
            projectiles.draw(screen, dt)

            grid.remove_objects()

            bug_manager.check_collision(grid)


            # Update bugs
            for bug in bug_manager.get_bugs():
                if bug.is_dead():
                    hand.add_energy(50)
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

            # Draws selected tower on mouse pos.
            hand.draw_selected(screen, mouse_x, mouse_y)
        # Draw pause button in the top-right corner
            pause_button_x = WIDTH - pause_button_img.get_width() - 10
            pause_button_y = 10
            if draw_button(pause_button_img, pause_button_choose_img, pause_button_x, pause_button_y, pause_button_img.get_width(), pause_button_img.get_height(), (mouse_x, mouse_y)):
                paused = True

            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Press 'P' to unpause
                    paused = False

            mouse_pos = pygame.mouse.get_pos()
            current_screen = draw_pause_screen(mouse_pos)
            if current_screen == "game_resume":
                paused = False
                current_screen = f"game_screen_{level}"
            elif current_screen == "main_menu":
                running = False
        pygame.display.flip()

    pygame.quit()
# Vòng lặp chính của chương trình
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_pos = pygame.mouse.get_pos()
    if current_screen == "main_menu":
        current_screen = draw_main_menu(mouse_pos)
    elif current_screen == "level_select":
        current_screen = draw_level_select(mouse_pos)
    elif "game_screen" in current_screen:
        level = int(current_screen.split('_')[-1])
        game_loop(level)
        current_screen = "main_menu"

        screen = pygame.display.set_mode((menu_screen_width, menu_screen_height))
        pygame.display.set_caption("Tower Defense Game")
    elif current_screen == "pause_screen":
        current_screen = draw_pause_screen(mouse_pos)
        if current_screen == "game_resume":
            current_screen = f"game_screen_{level}"

    pygame.display.flip()
