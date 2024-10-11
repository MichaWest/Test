from bs4 import BeautifulSoup

from json_creator import JSON_creator
from xml_creator import XML_creator, XML_node


creator_xml = XML_creator("input/test_input.xml", "out/output.xml")
creator_xml.create_file()

creator_json = JSON_creator("input/test_input.xml", "out/output.json")
creator_json.create_file()

