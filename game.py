import pygame
import time
from utils import scale_image
from car import Car

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.2)
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
FINISH = pygame.image.load("imgs/finish.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Cars")

FPS = 60

def draw(win, images, car):
    for img, pos in images:
        win.blit(img, pos)

    car.draw(win)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    running = True

    images = [
        (GRASS, (0, 0)),
        (TRACK, (0, 0))
    ]

    car = Car(accel_rate=0.5, 
              max_speed=4, 
              rotation_rate=4, 
              starting_pos=(190, 220))
    
    while running:
        clock.tick(FPS)

        draw(WIN, images, car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            car.turn(left=True)
        if keys[pygame.K_d]:
            car.turn(right=True)
        if keys[pygame.K_w]:
            car.move_forward()


    pygame.quit()


main()