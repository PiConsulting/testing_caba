import requests
import pandas as pd

def send_requests_for_reformulate(config: dict,
                  dataset: list[list],
                  url: str):
  
  responses = []

  for i, question in enumerate(dataset):
    