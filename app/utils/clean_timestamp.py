import re  
  
def clean_timestamp(timestamp):
  match = re.search(r'outcome_(\d{8}-\d{6})\.json', timestamp)
  timestamp = match.group(1) if match else None
  return timestamp