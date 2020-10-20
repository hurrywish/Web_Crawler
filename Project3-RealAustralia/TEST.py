

from selenium import webdriver

options = webdriver.ChromeOptions()
PROXY = "127.0.0.1:8080"
options.add_argument('--proxy-server=%s'%PROXY)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})


driver = webdriver.Chrome(options = options)
driver.get('https://www.realestate.com.au/sold/in-vic/list-1')
print(driver.page_source)
