import pygame

class VFXManager:
    class __VFX:
        def __init__(self, x, y, shape, duration, img_path):
            self.__x = x
            self.__y = y
            self.__shape = shape
            self.__duration = duration
            self.__img_path = img_path
            self.__current_time = 0
            self.__img_index = 0

        def draw(self, screen, dt):
            img = pygame.transform.scale(pygame.image.load(self.__img_path[self.__img_index]), self.__shape)
            screen.blit(img, (self.__x, self.__y))
            if self.__current_time >= 1/len(self.__img_path)*self.__duration:
                self.__img_index += 1
                self.__current_time = 0
            self.__current_time += dt
            if self.__img_index == len(self.__img_path):
                return True
            return False

    __vfx = []

    @staticmethod
    def add_vfx(x, y, shape, duration, img_path):
        VFXManager.__vfx.append(VFXManager.__VFX(x, y, shape, duration, img_path))

    @staticmethod
    def draw(screen, dt):
        for vfx in VFXManager.__vfx:
            if vfx.draw(screen, dt):
                VFXManager.__vfx.remove(vfx)
