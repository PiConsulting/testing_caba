import json

def clean_responses_load_testing(load_filename: str, 
                                 processed_filename: str):
  response_file_path = f'{load_filename}.json'
  with open(response_file_path, 'r', encoding='utf-8') as f:
    corrupted_data = json.load(f)
    
  fixed_data = []
  errors = []
  
  for i, item in enumerate(corrupted_data):
    try:
      if not item or not item.strip():
          errors.append(f"Item {i}: Empty string")
          continue
      
      parsed_item = json.loads(item)
      fixed_data.append(parsed_item)
      
    except json.JSONDecodeError as e:
      errors.append(f"Item {i}: {str(e)} - Content: {item[:100]}")
      continue
    
  with open(f'./app/data/processed/load/{processed_filename}.json', 'w', encoding='utf-8') as f:
    json.dump(fixed_data, f, indent=2, ensure_ascii=False)
