class ChatGPT:
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    import openai

    path = Path("Environment-Variables/.env")
    load_dotenv(dotenv_path=path)

    ORGKEY = os.getenv('organization')
    APIKEY = os.getenv("api_key")

    def __init__(self):
        self.openai.organization = self.ORGKEY
        self.openai.api_key = self.APIKEY
        
    def convertProblemToEquation(self):
        word_problem = input("Enter a word problem: ")
        response = self.openai.Completion.create(
            model="text-davinci-003",
            prompt="Use the word problem from below to create an equation, using any numerical figures from the question. Respond with only a mathematical equation and no text whatsoever. I do not need any explanatory text accompanying the equation. \n" + word_problem,
            temperature=0.3,
            max_tokens=64,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )
        return response["choices"][0]["text"]

    def extractEquation(self, response):
        equation = self.openai.Completion.create(
            model="text-davinci-003",
            prompt="From this text, extract an equation which i can put into an equation solver such as symbolab, and respond with only the equation and no accompanying text: \n" + response,
            temperature=0.3,
            max_tokens=64,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )
        return equation["choices"][0]["text"]
