import pygame
import time
import numpy as np
from utils import scale_image
from car import Car

pygame.init()
clock = pygame.time.Clock()

class Action:
    TURN_LEFT = 0
    TURN_RIGHT = 1
    ACCELERATE = 2
    ACCELERATE_LEFT = 3
    ACCELERATE_RIGHT = 4

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
        self.n_play_step = 0

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

            self.add_to_propagation_list((i+1, j, score + 1), coords_to_be_checked)
            self.add_to_propagation_list((i, j+1, score + 1), coords_to_be_checked)
            self.add_to_propagation_list((i-1, j, score + 1), coords_to_be_checked)
            self.add_to_propagation_list((i, j-1, score + 1), coords_to_be_checked)

    def play_step(self, actions):
        self.n_play_step += 1
        score = self.wavefront_distance[int(self.car.x)][int(self.car.y)]

        #print(self.n_play_step, '/', score)

        accelerating = False
        if actions[Action.TURN_LEFT]:
            self.car.turn(left=True)
        if actions[Action.TURN_RIGHT]:
            self.car.turn(right=True)
        if actions[Action.ACCELERATE]:
            self.car.accelerate()
            accelerating = True
        if actions[Action.ACCELERATE_LEFT]:
            self.car.turn(left=True)
            self.car.accelerate()
            accelerating = True
        if actions[Action.ACCELERATE_RIGHT]:
            self.car.turn(right=True)
            self.car.accelerate()
            accelerating = True

        if not accelerating:
            self.car.decelerate()

        reward = 0
        game_over = False

        if self.car.collide(self.TRACK_BORDER_MASK) == True:
            self.car.crash()
            game_over = True
            reward = -10

        if self.n_play_step > score + 100:
            self.car.crash()
            game_over = True
            reward = -50

        #reward += score / 10

        clock.tick(self.FPS)
        self.draw()

        return reward, game_over, score


def main():
    running = True

    game = Game()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        actions = [0 for i in range(5)]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_w]:
            actions[Action.ACCELERATE_LEFT] = 1
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            actions[Action.ACCELERATE_RIGHT] = 1
        elif keys[pygame.K_a]:
            actions[Action.TURN_LEFT] = 1
        elif keys[pygame.K_d]:
            actions[Action.TURN_RIGHT] = 1
        elif keys[pygame.K_w]:
            actions[Action.ACCELERATE] = 1

        reward, game_over, score = game.play_step(actions)
        #print(score)

        if game_over:
            game.reset()

    pygame.quit()


main()