# Author: Samarth Kulkarni

# Import the two modules needed, this is simply a management program, intended to make running this thing easier
import equation_solver
import problem_to_equation

# Initialize the convertor
convertor = problem_to_equation.ChatGPT()

# Convert the problem to an equation
equation_pass_1 = convertor.convertProblemToEquation()
print("Equation: " + equation_pass_1)

# Solve the equation
solution = EquationSolver.solveEquation(equation_pass_1)
print("Solution: " + solution)
