import chatGPT
import EquationSolver
import temp_dev_chatGPT

import os
from pathlib import Path
from dotenv import load_dotenv

testClass = temp_dev_chatGPT.ChatGPT()



# path = Path("Environment-Variables/.env")
# load_dotenv(dotenv_path=path)
#
# # Setting organization and API keys
# orgKey = os.getenv('organization')
# apiKey = os.getenv("api_key")


# equation_pass_1 = chatGPT.convertProblemToEquation(orgKey, apiKey)
# equation_pass_2 = chatGPT.extractEquation(equation_pass_1, orgKey, apiKey)

equation_pass_1 = testClass.convertProblemToEquation()
equation_pass_2 = testClass.extractEquation(equation_pass_1)

print("Equation: " + equation_pass_2)

# solution = EquationSolver.solveEquation(equation_pass_2)
#
# print("Solution: " + solution)
