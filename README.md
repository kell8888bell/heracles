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
  * Jenkins with Shining Panda

## And I found some bugs! :)
  There is a rounding issue in the underlying code...the code used for the formatter is not great, but it does the job, for the most part. Should totally be refactored, but I am going for speed here...

  * 555.555 incorrectly rounds to 555.55, however 0.555 rounds to 0.56
  * -0.00001, returns -0.00 when all the other zero based tests return 0.00
  * 500.005 should round to 500.01, but the code returns 500.00

## Reasons for some of my choices

I didn't use parameterized tests because, in this case, they are too slow. Running as a single test it kicks off one browser window and throws 8 values in the while loop, clearing each time, it takes 10 seconds. Running as a parametrized test - which means it closes and opens the browser every time - it takes 60 seconds for the same 8 test values. Speed is important, feedback has to be fast, and there is no positive tradeoff for it to be so slow. Speed is also the reason I don't run headless...it's several seconds slower to run all the tests in the file headless. Sometimes things that you think will help can actually slow it down. As the automation lead at Veracode, I found the number of parallel sessions we could use when running in Jenkins was variable, hitting a multi-tiered stack at a busy time could handle fewer sessions than a single tiered stack that was only running my tests, it would show false failures because they were getting blocked at the server end when everyone was trying to run complex automation at the same time (limits of our test environment, not the product).

I find that markers clutter the view - that big line blocks my view of the def. I use them when needed, when tests need to be grouped across files of tests, etc. but I usually wouldn't use them in a single file situation. We started using them a lot more when we were running in Jenkins because it was easier to group tests into suites, and I put the pytest line into the job description so that we could tell at a glance which blocks were failing.

Pytest will run anything that starts with "test_" so I just change the first part of the name to something else, usually xxxtest_, if I am just trying to isolate a test case - it's easier to add them in, move them around, etc. using "find" while I am working, instead of dealing with a decorator. I will use FAILtest_ if it is a bit more permanent, e.g. if I am just waiting for a fix to come in before it gets checked into the master suite and I can find it easily searching for FAIL when the fix comes in. I will use the skip marker when the parent class has a marker, so all tests inherit that marker, and I am not very hopeful that the broken test will ever be fixed, but I am not going to throw away the test - it serves as a reminder that we thought about testing whatever it is. I could comment out the test, but I used epydoc to get a HTML browsable/searchable list of all the tests and it throws all comments in there, so I didn't want "archived" tests in the doc.

Testing the formatting function via the GUI is not a bad idea - that is where the formatting is happening. I created some basic GUI tests (check for text present, etc.) to check the GUI itself, but all the other tests are testing the formatting at the GUI end - using a GUI tool, but not testing the GUI, per se. It is a fully functioning app and meets the requirements: Add associated tests for the functionality and for the user interface. It's not really conducive to performance testing, but then how much performance test data are you going to get throwing Jmeter at a currency format function? It might get some info on the performance of moving that data to a database, but everything I am doing is local to my machine and my database table would be tiny, a single table with a few columns, the limits found would be with my hardware.
There are always other ways to do things, of course...
 * the data that is typed in to the front end could be passed to the back end for formatting and then passed back and displayed
  * if this required a huge number cruncher and needed the power of a back end server, perhaps that would be the way to go, however, for something this small, the security code to sanitize all the data would add layers of code and a lot more testing.
 * the data could be formatted and then passed to a database and the formatting could be tested at the DB end
  * that would be points of failure...what if the function that moved the data changed it in some way?
