from maze import Maze
from robot import Robot
import random
import sys


if __name__ == '__main__':

    '''
    Define the A* search method to find the optimal path from start to
    goal. Find the heuristic for the maze first in order implement the A*
    method.
    '''

    # Test maze A* will run on
    testmaze = Maze(str(sys.argv[1]))
    # Goal for robot
    goal = [testmaze.dim / 2 - 1, testmaze.dim / 2]
    # Robot headings
    heading = ['up', 'right', 'down', 'left']
    # Inital position
    initial = [0, 11]

    ##################################################################
    # Incorporate these into A* search

    dir_sensors = {'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
                   'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}

    # Sense the distance from the walls
    sensing = [testmaze.dist_to_wall([x_prime][y_prime], heading)
               for heading in directions[heading[i]]]

    testmaze.is_permissible([x_prime][y_prime], heading[i])
    ##################################################################

    # Create heuristic grid for A* search
    heuristic = [[0 for row in range(testmaze.dim)] for col in range(testmaze.dim)]

    # Assign heuristic values to each square
    for i in range(testmaze.dim):
        for j in range(testmaze.dim):
            dX = abs(i - goal[0])
            dY = abs(j - goal[1])
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
    checked = [[0 for row in range(testmaze.dim)] for col in
               range(testmaze.dim)]
    # Number of which move was made
    move = [[0 for row in range(testmaze.dim)] for col in
            range(testmaze.dim)]

    # Starting location checked
    checked[initial[0]][initial[1]] = 1

    x = initial[0]
    y = initial[1]
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
    cost = 1

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
            print 'Successful Search'
        else:
            # Expand element and add to open list
            for i in range(len(delta)):
                x_prime = x + delta[i][0]
                y_prime = y + delta[i][1]
                if x_prime >= 0 and x_prime < testmaze.dim and y_prime >= 0 and \
                   y_prime < testmaze.dim:
                    if checked[x_prime][y_prime] == 0:
                        g_prime = g + cost
                        h_prime = heuristic[x_prime][y_prime]
                        f_prime = g_prime + h_prime
                        open.append([f_prime, g_prime, h_prime, x_prime, y_prime])
                        checked[x_prime][y_prime] = 1
                        move[x_prime][y_prime] = i
        count += 1

    policy = [[' ' for row in range(testmaze.dim)] for col in
              range(testmaze.dim)]
    x = goal[0]
    y = goal[1]
    policy[x][y] = 'x'

    while x != initial[0] and y != initial[1]:
        x_prime = x - delta[move[x][y]][0]
        y_prime = y - delta[move[x][y]][1]
        policy[x_prime][y_prime] = delta_sign[move[x][y]]
        x = x_prime
        y = y_prime

    for i in range(len(policy)):
        print policy[i]

    invpath = []
    x = goal[0]
    y = goal[1]
    invpath.append([x, y])
    while x != initial[0] or y != initial[1]:
        x_prime = x - delta[move[x][y]][0]
        y_prime = y - delta[move[x][y]][1]
        x = x_prime
        y = y_prime
        invpath.append([x, y])

    path = []
    for i in range(len(invpath)):
        path.append(invpath[len(invpath) - 1 - i])
