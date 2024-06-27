# -*- coding: utf-8 -*-
import pathlib, json, toga, toga.style, toga.style.pack, json, re
from ..inspector import Inspector


class JsonArchiver:
    @staticmethod
    def archive(widget:toga.Widget, name:str = None) -> dict:
        return {
            "toga-version": toga.__version__,
            "root": JsonArchiver._archive_widget(widget, name, True)
        }

    @staticmethod
    def archive_to_file(widget:toga.Widget, json_file:str, indent:int = 4):
        with open(str(pathlib.Path(json_file).resolve()), "w", encoding = "utf-8") as jfw:
            json.dump(JsonArchiver.archive(widget), jfw, indent = indent)


    @staticmethod
    def _archive_widget(widget:toga.Widget, name:str = None, include_name:bool = False) -> dict:
        widget_cls_name = widget.__class__.__name__
        if not hasattr(toga, widget_cls_name):
            widget_cls_name = widget.__class__.__base__.__name__

        widget_dict = {
            "class": widget_cls_name,
            "properties": JsonArchiver._archive_properties(Inspector.inspect(widget))
        }
        if hasattr(widget, "style"):
            widget_dict["properties"]["style"] = {
                key: widget.style[key].upper() if widget.style[key] in ( "column", "row" ) else widget.style[key]
                for key in widget.style.keys()
            }

        if include_name:
            widget_dict["properties"]["name"] = name or "".join([ part.capitalize() for part in re.findall("[A-Z][^A-Z]*", widget_cls_name) ])

        if hasattr(widget, "content"):
            # if window
            widget_dict["content"] = JsonArchiver._archive_widget(widget.content)
        elif widget.can_have_children:
            widget_dict["items"] = [
                JsonArchiver._archive_widget(child_widget)
                for child_widget in widget.children
            ]

        return widget_dict

    @staticmethod
    def _archive_properties(args_info:dict) -> dict:
        json_args = {}

        # remove content from attribs
        args_info.pop("content", None)

        for name, value in args_info.items():
            if isinstance(value, toga.Position):
                json_args[name] = { "x": int(value.x), "y": int(value.y) }
            elif isinstance(value, toga.Size):
                json_args[name] = { "width": int(value.width), "height": int(value.height) }
            elif name.startswith("on_"):
                if value is not None and not isinstance(value, bool):
                    json_args[name] = value.__name__
            else:
                json_args[name] = value

        return json_args
