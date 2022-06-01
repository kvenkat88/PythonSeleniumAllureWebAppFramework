Framework to automate the XXXX Hospital Web App using Appium and Python with PyTest as Testing Framework. It uses Allure Reporting tool for Report Generation.

#### Command to run single browser invocation(say chrome/firefox/edge)
py.cleanup -p && py.test -v --cache-clear tests/registered --platform chrome --role physician --patient very_high_risk --region country=US state=california provider=hps --alluredir reports & allure generate reports -o final_report --clean

#### Command to run Selenium Grid
py.cleanup -p && pytest -v --cache-clear tests/registered --platform sel_grid --role physician --patient very_high_risk --region country=US state=california provider=hps -n auto --alluredir reports & allure generate reports -o final_report --clean

#### Browser Drivers and configs
1. drivers/* directory will hold the necessary browser version drivers for execution.
2. configs/* directory holds the *.json files the Selenium Grid Setup.

#### Locator Strategy or Locators Fetched Categorized
1. locators/common directory have locators strategy fetched for both Guest and Registered user common screen flows.
2. locators/registered/<some_role> directory have locators strategy fetched for user specific role or other categories as per our requirements.
3. All of the locator strategy available in selenium will be supported in this framework.We can add additional as well.

#### Page Object Model(POM)
1. POM is created for each and every page of the Application Under Test(AUT).
2. pages/common directory have POM strategy methods fetched for common screen flows.
3. pages/registered/* directory have POM strategy methods fetched for specific user roles or feature pages.

#### Logs, Screenshots
1. Debug logs are available in logs/ directory.
2. Failure scenario screenshots are available in screenshots/ directory.

#### Framework and Support Utility Concepts and Methods
1. framework/ directory have utility methods for config file or property file reading, json or yaml file reading,
   reporting related utilities and other useful utility methods.
2. support/ directory have utility methods for text validations, appium driver instantiation, generalized appium and selenium methods to
   interact with Web Elements available.
3. support/ui_helpers.py python file have wrapper methods for different selenium utility functions(like fin_element(), find_elements(), etc).
4. support/base_helpers.py python file have wrapper methods for date utilties, date validations, regex validations, etc.
5. framework/logger_utility.py provider logging mechanisms for thr framework.
6. framework/execution_status_utility.py provides the mechanism for framework alure report regeneration(it provides execution status).
7. framework/data_reader_utility.py provides the mechanism to load different data releated files, parsing and retrieving records.

#### Pytest Framework Brain(conftest.py)
1. Pytest framework needs conftest.py for proper test collection and identification, report generation and other activities.
2. Always place the conftest.py file in tests/* directory(place in the main directory inside of tests).
3. conftest.py file holds the mechanism to invoke selenium grid, browser invocation, commandline utility helpers to fetch the commandline arguments,
   pytest fixtures(reuse functions as per different execution scopes), customize test generation reports and others.

#### Test Data for Framework
1. test_data/user_info.json file have different user related roles login and profile related info.
2. test_data/general_info.json file have general information specific to clinic available/displayed to the patient.
3. test_data/global_variables.py file have global variables and it wld be referenced across the framework during runtime.
4. test_data/brands_test_data/*.json - Have individual clinic information for booking appointment and validating the appointment flows.
5. test_data/insurance_card_images - Have insurance card images.
6. test_data/patient_data_source.xlsx - Holds the patient records available in ED/Hospitalization-Patient Roster Page. This data is source for the test validation at runtime.
7. test_data/<country_name>_patient.json will holds the specific patient under test when we validate for ED/Hospitalization-Patient View Page or other scenarios.
8. test_data/region_specific_data/<country_name>_region.json - As a service/solution provider, we might support different geography customers and to accomadate that we will specific that. During runtime, based upon commandline
   parameters this file would be referenced to fetch the base url to launch the page and test.
9. test_data/region_specific_data/dh_deployed_region.json - Should be updated based upon deployment and will gives detailed information about where the deployment is done.
10. test_data/url_redirect_route.py - to fetch or create the url routes across different pages.

#### Report Generation
1. This framework uses the interactive allure commandline plugin for generating the HTML reports.
2. Refer this URL - https://docs.qameta.io/allure/#_get_started for configuration.
3. This framework would create the test results in the form of **.txt and .json** and this is available in reports/* directory.
4. This intermediate files would be generated as part of pytest command invoked.
5. View the html reports using the command - allure open final_report

#### Necessary Library File Installation
1. This framework is developed with Python, Pytest and Allure Framework.
2. Refer requirement.text for more information.
3. Install in a single go - **pip install -r requirement.text**

#### Notes
1. Inside the pytest anotated classes, tests created are sorted alphabetically while running most of the times.

Boilerplate:
============
https://github.com/karimelkomy/Python-Test-Automation-Framework

https://github.com/Abhilash04/AppiumPythonHybridFramework
https://github.com/ikostan/TestAutomationFrameworkUsingAppiumWithPython/tree/master/tests

https://github.com/WasiqB/coteafs-appium/blob/master/src/test/resources/test-config.yaml
https://qxf2.com/blog/appium-mobile-automation/
https://dzone.com/articles/appium-tutorial-for-complete-beginners
https://www.browserstack.com/app-automate/appium-python
https://developer.nevercode.io/docs/appium-tests-written-in-python
https://www.appcoda.com/automated-ui-testing-appium/
https://github.com/topics/appium-framework

http://toolsqa.com/mobile-automation/appium/appium-tutorial/
http://toolsqa.com/mobile-automation/appium/set-up-android-environment-path/
http://blogs.quovantis.com/appium-basics-part-1-pre-requisites-and-setting-up-your-appium-environment-for-windows/
https://scrolltest.com/2016/02/21/appium-introduction/

https://riptutorial.com/selenium-webdriver/example/28140/scrolling-using-python
https://www.codegrepper.com/code-examples/python/how+to+scroll+down+web+element+in+selenium+python

https://www.browserstack.com/guide/verify-tooltip-in-selenium
https://www.toolsqa.com/selenium-webdriver/tooltip-in-selenium/

### Selenium Grid

https://www.softwaretestinghelp.com/selenium-grid-selenium-tutorial-29/

https://www.guru99.com/introduction-to-selenium-grid.html#3

https://www.selenium.dev/documentation/grid/

https://www.swtestacademy.com/selenium-4-grid-standalone-tutorial/

https://dzone.com/articles/selenium-grid-4-tutorial-for-distributed-testing

https://www.egrovesys.com/blog/implementing-selenium-grid-in-python/

https://gist.github.com/dzitkowskik/0fc641cf59af0dc3de62

https://testautomationu.applitools.com/ai-for-element-selection-erasing-the-pain-of-fragile-test-scripts/chapter1.html

https://tarunlalwani.com/post/reusing-existing-browser-session-selenium-grid-python/

https://www.testim.io/blog/selenium-grid-simple-introduction/

https://www.lambdatest.com/blog/test-automation-using-pytest-and-selenium-webdriver/

https://www.lambdatest.com/blog/selenium-grid-setup-tutorial-for-cross-browser-testing/

https://stackoverflow.com/questions/70121909/sessionnotcreatedexception-could-not-start-a-new-session-possible-causes-are-i

https://www.programcreek.com/python/example/100028/selenium.webdriver.Edge

https://stackoverflow.com/questions/65171183/how-to-run-microsoft-edge-headless-with-selenium-python

https://stackoverflow.com/questions/69441767/error-using-selenium-chrome-webdriver-with-python

https://www.swtestacademy.com/cross-browser-testing-in-selenium/

https://www.youtube.com/watch?v=QcMCfdE_AmE #Parallel exec

https://github.com/Divya1151/selenium-grid-appium-python

https://github.com/Specialize-Automation/Selenium_GRID_Configuration

https://raphael.codes/blog/customizing-your-pytest-test-suite-part-2/

https://www.lambdatest.com/automation-testing-advisor/python/pytest-pytest_sessionfinish

https://github.com/LambdaTest/pyunit-selenium-sample/blob/main/parallel_test.py

https://github.com/allure-framework/allure-python/issues/96

https://www.lambdatest.com/blog/selenium-grid-setup-tutorial/

https://www.lambdatest.com/blog/pytest-tutorial-parallel-testing-with-selenium-grid/?utm_source=Dzone&utm_medium=blog&utm_campaign=HS-280720-1&utm_term=himanshu

https://www.lambdatest.com/blog/selenium-grid-setup-tutorial-for-cross-browser-testing/?utm_source=Dzone&utm_medium=blog&utm_campaign=HS-280720-1&utm_term=himanshu

https://github.com/brianxlong/selenium-grid-setup

#### DOcker Selenium/Appium
https://github.com/budtmo/docker-android

https://github.com/startrug/selenium-python-framework

http://elementalselenium.com/tips/70-grid-extras


#### Grid Commands
   1. **Start the Grid hub** = java -jar -D selenium-server-4.1.3.jar hub
   2. **Grid with our hub config json** = java -jar -D selenium-server-4.1.3.jar hub --config ../configs/gridHub.json
   3. java -jar -D selenium-server-4.1.3.jar node --config ../configs/gridNode.json
   4. **Standalone server** - java -jar -D selenium-server-4.1.3.jar standalone


### Python Decorator references

https://www.geeksforgeeks.org/decorators-in-python/

https://www.programiz.com/python-programming/decorator

https://www.freecodecamp.org/news/python-decorators-explained-with-examples/

https://www.geeksforgeeks.org/class-as-decorator-in-python/

https://www.codementor.io/@sheena/advanced-use-python-decorators-class-function-du107nxsv

https://www.artima.com/weblogs/viewpost.jsp?thread=240845#decorator-functions-with-decorator-arguments

https://www.geeksforgeeks.org/decorators-with-parameters-in-python/

https://medium.com/@vadimpushtaev/decorator-inside-python-class-1e74d23107f6

https://www.geeksforgeeks.org/creating-decorator-inside-a-class-in-python/

https://stackoverflow.com/questions/11731136/class-method-decorator-with-self-arguments

https://realpython.com/primer-on-python-decorators/

https://www.scaler.com/topics/python/python-decorators/

https://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html

#### If text is not gettable - https://stackoverflow.com/questions/16705165/unable-to-extract-the-text-using-gettext-in-selenium-webdriver-and-also-unable-t
    - .get_attribute('innerHTML')