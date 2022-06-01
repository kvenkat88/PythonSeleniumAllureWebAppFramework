import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
from selenium import webdriver
import argparse
from utility.framework.data_reader_utility import DataReader
import test_data.global_variables as gv


#https://stackoverflow.com/questions/29986185/python-argparse-dict-arg
#https://github.com/Parsely/streamparse/blob/master/streamparse/cli/common.py
class StoreDictKeyPair(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreDictKeyPair, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        time_dict = {}
        print("values: {}".format(values))
        if values is not None:
            for kv in values:
                k, v = kv.split("=")
                time_dict[k] = v
        else:
            # parser.error("{0} ".format(option_string))
            # pytest.fail("{0} ".format(option_string))
            raise ValueError("{0} ".format(option_string))

        setattr(namespace, self.dest, time_dict)

def pytest_addoption(parser):
    """ Implement pytest hook that defines custom command line options to be passed to pytest.
    Args:
        parser (parser config object): Holds the pytest command line options information

    Attributes:
        --platform option (str) : Retrieve the browser for test execution
        --host option (str) : Retrieve the host url for different brands like HPS,Spark, etc
        --role option (str) : Retrieve the user role
        --region option (str) : Provide the region specific data
        --patient option (str) : Provide the patient specific data

    Returns:
            parser object which can be accessible via request fixture available to pytest
    """

    parser.addoption("--platform", dest="platform", action="store", required=True, default="chrome",help="Valid options for browser are headless_chrome or ie or edge or firefox or chrome")

    parser.addoption("--role", dest="role", action="store", required=True, default='physician',help="User role info for login and interact with the specific role based users")

    parser.addoption("--region", action=StoreDictKeyPair, required=True, nargs='+', metavar="KEY=VAL",help="Use this option to choose timeslot for appointment booking. For random timeslot, give --timeslot action=default to use default from the nextavailable screen available,give --timeslot action=random and for custom timeslot, give --timeslot action=custom day=Today/Tomorroe/Friday,"
                                                                                                              "session=Morning/Evening/Afternoon, for automation suite predefined test data select, --timeslot auto_run and then day,time and session would be automatically selected")

    parser.addoption("--patient", dest="patient", action="store", required=False, default='very_high_risk',help="Patient info for test execution specific to scenarios")

def pytest_collection_modifyitems(config, items):
    """ PytestHook to verify whether commandline arguments are available to the pytest runtime for later usage

        Args:
            config (_pytest.config.Config) object: Holds command line arguments passed and other config info
            items (items object): Holds the pytest mark and parameterize objects

        Attributes:
        --platform option (str) : Retrieve the browser for test execution
        --host option (str) : Retrieve the host url for different brands like HPS,Spark, etc
        --role option (str) : Retrieve the user role
        --region option (str) : Provide the region specific data
        --patient option (str) : Provide the patient specific data

        Returns:
            Fails the pytest session if requested commandline arguments is not available else return nothing
    """

    if config.getoption("--platform") or config.getoption("--user") or config.getoption('--region'):
        return

    if config.getoption("--patient"):
        return

    pytest.fail("Need to provide either --browser or --host or --user or --region or --patient for test execution..Please Check!!!")

@pytest.fixture(scope="session")
def browser_fetched(request):
    "pytest fixture for browser"
    return request.config.getoption("--platform")

@pytest.fixture(scope="session", name='get_config_params')
def get_config_params(request):
    config_param = {}
    config_param["browser"] = request.config.getoption("--platform")
    config_param["role"] = request.config.getoption("--role")
    config_param["region"] = request.config.getoption("--region")
    config_param["patient"] = request.config.getoption("--patient")
    return config_param

# @pytest.fixture(name='timezone_cmd_option',scope="session")
# def retrieve_timezone_from_command_line_fixture(request):
#     timezone_fetched = None
#
#     if (request.config.getoption("--time") is not None):
#         timezone_fetched = request.config.getoption("--time")
#
#     def finalizer():
#         pass
#     request.addfinalizer(finalizer)
#
#     return timezone_fetched

@pytest.fixture(name='patient_info_fetch_fixture',scope="session")
def retrieve_patient_info(request):
    patient_info_fecthed = None

    if (request.config.getoption("--patient") is not None):
        timezone_fetched = request.config.getoption("--patient")

    def finalizer():
        pass
    request.addfinalizer(finalizer)

    return patient_info_fecthed

@pytest.fixture(name='retreive_host_region_info',scope="session")
def retrieve_host_region_info_from_command_line_fixture(request, get_config_params):
    host_info_fetched = None

    try:
        if (request.config.getoption("--region") is not None):
            # Retrieve the host url based upon country, state and provider
            if 'country' in get_config_params['region'] and 'state' in get_config_params['region'] and 'provider' in get_config_params['region'] and 'county' not in get_config_params['region']:
                host_info_fetched = DataReader().fetch_info_from_region_specific_data_json(region_country_name=get_config_params['region']['country'], state_name=get_config_params['region']['state'], provider_short_name=get_config_params['region']['provider'])['launch_url']

            # Retrieve the host info based upon country, state_name and returns a list
            if 'country' in get_config_params['region'] and 'state' in get_config_params['region'] and 'provider' not in get_config_params['region'] and 'county' not in get_config_params['region']:
                host_info_fetched = DataReader().fetch_all_launch_urls_from_json_for_specific_state(region_country_name=get_config_params['region']['country'], state_name=get_config_params['region']['state'])

            # Retrieve the host info based upon country and returns a list
            if 'country' in get_config_params['region'] and 'state' not in get_config_params['region'] and 'county' not in get_config_params['region'] and 'provider' not in get_config_params['region'] :
                host_info_fetched = DataReader().fetch_all_launch_urls_from_json_for_country(region_country_name=get_config_params['region']['country'])

            # Retrieve the host info based upon country, state_name, county and returns a list
            if 'country' in get_config_params['region'] and 'state' in get_config_params['region'] and 'provider' not in get_config_params['region'] and 'county' in get_config_params['region']:
                host_info_fetched = DataReader().fetch_info_based_on_county_from_region_json(region_country_name=get_config_params['region']['country'], state_name=get_config_params['region']['state'], county_name=get_config_params['region']['county'])

            gv.base_url_fetched = host_info_fetched

    except Exception as e:
        pass

    def finalizer():
        pass

    request.addfinalizer(finalizer)

    return host_info_fetched

#https://stackoverflow.com/questions/12411431/how-to-skip-the-rest-of-tests-in-the-class-if-one-has-failed
# https://github.com/pytest-dev/pytest/issues/2417 ## Access the commandline line argument from conftest.py file to another test files
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "incremental: mark test to run incremental test i.e tests stop after certain no of failures"
    )

    config.addinivalue_line(
        "markers", "cleanup: mark test to cancel the existing appointments available"
    )

    config.addinivalue_line(
        "markers", "login: mark test to run login related tests only"
    )

    gv.region_country_name = config.getoption("--region")
    gv.patient_cat = config.getoption("--patient")

def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item

def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            #pytest.xfail("previous test failed ({})".format(previousfailed.name))
            pytest.mark.xfail("previous test failed ({})".format(previousfailed.name),run=True) #Even on failure tests will run

# @pytest.fixture
# def dummy_fixture():
#     def _loader(test_report_type, testcase, id, severity, story):
#         if test_report_type == "allure":
#             print("Called dummy fixture for processing")
#             from allure_commons._allure import testcase,feature,severity,story
#             testcase(testcase)
#             feature(id)
#             severity(severity)
#             story(story)
#     yield _loader

# BASE_URL = "http://localhost:10000"
BASE_URL = os.getenv('BASE_URL', "http://localhost:10000")
DRIVER = os.getenv('DRIVER', 'chrome')
SELENIUM = os.getenv('SELENIUM', 'http://localhost:4444/wd/hub')  #Remote Webdriver host URL to be run in Gitlab CI/CD

def get_chrome_driver():
    """
    This method is used to utilize the execution in local environment
    :return:
    """
    cur_path = os.path.abspath(os.path.dirname(__file__))
    driver_file_path = os.path.join(cur_path,r"../drivers/chromedriver.exe")

    desired_capabilities = webdriver.DesiredCapabilities.CHROME
    desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-instant-extended-api")

    desired_capabilities.update(chrome_options.to_capabilities())

    browser_to = webdriver.Chrome(
        executable_path=driver_file_path,
        desired_capabilities=desired_capabilities)

    # Desktop size
    #browser.set_window_position(0, 0)
    #browser.set_window_size(1366, 768)
    browser_to.delete_all_cookies()
    browser_to.maximize_window()
    return browser_to
    # yield browser_to

def get_firefox_driver():
    pass

def sel_grid_execution(browser_type):
    browser_to = None
    if browser_type == "chrome":
        try:
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
            desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-instant-extended-api")
            desired_capabilities.update(chrome_options.to_capabilities())

            # browser_to = webdriver.Remote(
            #     command_executor=SELENIUM,
            #     desired_capabilities={
            #         "browserName": "chrome",
            #         "browserVersion": "latest",
            #         "platform": "WIN10",
            #         "platformName": "windows",
            #         "javascriptEnabled": True
            #     })

            browser_to = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                desired_capabilities=desired_capabilities)

            # Desktop size  #this option is not utilized for taking screenshots
            # browser.set_window_position(0, 0)
            # browser.set_window_size(1366, 768)
            browser_to.delete_all_cookies()
            browser_to.maximize_window()
        except (Exception) as e:
            print("Exception Occurred :: {}".format(e))

    if browser_type == "edge":
        try:
            from selenium.webdriver.edge.options import Options

            desired_capabilities = webdriver.DesiredCapabilities.EDGE
            desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}

            edge_options = Options()
            desired_capabilities.update(edge_options.to_capabilities())

            browser_to = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                desired_capabilities=desired_capabilities)

            # Desktop size  #this option is not utilized for taking screenshots
            # browser.set_window_position(0, 0)
            # browser.set_window_size(1366, 768)
            browser_to.delete_all_cookies()
            browser_to.maximize_window()
        except (Exception) as e:
            print("Exception Occurred :: {}".format(e))

    return browser_to

def get_headless_chrome():
    desired_capabilities = webdriver.DesiredCapabilities.CHROME
    desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--user-data-dir=/tmp/browserdata/chrome")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")  #only for windows machines
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-instant-extended-api")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--window-size=1280,720')

    desired_capabilities.update(chrome_options.to_capabilities())

    print(SELENIUM)

    browser_to = webdriver.Remote(
        command_executor=SELENIUM,
        desired_capabilities=desired_capabilities)

    # Desktop size  #this option is not utilized for taking screenshots
    # browser.set_window_position(0, 0)
    # browser.set_window_size(1366, 768)
    browser_to.delete_all_cookies()
    browser_to.maximize_window()
    return browser_to
    # yield browser_to

DRIVERS = {
    'chrome': get_chrome_driver,
    'firefox': get_firefox_driver,
    'headless_chrome': get_headless_chrome
    #'sel_grid': sel_grid_execution
}

# def get_browser_driver():
#     return DRIVERS.get(DRIVER)

def get_browser_driver():
    return DRIVERS[DRIVER]()

@pytest.fixture(scope="session")
def test_setup(request, browser_fetched,retreive_host_region_info):
    # def driver_setup_close(request):
    print(browser_fetched)
    if browser_fetched == "headless_chrome":
        get_browser_driver_instance = get_browser_driver()
        get_browser_driver_instance.get(BASE_URL)

        session = request.node
        for item in session.items:
            cls = item.getparent(pytest.Class)
            setattr(cls.obj, "driver", get_browser_driver_instance)
        yield
        get_browser_driver_instance.quit()

    elif browser_fetched in ("chrome", "firefox"):
        get_browser_driver_instance = get_browser_driver()
        BASE_URL_FETCHED = retreive_host_region_info
        get_browser_driver_instance.get(BASE_URL_FETCHED)

        session = request.node
        for item in session.items:
            cls = item.getparent(pytest.Class)
            setattr(cls.obj, "driver", get_browser_driver_instance)
        yield
        get_browser_driver_instance.quit()
    else:
        raise Exception("Invalid browser option provided for execution")

# @pytest.fixture(scope="session",params=["chrome","edge"])
# def test_setup_grid(request, browser_fetched, retreive_host_region_info):
#     get_browser_driver_instance = None
#     BASE_URL_FETCHED = retreive_host_region_info
#     if browser_fetched == "sel_grid" and request.param == "chrome":
#         get_browser_driver_instance = sel_grid_execution(browser_type=request.param)
#         get_browser_driver_instance.get(BASE_URL_FETCHED)
#
#     if browser_fetched == "sel_grid" and request.param == "edge":
#         os.environ['browser_running'] = request.param
#         get_browser_driver_instance = sel_grid_execution(browser_type=request.param)
#         get_browser_driver_instance.get(BASE_URL_FETCHED)
#
#     session = request.node
#     for item in session.items:
#         cls = item.getparent(pytest.Class)
#         setattr(cls.obj, "driver", get_browser_driver_instance)
#     yield
#     get_browser_driver_instance.quit()

