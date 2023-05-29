# OpenAI-API-Shenanigans
A longer term project using the different models available through the OpenAI API. No clue where this is going, just that it's going to be a ride.

## Code that's Currently Here
- A very simple image generation program that leverages Dall-E to generate 1024x1024 Images around any prompt you give it
- A simple sentiment analyzer that takes a prompt and then analyzes if it is positive, negative or neutral, and also returns a rating from 1 - 10, where 1 is the most negative and 10 is the most positive.
- The beginnings of a Summarization Application that leverages the Speech-To-Text Functionality of the Whisper-1 model
- A simple program that uses TikToken to see how many tokens an input prompt contains (This one's still a work in progress, additional features that allow prompts to be shortened will be added

## Random Info
If you want to use any of this code, you need to either use environment variables placed in a .env, within a folder called "Environment Variables", or you can just get rid of the environment variable code entirely and hard-code your keys into it (I don't recommend this, because if you ever end up uploading your code or changing your keys, you've got to go in and edit it in every single program).

Speaking of Keys, you need two of them. One's an "Organization Key" and OpenAI assigns one to you. The second one's an API key, which you need to generate (ideally per application). Both of these can be found by going to the OpenAI website at <https://platform.openai.com/overview>

Every program here will have a section at the top which initializes both keys, and if you're hardcoding these keys, just paste them between quotes and you're good to go!

## Learnings
The OpenAI models are extremely powerful, but you need to know how to use them. Prompt design is especially important (shocking, I know). Generating a lot of stuff results in OpenAI charging you for a lot of stuff (again: shocking, I know).

Always make sure that you're monitoring your usage. Use simpler, cheaper models for less complex processes.

Speech to text is a very expensive process, and for longer content, you can sometimes end up with far more tokens than your model can handle. I'm not sure how to deal with this yet, but I'm working on it 👀

And finally, PyDub requires you to copy executable files from the PyDub source folder to your working directory. And that is annoying. Very. Annoying.
