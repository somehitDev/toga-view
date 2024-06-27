# -*- coding: utf-8 -*-
import toga, toga.style, toga.style.pack, re
from xml.etree import ElementTree as ET
from xml.dom.minidom import parseString
from ..inspector import Inspector


class XmlArchiver:
    @staticmethod
    def archive(widget:toga.Widget, name:str = None) -> ET.Element:
        ui_element = ET.Element("ui", { "toga-version": toga.__version__ })
        ui_element.append(XmlArchiver._archive_widget(widget, name, name is not None))

        return ui_element
    
    @staticmethod
    def archive_to_file(widget:toga.Widget, xml_file:str, indent:int = 2):
        with open(xml_file, "w", encoding = "utf-8") as mfw:
            mfw.write(
                parseString(
                    ET.tostring(
                        XmlArchiver.archive(widget),
                        encoding = "utf-8",
                        method = "xml"
                    ).decode("utf-8")
                ).toprettyxml(" " * indent).replace(
                    '<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>'
                )
            )


    @staticmethod
    def _archive_widget(widget:toga.Widget, name:str = None, include_name:bool = False) -> ET.Element:
        widget_cls_name = widget.__class__.__name__
        if not hasattr(toga, widget_cls_name):
            widget_cls_name = widget.__class__.__base__.__name__

        widget_element = ET.Element(widget_cls_name)
        if include_name:
            widget_element.attrib["name"] = name or "".join([ part.capitalize() for part in re.findall("[A-Z][^A-Z]*", widget_cls_name) ])

        for key, value in XmlArchiver._archive_attribs(Inspector.inspect(widget)).items():
            widget_element.attrib[key] = value

        if hasattr(widget, "style"):
            widget_element.attrib["style"] = ";".join([
                f"{key}:{widget.style[key].upper() if widget.style[key] in ( 'column', 'row' ) else widget.style[key]}"
                for key in widget.style.keys()
            ])

        if hasattr(widget, "content"):
            # if window
            content_element = ET.Element("content")
            content_element.append(XmlArchiver._archive_widget(widget.content))
            widget_element.append(content_element)
        elif widget.can_have_children:
            items_element = ET.Element("items")
            for child_widget in widget.children:
                items_element.append(XmlArchiver._archive_widget(child_widget))

            widget_element.append(items_element)
        
        return widget_element

    @staticmethod
    def _archive_attribs(args_info:dict) -> dict:
        xml_args = {}

        # remove content from attribs
        args_info.pop("content", None)

        for name, value in args_info.items():
            if isinstance(value, toga.Position):
                xml_args[name] = f"{int(value.x)},{int(value.y)}"
            elif isinstance(value, toga.Size):
                xml_args[name] = f"{int(value.width)},{int(value.height)}"
            elif name.startswith("on_"):
                if value is not None and not isinstance(value, bool):
                    xml_args[name] = value.__name__
            else:
                xml_args[name] = str(value)

        return xml_args
