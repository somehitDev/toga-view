# -*- coding: utf-8 -*-
import toga
from toga_view.parsers import XmlParser, JsonParser
from toga_view.archivers import XmlArchiver, JsonArchiver


app = toga.App("TogaViewTranspileTest", "test.togaview.transpile")

# transpile .ui.xml to .ui.json
JsonArchiver.archive_to_file(
    XmlParser.parse_file("test_origin.ui.xml"),
    "test_origin_transpile.ui.json"
)
# parse .ui.json file into widget
XmlArchiver.archive_to_file(
    JsonParser.parse_file("test_origin.ui.json"),
    "test_origin_transpile.ui.xml"
)

del app
