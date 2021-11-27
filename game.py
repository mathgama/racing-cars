import pygame
import time
import numpy as np
from utils import scale_image
from car import Car

pygame.init()

#GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.2)
#TRACK = pygame.image.load("imgs/track.png")
#TRACK_BORDER = pygame.image.load("imgs/track-border.png")
#TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
#FINISH = pygame.image.load("imgs/finish.png")
#CAR_STARTING_POS = (190, 220)
#WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Racing Cars")
#FPS = 60

#FONT = pygame.font.Font(pygame.font.get_default_font(), 1)

#WAVEFRONT_SURFACE = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
#WAVEFRONT_DISTANCE = np.zeros((WIDTH, HEIGHT), int)

class Game:
    GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.2)
    TRACK = pygame.image.load("imgs/track.png")
    TRACK_BORDER = pygame.image.load("imgs/track-border.png")
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
    FINISH = pygame.image.load("imgs/finish.png")

    CAR_STARTING_POS = (190, 220)
    FPS = 60

    FONT = pygame.font.Font(pygame.font.get_default_font(), 1)

    def __init__(self):
        self.width = self.TRACK.get_width()
        self.height = self.TRACK.get_height()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Racing Cars")

        self.wavefront_distance = np.zeros((self.width, self.height), int)
        self.wavefront_propagation((190, 220, 0))

        self.reset()

    def reset(self):
        self.car = Car(starting_pos=self.CAR_STARTING_POS)

    def draw(self):
        images = [
            (self.GRASS, (0, 0)),
            (self.TRACK, (0, 0)),
            (self.FINISH, (145, 270)),
            (self.TRACK_BORDER, (0, 0)),
            #(WAVEFRONT_SURFACE, (0, 0)),
        ]

        for img, pos in images:
            self.display.blit(img, pos)

        self.car.draw(self.display)
        pygame.display.update()

    def add_to_propagation_list(self, coord, coords_to_be_checked):
        i, j, score = coord

        if self.wavefront_distance[i][j] == 0:
            coords_to_be_checked.insert(0, coord)

    def wavefront_propagation(self, initial_pos):
        coords_to_be_checked = [initial_pos]

        while len(coords_to_be_checked) > 0:
            i, j, score = coords_to_be_checked.pop()

            if self.wavefront_distance[i][j] != 0:
                continue

            r, g, b, a = self.TRACK_BORDER.get_at((int(i), int(j)))

            if a != 0: # obstacle
                continue

            self.wavefront_distance[i][j] = score

            #score_render = FONT.render(str(score), True, (0, 255, 0))
            #WAVEFRONT_SURFACE.blit(score_render, (i, j))

            self.add_to_propagation_list((i+1, j, score + 1), coords_to_be_checked)
            self.add_to_propagation_list((i, j+1, score + 1), coords_to_be_checked)
            self.add_to_propagation_list((i-1, j, score + 1), coords_to_be_checked)
            self.add_to_propagation_list((i, j-1, score + 1), coords_to_be_checked)


""" def add_to_propagation_list(coord, coords_to_be_checked):
    i, j, score = coord

    if WAVEFRONT_DISTANCE[i][j] == 0:
        coords_to_be_checked.insert(0, coord)

def wavefront_propagation(initial_pos):
    coords_to_be_checked = [initial_pos]

    while len(coords_to_be_checked) > 0:
        i, j, score = coords_to_be_checked.pop()

        if WAVEFRONT_DISTANCE[i][j] != 0:
            continue

        r, g, b, a = TRACK_BORDER.get_at((int(i), int(j)))

        if a != 0: # obstacle
            continue

        WAVEFRONT_DISTANCE[i][j] = score

        #score_render = FONT.render(str(score), True, (0, 255, 0))
        #WAVEFRONT_SURFACE.blit(score_render, (i, j))

        add_to_propagation_list((i+1, j, score + 1), coords_to_be_checked)
        add_to_propagation_list((i, j+1, score + 1), coords_to_be_checked)
        add_to_propagation_list((i-1, j, score + 1), coords_to_be_checked)
        add_to_propagation_list((i, j-1, score + 1), coords_to_be_checked)

    #wavefront_propagation()

def draw(win, images, car):
    for img, pos in images:
        win.blit(img, pos)

    car.draw(win)
    pygame.display.update() """


def main():
    clock = pygame.time.Clock()
    running = True

    """ images = [
        (GRASS, (0, 0)),
        (TRACK, (0, 0)),
        (FINISH, (145, 270)),
        (TRACK_BORDER, (0, 0)),
        #(WAVEFRONT_SURFACE, (0, 0)),
    ]

    wavefront_propagation((190, 220, 0))

    car = Car(starting_pos=CAR_STARTING_POS) """
    
    while running:
        clock.tick(FPS)

        draw(WIN, images, car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        accelerating = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            car.turn(left=True)
        if keys[pygame.K_d]:
            car.turn(right=True)
        if keys[pygame.K_w]:
            car.accelerate()
            accelerating = True

        if not accelerating:
            car.decelerate()

        if car.collide(TRACK_BORDER_MASK) == True:
            car.crash()
            car = Car(starting_pos=CAR_STARTING_POS)

        score = WAVEFRONT_DISTANCE[int(car.x)][int(car.y)]
        #print(score)


    pygame.quit()


main()