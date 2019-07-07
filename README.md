<img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Twelve_Labours_Altemps_Inv8642.jpg" height="300px"/>

# Kelley's Heracles Notes

## My Plan + Execution
  As suggested: "A simplesimple HTML page with an input box", mine uses a bit of javascript and HTML. I "borrowed" the code that does the formatting from somewhere on the web and then modified it to make it what I needed it to be. I would expect that the testing side is more important than building better formatter (I could be wrong, though :) so I didn't spend a ton of time building it, I spent more time testing it. It's pretty...but not beautiful.

  I created a small suite of test cases in Python using Selenium WebDriver and pytest. There are some basic GUI tests, that could be expanded on (I have put information in the comments) but I moved on to other tests. There is a block of the Acceptance Tests that are specified in the requirements. Then there are the tests to check that it is doing the work it is supposed to do with a veritable array of inputs (literally and figuratively) - does it format correctly, does it only do numbers, Zero is a special case, is the rounding correct, what does it do when you throw garbage at it, etc. Of course there was some manual testing to start - the visual checks are all human eye, and some exploratory testing, both methodical and random. I also planned out the tests before I wrote them up, to make sure the coverage was decent, but not over the top.

  Because the application is so simple the testing is easier - it doesn't read or write anything to disk, or a database, or even store data in any way. I don't have to sanitize the strings for any environment (e.g. SQL injection, messing with a server or issuing any other rogue commands). It is pretty rigid in what it accepts - it's either a number or it's not a number. There are still over 100 tests. (That big list of naughty strings is a great collection!) I don't have it running headless, I think it's fun to watch, but headless is faster, in general - it's doing these tests in under 90 seconds, it wouldn't be that much faster.

  There is always more you can do with automation, e.g. I could have created a small framework to reduce the amount of code in the tests by creating a function for the entry field - a single call to pass the data, but it was a minor savings because it is such a tiny app...if this had multiple web pages with many fields, it would be a big saver for the writing and maintaining of the test, especially if GUI changes break something, I only have to update the function and not every test that uses that field.

  I have setup Jenkins, it pulls from my github repo, but it's running locally, so it is hitting the local webserver running the local version of the HTML page.  I also have it set up to export the JUnitXML reports so that it can track pass/fail history. With more data gathered over time it can graph that and one can see trends. Not very realistic, but it looks good. With more horsepower, and build machines, you can use xdist to test in parallel on multiple nodes. If there was an actual test server to deploy to (and it wasn't using the local webserver) you could set up Jenkins to poll for new content and deploy the new build and then kick off the tests. I have included some screen captures and a video to the repo.

## Software I am Using
  * git
  * Python 3.7.3
  * Selenium WebDriver with Chromedriver
  * pytest
  * Python SimpleHTTPServer
  * Jenkins

## And I found some bugs! :)
  There is a rounding issue in the underlying code...the code used for the formatter is not great, but it does the job, for the most part. Should totally be refactored, but I am going for speed here...

  * 555.555 incorrectly rounds to 555.55, however 0.555 rounds to 0.56
  * -0.00001, returns -0.00 when all the other zero based tests return 0.00
  * 500.005 should round to 500.01, but the code returns 500.00
