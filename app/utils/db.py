import os
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv('COSMOS_ENDPOINT')
KEY = os.getenv('COSMOS_KEY')
DATABASE = os.getenv('DATABASE_NAME')

client = CosmosClient(ENDPOINT, credential=KEY)

database = client.get_database_client(DATABASE)