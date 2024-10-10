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


@pytest.mark.parametrize('path_file,indent_root,expected',
                         [pytest.param('src/input/test_standart.xml', {'isRoot': 'true'}, ['name', 'BTS']),
                          pytest.param('src/input/test_without_root.xml', {'isRoot': 'true'}, None)
                          ], )
def test_get_rood_method(path_file, indent_root, expected):
    with open(path_file, 'r') as f:
        data = BeautifulSoup(f, features="xml")
    xml_creator = XML_creator(path_file)
    root_tag = xml_creator.get_root_tag(data, indent_root)
    if expected is None:
        assert root_tag is None
    else:
        assert root_tag.attrs[expected[0]] == expected[1]


def test__write_output_method():
    pass


def test_create_param_tags_method():
    pass


@pytest.mark.parametrize('fixture,path_file,root_tag_name',
                         [('build_tree_test_standart', 'src/input/test_standart.xml', 'BTS'),
                          ], )
def test_create_structure_method(fixture, path_file, root_tag_name, request):
    with open(path_file, 'r') as f:
        data = BeautifulSoup(f, features="xml")
    xml_creator = XML_creator(path_file)

    assert request.getfixturevalue(fixture) == xml_creator.__create_structure__(
        data.find('Class', {'name': root_tag_name}))


def test_write_parameters_method():
    pass









