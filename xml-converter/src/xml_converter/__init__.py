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

class Converter():
    def __init__(self, input_format: str, input: str, output_format: str):
        self.input_format_tree: etree.ElementTree = etree.fromstring(input_format).getroottree()
        self.input_tree: etree.ElementTree = etree.fromstring(input).getroottree()
        # Used for storing output as well
        self.output_format_tree: etree.ElementTree = etree.fromstring(output_format).getroottree()
        self.is_processed: bool = False;

    def convert_to_string(self):
        self.replace_all()

        return etree.tostring(self.output_format_tree, pretty_print=True).decode()

    def replace_all(self):
        if self.is_processed == True: return 
        self.is_processed = True
        for element_in in self.input_format_tree.xpath(XPATH_FILTER_IN):
            if not isinstance(element_in, etree.Element):
                raise Exception("XPath query found non element. Make sure your XPath queries only XML elements")
            new_value = self.get_value(element_in)
            (linked_path, linking_elem) = self.get_linked_parent_path(element_in)
            elem_out = self.output_format_tree.find(linked_path)
            if elem_out == None: raise Exception("Linked path not found")
            elem_out.text = new_value
            elem_out.remove(linking_elem)
        return

    def get_value(self, element_in: etree.Element):
        par = element_in.getparent()
        if par == None: raise Exception("Replace query cannot be root!")
        par_path = self.input_format_tree.getelementpath(par)
        target_element = self.input_tree.find(par_path)
        if target_element == None: raise Exception("File does not contain all query replacemant paths!")
        
        return target_element.text

    def get_linked_parent_path(self, elem_in: etree.Element):
        param = elem_in.get("param")
        elem_list = self.output_format_tree.xpath(XPATH_FILTER_OUT + f"[@param='{param}']")
        if not isinstance(elem_list, list): raise Exception("XPath found non XML element list.")
        elem = elem_list[0]
        if not isinstance(elem, etree.Element): raise Exception("XPath found non XML element.")
        par = elem.getparent()
        if par == None: raise Exception("Replace query cannot be root!")
        path = self.output_format_tree.getelementpath(par)
        return (path, elem)
