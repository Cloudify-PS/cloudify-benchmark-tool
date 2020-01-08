from cloudify import ctx

targets = dict()

for rel in ctx.instance.relationships:
    node_id = rel.target.instance.id
    runtime_properties = rel.target.instance.runtime_properties
    targets[node_id] = dict()
    if runtime_properties.get('result_properties'):
        if runtime_properties.get('result_properties'):
            targets[node_id]['counter']=runtime_properties.get(
            'result_properties').get('counter')
        if runtime_properties.get('Target_Nodes'):
            targets[node_id].update(runtime_properties.get('Target_Nodes'))
ctx.instance.runtime_properties['Target_Nodes'] = targets
