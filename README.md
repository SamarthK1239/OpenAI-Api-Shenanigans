# OpenAI-API-Shenanigans
A longer-term project using the different models available through the OpenAI API. No clue where this is going, just that it's going to be a ride.

**Important note:** ~~Some models are being deprecated in favor of GPT-3, GPT-3.5, and GPT-4. I still need to edit code in this repository to use the models not in danger of being deprecated. Additionally, any fine-tuning experiments will be paused until the newer models support it.~~ *All current projects on this repository have been updated to the latest version of the API, and where possible, use **GPT-3.5-Turbo-1106**.*

## Code that's Currently Here
- A very simple image generation program that leverages Dall-E to generate 1024x1024 Images around any prompt you give it (*API version upgrade COMPLETED*)
- An add-on to this that creates a variation on images that have been generated already (*API version upgrade COMPLETED*)
- A simple sentiment analyzer that takes a prompt and then analyzes if it is positive, negative, or neutral, and also returns a rating from 1 - 10, where 1 is the most negative and 10 is the most positive. (*API version upgrade COMPLETED*)
- The beginnings of a Summarization Application that leverages the Speech-To-Text Functionality of the Whisper-1 model (*API version upgrade COMPLETED*)
- A simple program that uses TikToken to see how many tokens an input prompt contains (This one's still a work in progress, additional features that allow prompts to be shortened will be added (*API version upgrade COMPLETED*)
- The beginnings of an equation solver that uses ChatGPT to convert word problems into solvable equations, and then passes those equations through the Wolfram Alpha API, allowing them to be solved (***ON HOLD, API version upgrade INCOMPLETE***)
- A dynamic, interactive storyteller that uses the GPT-3.5-Turbo model to create an interactive story that changes with the user's response. The goal is to create stories that are different every time, leading to crazy reusability with just a limited number of starting prompts! (***ONGOING!***)

## Random Info
If you want to use any of this code, you need to either use environment variables placed in a .env, within a folder called "Environment Variables", or you can just get rid of the environment variable code entirely and hard-code your keys into it (I don't recommend this, because if you ever end up uploading your code or changing your keys, you've got to go in and edit it in every single program).

Speaking of Keys, you need two of them. One's an "Organization Key" and OpenAI assigns one to you. The second one's an API key, which you need to generate (ideally per application). Both of these can be found by going to the OpenAI website at <https://platform.openai.com/overview>

Every program here will have a section at the top that initializes both keys and if you're hardcoding these keys, just paste them between quotes and you're good to go!

## Learnings
The OpenAI models are extremely powerful, but you need to know how to use them. Prompt design is especially important (shocking, I know). Generating a lot of stuff results in OpenAI charging you for a lot of stuff (again: shocking, I know). In most cases, if you're unsure what you should add as a starter statement, try it out on the free ChatGPT website. This lets you do as many variations as you want without being charged, and then you can do some minor fine-tuning when you code it in!

Always make sure that you're monitoring your usage. Use simpler, cheaper models for less complex processes.

Speech-to-text is a very expensive process, and for longer content, you can sometimes end up with far more tokens than your model can handle. I'm not sure how to deal with this yet, but I'm working on it 👀

PyDub requires you to copy executable files from the PyDub source folder to your working directory. And that is annoying. Very. Annoying. (Don't use it)

if you want to measure how many tokens an input has, OpenAI has another package, TikToken, that you can use to easily find this value. There's some sample code for this in *TokenSplitter.py*

The WolframAlpha solver is powerful, but only as long as you give it good inputs. There are still occasions where GPT-3.5 struggles to listen to the instructions given, and ends up just returning whatever it likes. There's a safeguard that needs to be implemented to prevent this from crashing the project as a whole.
