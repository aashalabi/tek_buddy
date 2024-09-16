import ingest
from openai import OpenAI
import json
from time import time
from dotenv import load_dotenv
import os

from pathlib import Path
env_path = Path('../.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)

# Get the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = openai_api_key

client = OpenAI()
index = ingest.load_index()

boost = {
    'equipment_name': 2.2286308944548905,
    'maker': 1.3065317502078608,
    'type_of_maintenance': 2.7847555728963282,
    'frequency': 0.4028772934987217,
    'parts_required': 0.4007776344493833
}

def search(query, index=index, boost=boost):

    boost = boost
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


entry_template = '''
equipment_name: {equipment_name},
maker: {maker},
type_of_maintenance: {type_of_maintenance},
frequency: {frequency},
parts_required: {parts_required}
'''.strip()

def create_prompt(knowledge_results, question):

    context=''
    for doc in knowledge_results:
        context = context + entry_template.format(**doc) + '\n\n'

    prompt = f"""
    You're a appliance repair assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our database. 
    Only use the facts from the CONTEXT. If the CONTEXT doesn't contan the answer, return "NONE"
                
    QUESTION: {question}
                
    CONTEXT:
                
    {context}
    """.strip()
    prompt = prompt.format(question=question, context=context)
    return prompt

def llm(prompt, client, model='gpt-3.5-turbo'):
    response = client.chat.completions.create(
        model=model,    
        messages=[{"role": "user", "content": prompt}]
    )
    return (response.choices[0].message.content)

def rag(query, client=client):
    knowledge_results = search(query)
    prompt = create_prompt(knowledge_results, query)
    return llm(prompt, client)
