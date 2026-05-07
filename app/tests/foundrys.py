from collections import Counter
from itertools import chain

def foundrys_tests(data: list[dict]) -> dict:
  links = []
  result = {}
  for item in data:
    
    if item is None or 'ok' in item:
      continue
    
    if 'router' in item['partial_answers'] and 'grounding' in item['partial_answers']:
      node_metadata = item['node_metadata']
      route = item['partial_answers'].get('router', {'route': ''}).get('route', '')
      
      ref_link = node_metadata.get('reformulate').get('endpoint_routing')[0].get('endpoint').split(':')[0]
      tri_link = node_metadata.get('triage').get('endpoint_routing')[0].get('endpoint', '').split(':')[0]
    
      rou_link = '99'

      if node_metadata['semantic_router']['endpoint_routing'][0].get('endpoint'):
        rou_link = node_metadata['semantic_router']['endpoint_routing'][0].get('endpoint').split(':')[0]
      else:
        node_metadata['llm_router']['endpoint_routing'][0].get('endpoint').split(':')[0]


      per_link = node_metadata.get('personality', {'endpoint': 'x'}).get('endpoint_routing')[0].get('endpoint', 'x').split(':')[0]
      gro_link = node_metadata.get('grounding', {'endpoint': 'x'}).get('endpoint_routing')[0].get('endpoint', 'x').split(':')[0]
      
      ree_link = node_metadata.get(f'agent_{route}', {'retrieve_embeddings', 'x'}).get('retrieve_embeddings','x').get('endpoint_routing')[0].get('endpoint', 'x').split(':')[0]
      rag_link = node_metadata.get(f'agent_{route}', {'rag_answer', 'x'}).get('rag_answer','x').get('endpoint_routing')[0].get('endpoint', 'x').split(':')[0]

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