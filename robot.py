import numpy as np
import random
from q_learning import QLearning


class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        # Starting location; bottom right corner
        self.location = [0, 11]
        # Starts heading up
        self.heading = 'up'
        # Dimensions of the maze
        self.maze_dim = maze_dim
        # Goal(square)
        self.goal = [self.maze_dim / 2 - 1, self.maze_dim / 2]
        # X location
        self.x = 0
        # Y location
        self.y = 0

    def a_star(self):
        '''
        Define the A* search method to fin the optimal path from start to
        goal. Find the heuristic for the maze first in order implement the A*
        method.
        '''

        heuristic = [[0 for row in range(self.maze_dim)] for col in
                     range(self.maze_dim)]

        for i in range(self.maze_dim):
            for j in range(self.maze_dim):
                dX = abs(i - self.goal[0])
                dY = abs(j - self.goal[1])
                heuristic[i][j] = dX + dY

        # Raise an error if heuristic is blank
        if heuristic == []:
            raise ValueError('No heuristic to implement A*')

        # Direction moves for the robot
        delta = [[0, 1],   # Move up
                 [1, 0],   # Move right
                 [0, -1],  # Move down
                 [-1, 0]]  # Move left

        # Direction signs
        delta_sign = ['^', '>', 'v', '<']

        # Check the locations the robot has visited
        checked = [[0 for row in range(self.maze_dim)] for col in
                   range(self.maze_dim)]
        # Number of which move was made
        move = [[0 for row in range(self.maze_dim)] for col in
                range(self.maze_dim)]

        # Starting location checked
        checked[self.x][self.y] = 1

        x = self.x
        y = self.y
        h = heuristic[x][y]
        g = 0
        f = g + h

        open = [[f, g, h, x, y]]

        # Search completed
        reached = False
        # Can't expand upon elements in list
        quit = False
        # Counter
        count = 0
        # Cost of moving
        self.cost = 1

        while not reached and not quit:
            # Check if elements in open list
            if len(open) == 0:
                quit = True
                print 'Unsucessful Search'
            else:
                # Remove node from the list
                open.sort()
                open.reverse()
                next = open.pop()
                x = next[3]
                y = next[4]
                g = next[1]

            # Check if we reached goal
            if x == self.goal[0] and y == self.goal[1]:
                reached = True
                print 'Successful Search'
            else:
                # Expand element and add to open list
                for i in range(len(delta)):
                    x_prime = x + delta[i][0]
                    y_prime = y + delta[i][1]
                    if x_prime >= 0 and x_prime < self.maze_dim and \
                       y_prime >= 0 and y_prime < self.maze_dim:
                        if checked[x_prime][y_prime] == 0:
                            g_prime = g + self.cost
                            h_prime = heuristic[x_prime][y_prime]
                            f_prime = g_prime + h_prime
                            open.append([f_prime, g_prime, h_prime, x_prime,
                                         y_prime])
                            checked[x_prime][y_prime] = 1
                            move[x_prime][y_prime] = i
            count += 1

        policy = [[' ' for row in range(self.maze_dim)] for col in
                  range(self.maze_dim)]
        x = self.goal[0]
        y = self.goal[1]
        policy[x][y] = 'x'

        while x != self.x and y != self.y:
            x_prime = x - delta[move[x][y]][0]
            y_prime = y - delta[move[x][y]][1]
            policy[x_prime][y_prime] = delta_sign[move[x][y]]
            x = x_prime
            y = y_prime

        for i in range(len(policy)):
            print policy[i]

    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''

        # Rotates counterclockwise 90 degrees(-90), no degrees(0),
        # clockwise 90 degrees (90)
        rotation = None  # [-90, 0 , 90]
        # Can move up 3 steps per turn; max 3 forward (3)
        # and max 3 backwards (-3)
        movement = None  # [-3, 3]

        # Actions the robot may be able to take
        actions = ['up', 'right', 'down', 'left']

        # Direction moves for the robot
        delta = [[0, 1],   # Move up
                 [1, 0],   # Move right
                 [0, -1],  # Move down
                 [-1, 0]]  # Move left

        # Make a copy to preserve original [L, F, R]
        view = list(sensors)

        # Implement Q-Learning
        q_learn = QLearning(self.location, self.maze_dim)
        # Build state through sesnsor information
        state = q_learn.build_state(view)
        # Create state in Q-table if not already there
        q_learn.create_Q(state)
        # Take action according to state
        action = q_learn.choose_action(state)

        # Reset when robot reaches the goal
        if self.location[0] in self.goal and self.location[1] in self.goal:
            rotation = 'Reset'
            movement = 'Reset'
            self.location[0] = 0
            self.location[1] = 0
        else:
            # Up
            if action == actions[0]:
                rotation = 0
                movement = 1
                self.location[0] += delta[0][0]
                self.location[1] += delta[0][1]
            # Right
            elif action == actions[1]:
                rotation = 90
                movement = 1
                self.location[0] += delta[1][0]
                self.location[1] += delta[1][1]
            # Down
            elif action == actions[2]:
                rotation = 0
                movement = -1
                self.location[0] += delta[2][0]
                self.location[1] += delta[2][1]
            # Left
            elif action == actions[3]:
                rotation = -90
                movement = 1
                self.location[0] += delta[3][0]
                self.location[1] += delta[3][1]
            else:
                rotation = 0
                movement = 0

        # Apply reward for each action
        reward = q_learn.act(state, action)
        # Learn through the state, action, and reward
        q_learn.learn(state, action, reward)
        # Update the functions with the current state, action, reward
        q_learn.update(view)

        print self.location
        # Returns tuple (rotation, movement)
        return rotation, movement
