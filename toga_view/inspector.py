# -*- coding: utf-8 -*-
import inspect, toga, toga.style
from travertino.declaration import BaseStyle


class Inspector:
    @staticmethod
    def inspect(widget:toga.Widget) -> dict:
        inspects = {}
        try:
            specs = inspect.getfullargspec(getattr(toga, widget.__class__.__name__).__init__)
            args, defaults = specs.args[1:], specs.defaults
        except AttributeError:
            specs = inspect.getfullargspec(getattr(toga, widget.__class__.__base__.__name__).__init__)
            args, defaults = specs.args[1:], specs.defaults

        if defaults is not None:
            for name, default_value in zip(args, defaults):
                if not name in ( "id", "resizeable", "closeable", "children" ):
                    try:
                        inspects[name] = getattr(widget, name)
                    except AttributeError:
                        inspects[name] = default_value

        return {
            key: value
            for key, value in inspects.items()
            if value is not None
        }
