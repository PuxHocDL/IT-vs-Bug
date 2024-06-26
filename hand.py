from card import *
from button import Button

class Hand:
    """
    Class representing the player's hand, which holds cards and manages energy.
    """
    __card_types = {-1: Card, 0: BasicTowerCard, 1: IceTowerCard, 2: FireTowerCard, 3: TheWallCard, 4: TheRookCard, 5: ObeliskCard, 6: HealingTowerCard, 7: TheBombCard, 8: GoldenRookCard}

    def __init__(self, x, y, card_size, starting_energy):
        """
        Initializes the Hand object.

        Parameters:
            x (int): The x-coordinate of the hand's position.
            y (int): The y-coordinate of the hand's position.
            card_size (int): The size of the cards.
            starting_energy (int): The initial amount of energy.
        """
        self.__x = x
        self.__y = y
        self.__energy = starting_energy
        self.__card_size = card_size
        self.__cards = []
        self.__selected = -1
        self.__energy_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "energy.png")), (card_size, card_size))
        self.__shovel_avt = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "Hammer.png")), (card_size, card_size))
        self.__font = pygame.font.Font(os.path.join("assets", "vinque.otf"), 15)

    def add_card(self, card_num):
        """
        Adds a card to the hand.

        Parameters:
            card_num (int): The type number of the card to be added.
        """
        self.__cards.append(Hand.__card_types[card_num](self.__x + (len(self.__cards) + 1) * (self.__card_size + 10), self.__y, size=self.__card_size))

    def draw(self, screen, dt, mouse_x, mouse_y):
        """
        Draws the hand and its components on the screen.

        Parameters:
            screen (pygame.Surface): The surface to draw on.
            dt (float): The time delta for updating animations.
            mouse_x (int): The x-coordinate of the mouse.
            mouse_y (int): The y-coordinate of the mouse.
        """
        self.__shovel = Button(
            self.__x + (len(self.__cards) + 1) * 1.25 * self.__card_size,
            self.__y,
            2 * self.__card_size,
            self.__card_size,
            pygame.image.load(os.path.join("assets", "menu", "Hammer.png")),
            pygame.image.load(os.path.join("assets", "menu", "Hammer_choose.png")),
            pygame.image.load(os.path.join("assets", "menu", "Hammer.png")),
            None,  # No hover sound
            None   # No click sound
        )
        screen.blit(self.__energy_img, (self.__x, self.__y + 0.25 * self.__card_size))

        if self.__energy == 0:
            self.__energy_text = self.__font.render(str(self.__energy), True, "red")
        else:
            self.__energy_text = self.__font.render(str(self.__energy), True, "black")
        self.__energy_rect = self.__energy_text.get_rect()
        screen.blit(self.__energy_text, (self.__x + self.__card_size * 0.5 - self.__energy_rect.w // 2, self.__y + self.__card_size - self.__energy_rect.h // 2))
        for i, card in enumerate(self.__cards):
            card.draw(screen, dt)
        self.__shovel.draw(screen, mouse_x, mouse_y)

    def draw_selected(self, screen, mouse_x, mouse_y):
        """
        Draws the selected card or shovel avatar at the mouse position.

        Parameters:
            screen (pygame.Surface): The surface to draw on.
            mouse_x (int): The x-coordinate of the mouse.
            mouse_y (int): The y-coordinate of the mouse.
        """
        if self.__selected not in [-1, -2]:
            screen.blit(self.__cards[self.__selected].get_img(), (mouse_x - self.__card_size // 2, mouse_y - self.__card_size // 2))
        elif self.__selected == -2:
            screen.blit(self.__shovel_avt, (mouse_x - self.__card_size // 2, mouse_y - self.__card_size // 2))

    def select(self, mouse_x, mouse_y):
        """
        Selects a card or the shovel based on the mouse position.

        Parameters:
            mouse_x (int): The x-coordinate of the mouse.
            mouse_y (int): The y-coordinate of the mouse.

        Returns:
            int: The index of the selected card or -2 if the shovel is selected, -1 otherwise.
        """
        for i, card in enumerate(self.__cards):
            if card.check_input(mouse_x, mouse_y) and card.check_avail():
                if self.is_affordable(card.price):
                    self.toggle_select(i)
                    self.__selected = i
                    return i
        if self.__shovel.check_hovering(mouse_x, mouse_y):
            self.__shovel.click()
            self.__selected = -2
            return -2
        self.__selected = -1
        return -1

    def toggle_select(self, index):
        """
        Toggles the selection state of a card.

        Parameters:
            index (int): The index of the card to be toggled.
        """
        self.__cards[index].toggle_select()

    def add_tower(self, grid, grid_x, grid_y):
        """
        Adds a tower to the grid if a card is selected.

        Parameters:
            grid (Grid): The game grid.
            grid_x (int): The x-coordinate on the grid.
            grid_y (int): The y-coordinate on the grid.
        """
        if self.__selected == -1:
            return
        self.__cards[self.__selected].add_tower(grid, grid_x, grid_y)
        self.__reset_time()
        self.remove_energy(self.__cards[self.__selected].price)

    def add_energy(self, value):
        """
        Adds energy to the hand.

        Parameters:
            value (int): The amount of energy to be added.
        """
        self.__energy += value

    def set_select(self, index):
        """
        Sets the selected card index.

        Parameters:
            index (int): The index of the selected card.
        """
        self.__selected = index

    def remove_energy(self, value):
        """
        Removes energy from the hand.

        Parameters:
            value (int): The amount of energy to be removed.
        """
        self.__energy -= value

    def is_affordable(self, value):
        """
        Checks if the current energy is sufficient to afford the given value.

        Parameters:
            value (int): The value to be checked.

        Returns:
            bool: True if the current energy is sufficient, False otherwise.
        """
        return self.__energy >= value

    def __reset_time(self):
        """
        Resets the cooldown time of the selected card.
        """
        self.__cards[self.__selected].reset_time()

    def set_affordable(self):
        """
        Sets the affordability state of all cards based on the current energy.
        """
        for card in self.__cards:
            card.set_affordable(self.__energy)
