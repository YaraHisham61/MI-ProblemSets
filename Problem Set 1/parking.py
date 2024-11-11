from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        #The init state is a tuple of position for each car
        #As the init state is a tuple it doesn't allow direct modifications 
        return self.cars
        
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # Iterate over each car in the state
        for i, car in enumerate(state):
            # Check if the current car is not in its designated slot
            if self.slots.get(car) != i:
                # If any car is not in its designated slot, return False
                return False
        # If all cars are in their designated slots, return True
        return True

    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        # Initialize an empty list to store possible actions
        a = []
        # Iterate over each car in the state
        for i, car in enumerate(state):
            # Iterate over each possible direction
            for d in Direction:
                # Calculate the new position of the car by adding the direction vector to the current position
                new_d = car + d.to_vector()
                # Check if the new position is within the passages and not already occupied by another car
                if new_d in self.passages and new_d not in state:
                    # Add the action (car index and direction) to the list of possible actions
                    a.append((i, d))
        # Return the list of possible actions
        return a
                

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # Extract the car index and direction from the action
        i, d = action
        # Calculate the new position of the car by adding the direction vector to the current position
        new_d = state[i] + d.to_vector()
        # Convert the current state (tuple) to a list to allow modifications
        new_state = list(state)
        # Update the position of the car in the new state
        new_state[i] = new_d
        # Convert the new state back to a tuple and return it
        return tuple(new_state)


    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE

        # Extract the car index and direction from the action
        i, d = action
        # Get the current position of the car
        car = state[i]
        # Initialize the cost to 1
        cost = 1
        # Calculate the new position of the car by adding the direction vector to the current position
        new_d = car + d.to_vector()
        # Check if the new position is a parking slot and not the designated slot for the car
        if new_d in self.slots and self.slots[new_d] != i:
            # Add a penalty cost if the car is moved to a wrong slot
            cost += 100
        # Return the calculated cost
        return cost
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
