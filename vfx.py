import pygame
class VFX:
    def __init__(self, x, y, shape, duration, img_path):
        self._x = x
        self._y = y
        self._shape = shape
        self._duration = duration
        self._img_path = img_path
        self._current_time = 0
        self._img_index = 0

    def draw(self, screen, dt):
        img = pygame.transform.scale(pygame.image.load(self._img_path[self._img_index]), self._shape)
        screen.blit(img, (self._x, self._y))
        if self._current_time >= 1/len(self._img_path)*self._duration:
            self._img_index += 1
            self._current_time = 0
        self._current_time += dt
        if self._img_index == len(self._img_path):
            return True
        return False
