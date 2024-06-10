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
    __WIDTH = 1300
    __HEIGHT = 750

    def __init__(self, tower_ids, monster_schedule):
        self.__monster_schedule = monster_schedule
        self.__tower_ids = tower_ids

    def run(self, fps, brightness):
        # initialize_game(1300, 750, FPS)

        pygame.init()
        screen = pygame.display.set_mode((Level.__WIDTH, Level.__HEIGHT))
        pygame.display.set_caption("Towers vs Monsters")

        grid = Grid(Level.__WIDTH, Level.__HEIGHT)
        hand = Hand(50, 5, 80)
        for tid in self.__tower_ids:
            hand.add_card(tid)

        bug_manager = BugManager()
        bulldozers = [Bulldozer(grid, row) for row in range(6)]

        projectiles = ProjectileManager()
        bug_projectiles = ProjectileManager()

        pause_button_img = pygame.image.load(os.path.join("assets", "menu", "Pause.png"))
        pause_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Pause_choose.png"))
        pause_button = Button(Level.__WIDTH - pause_button_img.get_width() - 10, 10, pause_button_img.get_width(), pause_button_img.get_height(), pause_button_img, pause_button_choose_img, pause_button_img)

        clock = pygame.time.Clock()
        dt = 0
        game_over = False
        running = True
        start_time = time.time()

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
                    if pause_button.check_hovering(mouse_x, mouse_y):
                        pause_button.click()
                        option = Level.__draw_pause_screen(screen)
                        if option == 0:
                            running = False
                        else:
                            clock.tick(fps)

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
            projectiles.check_collision(bug_manager.get_bugs(), Level.__WIDTH, Level.__HEIGHT)
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
                Level.__draw_game_over(screen)
                pygame.display.flip()
                time.sleep(3)
                running = False

            # Draws selected tower on mouse pos.
            hand.draw_selected(screen, mouse_x, mouse_y)
            # Draw pause button in the top-right corner
            pause_button.draw(screen, mouse_x, mouse_y)

            # Apply brightness adjustment here
            self.__apply_brightness(screen, brightness)

            pygame.display.flip()

        pygame.quit()
        return "main_menu"

    @staticmethod
    def __draw_game_over(screen):
        font = pygame.font.SysFont(None, 75)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (Level.__WIDTH // 2 - game_over_text.get_width() // 2, Level.__HEIGHT // 2 - game_over_text.get_height() // 2))

    @staticmethod
    def __draw_pause_screen(screen):
        screen.fill("white")
        center_x = Level.__WIDTH // 2

        continue_button_img = pygame.image.load(os.path.join("assets", "menu", "Back.png"))
        continue_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "Back_choose.png"))
        exit_button_img = pygame.image.load(os.path.join("assets", "menu", "exit.png"))
        exit_button_choose_img = pygame.image.load(os.path.join("assets", "menu", "exit_choose.png"))

        continue_button = Button(center_x - continue_button_img.get_width() // 2, 400, continue_button_img.get_width(), continue_button_img.get_height(), continue_button_img, continue_button_choose_img, continue_button_img)
        exit_button = Button(center_x - exit_button_img.get_width() // 2, 500, exit_button_img.get_width(), exit_button_img.get_height(), exit_button_img, exit_button_choose_img, exit_button_img)

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
        """Apply brightness to the surface."""
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        if brightness > 0:
            # Decrease brightness
            overlay.fill((0, 0, 0, int((1 - brightness) * 255)))

        surface.blit(overlay, (0, 0))