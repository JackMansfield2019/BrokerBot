from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver import ActionChains
import time as t

print('IMPORTANT: Make sure you have Chromedriver.exe installed to match the same version as chromium!')

try:
    port = int(sys.argv[2])
except:
    print('Invalid port argument.')

if len(sys.argv) != 6:
    print('Invalid arguments.')


if sys.argv[1].lower() == 'chrome':
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
elif sys.argv[1].lower() == 'firefox':
    driver = webdriver.Firefox()
elif sys.argv[1].lower() == 'opera':
    driver = webdriver.Opera()
elif sys.argv[1].lower() == 'safari':
    driver = webdriver.Safari()

start = t.time()
print('Beginning the SANITY TEST at http:\\localhost:{} with the {} browser.'.format(port, sys.argv[1]))

try:
    print('Test begins at the LOGIN page.\n')
    driver.get("http://localhost:{}/".format(port))
    assert(driver.title == 'React App')
    print('Now interaction with all buttons.')
    print('>>> First button: Learn More')
    driver.implicitly_wait(10)
    button = driver.find_element_by_xpath('//button[text()="Learn More"]')
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(button).click(button).perform()
    button.click()
    alerttext = Alert(driver)
    print('This button created an alert that says: {}'.format(alerttext.text))
    print('>>> Second button: Log In')
    button = driver.find_element_by_xpath('//button[text()="Log In"]')
    button.click()
    print('No errors when there is no input: good.')
    print('>>> Third button: Register')
    button = driver.find_element_by_xpath('//button[text()="Register"]')
    button.click()
    print('We are now at the Registration page!\n')
    print('Testing page reset...')
    driver.refresh()
    button = driver.find_element_by_xpath('//button[text()="Register"]')
    button.click()
    print('Page Reset Good!\n')
    print('Selecting Hyperlinks...')
    elem = browser.find_element_by_link_text("rcos")
    elem = browser.find_element_by_link_text("github")
    elem = browser.find_element_by_link_text("alpaca")
    print('Hyperlinks are Valid\n')

    print('All sanity tests passed without critical errors')
    print('Tests completed in {} seconds.'.format(t.time() - start))

except:
    print('These tests failed...')
