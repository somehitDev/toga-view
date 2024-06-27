# -*- coding: utf-8 -*-
import os, pathlib, json, toga, toga.style, toga.style.pack, json, re
from ..exceptions import VersionMismatchException, UnknownWidgetException
from .. import __version__


class JsonParser:
    @staticmethod
    def parse_file(json_file:str) -> toga.Widget:
        with open(str(pathlib.Path(json_file).resolve()), "r", encoding = "utf-8") as jfr:
            ui_data = json.load(jfr)

        if not ui_data["toga-version"] == toga.__version__:
            raise VersionMismatchException(ui_data["toga-version"])

        return JsonParser._parse_info(ui_data["root"])

    @staticmethod
    def parse_file_to_script(json_file:str, name:str = None, indent:int = 4) -> str:
        json_file = str(pathlib.Path(json_file).resolve())

        with open(json_file, "r", encoding = "utf-8") as jfr:
            ui_data = json.load(jfr)

        if not ui_data["toga-version"] == toga.__version__:
            raise VersionMismatchException(ui_data["toga-version"])

        root_widget_attribs, gen_name = JsonParser._parse_properties_to_script(ui_data["root"]["properties"], ui_data["root"]["class"])
        if name is None:
            name = gen_name
        else:
            name = "".join([ part.strip().capitalize() for part in re.findall("[A-Z][^A-Z]*", name) ])

        tab = " " * indent
        child_scripts = ""
        if "content" in ui_data["root"].keys():
            # if window
            widget_script, widget_name = JsonParser._parse_info_to_script(ui_data["root"]["content"], indent * 2)
            child_scripts += widget_script
            child_scripts += f"{tab * 2}self.content = self.{widget_name}\n"
        elif "items" in ui_data["root"].keys():
            # layout
            for child_info in ui_data["root"]["items"]:
                widget_script, widget_name = JsonParser._parse_info_to_script(child_info, indent * 2)
                child_scripts += widget_script
                child_scripts += f"{tab * 2}self.add(self.{widget_name})\n"

        return f"""# -*- coding: utf-8 -*-

##################################################################
# Generated from reading file '{os.path.basename(json_file)}'
# Created by: toga-view version {__version__}
# WARNING! All changes in this file will be lost when regenerated!
##################################################################

import toga, toga.style, toga.style.pack

class {name}(toga.{ui_data["root"]["class"]}):
{tab}def __init__(self, *args, **kwargs):
{tab * 2}kwargs.update({root_widget_attribs})
{tab * 2}super().__init__(*args, **kwargs)

{child_scripts}
"""


    @staticmethod
    def _parse_info(widget_info:dict) -> toga.Widget:
        if not hasattr(toga, widget_info["class"]):
            raise UnknownWidgetException(widget_info["class"])

        attribs = JsonParser._parse_properties(widget_info["properties"])
        widget = getattr(toga, widget_info["class"])(**attribs)

        if "content" in widget_info.keys():
            # if window
            widget.content = JsonParser._parse_info(widget_info["content"])
        elif "items" in widget_info.keys():
            # layout
            for child_info in widget_info["items"]:
                widget.add(JsonParser._parse_info(child_info))

        return widget

    @staticmethod
    def _parse_properties(attrib_info:dict) -> dict:
        parsed_attribs = {}

        # don't use name attribute parse to widget directly
        attrib_info.pop("name", None)

        for key, attrib in attrib_info.items():
            if key == "position":
                # parse position
                parsed_attribs["position"] = toga.Position(**attrib)
            elif key == "size":
                # parse size
                parsed_attribs["size"] = toga.Size(**attrib)
            elif key == "style":
                # parse style
                style_attrs = {}
                for style_name, style_value in attrib.items():
                    if style_value in ( "COLUMN", "ROW" ):
                        style_attrs[style_name] = getattr(toga.style.pack, style_value)
                    else:
                        style_attrs[style_name] = tuple(style_value) if isinstance(style_value, list) else style_value

                parsed_attribs["style"] = toga.style.Pack(**style_attrs)
            else:
                parsed_attribs[key] = attrib

        return parsed_attribs

    @staticmethod
    def _parse_info_to_script(widget_info:dict, indent:int = 8) -> tuple[str, str]:
        if not hasattr(toga, widget_info["class"]):
            raise UnknownWidgetException(widget_info["class"])

        tab = " " * indent
        attribs_string, name = JsonParser._parse_properties_to_script(widget_info["properties"], widget_info["class"])

        root_widget_script = f"{tab}self.{name} = toga.{widget_info['class']}({attribs_string})\n"
        if "content" in widget_info.keys():
            # if window
            widget_script, widget_name = JsonParser._parse_info_to_script(widget_info["content"], indent)
            root_widget_script += widget_script
            root_widget_script += f"{tab}self.{name}.content = self.{widget_name}\n"
        elif "items" in widget_info.keys():
            # layout
            for child_info in widget_info["items"]:
                widget_script, widget_name = JsonParser._parse_info_to_script(child_info, indent)
                root_widget_script += widget_script
                root_widget_script += f"{tab}self.{name}.add(self.{widget_name})\n"

        return root_widget_script + "\n", name

    @staticmethod
    def _parse_properties_to_script(attrib_info:dict, class_name:str) -> tuple[str, str]:
        attribs_string_list = []
        name = attrib_info.pop("name", "_".join([ part.lower() for part in re.findall("[A-Z][^A-Z]*", class_name) ]))

        for key, attrib in attrib_info.items():
            if key == "position":
                # parse position
                attribs_string_list.append(f"position = toga.Position({', '.join([ f'{key} = {value}' for key, value in  attrib.items() ])})")
            elif key == "size":
                # parse size
                attribs_string_list.append(f"size = toga.Size({', '.join([ f'{key} = {value}' for key, value in  attrib.items() ])})")
            elif key == "style":
                # parse style
                style_attrs_list = []
                for style_name, style_value in attrib.items():
                    if style_value in ( "COLUMN", "ROW" ):
                        style_attrs_list.append(f"{style_name} = toga.style.pack.{style_value}")
                    else:
                        if isinstance(style_value, str):
                            style_value = f'"{style_value}"'
                        elif isinstance(style_value, list):
                            style_value = f"{tuple(style_value)}"

                        style_attrs_list.append(f"{style_name} = {style_value}")

                attribs_string_list.append(f"style = toga.style.Pack({', '.join(style_attrs_list)})")
            elif isinstance(attrib, str):
                attribs_string_list.append(f'{key} = "{attrib}"')
            else:
                attribs_string_list.append(f"{key} = {attrib}")

        return ", ".join(attribs_string_list), name
