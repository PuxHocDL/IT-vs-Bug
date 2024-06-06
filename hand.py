from card import *


class Hand:
    __card_types = {-1: Card, 0: BasicTowerCard, 1: IceTowerCard}
    def __init__(self, x, y, card_size):
        self.__x = x
        self.__y = y
        self.__card_size = card_size
        self.__cards = []
        self.__selected = -1
        self.add_card(0)
        self.add_card(1)

    def add_card(self, card_num):
        self.__cards.append(Hand.__card_types[card_num](self.__x + len(self.__cards)*(self.__card_size+20), self.__y, size=self.__card_size))

    def draw(self, screen, dt):
        for i, card in enumerate(self.__cards):
            card.draw(screen, dt)

    def draw_selected(self, screen, mouse_x, mouse_y):
        if self.__selected != -1:
            screen.blit(self.__cards[self.__selected].get_img(), (mouse_x-self.__card_size//2, mouse_y-self.__card_size//2))

    def select(self, mouse_x, mouse_y):
        for i, card in enumerate(self.__cards):
            if card.check_input(mouse_x, mouse_y) and card.check_avail():
                card.toggle_select()
                self.__selected = i
                return i
        self.__selected = -1
        return -1

    def toggle_select(self, index):
        self.__cards[index].toggle_select()

    def reset_time(self, index):
        self.__cards[index].reset_time()

    def add_tower(self, grid, grid_x, grid_y):
        if self.__selected == -1:
            return
        self.__cards[self.__selected].add_tower(grid, grid_x, grid_y)
