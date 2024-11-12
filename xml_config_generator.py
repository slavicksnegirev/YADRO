import xml.etree.ElementTree as ET


class XMLConfigGenerator:
    def __init__(self, classes):
        self.classes = classes

    def generate_config(self):
        root_class = next(
            (cls for cls in self.classes.values() if cls.is_root), None)
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
