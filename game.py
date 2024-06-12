import pygame
import os
from level import Level
from button import Button
from utilities import load_json


def apply_brightness(surface, brightness):
    """
    Apply brightness adjustment to the given surface.

    Parameters:
    surface (pygame.Surface): The surface to adjust brightness for.
    brightness (float): The brightness level, where 1 is the original brightness, 
                        values < 1 decrease brightness, and values > 1 are not supported.

    Returns:
    pygame.Surface: The surface with the applied brightness adjustment.
    """
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    if brightness > 0:
        # Decrease brightness
        overlay.fill((0, 0, 0, int((1 - brightness) * 255)))

    surface.blit(overlay, (0, 0))
    return surface


def draw_options_menu(fps, brightness, screen, width, height, hover_sound, click_sound):
    """
    Display the options menu and handle user interactions.

    Parameters:
    fps (int): The current frames per second setting.
    brightness (float): The current brightness setting.
    screen (pygame.Surface): The screen surface to draw on.
    width (int): The width of the screen.
    height (int): The height of the screen.
    hover_sound (pygame.mixer.Sound): The sound to play when hovering over a button.
    click_sound (pygame.mixer.Sound): The sound to play when clicking a button.

    Returns:
    tuple: A tuple containing the next screen to display ("exit" or "lmao"), the updated FPS, and the updated brightness.
    """
    center_x = width // 2
    rules_background_img = pygame.image.load(os.path.join("assets", "menu", "background.png"))
    back_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
    back_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
    back_button = Button(center_x - back_button_img.get_width() // 2, 500, back_button_img.get_width(), back_button_img.get_height(), back_button_img, back_button_choose_img, back_button_img, hover_sound, click_sound)

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(rules_background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", fps, brightness
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_hovering(mouse_x, mouse_y):
                    back_button.click()
                    return "lmao", fps, brightness

        # Draw FPS Slider
        fps_text = pygame.font.SysFont(None, 40).render(f"FPS: {fps}", True, "white")
        screen.blit(fps_text, (center_x - 100, 200))
        if draw_slider(screen, center_x, 250, 200, (mouse_x, mouse_y), fps, 30, 120):
            fps = int(adjust_value_based_on_slider(center_x, 250, 200, (mouse_x, mouse_y), 30, 120))

        # Draw Brightness Slider
        brightness_text = pygame.font.SysFont(None, 40).render(f"Brightness: {int(brightness * 100)}%", True, "white")
        screen.blit(brightness_text, (center_x - 100, 350))
        if draw_slider(screen, center_x, 400, 200, (mouse_x, mouse_y), brightness * 100, 0, 100):  # Adjusted min and max values
            brightness = adjust_value_based_on_slider(center_x, 400, 200, (mouse_x, mouse_y), 0, 100) / 100.0  # Adjusted to 0-100 range

        back_button.draw(screen, mouse_x, mouse_y)
        apply_brightness(screen, brightness)

        pygame.display.flip()


def draw_slider(screen, x, y, width, mouse_pos, current_value, min_value, max_value):
    """
    Draw a slider on the screen and handle user interactions.

    Parameters:
    screen (pygame.Surface): The screen surface to draw on.
    x (int): The x-coordinate of the slider's center.
    y (int): The y-coordinate of the slider.
    width (int): The width of the slider.
    mouse_pos (tuple): The current position of the mouse cursor.
    current_value (float): The current value of the slider.
    min_value (float): The minimum value of the slider.
    max_value (float): The maximum value of the slider.

    Returns:
    float or None: The new value of the slider if adjusted, or None if not adjusted.
    """
    # Draw slider background
    pygame.draw.rect(screen, "gray", (x - width // 2, y, width, 5))

    # Calculate slider position
    slider_pos = int((current_value - min_value) / (max_value - min_value) * width)
    pygame.draw.rect(screen, "white", (x - width // 2 + slider_pos - 5, y - 10, 10, 25))

    # Check if the mouse is clicking the slider
    mouse_x, mouse_y = mouse_pos
    if y - 10 <= mouse_y <= y + 15 and x - width // 2 <= mouse_x <= x + width // 2:
        if pygame.mouse.get_pressed()[0]:
            new_value = (mouse_x - (x - width // 2)) / width * (max_value - min_value) + min_value
            return new_value

    return None


def adjust_value_based_on_slider(x, y, width, mouse_pos, min_value, max_value):
    """
    Adjust the value based on the slider's position and mouse interaction.

    Parameters:
    x (int): The x-coordinate of the slider's center.
    y (int): The y-coordinate of the slider.
    width (int): The width of the slider.
    mouse_pos (tuple): The current position of the mouse cursor.
    min_value (float): The minimum value of the slider.
    max_value (float): The maximum value of the slider.

    Returns:
    float or None: The new value based on the slider's position and mouse interaction, or None if not adjusted.
    """
    mouse_x, mouse_y = mouse_pos
    if y - 10 <= mouse_y <= y + 15 and x - width // 2 <= mouse_x <= x + width // 2:
        new_value = (mouse_x - (x - width // 2)) / width * (max_value - min_value) + min_value
        return new_value
    return None


def draw_rules_screen(screen, width, height, brightness, hover_sound, click_sound):
    """
    Display the rules screen and handle user interactions.

    Parameters:
    screen (pygame.Surface): The screen surface to draw on.
    width (int): The width of the screen.
    height (int): The height of the screen.
    brightness (float): The current brightness setting.
    hover_sound (pygame.mixer.Sound): The sound to play when hovering over a button.
    click_sound (pygame.mixer.Sound): The sound to play when clicking a button.

    Returns:
    str: The next screen to display ("exit" or "lmao").
    """
    center_x = width // 2

    rules_background_img = pygame.image.load(os.path.join("assets", "menu", "background.png"))
    back_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
    back_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
    back_button = Button(center_x - back_button_img.get_width() // 2, 500, back_button_img.get_width(), back_button_img.get_height(), back_button_img, back_button_choose_img, back_button_img, hover_sound, click_sound)

    # Display game rules
    rules = [
        "Welcome to Tower Defense Game!",
        "1. Place towers to defend against incoming bugs.",
        "2. Each tower type has different abilities.",
        "3. Earn gold by defeating bugs.",
        "4. Use energy to place more towers or upgrade existing ones.",
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
            rule_text = font.render(rule, True, "white")
            screen.blit(rule_text, (50, y))
            y += 50

        back_button.draw(screen, mouse_x, mouse_y)
        apply_brightness(screen, brightness)

        pygame.display.flip()


def draw_main_menu(fps, brightness, hover_sound, click_sound):
    """
    Display the main menu and handle user interactions.

    Parameters:
    fps (int): The current frames per second setting.
    brightness (float): The current brightness setting.
    hover_sound (pygame.mixer.Sound): The sound to play when hovering over a button.
    click_sound (pygame.mixer.Sound): The sound to play when clicking a button.

    Returns:
    tuple: A tuple containing the next screen to display ("exit", "main_menu", or a level index), the updated FPS, and the updated brightness.
    """
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

    font = pygame.font.Font(os.path.join("assets", "arcadeclassic.ttf"), 100)
    font2 = pygame.font.Font(os.path.join("assets", "arcadeclassic.ttf"), 50)
    title_towers = font.render("Towers", True, "red")
    title_vs = font2.render("vs", True, "white")
    title_monsters = font.render(" Monsters", True, "blue")
    title_width = title_towers.get_width() + title_vs.get_width() + title_monsters.get_width()

    play_button = Button(center_x - play_button_img.get_width() // 2, 200, play_button_img.get_width(), play_button_img.get_height(), play_button_img, play_button_choose_img, play_button_img, hover_sound, click_sound)
    option_button = Button(center_x - option_button_img.get_width() // 2, 300, option_button_img.get_width(), option_button_img.get_height(), option_button_img, option_button_choose_img, option_button_img, hover_sound, click_sound)
    rules_button = Button(center_x - rules_button_img.get_width() // 2, 400, rules_button_img.get_width(), rules_button_img.get_height(), rules_button_img, rules_button_choose_img, rules_button_img, hover_sound, click_sound)
    exit_button = Button(center_x - exit_game_button_img.get_width() // 2, 500, exit_game_button_img.get_width(), exit_game_button_img.get_height(), exit_game_button_img, exit_game_button_choose_img, exit_game_button_img, hover_sound, click_sound)

    option = "lmao"

    # Load and play main menu music
    pygame.mixer.music.load(os.path.join("assets", "music", "main_menu.ogg"))
    pygame.mixer.music.set_volume(0.3)  # Set music volume to 50%
    pygame.mixer.music.play(-1)

    while True:
        screen.blit(background_img, (0, 0))
        screen.blit(title_towers, (center_x-title_width//2, 100))
        screen.blit(title_vs, (center_x-title_vs.get_width()//2, 130))
        screen.blit(title_monsters, (center_x+title_vs.get_width(), 100))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", fps, brightness
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_hovering(mouse_x, mouse_y):
                    play_button.click()
                    option = draw_level_select(screen, WIDTH, HEIGHT, brightness, hover_sound, click_sound)
                elif option_button.check_hovering(mouse_x, mouse_y):
                    option_button.click()
                    option, fps, brightness = draw_options_menu(fps, brightness, screen, WIDTH, HEIGHT, hover_sound, click_sound)
                elif rules_button.check_hovering(mouse_x, mouse_y):
                    rules_button.click()
                    option = draw_rules_screen(screen, WIDTH, HEIGHT, brightness, hover_sound, click_sound)
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


def draw_loading_screen(screen, width, height, brightness):
    """
    Display the loading screen.

    Parameters:
    screen (pygame.Surface): The screen surface to draw on.
    width (int): The width of the screen.
    height (int): The height of the screen.
    brightness (float): The current brightness setting.
    """
    center_x = width // 2
    center_y = height // 2

    # Background color or image
    screen.fill("black")

    # Loading text
    pygame.init()
    font = pygame.font.SysFont(None, 50)
    loading_text = font.render("Loading...", True, "white")
    screen.blit(loading_text, (center_x - loading_text.get_width() // 2, center_y - loading_text.get_height() // 2))
    
    apply_brightness(screen, brightness)
    
    pygame.display.flip()
    pygame.time.delay(2000)  # Display for 2 seconds


def draw_level_select(screen, width, height, brightness, hover_sound, click_sound):
    """
    Display the level selection screen and handle user interactions.

    Parameters:
    screen (pygame.Surface): The screen surface to draw on.
    width (int): The width of the screen.
    height (int): The height of the screen.
    brightness (float): The current brightness setting.
    hover_sound (pygame.mixer.Sound): The sound to play when hovering over a button.
    click_sound (pygame.mixer.Sound): The sound to play when clicking a button.

    Returns:
    int: The selected level index, or "exit" if the user quits.
    """
    background_img = pygame.image.load(os.path.join("assets", "menu", "Background1.png"))

    level_buttons = [pygame.image.load(os.path.join("assets", "menu", f"level_{i}.png")) for i in range(0, 6)]
    level_buttons_choose = [pygame.image.load(os.path.join("assets", "menu", f"level_{i}_choose.png")) for i in range(0, 6)]
    buttons = []
    for i in range(len(level_buttons)):
        x = (i % 3) * (level_buttons[i].get_width() + 20) + (width - 3 * level_buttons[i].get_width() - 40) // 2
        y = (i // 3) * (level_buttons[i].get_height() + 20) + 200
        buttons.append(Button(x, y, level_buttons[i].get_width(), level_buttons[i].get_height(), level_buttons[i], level_buttons_choose[i], level_buttons[i], hover_sound, click_sound))

    # Load and play level select music
    pygame.mixer.music.load(os.path.join("assets", "music", "selected.ogg"))
    pygame.mixer.music.set_volume(0.3)  # Set music volume to 50%
    pygame.mixer.music.play(-1)

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
                        return i

        for button in buttons:
            button.draw(screen, mouse_x, mouse_y)
        apply_brightness(screen, brightness)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer

    # Load sound effects
    hover_sound = pygame.mixer.Sound(os.path.join("assets", "music", "hover.wav"))
    click_sound = pygame.mixer.Sound(os.path.join("assets", "music", "click.wav"))
    hover_sound.set_volume(1)  # Set sound effect volume to 50%
    click_sound.set_volume(1)  # Set sound effect volume to 50%

    fps = 60
    brightness = 1

    option, fps, brightness = draw_main_menu(fps, brightness, hover_sound, click_sound)
    WIDTH, HEIGHT = 1080, 607

    while True:
        if option == "exit":
            break
        if option == "main_menu":
            option, fps, brightness = draw_main_menu(fps, brightness, hover_sound, click_sound)
        else:
            # Initialize Pygame display for loading screen
            screen = pygame.display.set_mode((1300, 750))
            # Display the loading screen
            draw_loading_screen(screen, 1300, 750, brightness)

            tower_ids, level_schedule, starting_energy = load_json(os.path.join("level_data", f"level{option+1}.json"))
            level = Level(tower_ids, level_schedule, starting_energy, pygame.image.load(os.path.join("assets", "menu", f"map{option%3}.png")), os.path.join("assets", "music", f"battle_map{option%3}.ogg"))
            # Run the level
            option = level.run(fps, brightness)

    # Stop any playing music when exiting
    pygame.mixer.init()
    pygame.mixer.music.stop()
