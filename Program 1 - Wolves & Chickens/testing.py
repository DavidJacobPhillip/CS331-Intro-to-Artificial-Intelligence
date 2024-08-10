"""
Names: Santosh Ramesh & Anshul Batish
Date: 4-17-22
Class: CS 331 Intro to Artificial Intelligence
Program: Wolfs & Chicken
Description: You need to get the wolves and chickens to the otherside of the river bank without eating all of the chickens

"""

# IMPORTS
import sys
import copy

# GLOBALS
# Container for states to be explored
queue = []
checked = []

# CLASSES
# Object for a node (state of chickens, wolves, and boat)
class State:
    def __init__(self):
        self.l_chickens = 0
        self.l_wolves = 0
        self.l_boats = 0
        self.r_chickens = 0
        self.r_wolves = 0
        self.r_boats = 0
        self.previous_state = None
        self.move = ""

        # Used to hold the "depth" of the node in IDDFS and "weight" in A-star
        self.depth = 0
        self.heur = 0

    # Prints out the node
    def __str__(self): 
        state_print = "lc: " + str(self.l_chickens) + "  lw: " + str(self.l_wolves) + "  lb: " + str(self.l_boats) + "\n" 
        state_print = state_print + "rc: " + str(self.r_chickens) + "  rw: " + str(self.r_wolves) + "  rb: " + str(self.r_boats) + "\n" 
        return state_print

    # Compares this node to another
    def __eq__(self, other):
        if (isinstance(other, State)):
            return self.l_chickens == other.l_chickens and self.l_wolves == other.l_wolves and self.r_chickens == other.r_chickens and self.r_wolves == other.r_wolves and self.l_boats == other.l_boats and self.r_boats == other.r_boats
        else:
            return False

# FUNCTIONS
# Reading though goal & initial state files
def file_reader(initial, goal, starting, ending):
    # Parsing through initial and goal file to split it into left and right values for chickens
    initial_file = open(initial, 'r')
    lines = initial_file.readlines()
    start_left = lines[0].strip()
    start_right = lines[1].strip()
    initial_file.close()

    goal_file = open(goal, 'r')
    lines = goal_file.readlines()
    goal_left = lines[0].strip()
    goal_right = lines[1].strip()
    goal_file.close()

    # Converting the starting values into a list
    start_right = start_right.split(",")
    start_left = start_left.split(",")
    goal_right = goal_right.split(",")
    goal_left = goal_left.split(",")

    # Assinging the global starting/ending values individually    
    starting.l_chickens = int(start_left[0])
    starting.r_chickens = int(start_right[0])
    starting.l_wolves = int(start_left[1])
    starting.r_wolves = int(start_right[1])
    starting.l_boats = int(start_left[2])
    starting.r_boats = int(start_right[2])

    ending.l_chickens = int(goal_left[0])
    ending.r_chickens = int(goal_right[0])
    ending.l_wolves = int(goal_left[1])
    ending.r_wolves = int(goal_right[1])
    ending.l_boats = int(goal_left[2])
    ending.r_boats = int(goal_right[2])
    
    # Printing out starting values
    print("STARTING VALUES: ")
    print(starting)

    # Printing out goal values
    print("GOAL VALUES: ")
    print(ending)

# Checking if the node currently exists in the explored list
def explored_check(explored, current):
    for element in explored:
        if element == current:
            return True
    return False

# Creating a new link
def new_node(node):
    current = State()
    current = copy.deepcopy(node)
    return current

# Child nodes
def child_nodes(current, explored):
    explored_size = len(explored) - 1
    temporary = new_node(current)
    # If boat is on the left side:
    if current.l_boats == 1:
        # State of moving one chicken from left to right
        if current.l_chickens >= 1:
            # print("left to right one chicken")
            temporary.l_chickens = temporary.l_chickens - 1
            temporary.r_chickens = temporary.r_chickens + 1
            temporary.l_boats = 0
            temporary.r_boats = 1
            temporary.move = "left to right one chicken"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)
        
        # State of moving two chickens from left to right
        if current.l_chickens >= 2:
            # print("left to right two chickens")
            temporary.l_chickens = temporary.l_chickens - 2
            temporary.r_chickens = temporary.r_chickens + 2
            temporary.l_boats = 0
            temporary.r_boats = 1
            temporary.move = "left to right two chickens"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)
        
        # State of moving one wolf from left to right
        if current.l_wolves >= 1:
            # print("left to right one wolf")
            temporary.l_wolves = temporary.l_wolves - 1
            temporary.r_wolves = temporary.r_wolves + 1
            temporary.l_boats = 0
            temporary.r_boats = 1
            temporary.move = "left to right one wolf"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)

        # State of moving one chicken and one wolf from left to right
        if current.l_chickens >= 1 and current.l_wolves >= 1:
            # print("left to right one chicken and one wolf")
            temporary.l_chickens = temporary.l_chickens - 1
            temporary.r_chickens = temporary.r_chickens + 1
            temporary.l_wolves = temporary.l_wolves - 1
            temporary.r_wolves = temporary.r_wolves + 1
            temporary.l_boats = 0
            temporary.r_boats = 1
            temporary.move = "left to right one chicken and one wolf"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)

        # State of moving two wolves from left to right
        if current.l_wolves >= 2:
            # print("left to right two wolves")
            temporary.l_wolves = temporary.l_wolves - 2
            temporary.r_wolves = temporary.r_wolves + 2
            temporary.l_boats = 0
            temporary.r_boats = 1
            temporary.move = "left to right two wolves"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)
        
    # If boat is on the right side:
    else:
        # State of moving one chicken from right to left
        if current.r_chickens >= 1:
            # print("right to left one chicken")
            temporary.r_chickens = temporary.r_chickens - 1
            temporary.l_chickens = temporary.l_chickens + 1
            temporary.r_boats = 0
            temporary.l_boats = 1
            temporary.move = "right to left one chicken"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)
            
        # State of moving two chickens from right to left
        if current.r_chickens >= 2:
            # print("right to left two chickens")
            temporary.r_chickens = temporary.r_chickens - 2
            temporary.l_chickens = temporary.l_chickens + 2
            temporary.r_boats = 0
            temporary.l_boats = 1
            temporary.move = "right to left two chickens"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)

        # State of moving one wolf from right to left
        if current.r_wolves >= 1:
            # print("right to left one wolf")
            temporary.r_wolves = temporary.r_wolves - 1
            temporary.l_wolves = temporary.l_wolves + 1
            temporary.r_boats = 0
            temporary.l_boats = 1
            temporary.move = "right to left one wolf"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)

        # State of moving two wolves from right to left
        if current.r_wolves >= 2:
            # print("right to left two wolves")
            temporary.r_wolves = temporary.r_wolves - 2
            temporary.l_wolves = temporary.l_wolves + 2
            temporary.r_boats = 0
            temporary.l_boats = 1
            temporary.move = "right to left two wolves"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)
            temporary = copy.deepcopy(current)
        
        # State of moving one chicken and one wolf from right to left
        if current.r_chickens >= 1 and current.r_wolves >= 1:
            # print("right to left one chicken and one wolf")
            temporary.r_chickens = temporary.r_chickens - 1
            temporary.l_chickens = temporary.l_chickens + 1
            temporary.r_wolves = temporary.r_wolves - 1
            temporary.l_wolves = temporary.l_wolves + 1
            temporary.r_boats = 0
            temporary.l_boats = 1
            temporary.move = "right to left one chicken and one wolf"
            if explored_check(explored, temporary) == False:
                temporary.previous_state = explored[explored_size]
                temporary.depth = explored[explored_size].depth + 1
                temporary.heur = (temporary.l_chickens + temporary.l_wolves) / 2
                queue.append(temporary)
                explored.append(temporary)
                # print(temporary)

# Uninformed: Breadth-First Search
def BFS(starting, ending):
    counter = 0
    # Initializing frontier with initial state of problem
    queue.append(new_node(starting))
    checked.append(new_node(starting))
    expanded = 0
    moves = 0

    # Looping through frontier
    while True:
        counter = counter + 1
        if counter == 200000:
            print("looping through explored")
            for elem in checked:
                print(elem)
            break
        # If frontier is empty and there is no solution
        if len(queue) == 0:
            print ("No Solution Found")
            for elem in checked:
                print(elem)
            break

        # Popping from queue and adding the top-most node to the explored list
        current = queue.pop(0)        

        # Removing child node and checking if it is the solution
        if current == ending:
            current = new_node(current)

            # Printing out moves
            print("Solution Found")
            print("Nodes Expanded: ", expanded)
            print("Moves List:")
            while current.previous_state != None:
                print(current.move)
                # print(current)
                moves = moves + 1
                current = copy.deepcopy(current.previous_state)
            print("Total Path Moves: ", moves)
            break

        # Checking if right side has more wolves than chickens
        if current.r_chickens < current.r_wolves and current.r_chickens != 0:
            # print("RIGHT BAD MOVE")
            pass
        
        # Checking if left side has more wolves than chickens
        elif current.l_chickens < current.l_wolves and current.l_chickens != 0:
            # print("LEFT BAD MOVE") 
            pass
        
        # Expanding nodes and adding results to frontier
        else:
            expanded = expanded + 1
            child_nodes(current, checked)

# Uninformed: Depth-First Search
def DFS(starting, ending):
    # Initializing frontier with initial state of problem
    queue.append(new_node(starting))
    checked.append(new_node(starting))
    expanded = 0
    moves = 0

    # Looping through frontier
    while True:
        # If frontier is empty and there is no solution
        if len(queue) == 0:
            print ("No Solution Found")
            for elem in checked:
                print(elem)
            break

        # Popping from queue and adding the bottom-most node to the explored list
        current = queue.pop(len(queue) - 1)        

        # Removing child node and checking if it is the solution
        if current == ending:
            current = new_node(current)

            # Printing out moves
            print("Solution Found")
            print("Nodes Expanded: ", expanded)
            print("Moves List:")
            while current.previous_state != None:
                print(current.move)
                # print(current)
                moves = moves + 1
                current = copy.deepcopy(current.previous_state)
            print("Total Path Moves: ", moves)
            break

        # Checking if right side has more wolves than chickens
        if current.r_chickens < current.r_wolves and current.r_chickens != 0:
            # print("RIGHT BAD MOVE")
            pass
        
        # Checking if left side has more wolves than chickens
        elif current.l_chickens < current.l_wolves and current.l_chickens != 0:
            # print("LEFT BAD MOVE") 
            pass
        
        # Expanding nodes and adding results to frontier
        else:
            expanded = expanded + 1
            child_nodes(current, checked)
        
# Uninformed: Iteratively Deepening Depth-First Search
def IDDFS(starting, ending):
    current_depth = 1          
    max_depth = 10000
    expanded = 0
    moves = 0
    
    # Increasing the max depth and iterating again
    while current_depth < max_depth:
        # Initializing frontier with initial state of problem
        queue.append(new_node(starting))
        checked.append(new_node(starting))

        # Looping through frontier
        while True:
            # If frontier is empty and there is no solution
            if len(queue) == 0:
                print ("No Solution Found")
                print("elem")
                for elem in checked:
                    print(elem)

            # Popping from queue and adding the bottom-most node to the explored list
            current = queue.pop(len(queue) - 1)

            # Removing child node and checking if it is the solution
            if current == ending:
                current = new_node(current)

                # Printing out moves
                print("Solution Found")
                print("Nodes Expanded: ", expanded)
                print("Moves List:")
                current_depth = max_depth
                while current.previous_state != None:
                    print(current.move)
                    # print(current)
                    moves = moves + 1
                    current = copy.deepcopy(current.previous_state)
                print("Total Path Moves: ", moves)
                break

            # Checking if the node is smaller than the depth cut-off
            if current.depth > current_depth:
                queue.clear()
                checked.clear()
                break

            # Checking if right side has more wolves than chickens
            elif current.r_chickens < current.r_wolves and current.r_chickens != 0:
                # print("RIGHT BAD MOVE")
                pass
            
            # Checking if left side has more wolves than chickens
            elif current.l_chickens < current.l_wolves and current.l_chickens != 0:
                # print("LEFT BAD MOVE") 
                pass
            
            # Expanding nodes and adding results to frontier
            else:
                expanded = expanded + 1
                child_nodes(current, checked)
        current_depth = current_depth + 1

def A_Star(starting, ending):
    # Initializing frontier with initial state of problem
    queue.append(new_node(starting))
    checked.append(new_node(starting))
    expanded = 0
    moves = 0

    # Looping through frontier
    while True:
        # If frontier is empty and there is no solution
        if len(queue) == 0:
            print ("No Solution Found")
            for elem in checked:
                print(elem)
            break

        # Selecting the node with the smallest heuristic evaluation value
        heur_val = queue[0].heur
        lowest = 0
        counter = 0
        for state in queue:
            if state.heur < heur_val:
                lowest = counter
            counter = counter + 1

        current = queue.pop(lowest)

        # Removing child node and checking if it is the solution
        if current == ending:
            current = new_node(current)

            # Printing out moves
            print("Solution Found")
            print("Nodes Expanded: ", expanded)
            print("Moves List:")
            while current.previous_state != None:
                print(current.move)
                # print(current)
                moves = moves + 1
                current = copy.deepcopy(current.previous_state)
            print("Total Path Moves: ", moves)
            break

        # Checking if right side has more wolves than chickens
        if current.r_chickens < current.r_wolves and current.r_chickens != 0:
            # print("RIGHT BAD MOVE")
            pass
        
        # Checking if left side has more wolves than chickens
        elif current.l_chickens < current.l_wolves and current.l_chickens != 0:
            # print("LEFT BAD MOVE") 
            pass
        
        # Expanding nodes and adding results to frontier
        else:
            expanded = expanded + 1
            child_nodes(current, checked)

# MAIN
def main():
    if len(sys.argv) >= 4:
        # Initializing starting/ending nodes
        starting = State()
        ending = State()

        # Reads the arguments submitted by the command line input
        initial = sys.argv[1]
        goal = sys.argv[2]
        mode = sys.argv[3]
        output = sys.argv[4]

        # Printing to output file
        # sys.stdout =  open(output, 'w')

        # Reading files
        file_reader(initial, goal, starting, ending)
        
        # Selecting search mode based on input
        if mode == "bfs":
            BFS(starting, ending)
        elif mode == "dfs":
            DFS(starting, ending)
        elif mode == "iddfs":
            IDDFS(starting, ending)
        elif mode == "astar":
            A_Star(starting, ending)
        else:
            sys.exit("Error: mode argument must be either 'bfs', 'dfs', 'iddfs' or 'astar'")
        
# Runs the main function
if __name__ == "__main__":
    main()