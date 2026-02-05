import yaml
import json
from app.datasets.loader import load_multiple_test_cases
from app.datasets.validator import validate_dataset_schema
from app.datasets.preprocessing import preprocess_dataframe
from app.client.rag_client import RAGClient
from app.tests.run_tests import run_tests

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
}   

df = load_multiple_test_cases(file_list)
df = validate_dataset_schema(df)

with open('./app/config/config.yaml', 'r') as file:
  config_data = yaml.load(file, Loader= yaml.FullLoader) 
  
client = RAGClient(config_data)

save_responses_in_json, response_file_path = client.save_api_responses(responses)

with open(response_file_path, 'r', encoding='UTF-8') as f:
  data = json.load(f)

results = run_tests(
  config = test_config, 
  data = data, 
  df = df, 
  timestamp = str(response_file_path)
)