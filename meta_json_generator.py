import json


class MetaJSONGenerator:
    def __init__(self, classes):
        self.classes = classes

    def generate_meta(self):
        meta_data = []
        for class_info in self.classes.values():
            meta_class = {
                'class': class_info.name,
                'documentation': class_info.documentation,
                'isRoot': class_info.is_root,
                'parameters': []
            }

            for attr in class_info.attributes:
                meta_class['parameters'].append({
                    'name': attr['name'],
                    'type': attr['type']
                })

            for child in class_info.children:
                meta_class['parameters'].append({
                    'name': child['class'].name,
                    'type': 'class'
                })
                meta_class['min'] = child['min']
                meta_class['max'] = child['max']

            meta_data.append(meta_class)

        return meta_data

    def save(self, output_file):
        meta_json_data = self.generate_meta()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(meta_json_data, f, ensure_ascii=False, indent=4)
