import chatGPT
import EquationSolver

equation_pass_1 = chatGPT.convertProblemToEquation()
equation_pass_2 = chatGPT.extractEquation(equation_pass_1)

print("Equation: " + equation_pass_2)

solution = EquationSolver.solveEquation(equation_pass_2)

print("Solution: " + solution)