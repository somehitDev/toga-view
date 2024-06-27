# -*- coding: utf-8 -*-
import toga
from toga_view.archivers import XmlArchiver, JsonArchiver


app = toga.App("TogaViewArchiveTest", "test.togaview.archive")

# load ui from python file
from test_widget import TestWidget

# archive to .ui.xml
XmlArchiver.archive_to_file(TestWidget(), "test_origin_archive.ui.xml")
# parse .ui.json file into script
JsonArchiver.archive_to_file(TestWidget(), "test_origin_archive.ui.json")

del app
