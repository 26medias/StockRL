
from Arena import Arena


class Trainer:
    def __init__(self):
        print("Stock Game Trainer")
        self.train(0, 1000000, save="models/DQN-step-0")
        self.train(1, 1000000, load="models/DQN-step-0", save="models/DQN-step-1")
        self.train(2, 100000000, load="models/DQN-step-1", save="models/DQN-step-2")

    def train(self, rules=0, steps=1000000, load=False, save=False):
        arena = Arena(rules=rules, saveName=save)
        if load is not False:
            arena.load(load)
        arena.train(steps)
        if save is not False:
            arena.save(save)
        #arena.test()

trainer = Trainer()