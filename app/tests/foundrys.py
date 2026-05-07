from collections import Counter
from itertools import chain

def foundrys_tests(data: list[dict]) -> dict:
  links = []
  result = {}
  for item in data:
    
    if item is None or 'ok' in item:
      continue
    
    if 'router' in item['partial_answers']:
      node_metadata = item['node_metadata']
      route = item['partial_answers'].get('router', {'route': ''}).get('route', '')
      
      ref_link = node_metadata.get('reformulate', '').get('endpoint', '').split(':')[0]
      tri_link = node_metadata.get('triage').get('endpoint', '').split(':')[0]
    
      
      rou_link = node_metadata.get('router').get('endpoint', '').split(':')[0]
      per_link = node_metadata.get('personality', {'endpoint': 'x'}).get('endpoint', 'x').split(':')[0]
      gro_link = node_metadata.get('grounding', {'endpoint': 'x'}).get('endpoint', 'x').split(':')[0]
      
      ree_link = node_metadata.get(f'agent_{route}', {'retrieve_embeddings': {'endpoint': 'x'}}).get('retrieve_embeddings',{'endpoint': 'x'}).get('endpoint', 'x').split(':')[0]
      rag_link = node_metadata.get(f'agent_{route}', {'rag_answer': {'endpoint': 'x'}}).get('rag_answer',{'endpoint': 'x'}).get('endpoint', 'x').split(':')[0]

      
      links.append([
        ref_link, 
        tri_link, 
        rou_link, 
        per_link, 
        gro_link, 
        ree_link, 
        rag_link
      ])

  total_counts = Counter(chain.from_iterable(links))
  del total_counts['x']
  
  total = total_counts.total()
  result['total'] = total
  
  for i in range(len(total_counts)):    
    result[f'{i}'] = {
      'count': total_counts[f'{i}'],
      'percentage': round(total_counts[f'{i}'] * 100 / total, 2)
    }
  
  return result