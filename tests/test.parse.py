# -*- coding: utf-8 -*-
import toga
from toga_view.parsers import XmlParser, JsonParser


app = toga.App("TogaViewParseTest", "test.togaview.parse")

# parse .ui.xml file into widget
print(XmlParser.parse_file("test_origin.ui.xml"))
# parse .ui.json file into widget
print(JsonParser.parse_file("test_origin.ui.json"))

# parse .ui.xml file into script
print(XmlParser.parse_file_to_script("test_origin.ui.xml"))
# parse .ui.json file into script
print(JsonParser.parse_file_to_script("test_origin.ui.json"))

del app
