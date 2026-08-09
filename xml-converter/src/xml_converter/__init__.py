import os
from lxml import etree
from lxml import objectify
from lxml import builder

def main() -> None:
    print("Hello from xml-converter!")
    root_in = root_from_examples("metro_input.xml")
    tree_out = root_from_examples("metro_output.xml")
    root_out = tree_out.getroot()

    root_out["Zaglavlje"]["Program"] = "Caffe"
    objectify.deannotate(tree_out, cleanup_namespaces=True)
    tree_out.write("new_xml.xml")

def root_from_examples(filename: str):
    rel = "../../xml-examples/" + filename
    abs = os.path.dirname(__file__)
    abs_target = os.path.join(abs, rel)
    xml_file = open(os.path.abspath(abs_target))
    x = objectify.parse(xml_file)
    return x
