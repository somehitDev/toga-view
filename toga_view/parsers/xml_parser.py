# -*- coding: utf-8 -*-
import os, pathlib, toga, toga.style, toga.style.pack, re
from xml.etree import ElementTree as ET
from ..exceptions import VersionMismatchException, UnknownWidgetException
from .. import __version__
        

class XmlParser:
    @staticmethod
    def parse_file(xml_file:str) -> toga.Widget:
        root = ET.parse(str(pathlib.Path(xml_file).resolve())).getroot()
        if not root.attrib["toga-version"] == toga.__version__:
            raise VersionMismatchException(root.attrib["toga-version"])

        return XmlParser._parse_element(root[0])
    
    @staticmethod
    def parse_file_to_script(xml_file:str, name:str = None, indent:int = 4) -> str:
        xml_file = str(pathlib.Path(xml_file).resolve())

        root = ET.parse(xml_file).getroot()
        if not root.attrib["toga-version"] == toga.__version__:
            raise VersionMismatchException(root.attrib["toga-version"])
        
        root_widget = root[0]
        root_widget_attribs, gen_name = XmlParser._parse_attribs_to_script(root_widget.attrib, root_widget.tag)
        if name is None:
            name = gen_name
        else:
            name = "".join([ part.strip().capitalize() for part in re.findall("[A-Z][^A-Z]*", name) ])

        tab = " " * indent
        child_scripts = ""
        try:
            child_widget = root_widget[0]
            if child_widget.tag == "content":
                widget_script, widget_name = XmlParser._parse_element_to_script(child_widget[0], indent * 2)
                child_scripts += widget_script
                child_scripts += f"{tab * 2}self.content = self.{widget_name}"
            elif child_widget.tag == "items":
                for sub_element in child_widget:
                    widget_script, widget_name = XmlParser._parse_element_to_script(sub_element, indent * 2)
                    child_scripts += widget_script
                    child_scripts += f"{tab * 2}self.add(self.{widget_name})\n"
        except IndexError:
            pass

        return f"""# -*- coding: utf-8 -*-

##################################################################
# Generated from reading file '{os.path.basename(xml_file)}'
# Created by: toga-view version {__version__}
# WARNING! All changes in this file will be lost when regenerated!
##################################################################

import toga, toga.style, toga.style.pack

class {name}(toga.{root_widget.tag}):
{tab}def __init__(self, *args, **kwargs):
{tab * 2}kwargs.update({root_widget_attribs})
{tab * 2}super().__init__(*args, **kwargs)

{child_scripts}
"""

    @staticmethod
    def parse_xml(xml_string:str) -> toga.Widget:
        root = ET.fromstring(xml_string)
        if not root.attrib["toga-version"] == toga.__version__:
            raise VersionMismatchException(root.attrib["toga-version"])

        return XmlParser._parse_element(root[0])


    @staticmethod
    def _parse_element(element:ET.Element) -> toga.Widget:
        if not hasattr(toga, element.tag):
            raise UnknownWidgetException(element.tag)

        attribs = XmlParser._parse_attribs(element.attrib)
        widget = getattr(toga, element.tag)(**attribs)

        try:
            widget_child = element[0]
            if widget_child.tag == "content":
                widget.content = XmlParser._parse_element(widget_child[0])
            elif widget_child.tag == "items":
                for sub_element in widget_child:
                    widget.add(XmlParser._parse_element(sub_element))
        except IndexError:
            pass

        return widget

    @staticmethod
    def _parse_attribs(attribs:dict) -> dict:
        parsed_attribs = {}

        # don't use name attribute parse to widget directly
        attribs.pop("name", None)

        for key, attrib in attribs.items():
            if key == "position":
                # parse position
                position = [
                    int(item.strip())
                    for item in attrib.split(",")
                ]
                if len(position) != 2:
                    raise ValueError("position must be x, y pair!")

                parsed_attribs["position"] = toga.Position(*position)
            elif key == "size":
                # parse size
                size = [
                    int(item.strip())
                    for item in attrib.split(",")
                ]
                if len(size) != 2:
                    raise ValueError("size must be width, height pair!")

                parsed_attribs["size"] = toga.Size(*size)
            elif key == "style":
                # parse style
                style_attrs = {}
                for style_block in attrib.split(";"):
                    if not style_block == "":
                        name, value = [ item.strip() for item in  style_block.split(":") ]
                        if value in ( "COLUMN", "ROW" ):
                            style_attrs[name] = getattr(toga.style.pack, value)
                        elif "," in value:
                            value_list = []
                            for item in [ item.strip() for item in value.split(",") ]:
                                value_list.append(XmlParser._parse_value(item))

                            style_attrs[name] = tuple(value_list)
                        else:
                            style_attrs[name] = XmlParser._parse_value(value)

                parsed_attribs["style"] = toga.style.Pack(**style_attrs)
            elif attrib.capitalize() in ( "True", "False" ):
                parsed_attribs[key] = eval(attrib.capitalize())
            else:
                parsed_attribs[key] = attrib

        return parsed_attribs

    @staticmethod
    def _parse_element_to_script(element:ET.Element, indent:int = 8) -> tuple[str, str]:
        if not hasattr(toga, element.tag):
            raise UnknownWidgetException(element.tag)
        
        tab = " " * indent
        attribs_string, name = XmlParser._parse_attribs_to_script(element.attrib, element.tag)

        root_widget_script = f"{tab}self.{name} = toga.{element.tag}({attribs_string})\n"
        try:
            child_widget = element[0]
            if child_widget.tag == "content":
                widget_script, widget_name = XmlParser._parse_element_to_script(child_widget[0], indent)
                root_widget_script += widget_script
                root_widget_script += f"{tab}self.{name}.content = self.{widget_name}\n"
            elif child_widget.tag == "items":
                for sub_element in child_widget:
                    widget_script, widget_name = XmlParser._parse_element_to_script(sub_element, indent)
                    root_widget_script += widget_script
                    root_widget_script += f"{tab}self.{name}.add(self.{widget_name})\n"
        except IndexError:
            pass

        return root_widget_script + "\n", name

    @staticmethod
    def _parse_attribs_to_script(attribs:dict, tag_name:str) -> tuple[str, str]:
        attribs_string_list = []
        name = attribs.pop("name", "_".join([ part.lower() for part in re.findall("[A-Z][^A-Z]*", tag_name) ]))

        for key, attrib in attribs.items():
            if key == "position":
                # parse position
                position = [
                    int(item.strip())
                    for item in attrib.split(",")
                ]
                if len(position) != 2:
                    raise ValueError("position must be x, y pair!")

                attribs_string_list.append(f"position = toga.Position{tuple(position)}")
            elif key == "size":
                # parse size
                size = [
                    int(item.strip())
                    for item in attrib.split(",")
                ]
                if len(size) != 2:
                    raise ValueError("size must be width, height pair!")

                attribs_string_list.append(f"size = toga.Size{tuple(size)}")
            elif key == "style":
                # parse style
                style_attrs_list = []
                for style_block in attrib.split(";"):
                    if not style_block == "":
                        style_name, style_value = [ item.strip() for item in  style_block.split(":") ]
                        if style_value in ( "COLUMN", "ROW" ):
                            style_attrs_list.append(f"{style_name} = toga.style.pack.{style_value}")
                        elif "," in style_value:
                            value_list = []
                            for item in [ item.strip() for item in style_value.split(",") ]:
                                parsed_item = XmlParser._parse_value(item)
                                if isinstance(parsed_item, str):
                                    value_list.append(f'"{item}"')
                                else:
                                    value_list.append(f"{item}")

                            style_attrs_list.append(f"{style_name} = ( {', '.join(value_list)} )")
                        else:
                            parsed_value = XmlParser._parse_value(style_value)
                            if isinstance(parsed_value, str):
                                style_value = f'"{style_value}"'

                            style_attrs_list.append(f"{style_name} = {style_value}")

                attribs_string_list.append(f"style = toga.style.Pack({', '.join(style_attrs_list)})")
            elif isinstance(attrib, str):
                attribs_string_list.append(f'{key} = "{attrib}"')
            else:
                attribs_string_list.append(f"{key} = {attrib}")

        return ", ".join(attribs_string_list), name

    @staticmethod
    def _parse_value(source:str):
        try:
            value = int(source)
            if "." in source:
                return float(source)
            else:
                return value
        except:
            pass

        return source
