![tek_buddy_image6.png](README_files/cf1886d9-5d4a-4da5-83c4-f4773c27ea6f.png)

# Tech Buddy AI

## Problem Description

#### Introducing Tech Buddy AI: Your Intelligent Appliance Repair Assistant

```
Welcome to TechBuddy AI, a cutting-edge Retrieval-Augmented Generation (RAG) Large Language Model (LLM) application designed specifically for appliance repair professionals. TechBuddy AI combines the power of advanced natural language processing with a vast database of technical knowledge to provide instant, accurate, and context-aware assistance for all your repair challenges. 
```
```
Whether you're troubleshooting a complex refrigerator compressor issue or need step-by-step guidance for replacing a dishwasher control board, TechBuddy AI is your go-to digital partner. By leveraging the latest in AI technology and continually updated repair manuals, service bulletins, and expert knowledge, this innovative tool empowers technicians to work more efficiently, reduce diagnostic time, and increase first-time fix rates. Say goodbye to time-consuming manual searches and hello to smarter, faster repairs with TechBuddy AI – your intelligent assistant in the world of appliance maintenance and repair.
```

# Project Overview

### Use cases
```
TechBuddy AI: Smart Appliance Repair Assistant

TechBuddy AI is a RAG LLM app for appliance repair pros. It offers:
- Instant, accurate help for repair challenges
- Vast technical knowledge database
- Context-aware assistance
- Up-to-date repair info and expert knowledge
- Improved efficiency and first-time fix rates
- Streamline your repair process with TechBuddy AI.
```

## Data Set
```
The data set contains various elements about appliances including:
- Type of appliance (Dishwasher,Refrigerator, etc .. )
- Equipment name/model
- Maker
- Maintenace type
- Frquency
- Spare parts required for th job

The data set is generated using Claude and contains 1756 records
```

## Technologies
```
Knowledge base: Elasticsearch
LLM: openai
UI: streamlit
Monitoring: Grafana
API: Flask
Containerization: Docker
```

## Install Requirements
```
- Install Docker deskop (windows)
- Python above 3.9 version will work
- pip install -r requirements.txt
- create .env file and add various keys such as openai key
```

## RAG flow, RAG evaluation and retreival
```
The following results without boosting the index:
{'hit_rate': 0.8553530751708428, 'mrr': 0.6823731333839534}

With boosting:
{'hit_rate': 0.8490888382687927, 'mrr': 0.7397254763712625}

I used Chat gpt 3.5 turbo, may using better LLm could imporove the hit rate and mmr

Best boosting paramters:
boost = {
        'equipment_name': 2.2286308944548905,
        'maker': 1.3065317502078608,
        'type_of_maintenance': 2.7847555728963282,
        'frequency': 0.4028772934987217,
        'parts_required': 0.4007776344493833
    }

Using gpt-3.5-turbo among 1756 records, we have:
- RELEVANT           0.428815
- PARTLY_RELEVANT    0.378132
- NON_RELEVANT       0.192483
- Non_Relevant       0.000569

The LLM explanation  considers one part as partial becuase query asks for parts. Therefore, partial answer can be considered as RELEVANT.

Here is sample question and explanation:
- Question: 'What parts are required for cleaning the condenser fan blade on the MFI2269FRZ?'
- Explanation: 'The generated answer only mentions a soft cloth as the part required for cleaning the condenser fan blade, which is not accurate. The question asks for all the parts required, not just one.'


For `gpt-4o-mini`, in a sample with 200 records, the results are:

- RELEVANT           0.428815
- PARTLY_RELEVANT    0.378132
- NON_RELEVANT       0.192483
- Non_Relevant       0.000569
```

## Interface
```
Using Flask framework to serve the api and Minsearch  from https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/minsearch.py

cmd: python app.py
```
### Question API
```
URL=http://localhost:5000
QUESTION="What parts are required for cleaning the condenser fan blade on the MFI2269FRZ?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question

Result:
{
  "answer": "Soft cloth.",
  "conversation_id": "b50da356-c62d-4991-b68d-dc942f253fa3",
  "question": "What parts are required for cleaning the condenser fan blade on the MFI2269FRZ?"
}
```
### Feedback API
```
$ ID="b50da356-c62d-4991-b68d-dc942f253fa3"
$ FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

$ curl -X POST     -H "Content-Type: application/json"     -d "${FEEDBACK_DATA}"     ${URL}/feedback
{
  "message": "Feedback received for conversation b50da356-c62d-4991-b68d-dc942f253fa3: 1"
}
```

## Code
```
The code for the application is in the [`tek_buddy`](tek_buddy) folder:

- [`app.py`] - the Flask API, the main entrypoint to the application
- [`rag.py`] - the main RAG logic for building the retrieving the data and building the prompt
- [`ingest.py`] - loading the data into the knowledge base
- [`minsearch.py`] - an in-memory search engine
```

## Notebooks
```
- directory notebooks contains various notebooks for expereiments
```

## env file
```
OPENAI_API_KEY=xxxx
DATA_PATH=..\data\data_cleaned.csv

APP_PORT=5000

TZ=America/Los_Angeles

# PostgreSQL Configuration
POSTGRES_HOST=postgres
POSTGRES_DB=tek_buddy_db
POSTGRES_USER=your user name
POSTGRES_PASSWORD= your password
POSTGRES_PORT=5433

## Ingestion pipeline

Semi-automated ingestion of the dataset into the knowledge base
```
## Running the app
```
cmd: python app.py
```


```python

```
