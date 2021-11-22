import pygame
from utils import scale_image

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
        self.actual_speed += self.accel_rate

    def brake(self):
        self.actual_speed -= self.accel_rate * 2

    def turn(self, left=False, right=False):
        if left:
            self.angle += self.rotation_rate
        elif right:
            self.angle -= self.rotation_rate

    def draw(self, win):
        win.blit(CAR, (self.x, self.y))
        pygame.display.update()