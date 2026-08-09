import os
from lxml import etree
from lxml import objectify

def main() -> None:
    print("Hello from xml-converter!")
    rel = "../../xml-examples/foo.xml"
    abs = os.path.dirname(__file__)
    abs_target = os.path.join(abs, rel)
    xml_file = open(os.path.abspath(abs_target))
    x = objectify.parse(xml_file)
    root = x.getroot()


    print("This are the contents of file: ", root["setting"][1])
