import pytest
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestTestGUI():
  def setup_method(self, method):
    #chrome_options = Options()
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--headless")
    #self.browser = webdriver.Chrome(options=chrome_options)
    self.browser = webdriver.Chrome()
    self.vars = {}
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1000, 725)

  def teardown_method(self, method):
    self.browser.quit()

  def check_result(self, input):
    self.browser.find_element(By.ID, "inputValue").click()
    self.browser.find_element(By.ID, "inputValue").send_keys(input)
    self.browser.find_element(By.ID, "myButton").click()
    return self.browser.find_element(By.ID, "letsGo").text

  def test_testGUI(self):
    assert self.browser.find_element(By.CSS_SELECTOR, "h2").text == "Challenge for Pleo"
    assert self.browser.find_element(By.ID, "inputValue").get_attribute('placeholder') == "amount"
    assert self.browser.find_element(By.ID, "inputValue").text == ""
    assert self.browser.find_element(By.ID, "myButton").text == "Submit"
    # check that there are no results
    assert self.browser.find_element(By.ID, "letsGo").text == ""
    # create some results to check for new info
    assert self.check_result("1.00") == "Result: 1.00"
    # refresh to clear data
    self.browser.refresh();
    # check that it reset the page
    assert self.browser.find_element(By.ID, "inputValue").get_attribute('placeholder') == "amount"
    assert self.browser.find_element(By.ID, "inputValue").text == ""
    assert self.browser.find_element(By.ID, "letsGo").text == ""
    # OTHER TESTS: can also check tabbing order, key press button works,
    # that the image appears, a whole load of things can be tested, depending
    # on their importance to the app and the changabilty
    # haven't coded front end for enter key
    # haven't coded for a cancel button, that could clear the fields

  def test_testAcceptance(self):
    # data provided by Challenge
    #    formatMoney(2310000.159897); // '2 310 000.16'
    #    formatMoney(1600); // '1 600.00'
    assert self.check_result("2310000.159897") == "Result: 2 310 000.16"
    self.browser.refresh();   # refresh to start clean
    assert self.check_result("1600") == "Result: 1 600.00"

  # this while loop test take 10 seconds to run because it uses a single broswer window
  def test_testValuesIntegers(self):
    # test negative/positive integers
    inputListInt = [111, 2222, 333333, 44444444, -555, -6666, -777777, -88888888]
    outputListInt = ["111.00", "2 222.00", "333 333.00", "44 444 444.00", \
                     "-555.00", "-6 666.00", "-777 777.00", "-88 888 888.00"]
    listLength = len(inputListInt)
    i = 0
    while i < listLength:
        assert self.check_result(inputListInt[i]) == "Result: " + outputListInt[i]
        self.browser.refresh();
        i += 1

  # this parameterized test take 60 seconds to run
  # it launches a fresh browser for every value
  # it does make it easier to see the individual results
  # with testdata being defined before, it's harder to read
  # even though the test itself is only one line
  testdata = [(111, "111.00"),(2222, "2 222.00"),
              (333333, "333 333.00"),(44444444, "44 444 444.00"),
              (-555, "-555.00"),(-6666, "-6 666.00"),
              (-777777, "-777 777.00"),(-88888888, "-88 888 888.00")]
  @pytest.mark.skip(reason="it's too slow")
  @pytest.mark.parametrize("input, output", testdata)
  def test_testValuesIntegersP(self, input, output):
    # test negative/positive integers
    assert self.check_result(input) == "Result: " + output

  def test_testValuesFloats(self):
    # test negative/positive floats
    inputListFlt = ["111.111", "2222.2222", "333333.333333", "44444444.44444444", \
                    "-6666.6666", "-777777.777777", "-88888888.88888888"]
    outputListFlt = ["111.11", "2 222.22", "333 333.33", "44 444 444.44", \
                     "-6 666.67", "-777 777.78", "-88 888 888.89"]
    listLength = len(inputListFlt)
    i = 0
    while i < listLength:
        assert self.check_result(inputListFlt[i]) == "Result: " + outputListFlt[i]
        self.browser.refresh();
        i += 1

  def test_testValuesLeadingZero(self):
    # test positive/negative mixed number of decimal places, with and without leading 0
    inputListDecWith = ["0.111", "0.44444444", "0.1234567890123456789012345678901234567890", \
                        "-0.555", "-0.88888888", "-0.1234567890123456789012345678901234567890"]
    inputListDecWO = [".111", ".44444444", ".1234567890123456789012345678901234567890", \
                      "-.555", "-.88888888", "-.1234567890123456789012345678901234567890"]
    outputListDec = ["0.11", "0.44", "0.12", "-0.56", "-0.89", "-0.12"]
    listLength = len(inputListDecWith)
    i = 0
    while i < listLength:
        assert self.check_result(inputListDecWith[i]) == "Result: " + outputListDec[i]
        self.browser.refresh();
        assert self.check_result(inputListDecWO[i]) == "Result: " + outputListDec[i]
        self.browser.refresh();
        i += 1

  def test_testZeros(self):
    # test positive and negative zeroes with and without leading 0 - see FAILtest_testRound2 for bug test
    inputListZeros = [0, -0, "0.0", "-0.0", ".0", "-.0", "0.", "-0.", "0.00", "-0.00", \
                      "0.0000", "-0.0000", "0.00001", ".00", "-.00", ".0000", "-.0000", ".00001"]
    listLength = len(inputListZeros)
    i = 0
    while i < listLength:
        assert self.check_result(inputListZeros[i]) == "Result: 0.00"
        self.browser.refresh();
        i += 1

  def test_testBigNumbers(self):
    # test large numbers - using e/e+ (exponent) numbers in and out
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
        assert self.check_result(inputListBig[i]) == "Result: " + outputListBig[i]
        self.browser.refresh();
        i += 1

  def test_testRounding(self):
    # test rounding up and down at the edge cases - see FAILtest_testRound3 for bug test
    inputListRnd = ["100.1", "100.01", "100.011", "100.001", \
                    "400.4", "400.04", "400.044", "400.004", \
                    "500.5", "500.05", "500.055", \
                    "600.6", "600.06", "600.066", "600.006", \
                    "900.9", "900.09", "900.099", "900.009"]
    outputListRnd = ["100.10", "100.01", "100.01", "100.00", \
                     "400.40", "400.04", "400.04", "400.00", \
                     "500.50", "500.05", "500.06", \
                     "600.60", "600.06", "600.07", "600.01", \
                     "900.90", "900.09", "900.10", "900.01"]
    listLength = len(inputListRnd)
    i = 0
    while i < listLength:
        assert self.check_result(inputListRnd[i]) == "Result: " + outputListRnd[i]
        self.browser.refresh();
        i += 1

  def test_testJunkShouldFail(self):
    # test that stuff that is not a number returns that message
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
        assert self.check_result(inputListJunk[i]) == "Result: Not a valid number"
        self.browser.refresh();
        i += 1

  def test_testJunkShouldPass(self):
    # test that stuff that is technically a number is ok
    inputListJunk2 = ["0100", "-0100", "0100.99", "0xabad1dea", "0x0", "+1", "+1.0"]
    outputListJunk2 = ["100.00", "-100.00", "100.99", "2 880 249 322.00", "0.00", "1.00", "1.00"]
    listLength = len(inputListJunk2)
    i = 0
    while i < listLength:
        assert self.check_result(inputListJunk2[i]) == "Result: " + outputListJunk2[i]
        self.browser.refresh();
        i += 1

  @pytest.mark.skip(reason="run with intention - it takes about an hour")
  def test_testHammer(self):
    # hammer the field with data continiously
    inputHammer = 8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    i = 0
    while i < 5000:
        assert self.check_result(inputHammer) == "Result: 8.888888888888888e+99"
        self.browser.refresh();
        i += 1

  ######################
  ### TESTS FOR BUGS ###
  ######################

  @pytest.mark.skip(reason="this is a bug that hasn't been fixed - .555 rounding")
  def test_testRound1(self):
    # bug where 500.005 rounds to 500.00 and not 500.01
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1000, 725)
    assert self.check_result("555.555") == "Result: 555.56"

  @pytest.mark.skip(reason="this is a bug that hasn't been fixed - returns negative 0")
  def test_testRound2(self):
    # bug where -0.00001 rounds to -0.00 and not 0.00
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1000, 725)
    assert self.check_result("-0.00001") == "Result: 0.00"

  @pytest.mark.skip(reason="this is a bug that hasn't been fixed - .005 rounding")
  def test_testRound3(self):
    # bug where 500.005 rounds to 500.00 and not 500.01
    self.browser.get("http://localhost:1337/FormatMoney.html")
    self.browser.set_window_size(1000, 725)
    assert self.check_result("500.005") == "Result: 500.01"
