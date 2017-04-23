import numpy as np

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        # Starting location; bottom right corner
        self.location = [0, 0]
        # Starts heading up
        self.heading = 'up'
        # Dimensions of the maze
        self.maze_dim = maze_dim
        # Goal
        self.goal = [self.maze_dim / 2, self.maze_dim / 2 + 1]
        # X location
        self.x = self.location[0]
        # Y location
        self.y = self.location[1]

    def distance(self):
        '''
        Use this function to check the distance from the goal. It will index
        each location the robot has covered.
        '''

        # Chart for the maze
        Z = [[0 for row in range(self.maze_dim)] for col in
             range(self.maze_dim)]
        # Distance from the goal
        dx = abs(self.goal[0] - self.x)
        dy = abs(self.goal[1] - self.y)
        # Distance from location
        Z[self.x][self.y] = dx + dy

        return Z

    def a_star(self):
        '''
        Define the A* search method to fin the optimal path from start to
        goal. Find the heuristic for the maze first in order implement the A*
        method.
        '''

        # Create heuristic chart for maze
        self.heuristic = [[0 for row in range(self.maze_dim)] for col in
                          range(self.maze_dim)]
        for i in range(self.maze_dim):
            for j in range(self.maze_dim):
                dX = abs(self.goal[0] - i)
                dY = abs(self.goal[1] - j)
                heuristic[i][j] = dX + dY

        # Raise an error if heuristic is blank
        if heuristic == []:
            raise ValueError('No heuristic to implement A*')

        # Direction moves for the robot
        delta = [[0, 1],   # Move up
                 [1, 0],   # Move right
                 [0, -1],  # Move down
                 [-1, 0]]  # Move left

        # Check the locations the robot has visited
        checked = [[0 for row in range(self.maze_dim)] for col in
                   range(self.maze_dim)]
        # Number of which move was made
        move = [[0 for row in range(self.maze_dim)] for col in
                range(self.maze_dim)]

        # Origin location checked
        checked[self.x][self.y] = 1

        x = self.x
        y = self.y
        h = heuristic[x][y]
        g = 0
        f = g + h

        open = [[f, g, h, x, y]]

        reached = False  # Seatch completed
        quit = False     # Can't expand upon elements in list
        count = 0
        self.cost = 1    # Cost of moving

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
            if x == goal[0] and y == goal[1]:
                reached = True
            else:
                # Expand element and add to open list
                for i in range(len(delta)):
                    x_prime = x + delta[i][0]
                    y_prime = y + delta[i][1]
                    if x_prime >= 0 and x_prime < self.maze_dim and \
                       y_prime >= 0 and y_prime < self.maze_dim:
                        if checked[x_prime][y_prime] == 0:
                            g_prime = g + cost
                            h_prime = self.heuristic[x_prime][y_prime]
                            f_prime = g_prime + h_prime
                            open.append([f_prime, g_prime, h_prime, x_prime,
                                         y_prime])
                            checked[x_prime][y_prime] = 1
                            move[x_prime][y_prime] = i
            count += 1

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
        rotation = 0  # [-90, 0 , 90]
        # Can move up 3 steps per turn; max 3 forward (3)
        # and max 3 backwards (-3)
        movement = 0  # [-3, 3]

        cost = [8, 1, 2]  # cost for left, forward, right

        view = list(sensors)  # make a copy to preserve original [L, F, R]

        if view[2] == max(view):
            rotation = 90
            movement = 1
        elif view[0] == max(view):
            rotation = -90
            movement = 1
        else:
            rotation = 0
            movement = 1

        # Wall on front and right
        if view[0] > 0 and view[1] == 0 and view[2] == 0:
            rotation = -90
            movement = 1

        # Wall on both sides
        if view[0] == 0 and view[1] > 0 and view[2] == 0:
            rotation = 0
            movement = 1

        # Wall on left and front
        if view[0] == 0 and view[1] == 0 and view[2] > 0:
            rotation = 90
            movement = 1

        # Deadend
        if view == [0, 0, 0]:
            rotation = 0
            movement = -1

        if self.location[0] in self.goal and self.location[1] in self.goal:
            rotation = 'Reset'
            movement = 'Reset'

        # Returns tuple (rotation, movement)
        return rotation, movement
