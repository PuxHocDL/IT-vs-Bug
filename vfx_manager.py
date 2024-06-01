class VFXManager:
    class __VFX:
        def __init__(self, x, y, duration, imgs):
            self.__x = x
            self.__y = y
            self.__duration = duration
            self.__imgs = imgs
            self.__current_time = 0
            self.__img_index = 0

        def draw(self, screen, dt):
            screen.blit(self.__imgs[self.__img_index], (self.__x, self.__y))
            if self.__current_time >= 1/len(self.__imgs)*self.__duration:
                self.__img_index += 1
                self.__current_time = 0
            self.__current_time += dt
            if self.__img_index == len(self.__imgs):
                return True
            return False

    __vfx = []

    @staticmethod
    def add_vfx(x, y, duration, imgs):
        VFXManager.__vfx.append(VFXManager.__VFX(x, y, duration, imgs))

    @staticmethod
    def draw(screen, dt):
        for vfx in VFXManager.__vfx:
            if vfx.draw(screen, dt):
                VFXManager.__vfx.remove(vfx)
