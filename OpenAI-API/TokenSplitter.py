from nltk.tokenize import word_tokenize


def getTokenLength(prompt=None):
    if prompt is None:
        with open("transcription.txt") as f:
            transcription = f.readline()
    else:
        transcription = prompt

    tokenized_list = word_tokenize(transcription)
    input_size = len(tokenized_list)

    return input_size


print(getTokenLength())
