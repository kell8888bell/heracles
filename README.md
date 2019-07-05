<img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Twelve_Labours_Altemps_Inv8642.jpg" height="300px"/>

# Kelley's Heracles Notes

## My Plan + Execution
  As suggested: "A simplesimple HTML page with an input box", mine uses a bit of javascript and HTML. I "borrowed" the code that does the formatting from somewhere on the web and then modified it to make it what I needed it to be. I would expect that the testing side is more important than building better formatter (I could be wrong, though :) so I didn't spend a ton of time building it, I spent more time testing it. It's pretty...but not beautiful.

  I am creating a small suite of test cases in Python using Selenium WebDriver and pytest. There are some basic GUI tests, that can be expanded, I have put information in the comments. There is a block of the Acceptance Tests that are specified in the requirements. Then there are the tests to check that it is doing the work it is supposed to do, with an array of inputs (literally and figuratively).

  Because the application is so simple the testing is easier - it doesn't read or write anything to disk, or a database, or even store data in any way. I don't have to sanitize the strings for any environment (e.g. SQL injection, messing with a server or issuing any other rogue commands). It is pretty rigid in what it accepts - it's either a number or it's not a number. There are still over 100 tests.

## Software I am Using
  * git
  * Python 3.7.3
  * Selenium WebDriver with Chromedriver
  * pytest
  * Python SimpleHTTPServer
      * python -m http.server 1337
      * http://localhost:1337/FormatMoney.html

## And I found some bugs! :)
  There is a rounding issue in the underlying code...the code used for the formatter is not great, but it does the job, for the most part. Should totally be refactored, but I am going for speed here...

  * 555.555 incorrectly rounds to 555.55, however 0.555 rounds to 0.56
  * -0.00001, returns -0.00 when all the other zero based tests return 0.00
  * 500.005 should round to 500.01, but the code returns 500.00
