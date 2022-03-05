from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

port = int(sys.argv[2])
email = sys.argv[3]
password = sys.argv[4]
if sys.argv[1].lower() == 'chrome':
    driver = webdriver.Chrome()
elif sys.argv[1].lower() == 'firefox':
    driver = webdriver.Firefox()
elif sys.argv[1].lower() == 'opera':
    driver = webdriver.Opera()

try:
    with driver:
        driver.get("https://localhost:{}/".format(port))
        assert len(driver.window_handles) == 1
        form = driver.find_element_by_id("email")
        form.send_keys(email)
        form = driver.find_element_by_id("pass")
        form.send_keys(password)
        form.send_keys(Keys.RETURN)
        form.close()
        page = driver.title
        assert page == "Broker Bot"
        print('Done')
    print('Test Success!')
except:
    print('Test Failure...')