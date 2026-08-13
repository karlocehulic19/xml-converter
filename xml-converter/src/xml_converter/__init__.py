import os
from lxml import etree
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
env_path = os.path.join(dirname, "../../.env")
_ = load_dotenv(env_path)

XPATH_FILTER_IN = os.getenv("XPATH_FILTER_IN", ".//*[name()='replace']")
XPATH_FILTER_OUT = os.getenv("XPATH_FILTER_OUT", ".//*[name()='replace']")

def main() -> None:
    tree_format = tree_from_examples("metro_input.xml")
    tree_in = tree_from_examples("t1.xml")
    tree_format_out = tree_from_examples("metro_output.xml")
    replace_all(tree_format, tree_in, tree_format_out)
    tree_format_out.write("new_xml.xml")
    print("Done, check out new_xml.xml")

def convert_xml_string(input_format: str, input: str, output_format: str):
    tree_format_in = etree.fromstring(input_format).getroottree()
    tree_in = etree.fromstring(input).getroottree()
    tree_format_out = etree.fromstring(output_format).getroottree()
    replace_all(tree_format_in, tree_in, tree_format_out)
    return etree.tostring(tree_format_out, pretty_print=True)

def tree_from_examples(filename: str):
    rel = "../../xml-files/" + filename
    abs = os.path.dirname(__file__)
    abs_target = os.path.join(abs, rel)
    xml_file = open(os.path.abspath(abs_target))
    x = etree.parse(xml_file)
    return x


def replace_all(tree_format: etree.ElementTree, tree_in: etree.ElementTree, tree_format_out: etree.ElementTree):
    for element_in in tree_format.xpath(XPATH_FILTER_IN):
        if not isinstance(element_in, etree.Element):
            raise Exception("XPath query found non element. Make sure your XPath queries only XML elements")
        new_value = get_value(element_in, tree_format, tree_in)
        (linked_path, link_elem) = get_linked_path(element_in, tree_format_out)
        elem_out = tree_format_out.find(linked_path)
        if elem_out == None: raise Exception("Linked path not found")
        elem_out.text = new_value
        elem_out.remove(link_elem)
    return

def get_value(element_in: etree.Element, tree_format: etree.ElementTree, tree_in: etree.ElementTree):
    par = element_in.getparent()
    if par == None: raise Exception("Replace query cannot be root!")
    par_path = tree_format.getelementpath(par)
    target_element = tree_in.find(par_path)
    if target_element == None: raise Exception("File does not contain all query replacemant paths!")
    
    return target_element.text

def get_linked_path(elem_in: etree.Element, tree_out: etree.ElementTree):
    param = elem_in.get("param")
    elem_list = tree_out.xpath(XPATH_FILTER_OUT + f"[@param='{param}']")
    if not isinstance(elem_list, list): raise Exception("XPath found non XML element list.")
    elem = elem_list[0]
    if not isinstance(elem, etree.Element): raise Exception("XPath found non XML element.")
    par = elem.getparent()
    if par == None: raise Exception("Replace query cannot be root!")
    path = tree_out.getelementpath(par)
    return (path, elem)

