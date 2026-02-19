import os
import pandas as pd
import json

def generate_reports(config:dict, results:dict, timestamp: str, reports: list[list]):
  path = config.get('PATH', '')
  if path != '':
    path += timestamp
    try:
      os.makedirs(path)
    except OSError:
      pass
    
  for report in reports:
    df, name = report[0], report[1]
    df.to_excel(f'{path}/{name}.xlsx')
    
    with open(f'./app/data/processed/results_{timestamp}.json', 'w') as fp:
      json.dump(results, fp, indent=2)