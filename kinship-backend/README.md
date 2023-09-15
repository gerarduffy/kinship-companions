# kinship-backend

Kinship Backend Development Guide

This guide will help you understand and develop in the app.py file of the kinship-backend project.
Overview

The app.py file is the main entry point of the application. It initializes the Pinecone vector store, loads documents, creates embeddings, and sets up a conversational retrieval chain using OpenAI's GPT-3.5-turbo model. It also handles the conversation history and writes the conversation to a text file.
Setup

Before running the application, you need to set up the environment variables. Create a .env file in the root directory and add the following variables:

- PINECONE_API_KEY: Your Pinecone API key.
- PINECONE_ENVIRONMENT: The Pinecone environment to use.
- PINECONE_INDEX_NAME: The name of the Pinecone index.
- OPENAI_API_KEY: Your OpenAI API key.

Email connor@kinshipcompaions.org to get api keys.

Running the Application

Open app.py in Pycharm and scroll to the bottom, then right click the green arrow next to the
    __main__() function.

Edit the run config to enter your environment variables after the default PYTHONBUFFER variable by seperating each variable with a ; and leaving no whitespace.

Then click OK, and click the green arrow in the top right.

### CODE DOCS
Main Function

The main() function in app.py does the following:

- Initializes Pinecone and checks if the index specified in the environment variable exists. If not, it creates a new index.
- Loads documents from a PDF file and creates embeddings using the OpenAI model.
- Sets up a conversational retrieval chain using the OpenAI model and the Pinecone vector store.
- Loops through a list of questions, enhances them with additional context, and retrieves answers using the retrieval chain.
- Writes the conversation history to a text file.

Additional Functions

The marvin_reading_level_scorer() function calculates the reading level score of the companion's response.

The Companion, Message, Conversation, and CompanionConversations classes are models to represent the state of the Companion.
Extending the Application

To extend the application, you can modify the questions list in app.py to include more questions. You can also modify the main() function to change the way the application handles conversations.