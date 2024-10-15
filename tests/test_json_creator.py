import pytest

from src.json_creator import *
from src.xml_creator import *


@pytest.fixture()
def open_file_in_xml(request):
    if type(request.param) is str:
        with open(request.param, 'r') as f:
            data = BeautifulSoup(f, features="xml")
        return data


@pytest.mark.parametrize('open_file_in_xml,output_path_file',
                         [('src/input/test_empty.xml', 'src/out/test_output.json')],
                         indirect=['open_file_in_xml'])
def test_empty_file(open_file_in_xml, output_path_file):
    input_data = open_file_in_xml
    json_creator = JSON_creator(input_data, output_path_file)
    output_data = json_creator.create_file()

    assert output_data == []
