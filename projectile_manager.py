from projectile import *

class ProjectileManager:
    def __init__(self):
        self.__projectiles = []
        self.__bullet_name = {"Bullet": Bullet, "IceBullet": IceBullet, "FireBullet": FireBullet, "IceFireBullet": IceFireBullet}

    def add_projectile(self, x, y, angle, name):
        self.__projectiles.append(self.__bullet_name[name](x, y, angle))

    def get_projectiles(self):
        return self.__projectiles

    def remove_projectile(self, screen, proj):
        proj.draw_destroy(screen)
        self.__projectiles.remove(proj)

    def draw(self, screen):
        for projectile in self.__projectiles:
            projectile.draw(screen)
