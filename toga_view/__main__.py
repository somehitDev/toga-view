# -*- coding: utf-8 -*-

def run_cli():
    import os, argparse, pathlib
    from .parsers import XmlParser, JsonParser

    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest = "command")

    # parse
    cmd_parse = commands.add_parser("parse", help = "parse .ui.xml/.ui.json into .py")
    cmd_parse.add_argument("view_file", help = "view file(.ui.xml/.ui.json)")
    cmd_parse.add_argument("-o", "--output", dest = "output", default = None, help = "output file to write parsed python scripts")
    # transpile
    cmd_transpile = commands.add_parser("transpile", help = "transpile between .ui.xml, .ui.json")
    cmd_transpile.add_argument("view_file", help = "view file(.ui.xml/.ui.json)")
    cmd_transpile.add_argument("-o", "--output", dest = "output", default = None, help = "transpiled output file")

    args = parser.parse_args()

    if args.command == "parse":
        view_file = pathlib.Path(args.view_file).resolve()
        view_file_name, view_file_ext = view_file.name.split(os.path.extsep, 1)
        output_file = args.output or str(view_file.parent.joinpath(f"{view_file_name}.py"))

        if view_file_ext == "ui.xml":
            script_text = XmlParser.parse_file_to_script(str(view_file), view_file_name.replace("_", " ").replace("-", " ").title())
        elif view_file_ext == "ui.json":
            script_text = JsonParser.parse_file_to_script(str(view_file), view_file_name.replace("_", " ").replace("-", " ").title())
        else:
            raise TypeError(f"unsupported file format {view_file_ext}!")

        with open(output_file, "w", encoding = "utf-8") as ofw:
            ofw.write(script_text)
    elif args.command == "transpile":
        import toga
        from .archivers import XmlArchiver, JsonArchiver

        view_file = pathlib.Path(args.view_file).resolve()
        view_file_name, view_file_ext = view_file.name.split(os.path.extsep, 1)

        app = toga.App("TogaViewTranspile", "transpile.toga.view")

        if view_file_ext == "ui.xml":
            # xml -> json
            output_file = args.output or str(view_file.parent.joinpath(f"{view_file_name}.ui.json"))
            JsonArchiver.archive_to_file(
                XmlParser.parse_file(str(view_file)),
                output_file
            )
        elif view_file_ext == "ui.json":
            # json -> xml
            output_file = args.output or str(view_file.parent.joinpath(f"{view_file_name}.ui.xml"))
            XmlArchiver.archive_to_file(
                JsonParser.parse_file(str(view_file)),
                output_file
            )
        else:
            raise TypeError(f"unsupported file format {view_file_ext}!")

        del app
    else:
        parser.print_help()


if __name__ == "__main__":
    run_cli()
