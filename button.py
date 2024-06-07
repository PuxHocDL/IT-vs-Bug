class Button():
    """ Class for the Button object.
    """
    def __init__(self, pos, text_input, font, base_color, hovering_color, click_color):
        """
        Initializes the Button object.

        Parameters:
            pos (tuple): the (x, y) position on which the Button is drawn.
            __text_input (string): the __text of the Button.
            __font (pygame.Font): the __font of __text_input.
            base_color (tuple): RGB color code for the __text when the Button is not hovered.
            hovering_color (tuple): RGB color code for the __text when the Button is hovered.
        """
        self.__x_pos = pos[0]
        self.__y_pos = pos[1]
        self.__font = font
        self.__base_color, self.__hovering_color, self.__click_color = base_color, hovering_color, click_color
        self.__text_input = text_input
        self.__text = self.__font.render(self.__text_input, True, self.__base_color)
        self.__text_rect = self.__text.get_rect(topleft=(self.__x_pos, self.__y_pos))

    def draw(self, screen):
        """
        Draws the Button to the screen.

        Parameters:
            screen (pygame.Surface): the Surface on which the Button is drawn.
        """
        screen.blit(self.__text, self.__text_rect)

    def check_for_input(self, position):
        """
        Returns True if the mouse position is in the button box.

        Parameters:
            position (tuple): (x, y) position of the mouse.
        """
        if position[0] in range(self.__text_rect.left, self.__text_rect.right) and position[1] in range(self.__text_rect.top, self.__text_rect.bottom):
            return True
        return False

    def change_color(self, position):
        """
        Changes to hovering_color if the mouse position is in the button box, else changes to base_color.

        Parameters:
            position (tuple): (x, y) position of the mouse.
        """
        if position[0] in range(self.__text_rect.left, self.__text_rect.right) and position[1] in range(self.__text_rect.top, self.__text_rect.bottom):
            self.__text = self.__font.render(self.__text_input, True, self.__hovering_color)
        else:
            self.__text = self.__font.render(self.__text_input, True, self.__base_color)

    def click_color(self):
        """
        Changes to click_color.
        """
        self.__text = self.__font.render(self.__text_input, True, self.__click_color)
