class Button():
    """Class for the Button object."""
    def __init__(self, x, y, size_x, size_y, base_img, hovering_img, click_img, hover_sound, click_sound):
        """
        Initializes the Button object.

        Parameters:
            x (int): The x position of the Button.
            y (int): The y position of the Button.
            size_x (int): The width of the Button.
            size_y (int): The height of the Button.
            base_img (pygame.Surface): The base image of the Button.
            hovering_img (pygame.Surface): The image when the Button is hovered.
            click_img (pygame.Surface): The image when the Button is clicked.
            hover_sound (pygame.mixer.Sound): The sound played when hovering over the Button.
            click_sound (pygame.mixer.Sound): The sound played when clicking the Button.
        """
        self.__x = x
        self.__y = y
        self.__size_x = size_x
        self.__size_y = size_y
        self.__img_atlas = {0: base_img, 1: hovering_img, 2: click_img}
        self.__img_index = 0
        self.hover_sound = hover_sound
        self.click_sound = click_sound
        self.hovered = False

    def draw(self, screen, mouse_x, mouse_y):
        """
        Draws the Button to the screen.

        Parameters:
            screen (pygame.Surface): The Surface on which the Button is drawn.
            mouse_x (int): The x position of the mouse.
            mouse_y (int): The y position of the mouse.
        """
        screen.blit(self.__img_atlas[self.__img_index], (self.__x, self.__y))
        self.check_hovering(mouse_x, mouse_y)

    def check_hovering(self, mouse_x, mouse_y):
        """
        Checks if the mouse is hovering over the Button and updates the image index.

        Parameters:
            mouse_x (int): The x position of the mouse.
            mouse_y (int): The y position of the mouse.

        Returns:
            bool: True if the mouse is hovering over the Button, False otherwise.
        """
        if self.__x < mouse_x < self.__x + self.__size_x and self.__y < mouse_y < self.__y + self.__size_y:
            if not self.hovered:
                if self.hover_sound:
                    self.hover_sound.play()
                    self.hovered = True
            self.__img_index = 1
            return True
        self.__img_index = 0
        self.hovered = False
        return False

    def click(self):
        """Plays the click sound and sets the image index to 2 (clicked state)."""
        if self.click_sound:
            self.click_sound.play()
            self.__img_index = 2
