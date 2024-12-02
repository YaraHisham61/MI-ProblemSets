import random
from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any built in modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function

    # Get the index of the current agent
    agent_idx = game.get_turn(state)
    
    # Check if the current state is terminal and get the terminal values
    terminal, terminal_values = game.is_terminal(state)

    # If the state is terminal, return the terminal value for the current agent and None for the action
    if terminal:
        return terminal_values[agent_idx], None

    # If the maximum depth is reached
    if max_depth == 0:
        # If it is the player's turn (max node), return the heuristic value
        if agent_idx == 0:
            return heuristic(game, state, agent_idx), None
        # If it is an enemy's turn (min node), return the negative heuristic value
        else:
            return -heuristic(game, state, agent_idx), None

    # If it is the player's turn (max node)
    if agent_idx == 0:
        # Return the maximum value and corresponding action from the minimax search on successor states
        return max(((minimax(game, game.get_successor(state, action), heuristic, max_depth - 1)[0], action) 
                   for action in game.get_actions(state)), key=lambda x: x[0])
    # If it is an enemy's turn (min node)
    else:
        # Return the minimum value and corresponding action from the minimax search on successor states
        return min(((minimax(game, game.get_successor(state, action), heuristic, max_depth - 1)[0], action) 
                   for action in game.get_actions(state)), key=lambda x: x[0])

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def alphabeta_rec(state: S, heuristic: HeuristicFunction,alpha,beta, max_depth: int = -1) -> Tuple[float, A]:
        # Get the index of the current agent
        agent_idx = game.get_turn(state)
        # Check if the current state is terminal and get the terminal values
        terminal, terminal_values = game.is_terminal(state)
        # If the state is terminal, return the terminal value for the current agent and None for the action
        if terminal:
            return terminal_values[agent_idx], None

        # If the maximum depth is reached
        if max_depth == 0:
            # If it is the player's turn (max node), return the heuristic value
            if agent_idx == 0:
                return heuristic(game, state, agent_idx), None
            # If it is an enemy's turn (min node), return the negative heuristic value
            else:
                return -heuristic(game, state, agent_idx), None

        value , best_action = None, None

        # If it is the player's turn (max node)
        if agent_idx == 0:
            # Initialize value to -ve infinity for maximization
            value = float('-inf')
            # Iterate over all possible actions
            for action in game.get_actions(state):
                # Check the value of the child node
                child = alphabeta_rec(game.get_successor(state, action), heuristic, alpha, beta, max_depth - 1)[0]
                # Update value and best_action if the child value is greater than the current value
                if child > value:
                    value, best_action = child, action
                # Update alpha with the maximum value
                alpha = max(alpha, value)
                # Prune the remaining branches if value is greater than or equal to beta
                if value >= beta:
                    break
        
        # If it is an enemy's turn (min node)
        else:
            # Initialize value to infinity for minimization
            value = float('inf')
            # Iterate over all possible actions
            for action in game.get_actions(state):
                # Check the value of the child node
                child = alphabeta_rec(game.get_successor(state, action),heuristic,alpha,beta,max_depth-1)[0]
                # Update value and best_action if the child value is less than the current value
                if child < value:
                    value , best_action  = child,action
                # Update beta with the minimum value
                beta = min(beta,value)
                # Prune the remaining branches if value is less than or equal to alpha
                if value <= alpha:
                    break

        return value, best_action
    
    ############################################################################



    return alphabeta_rec(state,heuristic,float('-inf'),float('inf'),max_depth)
    

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def alphabeta_with_move_ordering_rec(state: S, heuristic: HeuristicFunction,alpha,beta, max_depth: int = -1) -> Tuple[float, A]:
        # Get the index of the current agent
        agent_idx = game.get_turn(state)
        # Check if the current state is terminal and get the terminal values
        terminal, terminal_values = game.is_terminal(state)
        # If the state is terminal, return the terminal value for the current agent and None for the action
        if terminal:
            return terminal_values[agent_idx], None

        # If the maximum depth is reached
        if max_depth == 0:
            # If it is the player's turn (max node), return the heuristic value
            if agent_idx == 0:
                return heuristic(game, state, agent_idx), None
            # If it is an enemy's turn (min node), return the negative heuristic value
            else:
                return -heuristic(game, state, agent_idx), None

        value , best_action = None, None
        sucessors = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # If it is the player's turn (max node)
        if agent_idx == 0:
            # Order successors based on heuristic value in descending order
            sucessors_ordered = sorted(sucessors , key=lambda x: (heuristic(game, x[1], agent_idx), -sucessors.index(x)), reverse=True)
            # Initialize value to -ve infinity for maximization
            value = float('-inf')
            # Iterate over all possible actions
            for action,state in sucessors_ordered:
                # Check the value of the child node
                child = alphabeta_with_move_ordering_rec(state, heuristic, alpha, beta, max_depth - 1)[0]
                # Update value and best_action if the child value is greater than the current value
                if child > value:
                    value, best_action = child, action
                # Update alpha with the maximum value
                alpha = max(alpha, value)
                # Prune the remaining branches if value is greater than or equal to beta
                if value >= beta:
                    break
        
        # If it is an enemy's turn (min node)
        else:
            # Order successors based on heuristic value in ascending order
            sucessors_ordered = sorted(sucessors , key=lambda x: (-heuristic(game, x[1], agent_idx), -sucessors.index(x)))
            # Initialize value to infinity for minimization
            value = float('inf')
            # Iterate over all possible actions
            for action,state in sucessors_ordered:
                # Check the value of the child node
                child = alphabeta_with_move_ordering_rec(state,heuristic,alpha,beta,max_depth-1)[0]
                # Update value and best_action if the child value is less than the current value
                if child < value:
                    value , best_action  = child,action
                # Update beta with the minimum value
                beta = min(beta,value)
                # Prune the remaining branches if value is less than or equal to alpha
                if value <= alpha:
                    break

        return value, best_action

    return alphabeta_with_move_ordering_rec(state,heuristic,float('-inf'),float('inf'),max_depth)

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def expectimax_rec(state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
        # Get the index of the current agent
        agent_idx = game.get_turn(state)
        
        # Check if the current state is terminal and get the terminal values
        terminal, terminal_values = game.is_terminal(state)

        # If the state is terminal, return the terminal value for the current agent and None for the action
        if terminal:
            return terminal_values[agent_idx], None

        # If the maximum depth is reached
        if max_depth == 0:
            # If it is the player's turn (max node), return the heuristic value
            if agent_idx == 0:
                return heuristic(game, state, agent_idx), None
            # If it is an enemy's turn (min node), return the negative heuristic value
            else:
                return -heuristic(game, state, agent_idx), None
        
        value , best_action = 0, None

         # If it is the player's turn (max node)
        if agent_idx == 0:
            # Initialize value to -ve infinity for maximization
            value = float('-inf')
            # Iterate over all possible actions
            for action in game.get_actions(state):
                # Check the value of the child node
                child = expectimax_rec(game.get_successor(state, action), heuristic, max_depth - 1)[0]
                # Update value and best_action if the child value is greater than the current value
                if child > value:
                    value, best_action = child, action
        
        # If it is an enemy's turn (min node)
        else:
            #getting the list of possible actions
            actions = game.get_actions(state)
            # Iterate over all possible actions
            for action in actions:
                # Getting the value of the child node
                child = expectimax_rec(game.get_successor(state, action),heuristic,max_depth-1)[0]
                # Add the value of the child to the total value
                value += child
            # Calculate the average value of the children
            value /= len(actions)
            # Randomly select an action from the list of possible actions
            best_action = actions[random.randint(0, len(actions) - 1)]

        return value, best_action
    
    return expectimax_rec(state,heuristic,max_depth)

