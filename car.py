import pygame
import math
from utils import scale_image, rotate_center

CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.5)
TRACK_BORDER = pygame.image.load("imgs/track-border.png")

class Car:
    def __init__(self, starting_pos, accel_rate=0.5, max_speed=4, rotation_rate=3.5):
        self.accel_rate = accel_rate
        self.max_speed = max_speed
        self.actual_speed = 0
        self.rotation_rate = rotation_rate
        self.angle = 0
        self.x, self.y = starting_pos
        self.sensors_update()

    def sensors_update(self):
        radians = math.radians(self.angle + 90)
        self.r_sensor = self.find_obstacle_distance(radians)

        radians = math.radians(self.angle + 135)
        self.fr_sensor = self.find_obstacle_distance(radians)

        radians = math.radians(self.angle + 180)
        self.f_sensor = self.find_obstacle_distance(radians)

        radians = math.radians(self.angle + 225)
        self.fl_sensor = self.find_obstacle_distance(radians)

        radians = math.radians(self.angle + 270)
        self.l_sensor = self.find_obstacle_distance(radians)

        #print('f:', self.front_sensor, 'r:', self.right_sensor, 'l:', self.left_sensor)

    def find_obstacle_distance(self, radians):
        horizontal = math.sin(radians)
        vertical = math.cos(radians)

        obstacle = False

        track_x = self.x
        track_y = self.y

        while obstacle != True:
            track_x += horizontal
            track_y += vertical

            r, g, b, a = TRACK_BORDER.get_at((int(track_x), int(track_y)))

            if a != 0:
                distance = math.sqrt((track_x - self.x)**2 + (track_y - self.y)**2)
                return distance


    def accelerate(self):
        self.actual_speed = min(self.actual_speed + self.accel_rate, self.max_speed)
        self.move()

    def decelerate(self):
        if self.actual_speed == 0:
            return

        self.actual_speed = max(self.actual_speed - self.accel_rate / 2, 0)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        horizontal = math.sin(radians) * self.actual_speed
        vertical = math.cos(radians) * self.actual_speed

        self.x -= horizontal
        self.y -= vertical

        self.sensors_update()

    def turn(self, left=False, right=False):
        if left:
            self.angle += self.rotation_rate
        elif right:
            self.angle -= self.rotation_rate

        self.sensors_update()

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