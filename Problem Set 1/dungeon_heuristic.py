from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)


def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

    def bfs_shortest_path(layout, start, target):
        # Initialize the queue with the starting position and distance 0
        q = [(0, start)] 
        # Initialize the visited set with the starting position
        visited = set([start]) 

        while q:
            # Sort the queue by distance
            q.sort(key=lambda x: x[0])
            # Pop the position with the smallest distance
            dist, pos = q.pop(0)

            # If we've reached the target, return the distance
            if pos == target:
                return dist

            # Explore neighbors
            for d in Direction:
            # Calculate the next position
                next_position = pos + d.to_vector()
                # If the next position is walkable and not visited
                if next_position in layout.walkable and next_position not in visited:
                    # Mark the next position as visited
                    visited.add(next_position)
                    # Add the next position to the queue with incremented distance
                    q.append((dist + 1, next_position))  

        # If target is unreachable, return infinity
        return float('inf')

    # Access or initialize cached distances
    cache = problem.cache()
    if 'distance' not in cache:
        cache['distance'] = {}
        
    # Helper to get the distance between two points, computing if necessary
    def get_distance(p1, p2):
        if (p1, p2) not in cache['distance']:
            # Compute distance using BFS and store it in the cache
            cache['distance'][(p1, p2)] = bfs_shortest_path(problem.layout, p1, p2)
        return cache['distance'][(p1, p2)]
    
    # If there are no remaining coins, return the distance from the player to the exit
    if not state.remaining_coins:
        return get_distance(state.player, problem.layout.exit)
    
    # Find the cost to the nearest coin
    nearest_coin = min(get_distance(state.player, coin) for coin in state.remaining_coins)
    
    # Calculate MST of remaining coins to estimate the minimum cost to collect all coins
    mst_edges = [(get_distance(p1, p2), p1, p2)
                 for p1 in state.remaining_coins for p2 in state.remaining_coins if p1 != p2]
    mst_edges.sort(key=lambda x: x[0])
    
    mst_cost = 0
    mst_set = set([list(state.remaining_coins)[0]])
    
    # While the MST set does not include all remaining coins
    while len(mst_set) < len(state.remaining_coins):
        # Iterate over the sorted edges
        for dist, p1, p2 in mst_edges:
            # If one of the points is in the MST set and the other is not, add the edge to the MST
            if (p1 in mst_set) ^ (p2 in mst_set): 
                # Add the distance to the MST cost
                mst_cost += dist
                # Add both points to the MST set
                mst_set.add(p1)
                mst_set.add(p2)
                # Break to re-evaluate the MST set condition
                break

    # Add the estimated cost from the last coin in MST to the exit
    mst_cost += min(get_distance(coin, problem.layout.exit) for coin in state.remaining_coins)
    
    # Total heuristic: player to nearest coin + MST cost to collect all coins
    return nearest_coin + mst_cost