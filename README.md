<h1 align="center">
    Toga-View
</h1>
<p align="center">
    xml/json view support for toga
</p>
<br/>

<div align="center">
    <img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue" />
    <br>
    <a href="https://github.com/somehitDev/toga-view/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/somehitDev/toga-view.svg" alt="MIT License" />
    </a>
    <a href="https://pypi.org/project/toga-view/">
        <img src="https://img.shields.io/pypi/v/toga-view.svg" alt="pypi" />
    </a>
</div><br><br>

## 🛠️ Features
- **Toga View Format**: support .ui.xml/.ui.json format file.
- **Parse/Archive**
  - support parse ui file and archive python to ui file
  - support parse ui file into python file
  - support transpile ui file between .ui.xml and .ui.json

<br>

## 💿 Installation
- install from git(latest)
```bash
pip install git@github.com:somehitDev/toga-view.git
```
- pypi
```bash
pip install toga-view
```

<br>

## 📑 Usage
- cli
```bash
# parse
toga_view_cli parse {ui_file} -o {py_file}
# transpile
toga_view_cli transpile {ui_file} -o {ui_file of different ext}
```
- python
```python
# parse(into toga.Widget)
XmlParser.parse_file("{ui_file}")
JsonParser.parse_file("{ui_file}")
# parse(into python script)
XmlParser.parse_file_to_script("{ui_file}", "{widget_class_name}")
JsonParser.parse_file_to_script("{ui_file}", "{widget_class_name}")

# archive(into element)
XmlArchiver.archive({toga.Widget})
JsonArchiver.archive({toga.Widget})
# archive(into ui file)
XmlArchiver.archive_to_file({toga.Widget}, "{ui_file}")
JsonArchiver.archive_to_file({toga.Widget}, "{ui_file}")
```
<br>

##  Project Structure
- `toga_view/`: toga-view source.
- `tests/`: examples.
