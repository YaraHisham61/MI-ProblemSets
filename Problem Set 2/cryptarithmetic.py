from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        
        problem.variables = list(set(LHS0 + LHS1 + RHS)) # add all the letters to the variables
        problem.domains = {x: set(range(10)) for x in problem.variables} # add the domain of each letter to be 0-9
        problem.constraints = [BinaryConstraint((x,y) , lambda x , y : x != y) for x in problem.variables for y in problem.variables if x != y] #ensure unique value for each letter
        problem.constraints += [UnaryConstraint(x , lambda v: v != 0) for x in set([LHS0[0], LHS1[0], RHS[0]])] # the last letter of each term can't be zero

        aux_variables_lhs = ['{}{}'.format(LHS0[i], LHS1[i]) for i in range (min(len(LHS0), len(LHS1)))] # aux variables for the sum of the LHS
        problem.variables += aux_variables_lhs # adding aux variables of the LHS to the problem variables
        problem.domains.update({x: set((d1, d2) for d1 in problem.domains.get(x[0]) for d2 in problem.domains.get(x[1])) for x in aux_variables_lhs}) # adding the domain of aux variables to be the cartesian product of d1 and d2

        problem.constraints += [BinaryConstraint((x,x[0]), lambda xy,x: x == xy[0]) for x in aux_variables_lhs] # adding constraints for the sum of the LHS
        problem.constraints += [BinaryConstraint((x,x[1]), lambda xy,y: y == xy[1]) for x in aux_variables_lhs] # adding constraints for the sum of the LHS

        carry_list = ['C{}'.format(i) for i in range(1, min(len(LHS0), len(LHS1)))] # carry variables for each digit except the last one
        if len(RHS) > min(len(LHS0), len(LHS1)):
            carry_list.append('C{}'.format(len(carry_list) + 1)) # add an extra carry if RHS is longer than the LHS
        
        problem.variables += carry_list # adding carry variables to the problem variables
        problem.domains.update({c: set([0,1]) for c in carry_list}) # adding the domain of carry variables to be 0,1

        aux_variables_rhs = ['{}{}'.format(RHS[len(RHS) - i - 1], c) for i,c in enumerate(carry_list)]
        problem.variables += aux_variables_rhs # adding aux variables of the RHS to the problem variables
        problem.domains.update({x: set((d1, d2) for d1 in problem.domains.get(x[0]) for d2 in problem.domains.get('{}{}'.format(x[1],x[2]))) for x in aux_variables_rhs}) # adding the domain of aux variables to be the cartesian product of d1 and d2

        problem.constraints += [BinaryConstraint((x,x[0]), lambda xy,x: x == xy[0]) for x in aux_variables_rhs] # adding constraints for the sum of the LHS
        problem.constraints += [BinaryConstraint((x,x[1:]), lambda xy,y: y == xy[1:]) for x in aux_variables_rhs] # adding constraints for the sum of the LHS

        for i,aux_v in enumerate(reversed(aux_variables_lhs)):
            problem.constraints += [BinaryConstraint((aux_v, aux_variables_rhs[i]), lambda x,y : x[0] + x[1] == y[0] + 10 * y[1:] )]

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())