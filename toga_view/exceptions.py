# -*- coding: utf-8 -*-
from toga import __version__


class VersionMismatchException(Exception):
    def __init__(self, ui_version:str, *args):
        super().__init__(f"{ui_version} not match with toga({__version__})!", *args)

class UnknownWidgetException(Exception):
    def __init__(self, tag:str, *args):
        super().__init__(f"Unknown widget class {tag}!", *args)
