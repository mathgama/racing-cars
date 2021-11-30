from collections import deque
from game import Game

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)

    def get_state(self, game):
        state = [
            game.car.actual_speed,
            game.car.angle,
            game.car.r_sensor,
            game.car.fr_sensor,
            game.car.f_sensor,
            game.car.fl_sensor,
            game.car.l_sensor,
        ]

        return state

    def remember(self, state, action, reward, next_state, game_over):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, game_over):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_avg_scores = []
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
                
            print('Game:', agent.n_games)
            print('Score:', score)
            print('Record:', best_score)

train()