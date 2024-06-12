import pygame
import os
import time
from bug_manager import BugManager
from bulldozer import Bulldozer
from grid import Grid
from hand import Hand
from projectile_manager import ProjectileManager
from vfx_manager import VFXManager
from button import Button

class Level:
    """
    Represents a game level in a tower defense game.

    Attributes:
        __WIDTH (int): The width of the game window.
        __HEIGHT (int): The height of the game window.
        __monster_schedule (list): The schedule of monster appearances.
        __tower_ids (list): The IDs of towers available in the level.
        __starting_energy (int): The starting energy for the player.
        __music (str): The path to the background music file.
        __total_time (int): The total time for the monster schedule.
        __max_progress (int): The maximum progress based on the monster schedule.
        __map (str): The path to the map image file.
    """

    __WIDTH = 1300
    __HEIGHT = 750

    def __init__(self, tower_ids, monster_schedule, starting_energy, map_img, music):
        """
        Initializes the Level instance.

        Args:
            tower_ids (list): The IDs of towers available in the level.
            monster_schedule (list): The schedule of monster appearances.
            starting_energy (int): The starting energy for the player.
            map_img (str): The path to the map image file.
            music (str): The path to the background music file.
        """
        self.__monster_schedule = monster_schedule
        self.__tower_ids = tower_ids
        self.__starting_energy = starting_energy
        self.__music = music
        self.__max_progress = len(monster_schedule)
        self.__map = map_img
        pygame.mixer.music.load(self.__music)
        pygame.mixer.music.set_volume(0.3) 
        pygame.mixer.music.play(-1)

    def run(self, fps, brightness):
        """
        Runs the main game loop.

        Args:
            fps (int): The frames per second for the game loop.
            brightness (float): The brightness level to apply to the screen.
        
        Returns:
            str: The next screen to display, typically "main_menu".
        """
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((Level.__WIDTH, Level.__HEIGHT))
        pygame.display.set_caption("Towers vs Monsters")

        # Load sound effects
        hover_sound = pygame.mixer.Sound(os.path.join("assets", "music", "hover.wav"))
        click_sound = pygame.mixer.Sound(os.path.join("assets", "music", "click.wav"))

        hover_sound.set_volume(0.5)
        click_sound.set_volume(0.5)

        grid = Grid(Level.__WIDTH, Level.__HEIGHT, self.__map)
        hand = Hand(50, 5, 80, self.__starting_energy)
        for tid in self.__tower_ids:
            hand.add_card(tid)

        bug_manager = BugManager()
        bulldozers = [Bulldozer(grid, row) for row in range(6)]

        projectiles = ProjectileManager()
        bug_projectiles = ProjectileManager()

        pause_button_img = pygame.image.load(os.path.join("assets", "menu", "Pause.png"))
        pause_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Pause_choose.png"))
        pause_button = Button(Level.__WIDTH - pause_button_img.get_width() - 10, 10, pause_button_img.get_width(), pause_button_img.get_height(), pause_button_img, pause_button_choose_img, pause_button_img, hover_sound, click_sound)

        clock = pygame.time.Clock()
        dt = 0
        game_over = False
        running = True
        start_time = time.time()
        victory_timer = None  # Add this variable to track the time when the last bug dies

        option = -1

        # Main game loop
        while running:
            dt = clock.tick(fps)
            current_time = time.time() - start_time

            for schedule in self.__monster_schedule:
                if current_time >= schedule["time"]:
                    bug_manager.add_bug(grid, schedule["name"])
                    self.__monster_schedule.remove(schedule)

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    grid_x, grid_y = grid.convert_to_grid_pos(mouse_x, mouse_y)
                    if event.button == 1:       # Left click
                        if pause_button.check_hovering(mouse_x, mouse_y):
                            pause_button.click()
                            choice = Level.__draw_pause_screen(screen, hover_sound, click_sound)
                            if choice == 0:
                                running = False
                            else:
                                clock.tick(fps)

                        if option not in [-1, -2]:
                            if not grid.is_occupied(grid_x, grid_y) and grid.is_inside_gird(grid_x, grid_y):
                                hand.add_tower(grid, grid_x, grid_y)
                            hand.toggle_select(option)
                        elif option == -2:  # If shovel is selected, remove the tower
                            if grid.is_occupied(grid_x, grid_y):
                                tower = grid.get_object_in_one_grid(grid_x, grid_y)
                                tower.damage(9999999)

                        option = hand.select(mouse_x, mouse_y)
                    elif event.button == 3:      # Right click
                        if option not in [-1, -2]:
                            hand.toggle_select(option)
                        else:
                            grid.upgrade_tower(grid_x, grid_y, hand)      # Upgrade tower
                        hand.set_select(-1)
                        option = -1

            hand.set_affordable()

            projectiles.add_projectiles(grid.draw(screen, dt, grid.get_objects(), bug_manager.get_bugs(), hand))

            # Towers shoot
            for bug_pos in bug_manager.get_bugs_pos():
                for tower in grid.get_objs_in_row(grid.convert_to_grid_pos(bug_pos[0], bug_pos[1])[0]):
                    if tower.get_name() == "Tower":
                        tower.set_mode(1)

            # Check bullet-bug collision
            projectiles.check_collision(bug_manager.get_bugs(), Level.__WIDTH, Level.__HEIGHT)
            projectiles.remove_projectiles()
            projectiles.draw(screen, dt)

            grid.remove_objects()

            bug_manager.check_collision(grid)

            # Update bugs
            for bug in bug_manager.get_bugs():
                if bug.is_dead():
                    hand.add_energy(80)
                    bug.draw_dead()
                    bug_manager.remove_bug(bug)
                else:
                    bug_projectiles.add_projectiles(bug.draw(screen, dt, bug_manager,grid))
                if bug.get_x() <= -60:
                    row_index = grid.convert_to_grid_pos(bug.get_x(), bug.get_y())[0]
                    if not bulldozers[row_index].active and not bulldozers[row_index].used:
                        bulldozers[row_index].activate()
                    elif bulldozers[row_index].used: 
                        game_over = True

            # Check bullet-tower collision
            bug_projectiles.check_collision(grid.get_objects(), Level.__WIDTH, Level.__HEIGHT)
            bug_projectiles.remove_projectiles()
            bug_projectiles.draw(screen, dt)

            # Draw vfx
            VFXManager.draw(screen, dt)
            hand.draw(screen, dt, mouse_x, mouse_y)

            for bulldozer in bulldozers:
                bulldozer.update(bug_manager)
                bulldozer.draw(screen)

            if game_over:
                pygame.time.delay(2000)
                Level.__draw_game_over(screen)
                pygame.display.flip()
                time.sleep(3)
                running = False

            # Start victory timer if all monsters are dead and there are no more scheduled
            if victory_timer is None and len(self.__monster_schedule) + len(bug_manager.get_bugs()) == 0:
                victory_timer = time.time()

            # Display victory screen after 3 seconds of the last monster's death
            if victory_timer and time.time() - victory_timer >= 3:
                Level.__draw_victory(screen)
                pygame.display.flip()
                time.sleep(3)
                running = False

            # Draws selected tower on mouse pos.
            hand.draw_selected(screen, mouse_x, mouse_y)
            # Draw pause button in the top-right corner
            pause_button.draw(screen, mouse_x, mouse_y)

            # Draw progress bar
            self.__draw_progress_bar(screen, len(self.__monster_schedule) + len(bug_manager.get_bugs()), self.__max_progress)

            # Apply brightness adjustment here
            self.__apply_brightness(screen, brightness)

            for bug in bug_manager.get_bugs():
                pygame.draw.rect(screen, "red", pygame.Rect(bug.get_x() + bug.get_size()*3//5, bug.get_y(), 4, 4))


            pygame.display.flip()

        VFXManager.clear()
        pygame.quit()
        return "main_menu"

    @staticmethod
    def __draw_game_over(screen):
        """
        Draws the game over screen.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
        game_over_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "game_over.png")), (Level.__WIDTH, Level.__HEIGHT))
        screen.blit(game_over_img, (0, 0))

    @staticmethod
    def __draw_victory(screen):
        """
        Draws the victory screen.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
        font = pygame.font.Font(os.path.join("assets", "arcadeclassic.ttf"), 75)
        vip_text = font.render("Vip", True, (255, 0, 0))
        vip_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "victory_img.png")), (Level.__WIDTH, Level.__HEIGHT))
        screen.blit(vip_img, (0, 0))
        screen.blit(vip_text, (Level.__WIDTH // 2 - vip_text.get_width() // 2, Level.__HEIGHT // 2 - vip_text.get_height() // 2))

    @staticmethod
    def __draw_pause_screen(screen, hover_sound, click_sound):
        """
        Draws the pause screen and handles user input for continuing or exiting the game.

        Args:
            screen (pygame.Surface): The game screen to draw on.
            hover_sound (pygame.mixer.Sound): The sound to play when hovering over a button.
            click_sound (pygame.mixer.Sound): The sound to play when clicking a button.

        Returns:
            int: 1 if the game should continue, 0 if the game should exit.
        """
        screen.fill("white")
        center_x = Level.__WIDTH // 2

        continue_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
        continue_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
        exit_button_img = pygame.image.load(os.path.join("assets", "menu", "exit.png"))
        exit_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "exit_choose.png"))

        continue_button = Button(center_x - continue_button_img.get_width() // 2, 300, continue_button_img.get_width(), continue_button_img.get_height(), continue_button_img, continue_button_choose_img, continue_button_img, hover_sound, click_sound)
        exit_button = Button(center_x - exit_button_img.get_width() // 2, 400, exit_button_img.get_width(), exit_button_img.get_height(), exit_button_img, exit_button_choose_img, exit_button_img, hover_sound, click_sound)

        while True:
            screen.fill("white")
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.check_hovering(mouse_x, mouse_y):
                        continue_button.click()
                        return 1
                    elif exit_button.check_hovering(mouse_x, mouse_y):
                        exit_button.click()
                        return 0

            continue_button.draw(screen, mouse_x, mouse_y)
            exit_button.draw(screen, mouse_x, mouse_y)

            pygame.display.flip()

    def __apply_brightness(self, surface, brightness):
        """
        Applies brightness to the surface.

        Args:
            surface (pygame.Surface): The game surface to apply brightness to.
            brightness (float): The brightness level to apply.
        """
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        if brightness > 0:
            # Decrease brightness
            overlay.fill((0, 0, 0, int((1 - brightness) * 255)))

        surface.blit(overlay, (0, 0))

    def __draw_progress_bar(self, screen, current_time, total_time):
        """
        Draws the progress bar.

        Args:
            screen (pygame.Surface): The game screen to draw on.
            current_time (int): The current progress time.
            total_time (int): The total time for the level.
        """
        # Define the size and position of the progress bar
        bar_width = 200
        bar_height = 20
        bar_x = Level.__WIDTH - bar_width - 20
        bar_y = Level.__HEIGHT - bar_height - 20

        # Calculate the progress
        progress = int(((total_time - current_time) / total_time) * bar_width)
        progress = min(progress, bar_width)  # Ensure progress doesn't exceed bar width

        # Draw the white background
        pygame.draw.rect(screen, (255, 255, 255), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))

        # Draw the background of the bar
        pygame.draw.rect(screen, "gray", (bar_x, bar_y, bar_width, bar_height))

        # Draw the progress of the bar
        pygame.draw.rect(screen, "green", (bar_x, bar_y, progress, bar_height))
