import pygame
import os
from level import Level
from button import Button
from utilities import load_json


def apply_brightness(surface, brightness):
    """Apply brightness to the surface."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    if brightness > 0:
        # Decrease brightness
        overlay.fill((0, 0, 0, int((1 - brightness) * 255)))

    surface.blit(overlay, (0,0))
    return surface


def draw_options_menu(fps, brightness, screen, width, height):
    center_x = width // 2

    back_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
    back_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
    back_button = Button(center_x - back_button_img.get_width() // 2, 500, back_button_img.get_width(), back_button_img.get_height(), back_button_img, back_button_choose_img, back_button_img)

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", fps, brightness
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_hovering(mouse_x, mouse_y):
                    back_button.click()
                    return "lmao", fps, brightness

        # Draw FPS Slider
        fps_text = pygame.font.SysFont(None, 40).render(f"FPS: {fps}", True, "black")
        screen.blit(fps_text, (center_x - 100, 200))
        if draw_slider(screen, center_x, 250, 200, (mouse_x, mouse_y), fps, 30, 120):
            fps = int(adjust_value_based_on_slider(center_x, 250, 200, (mouse_x, mouse_y), 30, 120))

        # Draw Brightness Slider
        brightness_text = pygame.font.SysFont(None, 40).render(f"Brightness: {int(brightness * 100)}%", True, "black")
        screen.blit(brightness_text, (center_x - 100, 350))
        if draw_slider(screen, center_x, 400, 200, (mouse_x, mouse_y), brightness * 100, 0, 100):  # Adjusted min and max values
            brightness = adjust_value_based_on_slider(center_x, 400, 200, (mouse_x, mouse_y), 0, 100) / 100.0  # Adjusted to 0-100 range

        back_button.draw(screen, mouse_x, mouse_y)
        apply_brightness(screen, brightness)

        pygame.display.flip()


def draw_slider(screen, x, y, width, mouse_pos, current_value, min_value, max_value):
    # Draw slider background
    pygame.draw.rect(screen, "gray", (x - width // 2, y, width, 5))

    # Calculate slider position
    slider_pos = int((current_value - min_value) / (max_value - min_value) * width)
    pygame.draw.rect(screen, "black", (x - width // 2 + slider_pos - 5, y - 10, 10, 25))

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


def draw_rules_screen(screen, width, height, brightness):
    center_x = width // 2

    rules_background_img = pygame.image.load(os.path.join("assets", "menu", "background.png"))
    back_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
    back_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
    back_button = Button(center_x - back_button_img.get_width() // 2, 500, back_button_img.get_width(), back_button_img.get_height(), back_button_img, back_button_choose_img, back_button_img)

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

    while True:
        screen.blit(rules_background_img, (0, 0))  # Draw the background image first
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_hovering(mouse_x, mouse_y):
                    back_button.click()
                    return "lmao"

        y = 100
        for rule in rules:
            rule_text = font.render(rule, True, "black")
            screen.blit(rule_text, (50, y))
            y += 50

        back_button.draw(screen, mouse_x, mouse_y)
        apply_brightness(screen, brightness)

        pygame.display.flip()


# Hàm vẽ màn hình chính
def draw_main_menu(fps, brightness):
    WIDTH, HEIGHT = 1080, 607

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Towers vs Monsters")
    center_x = WIDTH // 2

    background_img = pygame.image.load(os.path.join("assets", "Menu", "background.png"))

    play_button_img = pygame.image.load(os.path.join("assets", "menu", "Play.png"))
    play_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Play_choose.png"))
    option_button_img = pygame.image.load(os.path.join("assets", "menu", "Option.png"))
    option_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Option_choose.png"))
    rules_button_img = pygame.image.load(os.path.join("assets", "menu", "Help.png"))
    rules_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Help_choose.png"))
    exit_game_button_img = pygame.image.load(os.path.join("assets", "menu", "exit.png"))
    exit_game_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "exit_choose.png"))

    play_button = Button(center_x - play_button_img.get_width() // 2, 200, play_button_img.get_width(), play_button_img.get_height(), play_button_img, play_button_choose_img, play_button_img)
    option_button = Button(center_x - option_button_img.get_width() // 2, 300, option_button_img.get_width(), option_button_img.get_height(), option_button_img, option_button_choose_img, option_button_img)
    rules_button = Button(center_x - rules_button_img.get_width() // 2, 400, rules_button_img.get_width(), rules_button_img.get_height(), rules_button_img, rules_button_choose_img, rules_button_img)
    exit_button = Button(center_x - exit_game_button_img.get_width() // 2, 500, exit_game_button_img.get_width(), exit_game_button_img.get_height(), exit_game_button_img, exit_game_button_choose_img, exit_game_button_img)

    option = "lmao"

    while True:
        screen.blit(background_img, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", fps, brightness
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_hovering(mouse_x, mouse_y):
                    play_button.click()
                    option = draw_level_select(screen, WIDTH, HEIGHT, brightness)
                elif option_button.check_hovering(mouse_x, mouse_y):
                    option_button.click()
                    option, fps, brightness = draw_options_menu(fps, brightness, screen, WIDTH, HEIGHT)
                elif rules_button.check_hovering(mouse_x, mouse_y):
                    rules_button.click()
                    option = draw_rules_screen(screen, WIDTH, HEIGHT, brightness)
                elif exit_button.check_hovering(mouse_x, mouse_y):
                    exit_button.click()
                    option = "exit"

        if option != "lmao":
            break

        play_button.draw(screen, mouse_x, mouse_y)
        option_button.draw(screen, mouse_x, mouse_y)
        rules_button.draw(screen, mouse_x, mouse_y)
        exit_button.draw(screen, mouse_x, mouse_y)
        apply_brightness(screen, brightness)

        pygame.display.flip()

    pygame.quit()
    return option, fps, brightness


# Hàm vẽ màn hình chọn level
def draw_level_select(screen, width, height, brightness):
    background_img = pygame.image.load(os.path.join("assets", "menu", "Background1.png"))

    level_buttons = [pygame.image.load(os.path.join("assets", "menu", f"level_{i}.png")) for i in range(0, 6)]
    level_buttons_choose = [pygame.image.load(os.path.join("assets", "menu", f"level_{i}_choose.png")) for i in range(0, 6)]
    buttons = []
    for i in range(len(level_buttons)):
        x = (i % 3) * (level_buttons[i].get_width() + 20) + (width - 3 * level_buttons[i].get_width() - 40) // 2
        y = (i // 3) * (level_buttons[i].get_height() + 20) + 200
        buttons.append(Button(x, y, level_buttons[i].get_width(), level_buttons[i].get_height(), level_buttons[i], level_buttons_choose[i], level_buttons[i]))
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].check_hovering(mouse_x, mouse_y):
                        buttons[i].click()
                        return f"level{i+1}"

        for button in buttons:
            button.draw(screen, mouse_x, mouse_y)
        apply_brightness(screen, brightness)

        pygame.display.flip()


# Vòng lặp chính của chương trình
if __name__ == "__main__":
    level1_schedule = load_json(os.path.join("level_data", "level1.json"))
    level1 = Level([0, 1, 2, 3], level1_schedule)
    fps = 60
    brightness = 1

    option, fps, brightness = draw_main_menu(fps, brightness)
    while True:
        if option == "exit":
            break
        if option == "main_menu":
            option, fps, brightness = draw_main_menu(fps, brightness)
        else:
            option = level1.run(fps, brightness)
