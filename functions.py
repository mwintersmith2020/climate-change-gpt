#__import__('pysqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sys
import os
import json
import argparse
import logging
import time
import pdb
import requests
import streamlit as st
import sqlite3
import chromadb
import replicate
# import pandas as pd


from chromadb.config import Settings
from chromadb import Documents
from datetime import datetime

import streamlit as st
#from streamlit_gsheets import GSheetsConnection

#---------------------------
USER_IP = '<unknown>'
LOGGING_DF = None
GSHEET_CONN = None

if "name" not in st.session_state:
    st.session_state["name"] = "" 

# Define the embedding function
class ReplicateEmbeddingFunction:
    def __call__(self, input: Documents):
        embedding_dict = replicate.run(
            embeddings_model_name,
            input={"text": json.dumps(input)}
        )
        return [item["embedding"] for item in embedding_dict]

# def initializeGSheet():
#     return st.connection("gsheets", type=GSheetsConnection)

# def initializeDataFrame(conn):
#     return conn.read(worksheet="st_user_logs")

# def appendDataFrame(input_df, user_ip, message):
#     new_entry = {
#         'timestamp': [datetime.now()],
#         'IP': [user_ip],
#         'log_message': [message]
#     }
#     append_df = pd.DataFrame(new_entry)
#     output_df = pd.concat([input_df, append_df], ignore_index=True)
#     return output_df

# def logUserFeedback(message):
#     # global LOGGING_DF  # Ensure LOGGING_DF is treated as a global variable
#     global GSHEET_CONN

#     logging.info(f"{USER_IP}: {message}")
#     USER_NAME = st.session_state["name"]
    
#     # Refresh & append to sheet ...
#     LOGGING_DF = GSHEET_CONN.read(worksheet="st_user_logs")
#     LOGGING_DF = appendDataFrame(LOGGING_DF, USER_IP, f"[{USER_NAME}] {message}")
#     GSHEET_CONN.update(worksheet="st_user_logs", data=LOGGING_DF)

def getContext(criterion_text):
    CLEAN_FILTER = criterion_text.replace(':green[','')

    results = collection.query(
        query_texts=criterion_text,
        n_results=target_source_chunks,
            # where={
            #     'source': 'ca-voter-guide-2024' if CLEAN_FILTER.lower().startswith('prop') 
            #        else 'san-diego-voter-guide-2024' if CLEAN_FILTER.lower().startswith('measure') 
            #        else ''
            #     },
    )
    citations = '\n'.join(results['documents'][0])
    
    return citations

def getPrediction(prompt_template):
    model_response = replicate.run(
        model,
        input={"prompt": prompt_template}
    )

    # Concatenate the response into a single string.
    response = ''.join([str(s) for s in model_response])
    return response

def generatePrediction(USER_PROMPT):
    # logUserFeedback(f"PROPOSITION= {PROPOSITION}")
    # logUserFeedback(f"USER_PROMPT= {USER_PROMPT}")

    CITATIONS = getContext(USER_PROMPT)
    PROMPT_TEMPLATE = f"""
This is scientific journal about climate change.  You will be given a USER_PROMPT and a list of CITATIONS:

Make sure that your responses is strictly limited to CITATIONS.  
Do not include information not found in CITATIONS.
Write your responses at a level a high schooler can understand.

USER_PROMPT: {USER_PROMPT}

CITATIONS: {CITATIONS}
"""
    text = getPrediction(PROMPT_TEMPLATE)

    # Now do some post-processing ...
    # ... to use a markdown-compatible bullet symbol ...
    # ... to prevent '$' from trigger latex math-symbol mode ...
    modified_text = text.replace('• ','* ').replace('$','\\$')
    return modified_text

# -------------------- Start initialization --------------------

# st.set_page_config(layout="wide")

# model = os.environ.get("MODEL_NAME", "llama3")
# embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "hkunlp/instructor-large")

# -------------------- Initialize logging --------------------

logging.basicConfig(level=logging.INFO)
logging.info("------------ New Session ------------")
logging.info(f"Checking SQLite version: {sqlite3.sqlite_version}")
logging.info("Initializing variables ...")
ip_request = requests.get('https://api.ipify.org?format=json')
USER_IP = ip_request.json()['ip']
logging.info(f"USER_IP= {USER_IP}")

# logging.info("Initializing google sheets ...")
# GSHEET_CONN = initializeGSheet()

# logging.info("Initializing dataframe logging ...")
# LOGGING_DF = initializeDataFrame(GSHEET_CONN)

# -------------------- Initialize models --------------------

model = os.environ.get("MODEL_NAME", "llama3")
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "hkunlp/instructor-large")
persist_directory = os.environ.get("PERSIST_DIRECTORY", "db")
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',3))

logging.info("Initializing chroma db...")
client = chromadb.PersistentClient(path=persist_directory, settings=Settings(anonymized_telemetry=False))

logging.info("Initializing embedding function...")
embedding_function = ReplicateEmbeddingFunction()

logging.info("Loading collection...")
collection = client.get_collection(name="climate-change-summary", embedding_function=embedding_function)

logging.info("Done.")
