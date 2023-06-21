import wolframalpha
import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

client = wolframalpha.Client(os.getenv("wlf_appid"))


def solveEquation(equation):
    response = client.query(equation)
    return next(response.results).text
