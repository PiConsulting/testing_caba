import re
import os
import pandas as pd
import json
from app.tests.timings import timing_tests
from app.tests.tokens import token_tests
from app.tests.foundrys import foundrys_tests
from app.tests.nodes.triage import triage_tests
from app.tests.nodes.router import router_tests, create_validation_dataset
from app.tests.nodes.grounding import grounding_tests


def run_tests(config: dict, data: dict, df: pd.DataFrame, timestamp: str) -> dict:
  
  match = re.search(r'outcome_(\d{8}-\d{6})\.json', timestamp)
  timestamp = match.group(1) if match else None
  
  reports = []
  
  results = {
    'timestamp': timestamp,
    'nodes': {}
  }
  
  if config.get('TIMINGS',{'test': False}).get('test', False):
    timings_result, timings_report = timing_tests(data=data)
    results['timings'] = timings_result
    if config.get('TIMINGS', {'report': False}).get('report', False):
      reports.append([timings_report, 'timings'])
  
    
  if config.get('TOKENS',{'test': False}).get('test', False):
    tokens_result, tokens_report = token_tests(data=data)
    results['tokens'] = tokens_result
    if config.get('TOKENS', {'report': False}).get('report', False):
      reports.append([tokens_report, 'tokens'])
  
    
  if config.get('FOUNDRYS',{'test': False}).get('test', False):
    foudrys_result = foundrys_tests(data=data)
    results['foundrys'] = foudrys_result
    
  
  if config.get('TRIAGE',{'test': False}).get('test', False):
    triage_result, triage_report = triage_tests(data=data)
    results['nodes']['triage'] = triage_result
    if config.get('TRIAGE', {'report': False}).get('report', False):
      reports.append([triage_report, 'triage'])
    
    
  if config.get('ROUTER',{'test': False}).get('test', False):
    validation = create_validation_dataset(df)
    router_result, router_report = router_tests(data=data, validation=validation)
    results['nodes']['router'] = router_result
    if config.get('ROUTER', {'report': False}).get('report', False):
      reports.append([router_report, 'router'])
      
    
  if config.get('GROUNDING',{'test': False}).get('test', False):
    grounding_result, grounding_report = grounding_tests(data)
    results['nodes']['grounding'] = grounding_result
    if config.get('GROUNDING', {'report': False}).get('report', False):
      reports.append([grounding_report, 'grounding'])
    
  
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
    
  return results