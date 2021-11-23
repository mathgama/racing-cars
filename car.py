import pygame
import math
from utils import scale_image, blit_rotate_center

CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.5)

class Car:
    def __init__(self, accel_rate, max_speed, rotation_rate, starting_pos):
        self.accel_rate = accel_rate
        self.max_speed = max_speed
        self.actual_speed = 0
        self.rotation_rate = rotation_rate
        self.angle = 0
        self.x, self.y = starting_pos

    def move_forward(self):
        self.actual_speed = min(self.actual_speed + self.accel_rate, self.max_speed)
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
        blit_rotate_center(win, CAR, (self.x, self.y), self.angle)
        #win.blit(CAR, (self.x, self.y))

    