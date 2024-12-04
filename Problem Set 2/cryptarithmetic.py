from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint
import dis

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

        problem.constraints.extend([UnaryConstraint(x , lambda v: v != 0) for x in set([LHS0[0], LHS1[0], RHS[0]])]) # the 1st letter of each term can't be zero

        carry_list = ['C{}'.format(i) for i in range(1,len(RHS))] # carry variables for each digit except the last one
        
        problem.variables.extend(carry_list) # adding carry variables to the problem variables
        problem.domains.update({c: set([0,1]) for c in carry_list}) # adding the domain of carry variables to be 0,1

        #1st aux variable = 1st digit of the LHS0 + 1st digit of the LHS1
        aux_variables_lhs = [(LHS0[-1], LHS1[-1])] 

        # adding the rest of the aux variables of the LHS to the problem variables
        # the aux variables are the sum of the digits of the LHS and the carry
        aux_variables_lhs.extend([(LHS0[i], LHS1[i], carry_list[-(i+2)]) for i in range(-2,-min(len(LHS0), len(LHS1))-1,-1)]) # x+y+c

        # if the length of LHS0 is greater than the length of LHS1
        # then the aux variables of the LHS will be the sum of the digits of LHS0 and the carry
        if (len(LHS0) > len(LHS1)):
            aux_variables_lhs.extend([(LHS0[-i], carry_list[i-2]) for i in range(len(LHS1) + 1, len(LHS0) + 1)])

        problem.variables.extend(aux_variables_lhs) # adding aux variables of the LHS to the problem variables

        # Adding the domain of aux variables to be the cartesian product of their respective domains
        for x in aux_variables_lhs[1:]:
            problem.domains[x] = set((d1, d2, d3) for d1 in problem.domains[x[0]] for d2 in problem.domains[x[1]] for d3 in problem.domains[x[-1]])
        
        # Adding the domain of the first element to be the cartesian product of d1 and d2
        problem.domains[aux_variables_lhs[0]] = set((d1, d2) for d1 in problem.domains[aux_variables_lhs[0][0]] for d2 in problem.domains[aux_variables_lhs[0][1]])
        
        # Adding constraints for the sum of the LHS
        for x in aux_variables_lhs[1:]:
            problem.constraints.append(BinaryConstraint((x, x[0]), lambda xy, x: x == xy[0]))
            problem.constraints.append(BinaryConstraint((x, x[1]), lambda xy, y: y == xy[1]))
            problem.constraints.append(BinaryConstraint((x, x[-1]), lambda xy, y: y == xy[-1]))
        
        # Adding constraints for the first element
        problem.constraints.append(BinaryConstraint((aux_variables_lhs[0], aux_variables_lhs[0][0]), lambda xy, x: xy[0] == x))
        problem.constraints.append(BinaryConstraint((aux_variables_lhs[0], aux_variables_lhs[0][1]), lambda xy, x: xy[1] == x))
    
        # the rhs aux variable = rhs + carry 
        aux_variables_rhs = [(RHS[len(RHS) - i - 1], c) for i,c in enumerate(carry_list)]
        problem.variables.extend(aux_variables_rhs) # adding aux variables of the RHS to the problem variables
        problem.domains.update({x: set((d1, d2) for d1 in problem.domains.get(x[0]) for d2 in problem.domains.get(x[1])) for x in aux_variables_rhs}) # adding the domain of aux variables to be the cartesian product of d1 and d2

        problem.constraints.extend([BinaryConstraint((x,x[0]), lambda xy,x: x == xy[0]) for x in aux_variables_rhs]) # adding constraints for the sum of the LHS
        problem.constraints.extend([BinaryConstraint((x,x[1]), lambda xy,y: y == xy[1]) for x in aux_variables_rhs]) # adding constraints for the sum of the LHS

        # A + B = C + 10* Carry (last digit only)
        problem.constraints.append(BinaryConstraint((aux_variables_lhs[0],aux_variables_rhs[0]) , lambda lhs, rhs: lhs[0] + lhs[1] == rhs[0] + 10 * rhs[1]))

        # (middle digits)
        for i in range(1,len(aux_variables_rhs)):
            if i < len (LHS1):
                #  A + B + Carry = C + 10* Carry (middle digits)
                problem.constraints.append(BinaryConstraint((aux_variables_lhs[i],aux_variables_rhs[i]) , lambda lhs, rhs: lhs[0] + lhs[1] + lhs[2] == rhs[0] + 10 * rhs[1]))
            else:
                #  A + Carry = C + 10* Carry (middle digits)
                problem.constraints.append(BinaryConstraint((aux_variables_lhs[i],aux_variables_rhs[i]) , lambda lhs, rhs: lhs[0] + lhs[1] == rhs[0] + 10 * rhs[1]))

        if len(LHS0) > len(LHS1) and len(RHS) == len(LHS0):
            # if the length of LHS0 is greater than the length of LHS1 and the length of RHS is equal to the length of LHS0
            #then the last carry + 1st of Lhs0  = the 1st digit of the RHS
            problem.constraints.append(BinaryConstraint((aux_variables_lhs[-1],RHS[0]) , lambda lhs, rhs: lhs[0] + lhs[1] == rhs))

        if len(RHS) == len(LHS0) and len(LHS0) == len(LHS1):
            # if the length of 2 terms of LHS is equal to the length of the RHS
            #then the last carry + 1st of Lhs0 + 1st of lhs1  = the 1st digit of the RHS
            problem.constraints.append(BinaryConstraint((aux_variables_lhs[-1],RHS[0]) , lambda lhs, rhs: lhs[0] + lhs[1] + lhs[2] == rhs))

        if len(RHS) > len(LHS0):
            # 1st digit of RHS = last carry if the length of RHS is greater than the length of LHS0
            problem.constraints.append(BinaryConstraint((RHS[0],carry_list[-1]) , lambda rhs, c: c == rhs))

       
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())