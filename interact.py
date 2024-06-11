class Interact:
    """
    Class providing methods for collision detection and handling interactions between objects.
    """

    @staticmethod
    def check_collision(rect1, rect2):
        """
        Checks for collision between two rectangles and returns the intersection point if they collide.

        Parameters:
            rect1 (pygame.Rect): The first rectangle.
            rect2 (pygame.Rect): The second rectangle.

        Returns:
            tuple: The (x, y) coordinates of the intersection point if collision occurs, None otherwise.
        """
        if rect1.colliderect(rect2):
            intersection = rect1.clip(rect2)
            return (intersection.x, intersection.y)
        else:
            return None

    @staticmethod
    def check_collision_2(rect1, rect2):
        """
        Checks for collision between two rectangles and returns True if they collide and the y-axis difference is within 50 pixels.

        Parameters:
            rect1 (pygame.Rect): The first rectangle.
            rect2 (pygame.Rect): The second rectangle.

        Returns:
            bool: True if the rectangles collide and their y-axis difference is <= 50 pixels, False otherwise.
        """
        if rect1.colliderect(rect2):
            y_difference = abs(rect1.y - rect2.y)
            if y_difference <= 50:
                return True
        return False

    @staticmethod
    def collide_mask(mask1, mask2, pos1, pos2):
        """
        Checks for collision between two masks given their positions.

        Parameters:
            mask1 (pygame.Mask): The first mask.
            mask2 (pygame.Mask): The second mask.
            pos1 (tuple): The (x, y) position of the first mask.
            pos2 (tuple): The (x, y) position of the second mask.

        Returns:
            bool: True if the masks overlap, False otherwise.
        """
        return mask1.overlap(mask2, (pos2[0] - pos1[0], pos2[1] - pos1[1]))
