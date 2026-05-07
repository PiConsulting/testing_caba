TODO:
"""convertir en una prueba para poder incorporar al flujo normal"""
responses = []



agents_timings = {
  'tramites': [],
  'accesibilidad': [],
  'descubrir': []
}
for item in responses:
    
    list_of_agents = ['tramites', 'accesibilidad', 'descubrir']

    if item is None or 'ok' in item:
      continue

    if 'router' in item.get('partial_answers'):     
      route = item.get('partial_answers', {}).get('router', {}).get('route', '')

    node_metadata = item["node_metadata"]
    t_response_time = item.get('response_time', 0)

    if route == 'tramites':
      agents_timings['tramites'].append(t_response_time)
    elif route == 'accesibilidad':
      agents_timings['accesibilidad'].append(t_response_time)
    elif route == 'descubrir':
      agents_timings['descubrir'].append(t_response_time)

average_results = {
  'tramites': round(sum(agents_timings['tramites']) / len(agents_timings['tramites']),2),
  'accesibilidad': round(sum(agents_timings['accesibilidad']) / len(agents_timings['accesibilidad']), 2),
  'descubrir': round(sum(agents_timings['descubrir']) / len(agents_timings['descubrir']), 2),
}
print(average_results)
