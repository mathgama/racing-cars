import pygame
import time
from utils import scale_image
from car import Car

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.2)
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("imgs/finish.png")
CAR_STARTING_POS = (190, 220)

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

    car = Car(starting_pos=CAR_STARTING_POS)
    
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


    pygame.quit()


main()