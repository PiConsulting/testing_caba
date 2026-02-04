import os

from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv('COSMOS_ENDPOINT')
DATABASE = os.getenv('DATABASE_NAME')

credential = DefaultAzureCredential()

client = CosmosClient(ENDPOINT, credential)
for db in client.list_databases():
  print(f'Database: {db['id']}')