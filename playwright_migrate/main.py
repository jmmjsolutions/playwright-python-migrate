import os
import sys
import shutil
import argparse
from bowler import Query

methods = [
    ("evalOnSelector", "eval_on_selector"),
    ("expectDownload", "expect_download"),
    ("expectFileChooser", "expect_file_chooser"),
    ("newPage", "new_page"),
    ("newContext", "new_context"),
    ("innerText", "inner_text"),
    ("setInputFiles", "set_input_files"),
    ("waitForLoadState", "wait_for_load_state"),
    ("waitForSelector", "wait_for_selector"),
    ("querySelector", "query_selector"),
    ("querySelectorAll", "query_selector_all"),
]


class RefactorTool:
    def __init__(self, input, nobackups, show_diffs):
        """
        Args:
            input: path to file to be refactored.
            nobackups: If true no backup '.bak' files will be created for those
                files that are being refactored.
            show_diffs: Should diffs of the refactoring be printed to stdout?
        """
        self.nobackups = nobackups
        self.show_diffs = show_diffs
        self.fn = input

        self.query = Query([self.fn])

    def rename_methods(self):
        for old_name, new_name in methods:
            self.query.select_method(old_name).rename(new_name)

    def fix_imports(self):
        # Fix old style: from playwright import sync_playwright
        self.query.select_module("sync_playwright").select_module("playwright").rename(
            "playwright.sync_api"
        )
        pass

    def output_diffs(self):
        self.query.diff()

    def write_file(self):
        if not self.nobackups:
            # Make a backup before refactor
            backup = self.fn + ".bak"
            if os.path.lexists(backup):
                try:
                    os.remove(backup)
                except OSError as err:
                    self.log_message("Cannot remove backup %s" % backup)
            try:
                shutil.copyfile(self.fn, backup)
            except OSError as err:
                self.log_message("Cannot copy %s to %s" % (self.fn, backup))
        self.query.write()

    def log_message(self, msg):
        print("Info: " + msg)

    def log_error(self, msg):
        print("Error: " + msg)


def main(args=sys.argv[1:]):
    """Main program.
    Args:
        args: optional; a list of command line arguments. If omitted,
              sys.argv[1:] is used.
    """
    # Set up arg parser
    parser = argparse.ArgumentParser(description="Migrate playwright code to 1.8+")
    parser.add_argument(
        "--no-diffs",
        action="store_true",
        default=False,
        help="Don't show diffs of the refactoring",
    )
    parser.add_argument(
        "-n",
        "--nobackups",
        action="store_true",
        default=False,
        help="Don't write backups for modified files",
    )
    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        default=False,
        help="Write back modified files",
    )
    parser.add_argument("path", metavar="path", type=str, help="the path to the file")
    args = parser.parse_args()

    fix = RefactorTool(args.path, nobackups=False, show_diffs=(not args.no_diffs))
    fix.fix_imports()
    fix.rename_methods()
    if not args.no_diffs:
        fix.output_diffs()
    if args.write:
        fix.write_file()


if __name__ == "__main__":
    main(sys.argv[1:])