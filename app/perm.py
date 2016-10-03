from itertools import permutations

query = 'Create Wall method'
split_query = query.lower().split(' ')

perm_query = permutations(split_query)
# (('create', 'wall', 'method'), ('wall', 'create')
final_query = ''
for combo in perm_query:
    combo = '.+'.join('({})'.format(x) for x in combo)
    final_query += '({})|'.format(combo)

print(final_query)
