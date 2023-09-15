def split_text_into_conversations(file_data):
    # Split the text by two consecutive line breaks
    split_text = file_data.split('\n\n')

    conversations = []

    # Iterate over the list of split text chunks
    for text in split_text:
        # If a chunk is not empty string (it could happen if there are more than two consecutive line breaks)
        if text != '':
            # Append each non-empty chunk into the conversation list
            conversations.append(text)

    # Return the list of conversations
    return conversations


def split_text_into_messages(file_data):
    # Split the text by two consecutive line breaks
    split_text = file_data.split('\n')

    messages = []

    # Iterate over the list of split text chunks
    for text in split_text:
        # If a chunk is not empty string (it could happen if there are more than two consecutive line breaks)
        if text != '':
            # Append each non-empty chunk into the conversation list
            messages.append(text)

    # Return the list of conversations
    return messages