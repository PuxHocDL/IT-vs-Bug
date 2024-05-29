from projectile import *
from interact import Interact

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

    def remove_projectiles(self):
        for p in self.__remove_projectiles:
            p.draw_destroy()
            self.__projectiles.remove(p)
        self.__remove_projectiles = []

    def draw(self, screen, dt):
        for projectile in self.__projectiles:
            projectile.draw(screen,dt)

    def check_collision(self, objects, width, height):
        for projectile in self.__projectiles:
            proj_rect = projectile.get_rect()
            removed = False
            for obj in objects:
                obj_rect = obj.get_rect()
                collision_coordinates = Interact.check_collision(proj_rect, obj_rect)
                if collision_coordinates and not obj.is_dead():
                    self.add_remove_projectile(projectile)
                    obj.damage(projectile.get_damage())
                    obj.apply_slow(projectile.get_slow(), projectile.get_slow_time())
                    removed = True
                    break

            if projectile.check_border(width, height) and not removed:
                self.add_remove_projectile(projectile)
