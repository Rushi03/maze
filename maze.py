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
                walls.append(map(int,line.split(',')))
            self.walls = np.array(walls)

        # Perform validation on maze
        # Maze dimensions
        if self.dim % 2:
            raise Exception('Maze dimensions must be even in length!')
        if self.walls.shape != (self.dim, self.dim):
            raise Exception('Maze shape does not match dimension attribute!')

        # Wall permeability
        wall_errors = []
        # vertical walls
        for x in range(self.dim-1):
            for y in range(self.dim):
                if (self.walls[x, y] & 2 != 0) != (self.walls[x+1,y] & 8 != 0):
                    wall_errors.append([(x, y), 'v'])
        # horizontal walls
        for y in range(self.dim-1):
            for x in range(self.dim):
                if (self.walls[x, y] & 1 != 0) != (self.walls[x,y+1] & 4 != 0):
                    wall_errors.append([(x,y), 'h'])

        if wall_errors:
            for cell, wall_type in wall_errors:
                if wall_type == 'v':
                    cell2 = (cell[0]+1, cell[1])
                    print "Inconsistent vertical wall betweeen {} and {}".format(cell, cell2)
                else:
                    cell2 = (cell[0], cell[1]+1)
                    print "Inconsistent horizontal wall betweeen {} and {}".format(cell, cell2)
            raise Exception("Consistency errors found in wall specifications!")

    def is_permissible(self, cell, direction):
        """
        Returns a boolean designating whether or not a cell is passable in the
        given direction. Cell is input as a list. Directions may be
        input as single letter 'u', 'r', 'd', 'l', or complete words 'up',
        'right', 'down', 'left'.
        """
        dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8,
                   'up': 1, 'right': 2, 'down': 4, 'left': 8}
        try:
            return (self.walls[tuple(cell)] & dir_int[direction] != 0)
        except:
            print "Invalid direction provided!"

    def dist_to_wall(self, cell, direction):
        """
        Returns a number designating the number of open cells to the nearest
        wall in the indicated direction. Cell is input as a list. Directions
        may be input as a single letter 'u', 'r', 'd', 'l', or complete words
        'up', 'right', 'down', 'left'.
        """
        dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}

        sensing = True
        distance = 0
        curr_cell = list(cell)  # Make copy to preserve original
        while sensing:
            if self.is_permissible(curr_cell, direction):
                distance += 1
                curr_cell[0] += dir_move[direction][0]
                curr_cell[1] += dir_move[direction][1]
            else:
                sensing = False
        return distance

    def move(self, heading, location, action, rotate, movement):
        # Goal set for robot to reach
        self.goal = (self.dim / 2 - 1, self.dim / 2)

        # Direction moves for the robot
        delta = {'up': [0, -1], 'right': [1, 0], 'down': [0, 1], 'left': [-1, 0]}
        # Robot direction sensing
        sensor_direction = {'up': ['left', 'up', 'right'], 'right': ['up', 'right', 'left'],
                            'down': ['right', 'down', 'left'], 'left': ['down', 'left', 'up']}
        # Going down
        reverse = {'up': 'down', 'right': 'left', 'down': 'up', 'left': 'right'}

        # Sense distance to the wall
        sensing = [self.dist_to_wall(location, heading)
                   for heading in sensor_direction[heading]]

        if rotate == -90:
            heading = sensor_direction[heading][0]
        elif rotate == 90:
            heading = sensor_direction[heading][2]
        elif rotate == 0:
            pass
        else:
            print "Invalid rotation value."

        # self.bounds = [1, 2, self.dim, self.dim + 1]
        # location[0] = (location[0] + delta[heading][0] - self.bounds[0]) % (self.bounds[2] - self.bounds[0] + 1) + self.bounds[0]
        # location[1] = (location[1] + delta[heading][1] - self.bounds[1]) % (self.bounds[3] - self.bounds[1] + 1) + self.bounds[1]
        # location[0] = (location[0] + delta[reverse][0] - self.bounds[0]) % (self.bounds[2] - self.bounds[0] + 1) + self.bounds[0]
        # location[1] = (location[1] + delta[reverse][1] - self.bounds[1]) % (self.bounds[3] - self.bounds[1] + 1) + self.bounds[1]

        if abs(movement) > 3:
            print "Only can move 3 squares per turn."
        movement = max(min(int(movement), 3), -3)  # Range [-3, 3]
        while movement:
            if movement > 0:
                if self.is_permissible(location, heading):
                    location[0] = (location[0] + delta[heading][0]) % self.dim
                    location[1] = (location[1] + delta[heading][1]) % self.dim
                    movement -= 1
                else:
                    "Ran into wall. Movement stopped."
                    movement = 0
            else:
                reverse = reverse[heading]
                if self.is_permissible(location, heading):
                    location[0] = (location[0] + delta[reverse][0]) % self.dim
                    location[1] = (location[1] + delta[reverse][1]) % self.dim
                    movement += 1
                else:
                    "Ran into wall. Movement stopped."
                    movement = 0

        # self.reward starts between -1 and 1; [-1, 1]
        self.reward = 2 * random.random() - 1

        if action == 'up':
            self.reward += -0.25
        elif action == 'right':
            self.reward += -0.5
        elif action == 'down':
            self.reward += -1.5
        elif action == 'left':
            self.reward += -1.25
        else:
            self.reward += -2

        print location
        # self.reward for reaching the goal
        if location[0] in self.goal and location[1] in self.goal:
            self.reward += 10
            location[0] = 0
            location[1] = self.dim - 1
        return self.reward
