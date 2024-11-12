import xml.etree.ElementTree as ET

from class_info import ClassInfo
from aggregation import Aggregation


class XMLParser:
    def __init__(self, input_file):
        self.input_file = input_file
        self.classes = {}
        self.aggregations = []

    def parse(self):
        tree = ET.parse(self.input_file)
        root = tree.getroot()

        # Parse classes
        for cls in root.findall('Class'):
            class_name = cls.get('name')
            is_root = cls.get('isRoot') == 'true'
            documentation = cls.get('documentation', '')

            class_info = ClassInfo(class_name, is_root, documentation)
            for attr in cls.findall('Attribute'):
                class_info.add_attribute(attr.get('name'), attr.get('type'))

            self.classes[class_name] = class_info

        # Parse aggregations
        for agg in root.findall('Aggregation'):
            aggregation = Aggregation(
                source=agg.get('source'),
                target=agg.get('target'),
                source_multiplicity=agg.get('sourceMultiplicity'),
                target_multiplicity=agg.get('targetMultiplicity')
            )
            self.aggregations.append(aggregation)

        self._build_hierarchy()

    def _build_hierarchy(self):
        for agg in self.aggregations:
            source_class = self.classes[agg.source]
            target_class = self.classes[agg.target]
            min_mult, max_mult = self._parse_multiplicity(
                agg.source_multiplicity)
            target_class.add_child(source_class, min_mult, max_mult)

    @staticmethod
    def _parse_multiplicity(multiplicity):
        if '..' in multiplicity:
            return multiplicity.split('..')
        return multiplicity, multiplicity
