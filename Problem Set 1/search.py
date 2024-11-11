from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

#TODO: Import any modules you want to use

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    # Check if the initial state is the goal state
    if problem.is_goal(initial_state):
        return []

    # Initialize the frontier with the initial state and an empty path
    frontier = deque()
    frontier.append((initial_state, []))

    # Initialize the explored set to keep track of visited states
    explored = set()

    # Loop until a solution is found or the frontier is empty
    while True:
        # If the frontier is empty, return None (no solution)
        if len(frontier) == 0:
            return None

        # Pop the first state and path from the frontier
        state, path = frontier.popleft()

        # If the state has already been explored, skip it
        if state in explored:
            continue
        
        # Add the state to the explored set
        explored.add(state)

        # Iterate over all possible actions from the current state
        for action in problem.get_actions(state):
            # Get the next state by applying the action
            next_state = problem.get_successor(state, action)

            # If the next state has not been explored and is not in the frontier
            if next_state not in explored and next_state not in [state for state, path in frontier]:
                # If the next state is the goal state, return the path including the current action
                if problem.is_goal(next_state):
                    return path + [action]

                # Add the next state and the updated path to the frontier
                frontier.append((next_state, path + [action]))

            

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    # Initialize the frontier with the initial state and an empty path
    frontier = deque()
    frontier.append((initial_state, []))

    # Initialize the explored set to keep track of visited states
    explored = set()

    # Loop until a solution is found or the frontier is empty
    while True:
        # If the frontier is empty, return None (no solution)
        if len(frontier) == 0:
            return None

        # Pop the last state and path from the frontier
        state, path = frontier.pop()

        # If the state has already been explored, skip it
        if state in explored:
            continue
        # If the state is the goal state, return the path
        if problem.is_goal(state):
            return path
        
        # Add the state to the explored set
        explored.add(state)

        # Iterate over all possible actions from the current state
        for action in problem.get_actions(state):
            # Get the next state by applying the action
            next_state = problem.get_successor(state, action)

            # If the next state has not been explored
            if next_state not in explored:
                # Add the next state and the updated path to the frontier
                frontier.append((next_state, path + [action]))
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # Initialize the frontier with the initial state and an empty path
    frontier = []
    frontier.append((0, initial_state, []))

    # Initialize the explored set to keep track of visited states
    explored = set()

    # Loop until a solution is found or the frontier is empty
    while frontier:
        # Pop the state with the lowest cost from the frontier
        frontier.sort(key=lambda x: x[0])
        cost, state, path = frontier.pop(0)

        # If the state has already been explored, skip it
        if state in explored:
            continue

        # If the state is the goal state, return the path
        if problem.is_goal(state):
            return path

        # Add the state to the explored set
        explored.add(state)

        # Iterate over all possible actions from the current state
        for action in problem.get_actions(state):
            # Get the next state by applying the action
            next_state = problem.get_successor(state, action)

            # Calculate the cost to reach the next state
            next_cost = cost + problem.get_cost(state, action)

            # If the next state has not been explored
            if next_state not in explored:
                # Add the next state and the updated path to the frontier
                frontier.append((next_cost, next_state, path + [action]))

    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE

    # Initialize the frontier with the initial state and an empty path
    frontier = []
    frontier.append((heuristic(problem,initial_state), initial_state, []))

    # Initialize the explored set to keep track of visited states
    explored = set()
    
    # Loop until a solution is found or the frontier is empty
    while True:
        # If the frontier is empty, return None (no solution)
        if len(frontier) == 0:
            return None
        # Pop the state with the lowest cost from the frontier
        frontier.sort(key=lambda x: x[0])
        cost, state, path = frontier.pop(0)

        # If the state has already been explored, skip it
        if state in explored:
            continue

        # If the state is the goal state, return the path
        if problem.is_goal(state):
            return path
        
        # Add the state to the explored set
        explored.add(state)

        # Iterate over all possible actions from the current state
        for action in problem.get_actions(state):
            # Get the next state by applying the action
            next_state = problem.get_successor(state, action)

            # Calculate the cost to reach the next state
            # The next cost =  cost of current state + cost of the action - heuristic of current state + heuristic of next state
            next_cost = cost + problem.get_cost(state, action) - heuristic(problem,state) + heuristic(problem,next_state)

            # If the next state has not been explored
            if next_state not in explored:
                # Add the next cost the next state and the updated path to the frontier
                frontier.append((next_cost, next_state, path + [action]))

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # Initialize the frontier with the initial state and an empty path
    frontier = []
    frontier.append((heuristic(problem,initial_state), initial_state, []))

    # Initialize the explored set to keep track of visited states
    explored = set()
    
    # Loop until a solution is found or the frontier is empty
    while True:
        # If the frontier is empty, return None (no solution)
        if len(frontier) == 0:
            return None
        # Pop the state with the lowest cost from the frontier
        frontier.sort(key=lambda x: x[0])
        _, state, path = frontier.pop(0)

        # If the state has already been explored, skip it
        if state in explored:
            continue

        # If the state is the goal state, return the path
        if problem.is_goal(state):
            return path
        
        # Add the state to the explored set
        explored.add(state)

        # Iterate over all possible actions from the current state
        for action in problem.get_actions(state):
            # Get the next state by applying the action
            next_state = problem.get_successor(state, action)

            # Calculate the cost to reach the next state
            # The next cost =  heuristic of next state
            next_cost = heuristic(problem,next_state) 

            # If the next state has not been explored
            if next_state not in explored:
                # Add the next cost the next state and the updated path to the frontier
                frontier.append((next_cost, next_state, path + [action]))