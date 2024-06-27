# -*- coding: utf-8 -*-
import sys, toga
# from test_origin_xml import TestOrigin
from test_origin_json import TestOrigin

class TestApp(toga.App):
    def startup(self):
        self.main_window = TestOrigin()

        self.main_window.show()

if __name__ == "__main__":
    sys.exit(TestApp("TogaView", "com.togaxmlview").main_loop())
