import os
import sys
import shutil
import argparse
from bowler import Query

methods = [
    ("addInitScript", "add_init_script"),
    ("addScriptTag", "add_script_tag"),
    ("addStyleTag", "add_style_tag"),
    ("bringToFront", "bring_to_front"),
    ("dispatchEvent", "dispatch_event"),
    ("emulateMedia", "emulate_media"),
    ("evalOnSelector", "eval_on_selector"),
    ("evalOnSelectorAll", "eval_on_selector_all"),
    ("evaluateHandle", "evaluate_handle"),
    ("expectDownload", "expect_download"),
    ("expectFileChooser", "expect_file_chooser"),
    ("exposeBinding", "expose_binding"),
    ("exposeFunction", "expose_function"),
    ("newPage", "new_page"),
    ("newContext", "new_context"),
    ("innerHTML", "inner_html"),
    ("innerText", "inner_text"),
    ("setContent", "set_content"),
    ("setDefaultNavigationTimeout", "set_default_navigation_timeout"),
    ("setDefaultTimeout", "set_default_timeout"),
    ("setExtraHTTPHeaders", "set_extra_http_headers"),
    ("setInputFiles", "set_input_files"),
    ("setViewportSize", "set_viewport_size"),
    ("textContent", "text_content"),
    ("viewportSize", "viewport_size"),
    ("waitForEvent", "wait_for_event"),
    ("waitForFunction","wait_for_function"),
    ("waitForLoadState", "wait_for_load_state"),
    ("waitForSelector", "wait_for_selector"),
    ("querySelector", "query_selector"),
    ("querySelectorAll", "query_selector_all"),
    ("waitForTimeout","wait_for_timeout"),
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