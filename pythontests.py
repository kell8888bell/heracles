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

  def test_testGUI(self):
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

  def test_testAcceptance(self):
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

  def test_testValues(self):
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1022, 726)

    # test negative/positive integers and negative/positive floats, plus sign number
    inputListInt = [111, 2222, 333333, 44444444, -555, -6666, -777777, -88888888, "+1"]
    outputListInt = ["111.00", "2 222.00", "333 333.00", "44 444 444.00", \
                     "-555.00", "-6 666.00", "-777 777.00", "-88 888 888.00", "1.00"]
    inputListFlt = ["111.111", "2222.2222", "333333.333333", "44444444.44444444", \
                    "-555.555", "-6666.6666", "-777777.777777", "-88888888.88888888", "+1.0"]
    outputListFlt = ["111.11", "2 222.22", "333 333.33", "44 444 444.44", \
                     "-555.55", "-6 666.67", "-777 777.78", "-88 888 888.89", "1.00"]
    listLength = len(inputListInt)
    i = 0
    while i < listLength:
        self.browser.find_element(By.ID, "inputValue").click()
        self.browser.find_element(By.ID, "inputValue").send_keys(inputListInt[i])
        self.browser.find_element(By.ID, "myButton").click()
        assert self.browser.find_element(By.ID, "letsGo").text == "Result: " + outputListInt[i]
        self.browser.refresh();   # refresh to start clean
        self.browser.find_element(By.ID, "inputValue").click()
        self.browser.find_element(By.ID, "inputValue").send_keys(inputListFlt[i])
        self.browser.find_element(By.ID, "myButton").click()
        assert self.browser.find_element(By.ID, "letsGo").text == "Result: " + outputListFlt[i]
        self.browser.refresh();   # refresh to start clean
        i += 1

    # test positive/negative mixed number of decimal places, with and without leading 0
    inputListDecWith = ["0.111", "0.44444444", "0.1234567890123456789012345678901234567890", \
                        "-0.555", "-0.88888888", "-0.1234567890123456789012345678901234567890"]
    inputListDecWO = [".111", ".44444444", ".1234567890123456789012345678901234567890", \
                      "-.555", "-.88888888", "-.1234567890123456789012345678901234567890"]
    outputListDec = ["0.11", "0.44", "0.12", "-0.56", "-0.89", "-0.12"]
    listLength = len(inputListDecWith)
    i = 0
    while i < listLength:
        self.browser.find_element(By.ID, "inputValue").click()
        self.browser.find_element(By.ID, "inputValue").send_keys(inputListDecWith[i])
        self.browser.find_element(By.ID, "myButton").click()
        assert self.browser.find_element(By.ID, "letsGo").text == "Result: " + outputListDec[i]
        self.browser.refresh();   # refresh to start clean
        self.browser.find_element(By.ID, "inputValue").click()
        self.browser.find_element(By.ID, "inputValue").send_keys(inputListDecWO[i])
        self.browser.find_element(By.ID, "myButton").click()
        assert self.browser.find_element(By.ID, "letsGo").text == "Result: " + outputListDec[i]
        self.browser.refresh();   # refresh to start clean
        i += 1

    # positive and negative zeroes with and without leading 0 (THIS FAILS: "-0.00001", returns "-0.00")
    inputListZeros = [0, -0, "0.0", "-0.0", ".0", "-.0", "0.", "-0.", "0.00", "-0.00", \
                      "0.0000", "-0.0000", "0.00001", ".00", "-.00", ".0000", "-.0000", ".00001"]
    listLength = len(inputListZeros)
    i = 0
    while i < listLength:
        self.browser.find_element(By.ID, "inputValue").click()
        self.browser.find_element(By.ID, "inputValue").send_keys(inputListZeros[i])
        self.browser.find_element(By.ID, "myButton").click()
        assert self.browser.find_element(By.ID, "letsGo").text == "Result: 0.00"
        self.browser.refresh();   # refresh to start clean
        i += 1

    #BIG numbers - using e+ (exponent) numbers in and out
    inputListBig = [1234567890123456789012345678901234567890, -1234567890123456789012345678901234567890, \
                     "1234567890123456789012345678901234567890.1234567890123456789012345678901234567890", \
                     "-1234567890123456789012345678901234567890.1234567890123456789012345678901234567890", \
                     ".1234567890123456789012345678901234567890", "0.1234567890123456789012345678901234567890", \
                     "-.1234567890123456789012345678901234567890", "-0.1234567890123456789012345678901234567890", \
                     "1.524157875019e+16", "-1.524157875019e+16", "152e2", "-152e2" ]
    outputListBig = ["1.2345678901234568e+39", "-1.2345678901234568e+39", \
                     "1.2345678901234568e+39", "-1.2345678901234568e+39", \
                     "0.12", "0.12", "-0.12", "-0.12", \
                     "15 241 578 750 190 000.00", "-15 241 578 750 190 000.00", "15 200.00", "-15 200.00"]
    listLength = len(inputListBig)
    i = 0
    while i < listLength:
        self.browser.find_element(By.ID, "inputValue").click()
        self.browser.find_element(By.ID, "inputValue").send_keys(inputListBig[i])
        self.browser.find_element(By.ID, "myButton").click()
        assert self.browser.find_element(By.ID, "letsGo").text == "Result: " + outputListBig[i]
        self.browser.refresh();   # refresh to start clean
        i += 1

  def test_testRounding(self):
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1022, 726)

    # rounding up and down at the edge cases  - another bug here where 500.005 rounds to 500.00 and not 500.01
    inputListRnd = ["100.1", "100.01", "100.011", "100.001", \
                    "400.4", "400.04", "400.044", "400.004", \
                    "500.5", "500.05", "500.055", "500.005", \
                    "600.6", "600.06", "600.066", "600.006", \
                    "900.9", "900.09", "900.099", "900.009"]
    outputListRnd = ["100.10", "100.01", "100.01", "100.00", \
                     "400.40", "400.04", "400.04", "400.00", \
                     "500.50", "500.05", "500.06", "500.00", \
                     "600.60", "600.06", "600.07", "600.01", \
                     "900.90", "900.09", "900.10", "900.01"]
    listLength = len(inputListRnd)
    i = 0
    while i < listLength:
        self.browser.find_element(By.ID, "inputValue").click()
        self.browser.find_element(By.ID, "inputValue").send_keys(inputListRnd[i])
        self.browser.find_element(By.ID, "myButton").click()
        assert self.browser.find_element(By.ID, "letsGo").text == "Result: " + outputListRnd[i]
        self.browser.refresh();   # refresh to start clean
        i += 1

  def test_testJunk(self):
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1022, 726)

    # junk testing...woohoo! now it's getting fun :)
    # these work: 0100 -0100 0100.99 0xabad1dea, 0x0 (and hex in general)
    inputListJunk = ["Kelley", "( ͡° ͜ʖ ͡°)", "show me the money", "admin", "test", \
                     "NULL", "null", "true", "false", "TRUE", "FALSE", \
                     "+-100", "-+100", "--100", "++100", "0..0", "0.0.0", ".0.0", \
                     "1,000.00", "1 000.00","1.000,00","1'000.00","1'000,00","1,000.00", \
                     "$100", "100$", "$100.00", "$ 100", "EUR100", "EUR 100", "100 EUR", \
                     "מנסעפצק", "بريطانيا" "あいうえおの", "部落格", "â ç è é ê î ô û", \
                     "~!@#$", "%^&*(", ")-_=+]", "[{}|;", "':,./<>?", "=≤≥≠", "« »"]
    listLength = len(inputListJunk)
    i = 0
    while i < listLength:
        self.browser.find_element(By.ID, 'inputValue').click()
        self.browser.find_element(By.ID, 'inputValue').send_keys(inputListJunk[i])
        self.browser.find_element(By.ID, 'myButton').click()
        assert self.browser.find_element(By.ID, 'letsGo').text == 'Result: Not a valid number'
        self.browser.refresh()  # refresh to start clean
        i += 1
