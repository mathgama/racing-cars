import torch
import random
from collections import deque
from game import Game
from model import Linear_QNet, QTrainer
from utils import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001
#LEARNING_RATE = 0.1

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.6
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(6, 256, 5)
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma)

    def get_state(self, game):
        state = [
            game.car.actual_speed,
            #game.car.angle,
            game.car.r_sensor,
            game.car.fr_sensor,
            game.car.f_sensor,
            game.car.fl_sensor,
            game.car.l_sensor,
        ]

        return state

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 400 - self.n_games
        action = [0 for i in range(5)]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 4)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        action[move] = 1

        return action


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = Game()

    while True:
        state_old = agent.get_state(game)
        
        action = agent.get_action(state_old)

        reward, game_over, score = game.play_step(action)

        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, action, reward, state_new, game_over)

        agent.remember(state_old, action, reward, state_new, game_over)

        if game_over:
            game.reset()
            agent.train_long_memory()
            agent.n_games += 1

            if score > best_score:
                best_score = score
                agent.model.save()
                
                print('----- New Record -----')
                
            print('Game:', agent.n_games, 'Score:', score, 'Record:', best_score)

            """ plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores) """


train()