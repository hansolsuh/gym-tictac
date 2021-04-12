import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class TicTacEnv(gym.Env):
    metadata = {'render.modes': ['human']}


    def __init__(self):
        self.state = np.zeros(shape=(3,3),dtype=np.int8)
        self.counter = 0
        self.done = 0
        self.add = [0, 0]
        self.reward = 0
        self.action_space = spaces.Discrete(9)

    def check(self):
        if(self.counter<5):
            return 0

        ld = np.diag(self.state)
        rd = np.diag(np.fliplr(self.state))

        #TODO
        three_o1 = np.count_nonzero(self.state[:,0] == 1)
        three_o2 = np.count_nonzero(self.state[:,1] == 1)
        three_o3 = np.count_nonzero(self.state[:,2] == 1)
        three_o4 = np.count_nonzero(self.state[0,:] == 1)
        three_o5 = np.count_nonzero(self.state[1,:] == 1)
        three_o6 = np.count_nonzero(self.state[2,:] == 1)
        three_o7 = np.count_nonzero(ld == 1)
        three_o8 = np.count_nonzero(rd == 1)
        three_c1 = np.count_nonzero(self.state[:,0] == 2)
        three_c2 = np.count_nonzero(self.state[:,1] == 2)
        three_c3 = np.count_nonzero(self.state[:,2] == 2)
        three_c4 = np.count_nonzero(self.state[0,:] == 2)
        three_c5 = np.count_nonzero(self.state[1,:] == 2)
        three_c6 = np.count_nonzero(self.state[2,:] == 2)
        three_c7 = np.count_nonzero(ld == 2)
        three_c8 = np.count_nonzero(rd == 2)

        circle = np.array([three_o1,three_o2,three_o3,three_o4,three_o5,three_o6,three_o7,three_o8])
        cross  = np.array([three_c1,three_c2,three_c3,three_c4,three_c5,three_c6,three_c7,three_c8])
        total_arr = np.array([three_o1,three_o2,three_o3,three_o4,three_o5,three_o6,three_o7,three_o8,
                              three_c1,three_c2,three_c3,three_c4,three_c5,three_c6,three_c7,three_c8])

        if (np.count_nonzero(total_arr == 3) > 1):
            raise ValueError("Both O and X one... Logic Error")

        if (np.count_nonzero(circle == 3) > 0):
            return 1
        if (np.count_nonzero(cross == 3) > 0):
            return 2 #TODO 2 or -1?


    def step(self, target):
        if self.done == 1:
            print("Game Over")
            return [self.state, self.reward, self.done, self.add]
        elif self.state[int(target/3)][target%3] != 0:
            print("Invalid Step")
            return [self.state, self.reward, self.done, self.add]
        else:
            if(self.counter%2 == 0):
                self.state[int(target/3)][target%3] = 1
            else:
                self.state[int(target/3)][target%3] = 2 
            self.counter += 1
            if(self.counter == 9):
                self.done = 1;
        win = self.check()
        if(win):
            self.done = 1;
            print("Player ", win, " wins.", sep = "", end = "\n")
            self.add[win-1] = 1;
            if win == 1:
                self.reward = 100
            else:
                self.reward = -100
        return [self.state, self.reward, self.done, {"add:" : self.add}] #"info not getting used.. whatever is fine?

    def reset(self):
        for i in range(3):
            for j in range(3):
                self.state[i][j] = 0
        self.counter = 0
        self.done = 0
        self.add = [0, 0]
        self.reward = 0
        return self.state

    def render(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    print('-', end = " ")
                elif self.state[i][j] == 1:
                    print('O', end = " ")
                else:
                    print('X', end = " ")
            print("")
        print("-----------------------")        

