# Kinship Backend Development Guide

This guide helps developers understand and extend the `app.py` file of the `kinship-backend` project.

## Overview

The `app.py` file is the main entry point of the application. It initializes the Pinecone vector store, loads documents, creates embeddings, sets up a conversational retrieval chain using OpenAI's GPT-3.5-turbo model, manages conversation history, and writes the conversation to a text file.

## Setup 

Before running the application, you need to set the following environment variables. Create a `.env` in the root directory and add these variables:

```
PINECONE_API_KEY=<your_pinecone_api_key>
PINECONE_ENVIRONMENT=<your_pinecone_environment>
PINECONE_INDEX_NAME=<your_pinecone_index_name>
OPENAI_API_KEY=<your_openai_api_key>
```
Email `connor@kinshipcompaions.org` to obtain the respective API keys.

## Running the Application

1. Open `app.py` in Pycharm and scroll to the bottom.
2. Right-click the green arrow next to the `__main__()` function.
3. Edit the run configuration to enter your environment variables after the default `PYTHONBUFFERED` variable. Separate each variable with a semicolon (`;`) and leave no whitespace.
4. Click OK.
5. Click the green arrow in the top right to run the application.

## Code Documentation

### Main Function

The `main()` function in `app.py` does the following:

- Initializes Pinecone and checks if the index specified in the environment variable exists. If not, it creates a new index.
- Loads documents from a PDF file and creates embeddings using the OpenAI model.
- Sets up a conversational retrieval chain using the OpenAI model and the Pinecone vector store.
- Loops through a list of questions, enhances them with additional context, and retrieves answers using the retrieval chain.
- Writes the conversation history to a text file.

### Additional Functions

The `marvin_reading_level_scorer()` function calculates the reading level score for the companion's response.

The `Companion`, `Message`, `Conversation`, and `CompanionConversations` classes are models used to represent the state of the Companion.

## Extending the Application

To extend the application, modify the `questions` list in `app.py` to include more questions. You can also modify the `main()` function to change how the application handles conversations.