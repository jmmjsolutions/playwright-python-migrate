# Migrate pre-release Python Playwright test cases to the Playwright 1.8 API

With Python Playwright moving from pre to release with version 1.8, the API has changed since the last 0.170.0 pre-release version:
- Snake case notation for methods and arguments:

  ```py
  # old
  browser.newPage()
  ```
  ```py
  # new
  browser.new_page()
  ```

- Import has changed to include sync vs async mode explicitly:
  ```py
  # old
  from playwright import sync_playwright
  ```
  ```py
  # new
  from playwright.sync_api import sync_playwright
  ```

This script will migrate pre-release test cases to the new API. It uses Bowler (https://pybowler.io/) to do the heavy lifting for migration. The script handles automatic conversion of camelCase method names to snake_case for the following method names:

```
evalOnSelector to eval_on_selector 
expectDownload to expect_download
expectFileChooser to expect_file_chooser
newPage to new_page
newContext to new_context
innerText to inner_text
setInputFiles to set_input_files
waitForLoadState to wait_for_load_state
waitForSelector to wait_for_selector
querySelector to query_selector
querySelectorAll to query_selector_all
```

It will also fix sync_playwright imports of the following format:

```py
from playwright import sync_playwright
```

## Install / Setup

The Playwright migration utility can be installed from [GitHub](https://github.com/jmmjsolutions/playwright-python-migrate) using [pip](http://www.pip-installer.org)
    
    pip install git+https://github.com/jmmjsolutions/playwright-python-migrate.git


... or download the source distribution from [GitHub](https://github.com/jmmjsolutions/playwright-python-migrate/archive/master.zip), unarchive, and run

    python setup.py install

## Usage

The Playwright migration utility is a Python program that reads the test case source code and applies a series of fixers to transform the test case to valid Playwright 1.8.0 API calls.

So if we have a simple test case source file: test_example.py

```py
from playwright import sync_playwright

with sync_playwright() as pw:
    browser = pw.webkit.launch(headless=False)
    context = browser.newContext()
    page = context.newPage()
    page.goto("https://playwright.dev/python/docs/intro/")

    assert page.url == "https://playwright.dev/python/docs/intro/"

    browser.close()
```

We can run the migration utility in a non destructive mode to see what changes would be made.

```
playwright-migrate test_example.py
```
This will produce the following output on the console:

```diff
--- test_example.py
+++ test_example.py
@@ -1,9 +1,9 @@
-from playwright import sync_playwright
+from playwright.sync_api import sync_playwright

 with sync_playwright() as pw:
     browser = pw.webkit.launch(headless=False)
-    context = browser.newContext()
-    page = context.newPage()
+    context = browser.new_context()
+    page = context.new_page()
     page.goto("https://playwright.dev/python/docs/intro/")

     assert page.url == "https://playwright.dev/python/docs/intro/"
```

To apply the changes to the actual source code, run the migration utility with the --write argument. The utility creates a backup e.g. test_example.py.bak before overwriting the original file with the changes.

```
playwright-migrate --write test_example.py
```

The test_example.py file will now look like:

```py
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.webkit.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://playwright.dev/python/docs/intro/")

    assert page.url == "https://playwright.dev/python/docs/intro/"

    browser.close()
```


