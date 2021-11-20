import pygame
import time
import math

GRASS = pygame.image.load("imgs/grass.jpg")
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
FINISH = pygame.image.load("imgs/finish.png")
CAR = pygame.image.load("imgs/red-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Cars")

def main():
    running = True

    WIN.blit(TRACK, (0, 0))
    pygame.display.update()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


main()