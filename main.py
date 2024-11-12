import xml.etree.ElementTree as ET
import json


class XMLConfigGenerator:
    def __init__(self, classes):
        self.classes = classes

    def generate_config(self):
        root_class = next((cls for cls in self.classes.values() if cls.is_root), None)
        return self._build_element(root_class)

    def _build_element(self, class_info):
        element = ET.Element(class_info.name)
        for attr in class_info.attributes:
            attr_elem = ET.SubElement(element, attr['name'])
            attr_elem.text = attr['type']

        for child in class_info.children:
            child_elem = self._build_element(child['class'])
            element.append(child_elem)

        return element

    def save(self, output_file):
        config_xml_root = self.generate_config()
        tree = ET.ElementTree(config_xml_root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)


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


# Основной процесс выполнения
def main():
    input_file = 'impulse_test_input.xml'

    # Парсинг XML и создание классов
    parser = XMLParser(input_file)
    parser.parse()

    # Генерация config.xml
    config_generator = XMLConfigGenerator(parser.classes)
    config_generator.save('config.xml')

    # Генерация meta.json
    meta_generator = MetaJSONGenerator(parser.classes)
    meta_generator.save('meta.json')


if __name__ == '__main__':
    main()
