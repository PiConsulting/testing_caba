import json
import time # usar time.perf_counter()
import copy
import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path

import math


class RAGClient:
  
  def __init__(self, config):
    self.base_url = config['agent']['base_url']
    self.headers = config.get("headers") if isinstance(config.get("headers"), dict) else {}
    self.body = config.get("body") if isinstance(config.get("body"), dict) else {}
    self.timeout = config['agent'].get('timeout', 3)
    self.max_retries = config['agent'].get('max_retries', 3)
    
    
  def query(self, question: str) -> dict:
    
    attempt = 0
    
    while attempt < self.max_retries:
      req_body = copy.deepcopy(self.body)
      req_body['question'] = question
      try:
        response = requests.post(url=self.base_url,
                                 json=req_body,
                                 headers=self.headers)
                
        if response.status_code == 200:
          # print(f"Request successful on attempt: {attempt + 1}") # sacar
          data = response.json()
          return data
        
        elif response.status_code in [400, 429, 503]:
          attempt += 1
          # print(f"Problem with response status code: {response.status_code}. Attempt: {attempt}")
          time.sleep(self.timeout)
          
      except requests.exceptions.RequestException as e:
        attempt += 1
        time.sleep(self.timeout)
        print(f"Network error: {e}")
        
    print("Max retries exceeded")
    return None
   
  
  def query_batch(self, user_inputs: pd.Series, references: pd.Series) -> list[dict]:
    
    if len(user_inputs) != len(references):
      raise ValueError(f'user_inputs: {len(user_inputs)} and references: {len(references)} are not the same')
    
    if len(user_inputs) == 0:
      raise(ValueError(f'Input of length = 0'))
    
    results = []
    
    iterator = tqdm(
      zip(user_inputs, references),
      total = len(user_inputs),
      desc="Processing queries"
    )
    
    for question, reference in iterator:

      try:
        response = self.query(question)

        # if math.isnan(reference):
        #   reference = ''
          
        results.append(
          {
            'question': question,
            'reference': reference,
            'answer': response.get('answer', ''),
            # 'context': response.get('context', []),
            ## PARCHE PARA CABA
            # 'context': response['partial_answers']['agent_request']['data'].get('context', []),
            'context': response.get('partial_answers', {}).get('agent_request', {}).get('data', {}).get('context', []),
            ## PARCHE PARA CABA
            'response': response,
            'metadata': response.get('node_metadata', {})
          }
        )

        time.sleep(0.1)
      
      except Exception as e:
        print(f"Network Error: {e}")
      
    return results
  
  
  def save_api_responses(self,
                         responses: list[dict],
                         output_path: str = './app/data/processed/outcome.json',
                         pretty_print: bool = True) -> str:
  
  
    output_path = Path(output_path)
    output_path.parent.mkdir(parents= True, exist_ok=True)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    base_name = output_path.stem
    extension = output_path.suffix
    timestamped_path = output_path.parent / f"{base_name}_{timestr}{extension}"

    output_data = [item.get('response') for item in responses]

    try:
      with open(timestamped_path, 'w', encoding='UTF-8') as f:
        if pretty_print:
          f.write(json.dumps(output_data, indent=2,   ensure_ascii=False))
          return str(timestamped_path), timestamped_path

    except Exception as e:
      print('Failed to save responses to JSON')
      raise