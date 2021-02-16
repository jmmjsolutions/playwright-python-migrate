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

This script will migrate pre-release test cases to the new API. It handles automatic conversion of camelCase method names to snake_case for the following method names:

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


