import os
import json


GLTF_SCHEMA_ROOT = os.path.join(os.path.split(__file__)[0],
                                os.path.pardir,
                                os.path.pardir,
                                'glTF', 'specification', 'schema')
GLTF_SCHEMAS = {}
for filename in os.listdir(GLTF_SCHEMA_ROOT):
    if filename.endswith('.schema.json'):
        with open(os.path.join(GLTF_SCHEMA_ROOT, filename)) as f:
            GLTF_SCHEMAS[filename[:-len('.schema.json')]] = json.loads(f.read())


def make_default(gltf_type):
    return {prop_name: prop_spec['default']
            for prop_name, prop_spec in GLTF_SCHEMAS[gltf_type]['properties'].items()
            if 'default' in prop_spec}
