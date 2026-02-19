import pandas as pd
import numpy as np

def token_tests(data: list[dict]) -> dict:
  tokens = []
  excel_columns = ['in_ref', 'out_ref', 'in_tri', 'out_tri', 'in_rou', 'out_rou', 'in_per', 'out_per', 'in_gro', 'out_gro','in_rag', 'out_rag', 'retriever', 'in_tot', 'out_tot']
  
  for item in data:
    
    if item is None or 'ok' in item:
      continue
    
    if 'router' in item['partial_answers']:
      route = item['partial_answers']['router']['route']
    
    node_metadata = item["node_metadata"]
  
    t_reformulate = node_metadata.get('reformulate', {"tokens": {'input': 0, 'output': 0,   'total': 0}}).get("tokens")
    t_triage = node_metadata.get('triage', {"tokens": {'input': 0, 'output': 0, 'total':  0}}).get("tokens")
    t_router = node_metadata.get('router', {"tokens": {'input': 0, 'output': 0, 'total':  0}}).get("tokens")
    t_personality = node_metadata.get('personality', {"tokens": {'input': 0, 'output': 0,   'total': 0}}).get("tokens")
    t_grounding = node_metadata.get('grounding', {"tokens": {'input': 0, 'output': 0,   'total': 0}}).get("tokens")

    if 'answer' in item and item['answer'] != '':
      t_rag_answer = node_metadata[f'agent_{route}']['rag_answer']['tokens']
      t_agent_retriever = node_metadata[f'agent_{route}']['retrieve_embeddings']['tokens']  ['prompt_tokens']  
    else:
      t_rag_answer = {'input': 0, 'output': 0, 'total': 0}
      t_agent_retriever = 0

    total_input = sum([t_reformulate['input'], t_triage['input'], t_router['input'],  t_personality['input'], t_grounding['input'], t_rag_answer['input']])
    total_output = sum([t_reformulate['output'], t_triage['output'], t_router['output'],  t_personality['output'], t_grounding['output'], t_rag_answer['output']])

    tokens.append([t_reformulate['input'],t_reformulate['output'], 
                 t_triage['input'], t_triage['output'], 
                 t_router['input'], t_router['output'],
                 t_personality['input'], t_personality['output'],
                 t_grounding['input'], t_grounding['output'],
                 t_rag_answer['input'], t_rag_answer['output'],
                 t_agent_retriever, total_input, total_output])
    
  df_results = pd.DataFrame(tokens, columns=excel_columns)
    
  metrics = generate_token_metrics(df_results)
    
  return metrics, df_results

      
def generate_token_metrics(df:pd.DataFrame) -> dict:
  df_copy = df.copy()
  result = {}
  for i in df_copy:
    avg = np.nan_to_num(round(float(df[i][df[i] != 0].mean()), 3), nan=0.0)
    tot = int(df[i].sum())
    amount = int((df[i] != 0).sum())
    result[i] = {'prom':avg, 'total': tot, 'quantity': amount}
  return result