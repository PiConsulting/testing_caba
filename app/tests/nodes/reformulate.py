import os
import json
import time # usar time.perf_counter()
import requests
import pandas as pd
from pathlib import Path
from openai import AzureOpenAI
from app.datasets.loader import load_test_cases
from dotenv import load_dotenv
load_dotenv()

reformulate_dataset = load_test_cases('./app/data/raw/reformulate.xlsx')

deployment = "gpt-5-chat"

client = AzureOpenAI(
    api_version="2025-01-01-preview",
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key= os.getenv('AZURE_OPENAI_API_KEY'),
)

def send_reformulate_requests(config: dict, dataset: pd.DataFrame) -> list[dict]:
  all_responses = []
  headers = config.get('headers', {'Content-Type': 'application/json'})
  url = config['agent'].get('base_url')
  
  for _, row in dataset.iterrows():
    body = {
    'id': '',
    }
    questions = row['Pregunta']
    
    if '\n' in questions:
      questions = questions.split('\n')
      
      for question in questions:
        body['question'] = question
        
        try:
          response = requests.post(url=url, headers=headers, json=body)
          data = response.json()
          
          if body['id'] == '':
            body['id'] = data.get('id')
            
          all_responses.append(data)      
          
        except Exception as e:
          print(e)
      
  return all_responses


def save_reformualte_responses(responses: list[dict], output_path: str = './app/data/processed/results/reformulate_outcome.json', pretty_print: bool = True): 
    output_path = Path(output_path)
    output_path.parent.mkdir(parents= True, exist_ok=True)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    base_name = output_path.stem
    extension = output_path.suffix
    timestamped_path = output_path.parent / f"{base_name}_{timestr}{extension}"
    
    output_data = [item for item in responses]
    try:
      with open(timestamped_path, 'w', encoding='UTF-8') as f:
        if pretty_print:
          f.write(json.dumps(output_data, indent=2,   ensure_ascii=False))
          return str(timestamped_path), timestamped_path

    except Exception as e:
      print('Failed to save responses to JSON')
    

def _chat_completions(system_content: str, user_content):

  response = client.chat.completions.create(
    messages=[
        {
          "role": "system",
          "content": system_content,
        },
        {
          "role": "system",
          "content": user_content,
        }
    ],
    max_tokens=500,
    temperature=0,
    top_p=1.0,
    model=deployment,
    response_format={"type": "json_object"}
  )
    
  return response.choices[0].message.content


def _load_prompt(filepath: str) -> str:
  try:
    with open(filepath, 'r') as file:
      prompt = file.read()
  except Exception as e:
    print(e)
  return prompt


def reformulate_tests(responses: list[dict]):
  results = []
  system_role = _load_prompt('./app/prompts/reformulate_system.txt')
  user = _load_prompt('./app/prompts/reformulate_user.txt')
  
  for response in responses:
    messages = response.get("messages", [])
    user_role = user.format(messages = messages)
    score = _chat_completions(system_role, user_role)
    score_json = json.loads(score)
    results.append(score_json)
  
  # average_score = sum([eval["score"] for eval in results]) / len(results)
  average_score = sum([item['score'] for item in results]) / len(results)
  return round(average_score, 2)  