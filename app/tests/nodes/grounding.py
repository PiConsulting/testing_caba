import pandas as pd

def grounding_tests(data: dict,
                  output_file_name: str = './app/data/processed/grounding.xlsx',
                  generate_report: bool = False):
  groundings = []
  output_columns = ['question', 'grounding', 'reason']
  
  for item in data:
    
    if item is None or 'ok' in item:
      continue
    
    if 'grounding' not in item.get('partial_answers', {}):
      continue
    
    triage = item.get('partial_answers', {'triage': {'task': 'out_of_scope'}}).get('triage', {'task': 'out_of_scope'}).get('task', 'out_of_scope')
    
    if triage == 'out_of_scope':
      continue
    
    question = item.get('original_question', '')
    grounding = item.get('partial_answers', {'grounding': {'is_grounded': False}}).get('grounding',{'is_grounded': False}).get('is_grounded', False)
    reason = item.get('partial_answers', {'grounding': {'reason': ''}}).get('reason', '') 
    groundings.append([question, grounding, reason])
      
  df_results = pd.DataFrame(groundings, columns=output_columns)
  
  metrics = generate_grounding_metrics(df_results)
  
  if generate_report:
    df_results.to_excel(output_file_name, index=True)
  
  return metrics
    
def generate_grounding_metrics(df: pd.DataFrame) -> dict:
  df_copy = df.copy()
  result = {}
  
  total = int(df_copy['question'].count())
  value = int(df_copy['grounding'].sum())
  
  result = {
    'positives': value,
    'total': total,
    'result': round((value/total)*100, 2)  
  }
  
  return result
  