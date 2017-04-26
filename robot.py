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
        # Goal(square) for robot
        self.goal = [self.maze_dim / 2 - 1, self.maze_dim / 2]

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
        rotation = 0
        movement = 0
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
            if self.location[0] >= 0 and self.location[0] < self.maze_dim and \
               self.location[1] >= 0 and self.location[1] < self.maze_dim:
                # Up
                if action == 'up':
                    rotation = 0
                    movement = 1
                    self.location[0] += delta[0][0]
                    self.location[1] += delta[0][1]
                # Right
                elif action == 'right':
                    rotation = 90
                    movement = 1
                    self.location[0] += delta[1][0]
                    self.location[1] += delta[1][1]
                # Down
                elif action == 'down':
                    rotation = 0
                    movement = -1
                    self.location[0] += delta[2][0]
                    self.location[1] += delta[2][1]
                # Left
                elif action == 'left':
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

        # Returns tuple (rotation, movement)
        return rotation, movement
