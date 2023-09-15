import time
import openai
from langchain.memory import ConversationBufferWindowMemory
from ReadingLevelScore import ReadingLevelScore
import random
import os
import langchain
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from datetime import datetime
from pydantic import BaseModel, Field
import pinecone
from langchain.vectorstores import Pinecone
from langchain.document_loaders import JSONLoader
import json
from pathlib import Path
from pprint import pprint


### CONFIG ###
model_name = 'gpt-4'
# model_name = 'gpt-3.5-turbo'
# model_name = 'gpt-3.5-turbo-16k'
embedding_model_name = 'text-embedding-ada-002'

### FILE PATHS ###
file_path="./memory/goat.json"

### CHILD INFO ###
child_info = "The child prompting you is in grade 7, is 12 years old, and is at their typical reading level."
# The questions from the kid!
child_message_grade_7 = """
I want to be a voice actor someday for an anime like Full Metal Alchemist! What anime should I watch next that is like it?
"""
questions = [
    child_message_grade_7
]

def load_json(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the contents of the file
        json_data = file.read()
    # Print the contents to the console
    print("JSON DATA:")
    print(json_data)

    loader = JSONLoader(
        file_path=file_path,
        jq_schema='.wisdom[].description')

    data = loader.load()
    return data



def main():
    pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENVIRONMENT"])
    index_name = os.environ["PINECONE_INDEX"]
    if index_name in pinecone.list_indexes():
        print(f"Index {index_name} already exists, skipping creation")
    else:
        # we create a new index
        pinecone.create_index(
            name=index_name,
            metric='dotproduct',
            dimension=1536  # 1536 dim of text-embedding-ada-002
        )
        # wait for index to be initialized
        while not pinecone.describe_index(index_name).status['ready']:
            time.sleep(1)

    embed = OpenAIEmbeddings(
        model=embedding_model_name,
        openai_api_key=os.environ['OPENAI_API_KEY']
    )
    loader = PyPDFLoader("1. Top Tips for Parents Author Women Work The National Network for Women.pdf")
    books = loader.load_and_split()
    vectorstore = Pinecone.from_documents(documents=books, embedding=embed, index_name=os.environ["PINECONE_INDEX"])
    print("Vectorstore created successfully")

    loaded_json = load_json(file_path)
    vectorstore.add_documents(loaded_json)

    openai.api_key = os.environ['OPENAI_API_KEY']
    model_list_string = ''
    counter = 0
    for model in openai.Model.list()['data']:
        model_list_string += "--  " + model.id + "  --"
        counter += 1
        if counter % 10 == 0:
            model_list_string += '\n'
    print(model_list_string)

    model = ChatOpenAI(model_name=model_name, openai_api_key=os.environ['OPENAI_API_KEY'])
    qa = ConversationalRetrievalChain.from_llm(model, retriever=vectorstore.as_retriever())

    chat_history = []
    my_string = ""

    for question in questions:
        enhancer = '''
        CONTEXT: The child prompting you is in grade 7, is 12 years old, and is at their typical reading level.
        respond to them with care and compassion. and try to be as helpful as possible, and make sure you always respond
        with a suggestion or a question. If suggesting a game to play, make sure to include a link to the game.
        YOUR RESPONSE: "
        '''
        enhanced_question = enhancer + question
        result = qa({"question": enhanced_question, "chat_history": chat_history})
        chat_history.append((question, result["answer"]))
        print(f"Question: \n {question} \n")
        print(f"Answer: \n {result['answer']} \n")
        print("------------------------------------------------------------- \n")
        my_string += result['answer']
        marvin_reading_level_scorer(result['answer'])

    # Read the current file contents
    with open('kinship_conversations.txt', 'r') as f:
        file_data = f.read()

    # append the contents to the file
    file_data += my_string

    # Open the file in write mode
    with open('kinship_conversations.txt', 'w') as f:
        # Write the string to the file
        f.write(file_data)


def marvin_reading_level_scorer(companion_response: str):
    companion_response = child_info + companion_response
    reading_level_score = ReadingLevelScore(companion_response)
    print(f'Reading level score = {reading_level_score}\n')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# create models to represent the state of our Companion
class Companion(BaseModel):
    title: str
    description: str = None
    due_date: datetime = None
    done: bool = False


class Message(BaseModel):
    text: str
    timestamp: datetime = None


class Conversation(BaseModel):
    sent_messages: list[Message] = []
    received_messages: list[Message] = []


class CompanionConversations(BaseModel):
    conversations: list[Conversation] = []


if __name__ == '__main__':
    # # create the app with an initial state and description
    # Companion = AIApplication(
    #     state=CompanionConversations(),
    #     description=(
    #         "A conversation with a Companion that can help you with anything you need be providing information, and guidance."
    #     ),
    # )
    main()
