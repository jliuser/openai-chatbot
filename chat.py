# imports
import ast  # for converting embeddings saved as strings back to arrays
from openai import OpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
# import tiktoken  # for counting tokens
import os # for getting API token from env variable OPENAI_API_KEY
# from scipy import spatial  # for calculating vector similarities for search

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

with open('secret_keys.yaml', 'r') as file:
    openai_key = file['openai_key']

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", openai_key))


def create_embeddings():
    # takes in dataframe, outputs dataframe of <text, embedding>, where `text`` is a column of concatenated values
    pass


def search_for_dataset(user_response: str):
    # could create embedding of names of datasets to user response
    create_embeddings()
    pass

def rank_rows_by_relatedness(embedded_texts: pd.DataFrame, embedded_query: str):
    # ranks rows based on similarity to query
    pass


# Ask user
"what is your query about?" # could list out dataset options/categories

# pass user response to below function
search_for_dataset()

# create & store embeddings from the surfaced dataset
create_embeddings()

# ask user what they would like to know about the dataset
"what is your query"

# rank strings
rank_rows_by_relatedness()

# prompt chatgpt to respond to user given top K similar data chunks