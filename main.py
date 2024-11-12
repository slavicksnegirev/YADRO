from xml_parser import XMLParser
from xml_config_generator import XMLConfigGenerator
from meta_json_generator import MetaJSONGenerator


def main():
    input_file = 'impulse_test_input.xml'

    # Парсинг XML и создание классов
    parser = XMLParser(input_file)
    parser.parse()

    # Генерация config.xml
    config_generator = XMLConfigGenerator(parser.classes)
    config_generator.save('./out/config.xml')

    # Генерация meta.json
    meta_generator = MetaJSONGenerator(parser.classes)
    meta_generator.save('./out/meta.json')


if __name__ == '__main__':
    main()
