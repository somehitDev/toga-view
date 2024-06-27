# -*- coding: utf-8 -*-

##################################################################
# Generated from reading file 'test_origin.ui.xml'
# Created by: toga-view version 0.0.1
# WARNING! All changes in this file will be lost when regenerated!
##################################################################

import toga, toga.style, toga.style.pack

class TestOrigin(toga.MainWindow):
    def __init__(self, *args, **kwargs):
        kwargs.update(title = "toga view", position = toga.Position(200, 200), size = toga.Size(500, 300), resizable = "False")
        super().__init__(*args, **kwargs)

        self.box = toga.Box(style = toga.style.Pack(direction = toga.style.pack.COLUMN))
        self.label = toga.Label(text = "Hello, World!", style = toga.style.Pack(font_size = 24))

        self.box.add(self.label)
        self.button = toga.Button(text = "Press Me", style = toga.style.Pack(padding = 5))

        self.box.add(self.button)

        self.content = self.box
