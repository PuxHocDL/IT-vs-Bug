import pygame
from config import *
from bug import *
from interact import Interact
from bug_manager import BugManager
from vfx_manager import VFXManager
import time
from bulldozer import Bulldozer
import os
import sys

def initialize_game(x, y, FPS):
    global screen, WIDTH, HEIGHT, tile_imgs, grid, projectiles, bug_projectiles, hand, \
           game_screen_width, game_screen_height, play_button_img, exit_button_img, optition_button_img, \
           play_button_choose_img, exit_button_choose_img, optition_button_choose_img, background_img, \
           menu_screen_width, menu_screen_height, level_buttons, level_buttons_choose, white, black, green, blue, \
           BULLET_SIZE, TOWER_SIZE, SLOW_SIZE, bullet_speed, tower_cost, slow_cost, ice_cost, count, \
           upgrade_cost, gold, shoot_delay, shoot_counters, pause_button_img, pause_button_choose_img, \
           continue_button_img, continue_button_choose_img, exit_game_button_img, exit_game_button_choose_img, \
           rules_button_img, rules_button_choose_img, back_button_img, back_button_choose_img, brightness, monster_schedule,\
           shovel_choose_img, shovel_img, rules_background_img,gray, background1_img

    pygame.init()
    WIDTH, HEIGHT = 1300, 750
    screen = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Tower Defense Game")

    # Load button images
    pause_button_img = pygame.image.load(os.path.join("assets", "menu", "Pause.png"))
    pause_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Pause_choose.png"))
    continue_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
    continue_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
    exit_game_button_img = pygame.image.load(os.path.join("assets", "menu", "exit.png"))
    exit_game_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "exit_choose.png"))
    rules_button_img = pygame.image.load(os.path.join("assets", "menu", "Help.png"))
    rules_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Help_choose.png"))
    back_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
    back_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
    shovel_img = pygame.image.load(os.path.join("assets", "menu", "Hammer.png"))
    shovel_choose_img = pygame.image.load(os.path.join("assets", "menu", "Hammer_choose.png"))
    rules_background_img = pygame.image.load(os.path.join("assets", "menu", "background.png"))

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


    # Độ sáng mặc định
  

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

    grid = Grid(WIDTH, HEIGHT)

    projectiles = ProjectileManager()
    bug_projectiles = ProjectileManager()

    hand = Hand(50, 5, 80)

    # Thiết lập kích thước cửa sổ cho màn hình game
    game_screen_width = 1300
    game_screen_height = 750

    # Tải hình ảnh nút và hình nền
    play_button_img = pygame.image.load(os.path.join("assets", "menu", "Play.png"))
    exit_button_img = pygame.image.load(os.path.join("assets", "menu", "exit.png"))
    optition_button_img = pygame.image.load(os.path.join("assets", "menu", "Option.png"))
    play_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Play_choose.png"))
    exit_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "exit_choose.png"))
    optition_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Option_choose.png"))
    background_img = pygame.image.load(os.path.join("assets", "menu", "background.png"))
    background1_img = pygame.image.load(os.path.join("assets", "menu", "Background1.png"))

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
    gray = (128, 128, 128)
    
    monster_schedule = [[
    {"time": 5, "name": "BigBug"},
    {"time": 6, "name": "TriangleBug"},
    {"time": 10, "name": "BigBug"},
    {"time": 11, "name": "HexagonBug"},
    {"time": 12, "name": "HexagonBug"},
    {"time": 21, "name": "HexagonBug"},
    {"time": 22, "name": "HexagonBug"},
    {"time": 27, "name": "HexagonBug"},
    {"time": 21, "name": "HexagonBug"},
    {"time": 22, "name": "HexagonBug"},
    {"time": 27, "name": "HexagonBug"},
    {"time": 21, "name": "HexagonBug"},
    {"time": 22, "name": "HexagonBug"},
    {"time": 27, "name": "HexagonBug"},
    {"time": 28, "name": "HexagonBug"},
    {"time": 30, "name": "HexagonBug"},
    {"time": 31, "name": "HexagonBug"},
    {"time": 40, "name": "HexagonBug"},
    ], [{"time": 5, "name": "BigBug"},
    {"time": 6, "name": "TriangleBug"},
    {"time": 10, "name": "BigBug"},
    {"time": 11, "name": "HexagonBug"},
    {"time": 12, "name": "HexagonBug"},
    {"time": 21, "name": "HexagonBug"},
    {"time": 22, "name": "HexagonBug"},
    {"time": 27, "name": "HexagonBug"},
    {"time": 21, "name": "BigBug"},
    {"time": 22, "name": "BigBug"},
    {"time": 27, "name": "BigBug"},
    {"time": 21, "name": "HexagonBug"},
    {"time": 22, "name": "HexagonBug"},
    {"time": 27, "name": "HexagonBug"},
    {"time": 28, "name": "BigBug"},
    {"time": 30, "name": "TriangleBug"},
    {"time": 31, "name": "HexagonBug"},
    {"time": 40, "name": "HexagonBug"}]]

# Initialize Pygame
initialize_game(1080,607,FPS)

# Trạng thái của màn hình
# Trạng thái của màn hình
current_screen = "main_menu"
button_pressed = False  # Biến theo dõi trạng thái nhấn nút
def apply_brightness(surface, brightness):
    """Apply brightness to the surface."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    if brightness > 0 :
        # Decrease brightness
        overlay.fill((0, 0, 0, int((1 - brightness) * 255)))
    
    surface.blit(overlay, (0,0))
    return surface

def draw_options_menu(mouse_pos):
    global FPS, brightness

    screen.fill(white)
    center_x = menu_screen_width // 2

    # Draw FPS Slider
    fps_text = pygame.font.SysFont(None, 40).render(f"FPS: {FPS}", True, black)
    screen.blit(fps_text, (center_x - 100, 200))
    if draw_slider(center_x, 250, 200, mouse_pos, FPS, 30, 120):
        FPS = int(adjust_value_based_on_slider(center_x, 250, 200, mouse_pos, 30, 120))

    # Draw Brightness Slider
    brightness_text = pygame.font.SysFont(None, 40).render(f"Brightness: {int(brightness * 100)}%", True, black)
    screen.blit(brightness_text, (center_x - 100, 350))
    if draw_slider(center_x, 400, 200, mouse_pos, brightness * 100, 0, 100):  # Adjusted min and max values
        brightness = adjust_value_based_on_slider(center_x, 400, 200, mouse_pos, 0, 100) / 100.0  # Adjusted to 0-100 range

    # Draw Back Button
    if draw_button(back_button_img, back_button_choose_img, center_x - back_button_img.get_width() // 2, 500, back_button_img.get_width(), back_button_img.get_height(), mouse_pos):
        return "main_menu"
        
    return "options_menu"

def draw_slider(x, y, width, mouse_pos, current_value, min_value, max_value):
    # Draw slider background
    pygame.draw.rect(screen, gray, (x - width // 2, y, width, 5))

    # Calculate slider position
    slider_pos = int((current_value - min_value) / (max_value - min_value) * width)
    pygame.draw.rect(screen, black, (x - width // 2 + slider_pos - 5, y - 10, 10, 25))

    # Check if the mouse is clicking the slider
    mouse_x, mouse_y = mouse_pos
    if y - 10 <= mouse_y <= y + 15 and x - width // 2 <= mouse_x <= x + width // 2:
        if pygame.mouse.get_pressed()[0]:
            new_value = (mouse_x - (x - width // 2)) / width * (max_value - min_value) + min_value
            return new_value
    
    return None

def adjust_value_based_on_slider(x, y, width, mouse_pos, min_value, max_value):
    mouse_x, mouse_y = mouse_pos
    if y - 10 <= mouse_y <= y + 15 and x - width // 2 <= mouse_x <= x + width // 2:
        new_value = (mouse_x - (x - width // 2)) / width * (max_value - min_value) + min_value
        return new_value
    return None

def draw_rules_screen(mouse_pos):
    global rules_background_img  # Ensure the background image is accessible here
    
    screen.blit(rules_background_img, (0, 0))  # Draw the background image first
    center_x = menu_screen_width // 2

    # Display game rules
    rules = [
        "Welcome to Tower Defense Game!",
        "1. Place towers to defend against incoming bugs.",
        "2. Each tower type has different abilities.",
        "3. Earn gold by defeating bugs.",
        "4. Use gold to place more towers or upgrade existing ones.",
        "5. Stop the bugs from reaching the left edge of the screen."
    ]

    font = pygame.font.SysFont(None, 30)
    y = 100
    for rule in rules:
        rule_text = font.render(rule, True, black)
        screen.blit(rule_text, (50, y))
        y += 50

    # Draw Back Button
    if draw_button(back_button_img, back_button_choose_img, center_x - back_button_img.get_width() // 2, 500, back_button_img.get_width(), back_button_img.get_height(), mouse_pos):
        return "main_menu"

    return "rules_screen"



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
    if draw_button(play_button_img, play_button_choose_img, center_x - play_button_img.get_width() // 2, 200, play_button_img.get_width(), play_button_img.get_height(), mouse_pos):
        return "level_select"
    if draw_button(optition_button_img, optition_button_choose_img, center_x - optition_button_img.get_width() // 2, 300, optition_button_img.get_width(), optition_button_img.get_height(), mouse_pos):
        return "options_menu"
    if draw_button(rules_button_img, rules_button_choose_img, center_x - rules_button_img.get_width() // 2, 400, rules_button_img.get_width(), rules_button_img.get_height(), mouse_pos):
        return "rules_screen"
    if draw_button(exit_button_img, exit_button_choose_img, center_x - exit_button_img.get_width() // 2, 500, exit_button_img.get_width(), exit_button_img.get_height(), mouse_pos):
        pygame.quit()
        sys.exit()
    return "main_menu"

def draw_game_over():
    font = pygame.font.SysFont(None, 75)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

# Hàm vẽ màn hình chọn level
def draw_level_select(mouse_pos):
    screen.blit(background1_img, (0, 0))
    for i, (button_img, button_choose_img) in enumerate(zip(level_buttons, level_buttons_choose)):
        x = (i % 3) * (button_img.get_width() + 20) + (menu_screen_width - 3 * button_img.get_width() - 40) // 2
        y = (i // 3) * (button_img.get_height() + 20) + 200
        if draw_button(button_img, button_choose_img, x, y, button_img.get_width(), button_img.get_height(), mouse_pos):
            return f"game_screen_{i+1}"
    return "level_select"

def game_loop(level):
    global screen, current_screen, brightness
    initialize_game(1300, 750, FPS)  
    
    bug_manager = BugManager()
    bulldozers = [Bulldozer(grid, row) for row in range(6)]
    clock = pygame.time.Clock()
    dt = 0   
    print(brightness)
    slow_placed_time = 0
    slow_placed = False
    paused = False
    game_over = False
    running = True
    rect_size = grid.get_cell_size()
    start_time = time.time()
    shovel_selected = False

    option = -1

    while running:
        if not paused:
            
            dt = clock.tick(FPS)


            current_time = time.time() - start_time

            for schedule in monster_schedule[:][1]:
                if current_time >= schedule["time"]:
                    bug_manager.add_bug(grid, schedule["name"])
                    monster_schedule[1].remove(schedule)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = grid.convert_to_grid_pos(mouse_x, mouse_y)
                    
                    if option not in [-1, -2]:
                        if not grid.is_occupied(grid_x, grid_y) and grid.is_inside_gird(grid_x, grid_y):
                            hand.add_tower(grid, grid_x, grid_y)
                        hand.toggle_select(option)
                    elif option == -2:  # If shovel is selected, remove the tower
                        if grid.is_occupied(grid_x, grid_y):
                            tower = grid.get_object_in_one_grid(grid_x, grid_y)
                            tower.damage(9999999)
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
                if bug.get_x() <= -60:
                    row_index = grid.convert_to_grid_pos(bug.get_x(), bug.get_y())[0]
                    if not bulldozers[row_index].active and not bulldozers[row_index].used:
                        bulldozers[row_index].activate()
                    elif bulldozers[row_index].used: 
                        game_over = True


            # Check bullet-tower collision
            bug_projectiles.check_collision(grid.get_objects(), WIDTH, HEIGHT)
            bug_projectiles.remove_projectiles()
            bug_projectiles.draw(screen,dt)

            # Draw vfx
            VFXManager.draw(screen, dt)
            hand.draw(screen, dt, mouse_x, mouse_y)

            for bulldozer in bulldozers:
                bulldozer.update(bug_manager)
                bulldozer.draw(screen)
            
            if game_over:
                draw_game_over()
                pygame.display.flip()
                time.sleep(3)
                running = False
                current_screen = "main_menu"
            
            # Draws selected tower on mouse pos.
            hand.draw_selected(screen, mouse_x, mouse_y)
        # Draw pause button in the top-right corner
            pause_button_x = WIDTH - pause_button_img.get_width() - 10
            pause_button_y = 10
            if draw_button(pause_button_img, pause_button_choose_img, pause_button_x, pause_button_y, pause_button_img.get_width(), pause_button_img.get_height(), (mouse_x, mouse_y)):
                paused = True

            # Apply brightness adjustment here
            apply_brightness(screen, brightness)

            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Press 'P' to unpause
                    paused = False
            

            mouse_pos = pygame.mouse.get_pos()
            current_screen = draw_pause_screen(mouse_pos)
            screen = apply_brightness(screen, brightness)
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
    elif current_screen == "options_menu":
        current_screen = draw_options_menu(mouse_pos)
    elif current_screen == "rules_screen":
        current_screen = draw_rules_screen(mouse_pos)
    elif "game_screen" in current_screen:
        level = int(current_screen.split('_')[-1])
        game_loop(level)
        current_screen = "main_menu"
        screen = pygame.display.set_mode((menu_screen_width, menu_screen_height))
        pygame.display.set_caption("Tower Defense Game")
        pygame.init()
    elif current_screen == "pause_screen":
        current_screen = draw_pause_screen(mouse_pos)
        if current_screen == "game_resume":
            current_screen = f"game_screen_{level}"
    screen = apply_brightness(screen, brightness)
    pygame.display.flip()
