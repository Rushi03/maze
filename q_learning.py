import random
import sys



class QLearning(object):
    def __init__(self):
        self.Q = dict()        # Q-table
        self.epsilon = 0.95    # Exploration factor
        self.alpha = 1        # Learning factor
        self.actions = ['up', 'right', 'down', 'left']  # Available acitons
        self.discount = 0
        self.t = 0

    def build_state(self, sense):
        state = (sense)
        return state

    def get_maxQ(self, state):
        # Get the max Q value
        maxQ = max(list(self.Q[state].values()))
        return maxQ

    def create_Q(self, state):
        if state not in self.Q:
                # Create new state key, value new dictionary
                self.Q[state] = {}
                for action in self.actions:
                    # Intialize the actions value to 0.0
                    self.Q[state][action] = 0.0
        return

    def choose_action(self, state):
        self.state = state
        action = None

        # 0 < a < 1
        a = 0.85
        self.epsilon = pow(a, self.t)
        self.t += 1

        # Probability 1 - epsilon
        if self.epsilon > random.random():
            action = random.choice(self.actions)
        else:
            # Get the max value of Q for the current state
            max_Q_value = self.get_maxQ(state)
            # Get the list of actions correlated to max Q
            max_Q_actions = [Q_value for Q_value in self.Q[state].keys() if
                             self.Q[state][Q_value] == max_Q_value]
            # Make the action a random choice of actions for the max Q
            action = random.choice(max_Q_actions)
        return action

    def learn(self, state, action, reward):
        max_Q = self.get_maxQ(state)
        old_Qsa = self.Q[state][action]
        self.Q[state][action] = (old_Qsa * (1 - self.alpha) + self.alpha *
                                 (reward + self.discount * max_Q))
        return

    '''def update(self, sense):
        state = self.build_state(sense)      # Get current state
        self.create_Q(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)   # Choose an action
        self.learn(state, action, reward)    # Q-learn
        return'''
