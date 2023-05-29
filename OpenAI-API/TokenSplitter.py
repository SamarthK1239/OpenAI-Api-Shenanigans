import tiktoken


def getInputTokenSize(model, input_message):
    encoding = tiktoken.encoding_for_model(model)
    tokenized = encoding.encode(input_message)
    length = len(tokenized)

    returned_list = [length, encoding.max_token_value]

    return returned_list
