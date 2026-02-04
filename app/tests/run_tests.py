import re
import pandas as pd
import json
from app.tests.timings import timing_tests
from app.tests.tokens import token_tests
from app.tests.nodes.triage import triage_tests
from app.tests.nodes.router import router_tests, create_validation_dataset
from app.tests.nodes.grounding import grounding_tests

def run_tests(config: dict, data: dict, df: pd.DataFrame, timestamp: str) -> dict:
  
  match = re.search(r'outcome_(\d{8}-\d{6})\.json', timestamp)
  timestamp = match.group(1) if match else None
  
  results = {
    'timestamp': timestamp,
    'nodes': {}
  }
  
  if config.get('TIMINGS'):
    timings_result = timing_tests(data=data)
    results['timings'] = timings_result
    
  if config.get('TOKENS'):
    tokens_result = token_tests(data=data)
    results['tokens'] = tokens_result
    
  if config.get('TRIAGE'):
    triage_result = triage_tests(data=data)
    results['nodes']['triage'] = triage_result
    
  if config.get('TRIAGE'):
    validation = create_validation_dataset(df)
    router_result = router_tests(data=data, validation=validation)
    results['nodes']['router'] = router_result
    
  if config.get('GROUNDING'):
    grounding_result = grounding_tests(data)
    results['nodes']['grounding'] = grounding_result
  
  with open(f'./app/data/processed/results_{timestamp}.json', 'w') as fp:
    json.dump(results, fp, indent=2)
    
  return results