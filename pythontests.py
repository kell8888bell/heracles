import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

class TestTestGUI():
  def setup_method(self, method):
    self.browser = webdriver.Chrome()
    # self.options = webdriver.ChromeOptions()
    # run headless
    # self.options.add_argument('headless')
    # set the window size
    # self.options.add_argument('window-size=1200x600')
    # initialize the driver
    #self.browser = webdriver.Chrome(chrome_options=options)
    self.vars = {}

  def teardown_method(self, method):
    self.browser.quit()

  def PASSINGtest_testGUI(self):
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1022, 726)
    assert self.browser.find_element(By.CSS_SELECTOR, "h2").text == "Challenge for Pleo"
    assert self.browser.find_element(By.ID, "inputValue").get_attribute('placeholder') == "amount"
    assert self.browser.find_element(By.ID, "inputValue").text == ""
    assert self.browser.find_element(By.ID, "myButton").text == "Submit"
    # check that there are no results
    assert self.browser.find_element(By.ID, "letsGo").text == ""
    # create some results to check for new info
    self.browser.find_element(By.ID, "inputValue").click()
    self.browser.find_element(By.ID, "inputValue").send_keys("1.00")
    self.browser.find_element(By.ID, "myButton").click()
    assert self.browser.find_element(By.ID, "letsGo").text == "Result: 1.00"
    # refresh to clear data
    self.browser.refresh();
    # check that it reset the page
    assert self.browser.find_element(By.ID, "inputValue").get_attribute('placeholder') == "amount"
    assert self.browser.find_element(By.ID, "inputValue").text == ""
    assert self.browser.find_element(By.ID, "letsGo").text == ""
    # can also check tabbing order and key press button works
    # haven't coded front end for enter key, could also di that and test for it

  def test_testValues(self):
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1022, 726)
    # 0
    # negative, positive integers
    # negative, positive floats
    # decimal places 0 1 2 3 4 5 10 50 100 what about E numbers?
    # positive and negative 0. 0.0 0.00 0.0000 0.1 0.01 0.000001
    # rounding up and down .4 .03 .002 .00001 .8 .07 .006 .00555
    # huge numbers positive and negative
    # junk testing


  def PASSINGtest_testAcceptance(self):
    # data provided by Challenge
    #    formatMoney(2310000.159897); // '2 310 000.16'
    #    formatMoney(1600); // '1 600.00'
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1022, 726)
    self.browser.find_element(By.ID, "inputValue").click()
    self.browser.find_element(By.ID, "inputValue").send_keys("2310000.159897")
    self.browser.find_element(By.ID, "myButton").click()
    assert self.browser.find_element(By.ID, "letsGo").text == "Result: 2 310 000.16"
    self.browser.refresh();   # refresh to start clean
    self.browser.find_element(By.ID, "inputValue").click()
    self.browser.find_element(By.ID, "inputValue").send_keys("1600")
    self.browser.find_element(By.ID, "myButton").click()
    assert self.browser.find_element(By.ID, "letsGo").text == "Result: 1 600.00"


    #elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
