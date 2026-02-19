import yaml
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
  'TIMINGS': {'test': True, 'report': False},
  'TOKENS': {'test': True, 'report': False},
  'FOUNDRYS': {'test': True, 'report': False},
  'TRIAGE': {'test': True, 'report': False},
  'ROUTER': {'test': True, 'report': False},
  'GROUNDING': {'test': True, 'report': False},
  'SAVE_RESULTS': False,
  # 'PATH': './app/data/processed/reports/report'
}     

df = load_multiple_test_cases(file_list)
df = validate_dataset_schema(df)

with open('./app/config/config.yaml', 'r') as file:
  config_data = yaml.load(file, Loader= yaml.FullLoader) 
  
client = RAGClient(config_data)

responses = client.query_batch(df['user_input'],df['reference'])

save_responses_in_json, response_file_path = client.save_api_responses(responses)

results = run_tests(
  config = test_config, 
  data = responses, 
  df = df, 
  timestamp = str(response_file_path)
)

if test_config.get('SAVE_RESULTS'):
  save_results_on_cosmos(results=results)