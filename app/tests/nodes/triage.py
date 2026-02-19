import pandas as pd

def triage_tests(data: list[dict],
                 ouput_file_name: str = './app/data/processed/triage.xlsx', 
                 generate_report: bool = False) -> dict:
  
  triages = []
  # agregar route para evaluaciaon individual hacia cada agente
  output_columns = ['question', 'tag', 'comparison', 'reason']
  
  for item in data:
    if item is None or 'ok' in item:
      continue
    
    og_question = item['original_question']
    tag = item['partial_answers'].get('triage', {'task': ''}).get('task')
    reasoning = item['partial_answers'].get('triage', {'reason': ''}).get('reason')
    value = 1 if tag == 'question_answering' else 0
    
    triages.append([og_question, tag, value, reasoning])
    
  df_results = pd.DataFrame(triages, columns= output_columns)
  metrics = generate_triage_metrics(df_results)
  
  if generate_report:
    df_results.to_excel(ouput_file_name, index=True)
  
  return metrics
  

def generate_triage_metrics(df:pd.DataFrame) -> dict:
  
  df_copy = df.copy()
  
  total = int(df_copy['tag'].count())
  value = int(df_copy['comparison'].values.sum())
  
  result = {
    'positives': value,
    'total': total,
    'result': round((value/total)*100, 2)  
  }
  
  return result
    
    