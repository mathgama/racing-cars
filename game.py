import pygame
import time
import math
from utils import scale_image
from car import Car

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.2)
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
FINISH = pygame.image.load("imgs/finish.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Cars")

def draw(win, images):
    for img, pos in images:
        win.blit(img, pos)

def main():
    running = True

    images = [
        (GRASS, (0, 0)),
        (TRACK, (0, 0))
    ]

    draw(WIN, images)
    pygame.display.update()

    car = Car(1, 10, 1, (190, 220))
    car.draw(WIN)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


main()