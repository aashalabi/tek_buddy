import ingest
from openai import OpenAI
import json
from time import time
from dotenv import load_dotenv
import os
import openai 

from pathlib import Path

#env_path = Path('../.env')
# Load the .env file
#load_dotenv(dotenv_path=env_path)
load_dotenv() 
# Get the API key
#openai_api_key = os.getenv("OPENAI_API_KEY")
#os.environ['OPENAI_API_KEY'] = openai_api_key


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
    start_time = time()
    #response = client.chat.completions.create(
    response = openai.chat.completions.create(
        model=model,    
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content

    token_stats = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    end_time = time()
    response_time = end_time - start_time
    
    return answer, token_stats, response_time

def rag(query, client=client, model_choice='openai/gpt-3.5-turbo'):
    model = model_choice.split('/')[-1]
    print('model')
    print(model)
    print('client', type(client))

    knowledge_results = search(query)
    prompt = create_prompt(knowledge_results, query)
    return llm(prompt=prompt, client=client, model=model)

def evaluate_relevance(question, answer):
    prompt_template = """
    You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
    Your task is to analyze the relevance of the generated answer to the given question.
    Based on the relevance of the generated answer, you will classify it
    as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

    Please classify valid company names as "RELEVANT" answer.
    Please consider part or parts required as "RELEVANT".
    Please consider answer "RELEVANT" as long answer doesn't conflict with technical facts about the machine.

    Here is the data for evaluation:

    Question: {question}
    Generated Answer: {answer}

    Please analyze the content and context of the generated answer in relation to the question
    and provide your evaluation in parsable JSON without using code blocks:

    {{
      "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
      "Explanation": "[Provide a brief explanation for your evaluation]"
    }}
    """.strip()

    prompt = prompt_template.format(question=question, answer=answer)
    evaluation, tokens, _ = llm(prompt, 'openai/gpt-3.5-turbo')
    
    try:
        json_eval = json.loads(evaluation)
        return json_eval['Relevance'], json_eval['Explanation'], tokens
    except json.JSONDecodeError:
        return "UNKNOWN", "Failed to parse evaluation", tokens


def calculate_openai_cost(model_choice, tokens):
    openai_cost = 0

    if model_choice == 'openai/gpt-3.5-turbo':
        openai_cost = (tokens['prompt_tokens'] * 0.0015 + tokens['completion_tokens'] * 0.002) / 1000
    elif model_choice in ['openai/gpt-4o', 'openai/gpt-4o-mini']:
        openai_cost = (tokens['prompt_tokens'] * 0.03 + tokens['completion_tokens'] * 0.06) / 1000

    return openai_cost
def get_answer(query, model_choice='openai/gpt-3.5-turbo'):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    answer, tokens, response_time = rag(query, client=client, model_choice= model_choice)
    
    relevance, explanation, eval_tokens = evaluate_relevance(query, answer)

    openai_cost = calculate_openai_cost(model_choice, tokens)
 
    return {
        'answer': answer,
        'response_time': response_time,
        'relevance': relevance,
        'relevance_explanation': explanation,
        'model_used': model_choice,
        'prompt_tokens': tokens['prompt_tokens'],
        'completion_tokens': tokens['completion_tokens'],
        'total_tokens': tokens['total_tokens'],
        'eval_prompt_tokens': eval_tokens['prompt_tokens'],
        'eval_completion_tokens': eval_tokens['completion_tokens'],
        'eval_total_tokens': eval_tokens['total_tokens'],
        'openai_cost': openai_cost
    }
