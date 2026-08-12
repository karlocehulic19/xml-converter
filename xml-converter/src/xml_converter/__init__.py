import os
from lxml import etree
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
env_path = os.path.join(dirname, "../../.env")
_ = load_dotenv(env_path)

QUERY_WORD_IN = os.getenv("QUERY_WORD_IN")
QUERY_WORD_OUT = os.getenv("QUERY_WORD_OUT")
if not QUERY_WORD_IN or not QUERY_WORD_OUT:
    raise Exception("Make sure environmental variables for query element words are set!")

def main() -> None:
    tree_format = tree_from_examples("metro_input.xml")
    tree_in = tree_from_examples("t1.xml")
    tree_format_out = tree_from_examples("metro_output.xml")
    replace_all(tree_format, tree_in, tree_format_out)
    tree_format_out.write("new_xml.xml")
    print("Done, check out new_xml.xml")

def tree_from_examples(filename: str):
    rel = "../../xml-files/" + filename
    abs = os.path.dirname(__file__)
    abs_target = os.path.join(abs, rel)
    xml_file = open(os.path.abspath(abs_target))
    x = etree.parse(xml_file)
    return x

def replace_all(tree_format: etree.ElementTree, tree_in: etree.ElementTree, tree_format_out: etree.ElementTree):
    xpath_filter_in = f".//{QUERY_WORD_IN}"
    for element_in in tree_format.findall(xpath_filter_in):
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
    xpath_filter_out = f".//{QUERY_WORD_OUT}[@param='{param}']"
    elem = tree_out.find(xpath_filter_out)
    if elem == None: raise Exception(f"Replace query with param {param} not found!")
    par = elem.getparent()
    if par == None: raise Exception("Replace query cannot be root!")
    path = tree_out.getelementpath(par)
    return (path, elem)

