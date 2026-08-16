from xml_converter import Converter
from typing import Callable
from os import path

def test_string_conversion():
    get_asset_path: Callable[[str], str]= lambda file: path.dirname(__file__) + "/assets/" + file
    input_s = open(get_asset_path("input.xml")).read()
    input_format_s = open(get_asset_path("input_format.xml")).read()
    output_s = open(get_asset_path("output.xml")).read()
    output_format_s = open(get_asset_path("output_format.xml")).read()
    res = Converter.convert_to_string(input_format_s, input_s, output_format_s)
    assert res == output_s
    
