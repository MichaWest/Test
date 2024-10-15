import json

from bs4 import BeautifulSoup, element


class JSON_node:

    def __init__(self):
        self.class_name: str = ''
        self.isRoot: bool = False
        self.documentation: str = ''
        self.parameters: list[{str: str}] = []

    def add_param(self, param_name: str, param_type: str):
        self.parameters.append({param_name: param_type})

    def get_json_dict(self):
        json_dict = {'class': self.class_name}
        json_dict.update(self.__dict__.copy())
        del json_dict['class_name']
        return json_dict

    def __len__(self):
        return len(self.__dict__) + len(self.parameters) + 1


class JSON_creator:

    def __init__(self, input_bs: BeautifulSoup, output_path: str):
        self.list_node: list[JSON_node] = []
        self.output_path = output_path
        self.BS_data = input_bs

    def create_file(self) -> list:
        json_list = []
        if len(self.BS_data.find_all()) != 0:
            first_tag = self.BS_data.find('Class')
            self.__create_structure__(first_tag)
            json_list = self.__write_out_structure__()

        with open(self.output_path, mode='w') as f:
            f.write(json.dumps(json_list, indent=4))
        return json_list

    def __create_structure__(self, tag: element.Tag) -> JSON_node:
        node = JSON_node()
        self.__define_fields__(node, tag)
        self.list_node.append(node)

        next_tag = tag.find_next('Class')
        if next_tag is not None:
            self.__create_structure__(next_tag)

        return node

    def __define_fields__(self, node: JSON_node, tag: element.Tag) -> None:
        # определяем поле 'name'
        tag_name = tag.attrs['name']
        node.class_name = tag_name

        # определяем поле documentation
        tag_doc = tag.attrs['documentation']
        node.documentation = tag_doc

        # определяем поле isRoot
        tag_is_root = tag.attrs['isRoot']
        node.isRoot = (tag_is_root == 'true')

        # определяем поле parameters
        attribute_tags = tag.findAll('Attribute')
        for t in attribute_tags:
            attr_name = t.attrs['name']
            attr_type = t.attrs['type']
            node.parameters.append({'name': attr_name, 'type': attr_type})

        aggregation_tags = self.BS_data.findAll('Aggregation', {'target': tag_name})
        for t in aggregation_tags:
            child_name = t.attrs['source']
            node.parameters.append({'name': child_name, 'type': 'class'})

    def __write_out_structure__(self) -> list:
        json_list = []
        for n in self.list_node:
            json_list.append(n.get_json_dict())
        return json_list

