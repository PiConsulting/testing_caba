import pandas as pd
import json

def load_test_cases(path: str = './app/data/raw/input.xlsx') -> pd.DataFrame:
  
  if path.endswith('.csv'):
    return pd.read_csv(path)
  
  elif path.endswith('.xlsx'):
    return pd.read_excel(path)
  
  elif path.endswith('.json'):
    with open(path, encoding='utf-8') as f:
      dict_train = json.load(f)
    return pd.DataFrame.from_dict(dict_train)
  
  else:
    raise ValueError('ValueError: Unsupported file format')
  
  

def load_multiple_test_cases(list_of_files: list[str]) -> pd.DataFrame:
  
  dataframes = [load_test_cases(df) for df in list_of_files]
    
  return pd.concat(dataframes, ignore_index=True)  