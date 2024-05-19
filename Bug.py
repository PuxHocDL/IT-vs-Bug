import pygame
import random
import math
from config import *

class Bug:
    def __init__(self, x, y, speed, health, max_health, BUG_SIZE, shape):
        self.x = x
        self.y = y
        self.speed = speed
        self.original_speed = speed  # Lưu trữ tốc độ ban đầu
        self.health = health
        self.max_health = max_health
        self.slowed = False
        self.slow_timer = 0
        self.BUG_SIZE = BUG_SIZE
        self.shape = shape
        self.angle = 0 
        self.dy = 0

    def draw_BUG(self):
        if self.shape == "rec":
            pygame.draw.rect(screen, mediumaquamarine, (self.x, self.y, self.BUG_SIZE, self.BUG_SIZE))
        elif self.shape == "rec_big":
            pygame.draw.rect(screen, (75,0,130), (self.x, self.y, self.BUG_SIZE, self.BUG_SIZE))
        elif self.shape == "triangle":
            points = [(self.x - self.BUG_SIZE, self.y - self.BUG_SIZE // 2), (self.x, self.y - self.BUG_SIZE), (self.x, self.y)]
            pygame.draw.polygon(screen, (72, 61, 139), points)
        elif self.shape == "hexagon":
            self.draw_hexagon(self.x, self.y, self.BUG_SIZE, self.angle)

    def update(self):
        if self.slowed and pygame.time.get_ticks() > self.slow_timer:
            self.speed = self.original_speed  # Khôi phục tốc độ ban đầu
            self.slowed = False
        self.x -= self.speed

        if self.shape == "hexagon":
            self.angle += 3  # Quái vật xoay
            self.dy = 4 * math.sin(pygame.time.get_ticks() / 300)  # Quái vật nhún lên nhún xuống
            self.y += self.dy

    def apply_slow(self):
        self.speed = self.original_speed * 0.5  # Giảm tốc độ đi 70%
        self.slowed = True
        self.slow_timer = pygame.time.get_ticks() + 10000


    def create_BUG(bugs):
        bug_x = WIDTH
        bug_y = random.randint(100, HEIGHT - 100)
        bugs.append(Bug(bug_x, bug_y, 1, 100, 100, 50, shape="rec"))

    def create_big_BUG(bugs):
        bug_x = WIDTH
        bug_y = random.randint(200, HEIGHT - 200)
        bugs.append(Bug(bug_x, bug_y, 0.75, 300, 300, 100, shape="rec_big"))


    def create_triangle_BUG(bugs):
        bug_x = WIDTH
        bug_y = random.randint(100, HEIGHT - 100)
        bugs.append(Bug(bug_x, bug_y, 2, 70, 70, 60, shape="triangle"))


    def create_hexagon_BUG(bugs):
        bug_x = WIDTH
        bug_y = random.randint(100, HEIGHT - 100)
        bugs.append(Bug(bug_x, bug_y, 0.5, 400, 400, 80, shape="hexagon"))


    def draw_BUG(x, y, bug):
        if bug.shape == "rec":
            pygame.draw.rect(screen, mediumaquamarine, (x, y, bug.BUG_SIZE, bug.BUG_SIZE))
        elif bug.shape == "rec_big":
            pygame.draw.rect(screen, (75, 0, 130), (x, y, bug.BUG_SIZE, bug.BUG_SIZE))
        elif bug.shape == "triangle":
            points = [(x - bug.BUG_SIZE, y - bug.BUG_SIZE // 2), (x, y - bug.BUG_SIZE), (x, y)]
            pygame.draw.polygon(screen, (72, 61, 139), points)
        elif bug.shape == "hexagon":
            bug.draw_hexagon(x, y, bug.BUG_SIZE, bug.angle)

    @staticmethod
    def apply_slow_effect(bugs):
        for bug in bugs:
            bug.apply_slow()
    
    def draw_hexagon(self, x, y, size, angle):
        points = []
        for i in range(6):
            theta = math.radians(angle + i * 60)
            x_i = x + size * math.cos(theta)
            y_i = y + size * math.sin(theta)
            points.append((x_i, y_i))
        pygame.draw.polygon(screen, (255, 165, 0), points)

    @staticmethod
    def draw_health_bar(x, y, bug):
        if bug.shape in ["rec", "rec_big"]:
            if x > 11:
                health_bar_length = bug.BUG_SIZE
                health_bar_height = 5
                fill = (bug.health / bug.max_health) * health_bar_length
                outline_rect = pygame.Rect(x, y - 10, health_bar_length, health_bar_height)
                fill_rect = pygame.Rect(x, y - 10, fill, health_bar_height)
                pygame.draw.rect(screen, (152, 251, 152), fill_rect)
                pygame.draw.rect(screen, BLACK, outline_rect, 1)
        elif bug.shape == "triangle":
            if x > 11:
                health_bar_length = bug.BUG_SIZE
                health_bar_height = 5
                fill = (bug.health / bug.max_health) * health_bar_length
                outline_rect = pygame.Rect(x - bug.BUG_SIZE, y + bug.BUG_SIZE // 3, health_bar_length, health_bar_height)
                fill_rect = pygame.Rect(x - bug.BUG_SIZE, y + bug.BUG_SIZE // 3, fill, health_bar_height)
                pygame.draw.rect(screen, (152, 251, 152), fill_rect)
                pygame.draw.rect(screen, BLACK, outline_rect, 1)
        elif bug.shape == "hexagon":
            if x > 11:
                health_bar_length = bug.BUG_SIZE
                health_bar_height = 5
                fill = (bug.health / bug.max_health) * health_bar_length
                outline_rect = pygame.Rect(x - bug.BUG_SIZE // 2, y + bug.BUG_SIZE, health_bar_length, health_bar_height)
                fill_rect = pygame.Rect(x - bug.BUG_SIZE // 2, y + bug.BUG_SIZE, fill, health_bar_height)
                pygame.draw.rect(screen, (152, 251, 152), fill_rect)
                pygame.draw.rect(screen, BLACK, outline_rect, 1)

# Khởi tạo bộ đếm thời gian để tạo quái vật mới
Bug.spawn_BUG_event = pygame.USEREVENT + 1
pygame.time.set_timer(Bug.spawn_BUG_event, 2000)  # Tạo quái vật mới mỗi giây

Bug.spawn_big_BUG_event = pygame.USEREVENT + 2
pygame.time.set_timer(Bug.spawn_big_BUG_event, 3000)  # Tạo quái vật lớn mỗi hai giây

Bug.spawn_triangle_BUG_event = pygame.USEREVENT + 3
pygame.time.set_timer(Bug.spawn_triangle_BUG_event, 8000)  # Tạo quái vật tam giác mỗi ba giây

Bug.spawn_hexagon_BUG_event = pygame.USEREVENT + 4
pygame.time.set_timer(Bug.spawn_hexagon_BUG_event, 10000)  # Tạo quái vật lục giác đều mỗi sáu giây
