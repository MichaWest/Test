from bs4 import BeautifulSoup

from json_creator import JSON_creator
from xml_creator import XML_creator, XML_node


# creator_xml = XML_creator("input/test_input.xml", "out/output.xml")
# creator_xml.create_file()
#
# creator_json = JSON_creator("input/test_input.xml", "out/output.json")
# creator_json.create_file()

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


path_file = "input/test_standart.xml"
root_tag_name = 'BTS'

with open(path_file, 'r') as f:
    data = BeautifulSoup(f, features="xml")
xml_creator = XML_creator(path_file)

root = xml_creator.__create_structure__(data.find('Class', {'name': root_tag_name}))
exp_root = build_tree_test_standart()

print(root == exp_root)

print()