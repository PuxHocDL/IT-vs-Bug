class Button():
    """ Class for the Button object.
    """
    def __init__(self, x, y, size_x, size_y, base_img, hovering_img, click_img):
        """
        Initializes the Button object.

        Parameters:
            pos (tuple): the (x, y) position on which the Button is drawn.
            __text_input (string): the __text of the Button.
            __font (pygame.Font): the __font of __text_input.
            base_color (tuple): RGB color code for the __text when the Button is not hovered.
            hovering_color (tuple): RGB color code for the __text when the Button is hovered.
        """
        self.__x = x
        self.__y = y
        self.__size_x = size_x
        self.__size_y = size_y
        self.__img_atlas = {0: base_img, 1: hovering_img, 2: click_img}
        self.__img_index = 0

    def draw(self, screen, mouse_x, mouse_y):
        """
        Draws the Button to the screen.

        Parameters:
            screen (pygame.Surface): the Surface on which the Button is drawn.
        """
        screen.blit(self.__img_atlas[self.__img_index], (self.__x, self.__y))
        self.check_hovering(mouse_x, mouse_y)

    def check_hovering(self, mouse_x, mouse_y):
        """
        Returns True if the mouse position is in the button box.

        Parameters:
            position (tuple): (x, y) position of the mouse.
        """
        if self.__x < mouse_x < self.__x+self.__size_x and self.__y < mouse_y < self.__y+self.__size_y:
            self.__img_index = 1
            return True
        self.__img_index = 0
        return False

    def click(self):
        self.__img_index = 2
