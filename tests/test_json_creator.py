import pytest

from src.json_creator import *
from src.xml_creator import *


@pytest.fixture()
def open_file_in_xml(request):
    if type(request.param) is str:
        with open(request.param, 'r') as f:
            data = BeautifulSoup(f, features="xml")
        return data


@pytest.fixture()
def create_node(request):
    class_name, documentation, is_root, param = request.param
    is_root = is_root == "true"
    node = JSON_node(class_name, is_root, documentation, param)
    return node


@pytest.mark.parametrize('open_file_in_xml,output_path_file',
                         [('src/input/test_empty.xml', 'src/out/test_output.json')],
                         indirect=['open_file_in_xml'])
def test_empty_file(open_file_in_xml, output_path_file):
    input_data = open_file_in_xml
    json_creator = JSON_creator(input_data, output_path_file)
    output_data = json_creator.create_file()

    assert output_data == []


@pytest.mark.parametrize('open_file_in_xml,tag_identifier,create_node',
                         [('src/input/test_input.xml', {"name": "BTS"},
                           ['BTS', 'Base Transmitter Station. This is the only root class', 'true',
                            [{"name": "id", "type": "uint32"}, {"name": "name", "type": "string"},
                             {"name": "MGMT", "type": "class"}, {"name": "HWE", "type": "class"},
                             {"name": "COMM", "type": "class"}]])
                          ],
                         indirect=['open_file_in_xml', 'create_node'])
def test_define_fields_method(open_file_in_xml, tag_identifier, create_node):
    data = open_file_in_xml
    tag = data.find('Class', tag_identifier)

    json_creator = JSON_creator(data)
    result_node = json_creator.__define_fields__(JSON_node(), tag)
    expected_node = create_node

    assert result_node == expected_node


@pytest.mark.parametrize("open_file_in_xml,output_path",
                         [("src/input/test_input.xml", "src/input/test_output.xml")],
                         indirect=['open_file_in_xml'])
def test_invalid_output_path(open_file_in_xml, output_path):
    data = open_file_in_xml
    with pytest.raises(ValueError):
        JSON_creator(data, output_path)
