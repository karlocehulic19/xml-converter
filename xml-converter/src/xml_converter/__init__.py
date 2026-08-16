import os
from typing import Counter
from lxml import etree
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
env_path = os.path.join(dirname, "../../.env")
_ = load_dotenv(env_path)

XPATH_FILTER_IN = os.getenv("XPATH_FILTER_IN", ".//*[name()='replace']")
XPATH_FILTER_OUT = os.getenv("XPATH_FILTER_OUT", ".//*[name()='replace']")

def main() -> None:
    input_format_path = get_xml_file_path("input_format.xml")
    input_path = get_xml_file_path("input.xml")
    output_format_path = get_xml_file_path("output_format.xml")

    print(Converter.file_to_string(input_format_path, input_path, output_format_path))

def get_xml_file_path(filename: str) -> str:
    return os.path.join(dirname, "../../xml-files/" + filename)

class ConvertingElementTree():
    def __init__(self, tree: etree.ElementTree):
        self.tree: etree.ElementTree = tree

    def get_linked_path(self, linked_elem: etree.Element):
        linked_parent = linked_elem.getparent()
        if linked_parent == None: raise Exception("Replace query cannot be root!")
        return self.tree.getelementpath(linked_parent)
    
    def replace_query_element(self, query_param: str, new_value: str):
        elem_list = self.tree.xpath(XPATH_FILTER_OUT + f"[@param='{query_param}']")
        if not isinstance(elem_list, list): raise Exception("XPath found non XML element list.")
        elem = elem_list[0]
        if not isinstance(elem, etree.Element): raise Exception("XPath found non XML element.")
        par = elem.getparent()
        if par == None: raise Exception("Replace query cannot be root!")
        par.remove(elem)
        par.text = new_value

class Converter():
    def __init__(self, input_format: str, input: str, output_format: str):
        self.input_format_tree: ConvertingElementTree = ConvertingElementTree(etree.fromstring(input_format).getroottree())
        self.input_tree: ConvertingElementTree = ConvertingElementTree(etree.fromstring(input).getroottree())
        # Used for storing output as well
        self.output_format_tree: ConvertingElementTree = ConvertingElementTree(etree.fromstring(output_format).getroottree())
        self.is_processed: bool = False;

    @staticmethod
    def file_to_string(input_format_path: str, input_path: str, output_format_path: str):
        input_format_tree = etree.parse(open(input_format_path))
        input_tree = etree.parse(open(input_path))
        output_format_tree = etree.parse(open(output_format_path))
        return Converter.convert_to_string(input_format_tree, input_tree, output_format_tree)

    @staticmethod
    def string_to_string(input_format: str, input: str, output_format: str):
        input_format_tree = etree.fromstring(input_format).getroottree()
        input_tree = etree.fromstring(input).getroottree()
        # Used for storing output as well
        output_format_tree = etree.fromstring(output_format).getroottree()
        return Converter.convert_to_string(input_format_tree, input_tree, output_format_tree)

    @staticmethod
    def convert_to_string(input_format_tree_in: etree.ElementTree, input_tree_in: etree.ElementTree, output_format_tree_in: etree.ElementTree):
        input_format_tree: ConvertingElementTree = ConvertingElementTree(input_format_tree_in)
        input_tree: ConvertingElementTree = ConvertingElementTree(input_tree_in)
        # Used for storing output as well
        output_format_tree: ConvertingElementTree = ConvertingElementTree(output_format_tree_in)

        for element_in in input_format_tree.tree.xpath(XPATH_FILTER_IN):
            if not isinstance(element_in, etree.Element):
                raise Exception("XPath query found non element. Make sure your XPath queries only XML elements")
            linking_path = input_format_tree.get_linked_path(element_in)
            new_value_elem = input_tree.tree.find(linking_path)
            if new_value_elem == None: raise Exception("Linked path not found in input file")
            new_value = new_value_elem.text
            if new_value == None: raise Exception("Empty switches not yet developed")

            # Looking at output, finding the path to inject new value, remove replace
            param = element_in.get("param")
            if param == None: raise Exception("Query elements must have 'param' attribute")
            output_format_tree.replace_query_element(param, new_value)

        return etree.tostring(output_format_tree.tree).decode()

