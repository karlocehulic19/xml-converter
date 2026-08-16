from typing import Callable
from datetime import datetime

type AttribItems = list[tuple[str, str]]

def dparse_tag_method(attrib_val_in: str, attrib_val_out: str, value: str):
    d = datetime.strptime(value, attrib_val_in)
    return datetime.strftime(d, attrib_val_out)


tag_methods: dict[str, Callable[[str, str, str], str]] = {
        "param": lambda attrib_val_in, attrib_val_out, value: value,
        "uppercase": lambda attrib_val_in, attrib_val_out, value: value.upper(),
        "dparse": lambda a_in, a_out, value: dparse_tag_method(a_in, a_out, value)
        }

def get_input_parsed_callback(attributes_in: AttribItems, text_value: str):
    input_mapping: dict[str, str] = {}
    for attrib, attrib_val_in in attributes_in:
        if attrib not in tag_methods: raise Exception(f"Custom attribute {attrib} isn't included as attribute method")

        input_mapping[attrib] = attrib_val_in

    returning_callback: Callable[[AttribItems], str] = lambda atts_out: input_callback(text_value, input_mapping, atts_out)
    return returning_callback

def input_callback(text_value: str, input_mapping: dict[str, str], attributes_out: AttribItems):
    curr_val = text_value
    for attrib, attrib_val_out in attributes_out:
        attrib_val_in = input_mapping[attrib]
        curr_val = tag_methods[attrib](attrib_val_in, attrib_val_out, curr_val)

    return curr_val
