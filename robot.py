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
        # Location index
        self.index = 0

    def distance(self):
        '''
        Use this function to check the distance from the goal. It will index
        each location the robot has covered.
        '''

        Z = []
        # Distance from the goal
        dx = self.goal[0] - self.x
        dy = self.goal[1] - self.y
        Z.append([self.index, dx, dy])
        self.index += 1

        return Z

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

        if self.location[0] in goal and self.location[1] in goal:
            rotation = 'Reset'
            movement = 'Reset'



        # Returns tuple (rotation, movement)
        return rotation, movement
