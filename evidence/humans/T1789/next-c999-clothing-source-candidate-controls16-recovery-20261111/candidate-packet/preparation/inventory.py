from pathlib import Path
import ast, hashlib, json

P = Path('/tmp/T1789-NEXT-CLOTHING-C999-SOURCE-CANDIDATE-20261111')
APP = Path('/dev/shm/chicago-t1789-charles-gate-20261110/chicago/4d')
PREFIX = 'chicago/4d/'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def save(name, data):
    with (P/name).open('x') as stream: json.dump(data, stream, indent=2); stream.write('\n')
targets = {'human_dress_components':{'apron','bib','collar_band'},
    'human_merchant_1835':{'stock'}, 'human_coachman_1904':{'livery_coat'},
    'human_maid_1904':{'apron_skirt'}, 'human_cook_1904':{'apron_skirt'}}
edges = []; source_pins = []; changed_functions = {}; test_counts = {}
for name in sorted({p.name for p in (APP/'tools').glob('human_*.py')}
                   | {p.name for p in (P/'candidate'/PREFIX/'tools').glob('human_*.py')}):
    module = name[:-3]; candidate = P/'candidate'/PREFIX/'tools'/name
    path = candidate if candidate.exists() else APP/'tools'/name
    raw = path.read_bytes(); tree = ast.parse(raw, filename=name)
    aliases = {}; functions = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in targets:
            for item in node.names:
                if item.name in targets[node.module]: aliases[item.asname or item.name] = node.module+'.'+item.name
        if isinstance(node, ast.Import):
            for item in node.names:
                if item.name in targets: aliases[item.asname or item.name] = item.name
    found = []
    for fn, node in functions.items():
        for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
            target = None
            if isinstance(call.func, ast.Name):
                target = aliases.get(call.func.id)
                if module in targets and call.func.id in targets[module]: target = module+'.'+call.func.id
            elif isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name):
                owner = aliases.get(call.func.value.id)
                if owner in targets and call.func.attr in targets[owner]: target = owner+'.'+call.func.attr
            if target:
                edge = dict(caller=module+'.'+fn, target=target, line=call.lineno)
                edges.append(edge); found.append(edge)
    if found: source_pins.append(dict(file='tools/'+name, candidate_overlay=candidate.exists(), sha256=sha(raw), bytes=len(raw)))
    if candidate.exists():
        before = P/'before'/PREFIX/'tools'/name
        if before.exists():
            old = {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(before.read_bytes()).body if isinstance(n,ast.FunctionDef)}
            changed_functions['tools/'+name] = [n for n in old if n not in functions or old[n] != ast.dump(functions[n],include_attributes=False)]

mechanisms = {
 'merchant_1835_v1':['stock side-rim fairing'],
 'coachman_livery_1904_v1':['stock side-rim fairing','breeches-supported closed coat skirt and skin correspondence'],
 'soldier_1812_v1':['stock side-rim fairing','outer coat collar derives returned side tops'],
 'officer_1812_v1':['stock side-rim fairing','outer coat collar derives returned side tops'],
 'trader_1812_v1':['stock/neckcloth side-rim fairing'],
 'adult_dress_v1':['actual-skirt lower-apron support','source-conforming bib and level collar only when1904 outfit enables them'],
 'maid_1904_v1':['actual-skirt lower-apron support','source-conforming bib','level clipped collar'],
 'cook_1904_v1':['actual-skirt lower-apron support','source-conforming bib','level clipped neckband'],
 'child_girl_1812_v1':['TRANSITIVE source-conforming pinafore bib via shared dress bib(); child lower apron unchanged'],
}
variants = []; recipe_pins = []
for f in sorted((APP/'data/humans/recipes').glob('*.json')):
    candidate = P/'candidate'/PREFIX/'data/humans/recipes'/f.name
    raw = (candidate if candidate.exists() else f).read_bytes(); doc = json.loads(raw)
    matched = [v for v in doc.get('proof_variants',[]) if v.get('component_assembly') in mechanisms]
    if matched:
        recipe_pins.append(dict(file='data/humans/recipes/'+f.name, candidate_overlay=candidate.exists(), sha256=sha(raw), bytes=len(raw)))
    for v in matched:
        variants.append(dict(asset_id=v['id'], assembly=v['component_assembly'], recipe='data/humans/recipes/'+f.name,
            mechanisms=mechanisms[v['component_assembly']], person_reference_id=v.get('person_reference_id'),
            expected_native_parents=[f'assets/humans/{web}{v["id"]}.lod{lod}.glb' for web in ('','web/') for lod in range(4)]))
assert len({v['asset_id'] for v in variants}) == len(variants)
ids = {v['asset_id'] for v in variants}
registry = []; registry_pins = []; scanned = 0
for year in ('1812','1835','1904'):
    index = APP/f'data/humans/instances/{year}/index.json'; raw = index.read_bytes(); doc=json.loads(raw)
    assert len(doc['instances']) <= 2048
    registry_pins.append(dict(file=index.relative_to(APP).as_posix(), sha256=sha(raw), bytes=len(raw)))
    for ident in doc['instances']:
        assert isinstance(ident,str) and '/' not in ident and '\\' not in ident
        f=index.parent/(ident+'.json');raw=f.read_bytes();row=json.loads(raw);scanned+=1
        asset=row.get('appearance',{}).get('asset_id')
        if asset in ids:
            registry.append(dict(kind='indexed_instance',file=f.relative_to(APP).as_posix(),
                instance=row.get('id',ident),asset_id=asset,sha256=sha(raw)))
lazy = APP/'data/humans/inside_1812.json';raw=lazy.read_bytes();doc=json.loads(raw)
registry_pins.append(dict(file=lazy.relative_to(APP).as_posix(),sha256=sha(raw),bytes=len(raw)))
assert len(doc['people']) <= 2048
for row in doc['people']:
    if row.get('asset_id') in ids:registry.append(dict(kind='inside_1812_lazy_person',file=lazy.relative_to(APP).as_posix(),
        person=row.get('person'),asset_id=row['asset_id']))
for f in sorted((P/'candidate'/PREFIX/'tools').glob('test_*.py')):
    tree=ast.parse(f.read_bytes());test_counts[f.name]=sum(isinstance(n,ast.FunctionDef) and n.name.startswith('test_') for n in ast.walk(tree))
save('AFFECTED-CONSUMERS.json',dict(status='STATIC_SOURCE_REACHABILITY_NOT_NATIVE_QUALIFICATION',
    base='c9990d8b32517612a94e339a98bd5700436b5689',direct_recipe_proof_variant_count=len(variants),
    variants=variants,actual_call_edges=edges,caller_source_pins=source_pins,recipe_pins=recipe_pins,
    runtime_registry=dict(indexed_instance_files_scanned=scanned,lazy_people_scanned=len(doc['people']),
        matched_current_entries=registry,index_and_lazy_source_pins=registry_pins,
        limitation='Actual static indexed/lazy source consumers only; no scene load or proof of present visibility, all dynamic spawn aliases, every native derivative or individual photographic fit.'),
    explicit_nonconsumers=['1904 gentleman separate shirt collar unchanged','1812 toddler/boy/Potawatomi frocks do not take the child-girl pinafore-bib branch',
        'Shared dress helpers need/digest/empty/bodice/blouse/leg_follow are unchanged; importing the module alone is not a garment change'],
    child_scope='Existing shared bib hunk reaches child_girl_1812; no new child code or lower-pinafore fix added. Actual child native LOD/pose clearance remains required.',
    changed_existing_functions=changed_functions,prepared_test_method_counts=test_counts,
    source_tests_run=False,native_fit_accepted=False))
print(json.dumps(dict(variants=len(variants),call_edges=len(edges),indexed_files=scanned,lazy_people=len(doc['people']),
    matching_runtime_entries=len(registry),prepared_test_methods=sum(test_counts.values()),tests_run=False)))
