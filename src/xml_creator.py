import os

import bs4
from bs4 import BeautifulSoup, element


class XML_node:

    def __init__(self, name: str):
        self.parameters: dict = {}
        self.name = name
        self.children: list[XML_node] = []

    def add_param(self, param_name: str, param_val: str) -> None:
        self.parameters[param_name] = param_val

    def add_child(self, child) -> None:
        self.children.append(child)

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        res_1 = self.parameters == other.parameters
        res_2 = self.children.sort() == other.children.sort()
        res_3 = self.name == other.name
        return res_3 and res_1 and res_2


class XML_creator:

    def __init__(self, input_bs: BeautifulSoup, output_path: str = "out/config.xml"):
        filename, file_extension = os.path.splitext(output_path)

        if file_extension != ".xml":
            raise ValueError("The path must point to the format file .xml")

        self.BS_result = BeautifulSoup(features="xml")
        self.output_path = output_path
        self.BS_data = input_bs

    def create_file(self) -> BeautifulSoup:
        if len(self.BS_data.find_all()) != 0:
            root_tag = self.get_root_tag(self.BS_data, {'isRoot': "true"})

            root_node = self.__create_structure__(root_tag)

            self.__add_param_tags__(root_node.parameters, root_tag)

            self.BS_result.append(self.__write_output__(root_node))

        with open(self.output_path, "w") as f:
            f.write(self.BS_result.prettify())

        return self.BS_result

    def get_root_tag(self, data: bs4.BeautifulSoup, indent_root: dict[str:str]) -> element.Tag:
        return data.find('Class', indent_root)

    def __write_output__(self, node: XML_node) -> element.Tag:
        new_tag = self.BS_result.new_tag(node.name)
        self.__add_param_tags__(node.parameters, new_tag)
        for c in node.children:
            new_tag.append(self.__write_output__(c))
        return new_tag

    def __add_param_tags__(self, params: dict, tag: element.Tag) -> element.Tag:
        for param in params:
            tag.append(self.__create_param_tag__(param, params[param]))
        return tag

    def __create_param_tag__(self, name: str, value: str) -> element.Tag:
        param_tag = self.BS_result.new_tag(name)
        param_tag.string = value
        return param_tag

    def __create_structure__(self, tag: element.Tag) -> XML_node:
        tag_name = tag.attrs['name']
        xml_node = XML_node(tag_name)

        xml_node = self.__write__parameters__(tag, xml_node)

        # находим детей и запускаем для них функцию create_xml_tree
        aggregation_tags = self.BS_data.findAll('Aggregation', {'target': tag_name})
        for t in aggregation_tags:
            child_name = t.attrs['source']
            child_tag = self.BS_data.find('Class', {'name': child_name})
            child_node = self.__create_structure__(child_tag)
            xml_node.add_child(child_node)

        return xml_node

    def __write__parameters__(self, tag: element.Tag, xml_node: XML_node) -> XML_node:
        for key in tag.contents:
            if type(key) is element.Tag:
                xml_node.add_param(key.attrs['name'], key.attrs['type'])

        return xml_node
