import os
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

def save_results_on_cosmos(results: dict):

  ENDPOINT = os.getenv('COSMOS_ENDPOINT')
  KEY = os.getenv('COSMOS_KEY')
  DATABASE = os.getenv('DATABASE_NAME')
  CONTAINER = 'datasources'

  client = CosmosClient(ENDPOINT, credential=KEY)
  database = client.get_database_client(DATABASE)
  container = database.get_container_client(CONTAINER)
  
  results['id'] = results.get('timestamp')
  
  response = container.create_item(body=results)
  
  print("Item created:", response)