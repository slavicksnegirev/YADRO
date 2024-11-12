class ClassInfo:
    def __init__(self, name, is_root, documentation):
        self.name = name
        self.is_root = is_root
        self.documentation = documentation
        self.attributes = []
        self.children = []

    def add_attribute(self, name, type_):
        self.attributes.append({'name': name, 'type': type_})

    def add_child(self, child_class, min_mult, max_mult):
        self.children.append({'class': child_class, 'min': min_mult, 'max': max_mult})
