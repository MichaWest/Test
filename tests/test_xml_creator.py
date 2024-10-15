import pytest

from src.xml_creator import *


@pytest.fixture()
def build_tree_test_standart():
    bts = XML_node("BTS")
    bts.add_param("id", "uint32")
    bts.add_param("name", "string")

    hwe = XML_node("HWE")

    ru = XML_node("RU")
    ru.add_param("hwRevision", "string")
    ru.add_param("id", "uint32")

    comm = XML_node("COMM")

    mgmt = XML_node("MGMT")

    cplane = XML_node("CPLANE")

    metricJob = XML_node("MetricJob")
    metricJob.add_param("isFinished", "boolean")
    metricJob.add_param("jobid", "uint32")

    bts.children.append(hwe)
    bts.children.append(comm)
    bts.children.append(mgmt)

    hwe.children.append(ru)

    mgmt.children.append(cplane)
    mgmt.children.append(metricJob)

    return bts


@pytest.fixture()
def open_file_in_xml(request):
    if type(request.param) is str:
        with open(request.param, 'r') as f:
            data = BeautifulSoup(f, features="xml")
        return data


@pytest.mark.parametrize('open_file_in_xml,indent_root,expected',
                         [('src/input/test_standart.xml', {'isRoot': 'true'}, ['name', 'BTS']),
                          ('src/input/test_without_root.xml', {'isRoot': 'true'}, None)
                          ], indirect=['open_file_in_xml'])
def test_get_rood_method(open_file_in_xml, indent_root, expected):
    data = open_file_in_xml
    xml_creator = XML_creator(data)
    root_tag = xml_creator.get_root_tag(data, indent_root)
    if expected is None:
        assert root_tag is None
    else:
        assert root_tag.attrs[expected[0]] == expected[1]


def test__write_output_method():
    pass


@pytest.mark.parametrize('open_file_in_xml,tag_name,tag_value',
                         [('src/input/test_create_param_tag.xml', 'id', 'uint32'),
                          ('src/input/test_create_param_tag.xml', 'name', 'string'),
                          ('src/input/test_create_param_tag.xml', 'isFinished', 'boolean'),
                          ('src/input/test_create_param_tag.xml', 'jobId', 'uint32'),
                          ('src/input/test_create_param_tag.xml', 'hwRevision', 'string'),
                          ('src/input/test_create_param_tag.xml', 'ipv4Address', 'string'),
                          ('src/input/test_create_param_tag.xml', 'manufacturerName', 'string')],
                         indirect=['open_file_in_xml'])
def test_create_param_tag_method(open_file_in_xml, tag_name, tag_value):
    data = open_file_in_xml
    expected_tag = data.find(tag_name)
    xml_creator = XML_creator(data)
    assert xml_creator.__create_param_tag__(tag_name, tag_value) == expected_tag


@pytest.mark.parametrize('fixture,open_file_in_xml,root_tag_name',
                         [('build_tree_test_standart', 'src/input/test_standart.xml', 'BTS'),
                          ],
                         indirect=['open_file_in_xml'])
def test_create_structure_method(fixture, open_file_in_xml, root_tag_name, request):
    data = open_file_in_xml
    xml_creator = XML_creator(data)

    assert request.getfixturevalue(fixture) == xml_creator.__create_structure__(
        data.find('Class', {'name': root_tag_name}))


@pytest.mark.parametrize('open_file_in_xml,indent_tag,expected_dict',
                         [('src/input/test_standart.xml', {'name': 'BTS'}, {'id': 'uint32', 'name': 'string'}),
                          ('src/input/test_standart.xml', {'name': 'MGMT'}, {}),
                          ('src/input/test_standart.xml', {'name': 'RU'},
                           {'hwRevision': 'string', 'id': 'uint32', 'ipv4Address': 'string',
                            'manufacturerName': 'string'})
                          ], indirect=['open_file_in_xml'])
def test_write_parameters_method(open_file_in_xml, indent_tag, expected_dict):
    data = open_file_in_xml
    tag = data.find('Class', indent_tag)
    xml_creator = XML_creator(data)
    xml_node = XML_node('test')
    assert xml_creator.__write__parameters__(tag, xml_node).parameters == expected_dict


@pytest.mark.parametrize('open_file_in_xml,output_path_file',
                         [('src/input/test_empty.xml', 'src/out/test_output.xml')],
                         indirect=['open_file_in_xml'])
def test_empty_file(open_file_in_xml, output_path_file):
    input_data = open_file_in_xml
    xml_creator = XML_creator(input_data, output_path_file)
    output_data = xml_creator.create_file()

    assert bool(output_data.find_all)
