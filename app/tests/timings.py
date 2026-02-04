import pandas as pd
import numpy as np

def timing_tests(data: list[dict], 
                 ouput_file_name: str = './app/data/processed/timings.xlsx', 
                 generate_report: bool = False) -> dict:
  
  output_columns = ['reformulate', 'triage', 'router', 'ag_call', 'personality', 'grounding', 'retriever', 'ret_embeddings', 'rag_answer','response_time']
  timings = []
  
  for item in data:
    
    if item is None or 'ok' in item:
      continue
    
    if 'router' in item['partial_answers']:
      route = item['partial_answers']['router']['route']
      
    node_metadata = item["node_metadata"]

    t_reformulate = node_metadata.get('reformulate', {'timings': 0}).get('timings')
    t_triage = node_metadata.get('triage', {'timings': 0}).get('timings')
    t_router = node_metadata.get('router', {'timings': 0}).get('timings')
    t_agent_call = node_metadata.get('agent_call', {'timings': 0}).get('timings')
    t_personality = node_metadata.get('personality', {'timings': 0}).get('timings') 
    t_grounding = node_metadata.get('grounding', {'timings': 0}).get('timings')
    t_response_time = item.get('response_time', 0)

    if 'grounding' in node_metadata:
      t_retriever = node_metadata[f'agent_{route}']['retrieve']['timing']
      t_retrieve_emb = node_metadata[f'agent_{route}']['retrieve_embeddings']['timing']
      t_rag_answer = node_metadata[f'agent_{route}']['rag_answer']['timing']
    else:
      t_retriever = 0
      t_rag_answer = 0
      t_retrieve_emb = 0
  
    timings.append([t_reformulate, t_triage, t_router, t_agent_call, t_personality, t_grounding, t_retriever, t_retrieve_emb, t_rag_answer, t_response_time])
    
  df_results = pd.DataFrame(timings, columns=output_columns)
    
  metrics = generate_timing_metrics(df_results)
  
  if generate_report:
    df_results.to_excel(ouput_file_name, index=True)
      
  return metrics


def generate_timing_metrics(df:pd.DataFrame) -> dict:
  df_copy = df.copy()
  result = {}
  for i in df_copy:
    
    if i == 'response_time':
      avg = np.nan_to_num(round(float(df[i][df[i] >= 3].mean()), 3), nan=0.0)
      amount = int((df[i] >= 3).sum())
    else:
      avg = np.nan_to_num(round(float(df[i][df[i] != 0].mean()), 3), nan=0.0)
      amount = int((df[i] != 0).sum())
      
    p90 = np.nan_to_num(round(float(df[i][df[i] != 0].quantile(0.9)), 3), nan=0.0)
    p95 = np.nan_to_num(round(float(df[i][df[i] != 0].quantile(0.95)), 3), nan=0.0)
    
    result[i] = {'prom': avg, 'p90':p90, 'p95':p95, 'quantity': amount}
  return result