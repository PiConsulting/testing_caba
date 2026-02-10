import yaml
import json
from app.datasets.loader import load_multiple_test_cases
from app.datasets.validator import validate_dataset_schema

from app.client.rag_client import RAGClient
from app.tests.run_tests import run_tests
from app.utils.db import save_results_on_cosmos

file_list = [
  './app/data/raw/tramites.xlsx',
  './app/data/raw/accesibilidad.xlsx',
  './app/data/raw/descubrir.xlsx',
  './app/data/raw/solicitudes.xlsx',
  './app/data/raw/organigrama.xlsx'
]

test_config = {
  'TIMINGS': True,
  'TOKENS': True,
  'FOUNDRYS': True,
  'TRIAGE': True,
  'ROUTER': True,
  'GROUNDING': True,
  'SAVE_RESULTS': True,
}   

df = load_multiple_test_cases(file_list)
df = validate_dataset_schema(df)

with open('./app/config/config.yaml', 'r') as file:
  config_data = yaml.load(file, Loader= yaml.FullLoader) 
  
client = RAGClient(config_data)

responses = client.query_batch(df['user_input'],df['reference'])

save_responses_in_json, response_file_path = client.save_api_responses(responses)

with open(response_file_path, 'r', encoding='UTF-8') as f:
  data = json.load(f)

results = run_tests(
  config = test_config, 
  data = data, 
  df = df, 
  timestamp = str(response_file_path)
)

if test_config.get('SAVE_RESULTS'):
  save_results_on_cosmos(results=results)