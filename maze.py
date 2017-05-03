import numpy as np
import random


class Maze(object):
    def __init__(self, filename):
        '''
        Maze objects have two main attributes:
        - dim: mazes should be square, with sides of even length. (integer)
        - walls: passages are coded as a 4-bit number, with a bit value taking
            0 if there is a wall and 1 if there is no wall. The 1s register
            corresponds with a square's top edge, 2s register the right edge,
            4s register the bottom edge, and 8s register the left edge. (numpy
            array)
        The initialization function also performs some consistency checks for
        wall positioning.
        '''
        with open(filename, 'rb') as f_in:

            # First line should be an integer with the maze dimensions
            self.dim = int(f_in.next())

            # Subsequent lines describe the permissability of walls
            walls = []
            for line in f_in:
                walls.append(map(int, line.split(',')))
            self.walls = np.array(walls)

        # Perform validation on maze
        # Maze dimensions
        if self.dim % 2:
            raise Exception("Maze dimensions must be even in length!")
        if self.walls.shape != (self.dim, self.dim):
            raise Exception("Maze shape does not match dimension attribute!")

        # Wall permeability
        wall_errors = []
        # vertical walls
        for x in range(self.dim - 1):
            for y in range(self.dim):
                if (self.walls[x, y] & 2 != 0) != (self.walls[x + 1, y] & 8 != 0):
                    wall_errors.append([(x, y), 'v'])
        # horizontal walls
        for y in range(self.dim - 1):
            for x in range(self.dim):
                if (self.walls[x, y] & 1 != 0) != (self.walls[x, y + 1] & 4 != 0):
                    wall_errors.append([(x, y), 'h'])

        if wall_errors:
            for cell, wall_type in wall_errors:
                if wall_type == 'v':
                    cell2 = (cell[0] + 1, cell[1])
                    print "Inconsistent vertical wall betweeen {} and {}".format(cell, cell2)
                else:
                    cell2 = (cell[0], cell[1] + 1)
                    print "Inconsistent horizontal wall betweeen {} and {}".format(cell, cell2)
            raise Exception("Consistency errors found in wall specifications!")

    def is_permissible(self, cell, direction):
        '''
        Returns a boolean designating whether or not a cell is passable in the
        given direction. Cell is input as a list. Directions may be
        input as single letter 'u', 'r', 'd', 'l', or complete words 'up',
        'right', 'down', 'left'.
        '''
        dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8,
                   'up': 1, 'right': 2, 'down': 4, 'left': 8}
        try:
            return (self.walls[tuple(cell)] & dir_int[direction] != 0)
        except:
            print "Invalid direction provided!"

    def dist_to_wall(self, cell, direction):
        '''
        Returns a number designating the number of open cells to the nearest
        wall in the indicated direction. Cell is input as a list. Directions
        may be input as a single letter 'u', 'r', 'd', 'l', or complete words
        'up', 'right', 'down', 'left'.
        '''
        dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}

        sensing = True
        distance = 0
        # Make copy to preserve original
        curr_cell = list(cell)
        while sensing:
            if self.is_permissible(curr_cell, direction):
                distance += 1
                curr_cell[0] += dir_move[direction][0]
                curr_cell[1] += dir_move[direction][1]
            else:
                sensing = False
        return distance

    def heuristic(self, goal, location):
        '''
        Using the Manhattan distance to determine how far the
        robot is relevant to it's location.
        '''
        # Current x-value from goal
        self.dx = abs(location[0] - goal[0])
        # Current y-value from goal
        self.dy = abs(location[1] - goal[1])
        # Total distance of x and y from goal
        return self.dx + self.dy

    def move(self, goal, location, action):
        '''
        Returns the reward per action taken by the robot. Each action has the same
        reward due having freedom of actions to move freely about the maze. The robot
        will also be rewarded upon how well it changes it location. If it goes in a loop
        or a previous  location is visited then it would receive a negative reward.
        '''
        # Initial reward value
        self.reward = 0.0

        # Manhattan distance from location to goal
        distance = self.heuristic(goal, location)
        # Previous distance; initialized at 0
        previous = 0
        # History of previous locations visited in a list
        history = []

        if location[0] in goal and location[1] in goal:
            self.reward += 10
        else:
            if distance < previous and location not in history:
                self.reward += 0.25
                previous = distance
                history.append(location)
            elif distance == previous or location in history or distance == previous and location \
                in history:
                    self.reward += -0.25
                    previous = distance
                    history.append(location)
            elif distance > previous or distance in history or distance > previous and distance in \
                history:
                    self.reward += -0.25
                    previous = distance
                    history.append(location)
            else:
                self.reward += -0.25
                previous = distance
                history.append(location)

        # Reward for actions taken
        if action == 'up':
            self.reward += 0.25
        elif action == 'right':
            self.reward += 0.25
        elif action == 'down':
            self.reward += 0.25
        elif action == 'left':
            self.reward += 0.25
        else:
            self.reward += -0.25

        return self.reward
