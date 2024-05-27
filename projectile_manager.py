from projectile import *

class ProjectileManager:
    def __init__(self):
        self.__projectiles = []
        self.__remove_projectiles = []

    def add_projectiles(self, projectiles):
        self.__projectiles.extend(projectiles)

    def add_remove_projectile(self, proj):
        self.__remove_projectiles.append(proj)

    def get_projectiles(self):
        return self.__projectiles

    def remove_projectiles(self, screen):
        for p in self.__remove_projectiles:
            p.draw_destroy(screen)
            self.__projectiles.remove(p)
        self.__remove_projectiles = []

    def draw(self, screen):
        for projectile in self.__projectiles:
            projectile.draw(screen)
