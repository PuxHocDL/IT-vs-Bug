from card import *
from button import Button


class Hand:
    __card_types = {-1: Card, 0: BasicTowerCard, 1: IceTowerCard, 2: FireTowerCard, 3: TheWallCard, 4: TheRookCard}
    def __init__(self, x, y, card_size):
        self.__x = x
        self.__y = y
        self.__energy = 10000
        self.__card_size = card_size
        self.__cards = []
        self.__selected = -1
        self.add_card(0)
        self.add_card(1)
        self.add_card(2)
        self.add_card(3)
        self.add_card(4)
        self.__energy_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "energy.png")), (card_size, card_size))
        
        self.__shovel = Button(self.__x + (len(self.__cards)+1)*1.25*self.__card_size, self.__y, 2*self.__card_size, self.__card_size, pygame.image.load(os.path.join("assets", "menu", "Hammer.png")), pygame.image.load(os.path.join("assets", "menu", "Hammer_choose.png")), pygame.image.load(os.path.join("assets", "menu", "Hammer.png")))
        self.__shovel_avt = pygame.transform.scale(pygame.image.load(os.path.join("assets", "UI", "Avatar", "Hammer.png")), (card_size, card_size))

        self.__font = pygame.font.Font(os.path.join("assets", "vinque.otf"), 15)

    def add_card(self, card_num):
        self.__cards.append(Hand.__card_types[card_num](self.__x + (len(self.__cards)+1)*(self.__card_size+10), self.__y, size=self.__card_size))

    def draw(self, screen, dt, mouse_x, mouse_y):
        screen.blit(self.__energy_img, (self.__x, self.__y+0.25*self.__card_size))

        if self.__energy == 0:
            self.__energy_text = self.__font.render(str(self.__energy), True, "red")
        else:
            self.__energy_text = self.__font.render(str(self.__energy), True, "black")
        self.__energy_rect = self.__energy_text.get_rect()
        screen.blit(self.__energy_text, (self.__x+self.__card_size*0.5-self.__energy_rect.w//2, self.__y+self.__card_size-self.__energy_rect.h//2))
        for i, card in enumerate(self.__cards):
            card.draw(screen, dt)
        self.__shovel.draw(screen, mouse_x, mouse_y)

    def draw_selected(self, screen, mouse_x, mouse_y):
        if self.__selected not in [-1, -2]:
            screen.blit(self.__cards[self.__selected].get_img(), (mouse_x-self.__card_size//2, mouse_y-self.__card_size//2))
        elif self.__selected == -2:
            screen.blit(self.__shovel_avt, (mouse_x-self.__card_size//2, mouse_y-self.__card_size//2))

    def select(self, mouse_x, mouse_y):
        for i, card in enumerate(self.__cards):
            if card.check_input(mouse_x, mouse_y) and card.check_avail():
                if self.__is_affordable(Hand.__card_types[i].price):
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
        self.__cards[index].toggle_select()

    def add_tower(self, grid, grid_x, grid_y):
        if self.__selected == -1:
            return
        self.__cards[self.__selected].add_tower(grid, grid_x, grid_y)
        self.__reset_time()
        self.__remove_energy()
        self.__set_affordable()

    def add_energy(self, value):
        self.__energy += value

    def __remove_energy(self):
        self.__energy -= Hand.__card_types[self.__selected].price

    def __is_affordable(self, value):
        return self.__energy >= value

    def __reset_time(self):
        self.__cards[self.__selected].reset_time()

    def __set_affordable(self):
        for card in self.__cards:
            card.set_affordable(self.__energy)
