from bs4 import BeautifulSoup

from json_creator import JSON_creator
from xml_creator import XML_creator

input_path = "input/test_input.xml"
with open(input_path, 'r') as f:
    BS_data = BeautifulSoup(f, features="xml")
    creator_xml = XML_creator(BS_data, "out/config.xml")
    creator_json = JSON_creator(BS_data, "out/meta.json")

    creator_xml.create_file()
    creator_json.create_file()

