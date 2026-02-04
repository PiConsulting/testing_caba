import pandas as pd

def router_tests(data: list[dict],
                validation: dict,
                output_file_name: str = './app/data/processed/router.xlsx',
                generate_report: bool=False) -> dict:
  routes = []
  output_colums = ['question', 'expected_route', 'obtained_route', 'comparison']
  
  for item in data:
    
    if item is None or 'ok' in item:
      continue
    
    triage = item.get('partial_answers', {'triage': {'task': 'out_of_scope'}}).get('triage', {'task': 'out_of_scope'}).get('task', 'out_of_scope')
    
    if triage == 'out_of_scope':
      continue
    
    question = item.get('original_question', '')
    exp_route = validation.get(question, 'Ruta no encontrada')
    obt_route = item.get('partial_answers', {'router':{'route': 'Ruta no encontrada'}}).get('router',{'route': 'Ruta no encontrada'}).get('route')
    comparison = 1 if exp_route == obt_route else 0
    
    routes.append([question, exp_route, obt_route, comparison])
  
  df_results = pd.DataFrame(routes, columns= output_colums)
  metrics = generate_router_metrics(df_results)
  
  if generate_report:
    df_results.to_excel(output_file_name, index=True)
    
  return metrics


def generate_router_metrics(df: pd.DataFrame) -> dict:
  df_copy = df.copy()
  total = int(df_copy['obtained_route'].count())
  value = int(df_copy['comparison'].values.sum())
  
  result = {
    'positives': value,
    'total': total,
    'result': round((value/total)*100, 2)  
  }
  
  return result


def create_validation_dataset(df: pd.DataFrame) -> dict:
  validation = {}
  for _, row in df.iterrows():
    
    question = row['user_input']
    route = row['route']
    validation[question] = route
  return validation
