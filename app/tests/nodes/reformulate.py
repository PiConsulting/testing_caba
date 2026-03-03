import json
import time # usar time.perf_counter()
import requests
import pandas as pd
from pathlib import Path
from app.datasets.loader import load_test_cases

reformulate_dataset = load_test_cases('./app/data/raw/reformulate.xlsx')

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


def save_reformualte_responses(responses: list[dict], output_path: str = './app/data/processed/reformulate_outcome.json', pretty_print: bool = True): 
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
      raise
    
    
def reformulate_tests():
  raise NotImplementedError
  