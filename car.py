import pygame
import math
from utils import scale_image, rotate_center

CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.5)

class Car:
    def __init__(self, accel_rate, max_speed, rotation_rate, starting_pos):
        self.accel_rate = accel_rate
        self.max_speed = max_speed
        self.actual_speed = 0
        self.rotation_rate = rotation_rate
        self.angle = 0
        self.x, self.y = starting_pos

    def accelerate(self):
        self.actual_speed = min(self.actual_speed + self.accel_rate, self.max_speed)
        self.move()

    def decelerate(self):
        self.actual_speed = max(self.actual_speed - self.accel_rate / 2, 0)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        horizontal = math.sin(radians) * self.actual_speed
        vertical = math.cos(radians) * self.actual_speed

        self.x -= horizontal
        self.y -= vertical

    def turn(self, left=False, right=False):
        if left:
            self.angle += self.rotation_rate
        elif right:
            self.angle -= self.rotation_rate

    def draw(self, win):
        rotated_image, rect = rotate_center(CAR, (self.x, self.y), self.angle)
        win.blit(rotated_image, rect.topleft)

    def collide(self, mask, x=0, y=0):
        rotated_image, rect = rotate_center(CAR, (self.x, self.y), self.angle)
        car_mask = pygame.mask.from_surface(rotated_image)
        offset = (int(rect.x - x), int(rect.y - y))
        return True if mask.overlap(car_mask, offset) else False

    def crash(self):
        self.actual_speed = 0
        self.accel_rate = 0
        self.max_speed = 0
        self.rotation_rate = 0