
import os
import time, datetime
import logging
from builtins import staticmethod
from traceback import print_stack
#from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import utility.framework.logger_utility as log_utils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class UIHelpers():

    """
    UI Helpers class to contains all ui helper methods.
    """

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def wait_for_sync(seconds=5):
        time.sleep(seconds)

    def action_chains(self, element):
        """
        THis method is used to interact with SignPad Element and enter some random signature
        :param element: Web Element
        :return: Perform some actions on Signature Pad element
        """
        #https://github.com/bonigarcia/webdrivermanager-examples/blob/master/src/test/java/io/github/bonigarcia/wdm/test/CanvasTest.java
        #https://sqa.stackexchange.com/questions/3253/how-to-automate-the-action-on-a-canvas-object-when-the-canvas-element-has-no-na
        #https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html
        #https://stackoverflow.com/questions/42621593/how-to-automate-e-signature-input-using-selenium

        actions = ActionChains(self.driver)
        #actions.click(element).move_to_element_with_offset(element,20,20).click_and_hold(element).move_by_offset(120,120).move_by_offset(-120,120).move_by_offset(-120,-120).move_by_offset(8,8).release(element).perform()

        actions.click(element).move_to_element_with_offset(element,20,20).click_and_hold(element).move_by_offset(32,13).move_by_offset(32,12).move_by_offset(31,11).move_by_offset(32,11).release(element).perform()

        # actions.send_keys_to_element(element, "Test Sign")
        # actions.release().perform()


    def take_screenshots(self, file_name_initials):

        """
        This method takes screen shot for reporting
        :param file_name_initials: it takes the initials for file name
        :return: it returns the destination directory of screenshot
        """

        file_name = file_name_initials + "." + str(round(time.time() * 1000)) + ".png"
        cur_path = os.path.abspath(os.path.dirname(__file__))
        screenshot_directory = os.path.join(cur_path, r"../../screenshots/")

        destination_directory = os.path.join(screenshot_directory, file_name)

        try:
            if not os.path.exists(screenshot_directory):
                os.makedirs(screenshot_directory)
            self.driver.save_screenshot(destination_directory)
            self.log.info("Screenshot saved to directory: " + destination_directory)
        except Exception as ex:
            self.log.error("### Exception occurred:: ", ex)
            print_stack()

        return destination_directory

    def get_title(self):
        return self.driver.title

    def identify_day_session_info(self, time_slot_info):
        """
        Identify the session of the day i.e Morning/Afternoon/Morning
        :param time_slot: time_slot as a string
        :return: session_name as a string
        """
        session_name = None

        time_slot = time_slot_info.split(' ')[0].split(':')[0]

        if 8 <= int(time_slot) < 12:
            session_name = "Morning"
        elif 12 <= int(time_slot) < 4:
            session_name = "Afternoon"
        else:
            if 4 <= int(time_slot) < 10:
                session_name = "Evening"

        return session_name

    def get_locator_by_type(self, locator_type):

        locator_type = locator_type.lower()

        if locator_type == 'id':
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == 'xpath':
            return By.XPATH
        elif locator_type == 'css':
            return By.CSS_SELECTOR
        elif locator_type == 'class':
            return By.CLASS_NAME
        elif locator_type == 'link':
            return By.LINK_TEXT
        elif locator_type == 'partial_link':
            return By.PARTIAL_LINK_TEXT
        elif locator_type == 'tag':
            return By.TAG_NAME
        elif locator_type == 'link':
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locator_type +
                          " not correct/supported")
            # raise Exception("Not supported locator!")

        return False

    def click_element_using_webdriverio(self, locator_xpath):
        """
        click specific element using WebdriverIO click method
        :param locator_xpath: locator_xpath as string
        """
        try:
            # http://appium.io/docs/en/commands/session/execute-driver/
            # https://webdriver.io/docs/api/element/scrollIntoView/

            import textwrap
            script = """
                const el = await driver.$(`{}`);
                await el.click();
            """.format(locator_xpath)

            self.driver.execute_driver(script=textwrap.dedent(script))
            # self.driver.execute_script(script=textwrap.dedent(script))
            self.log.info("Clicking on the specific element")

        except Exception as ex:
            self.log.error("Exception occurred while clicking on the element is::::::::{}".format(ex))
            # self.log.error("Exception occurred while vertically scrolling into the view: ", ex)

    def fetch_textView_text(self, text):
        """
        This function is used for fetching the text from textView element by using find_element_by_android_uiautomator()
        :param text: text of the element
        :return: this function returns nothing
        """
        # https://www.programmersought.com/article/568053149/
        fetched_text = None
        try:
            fetched_text = self.driver.find_element_by_android_uiautomator("new UiSelector().textContains(\"{}\")".format(text)).text
        except Exception as ex:
            self.log.error("Exception occurred while fetching text from textView: ", ex)

        return fetched_text

    def text_to_be_present_in_element(self, locator_type,locator,expected_text,poll_frequency=0.5,timeout = 60):
        """
         An expectation for checking if the given text is present in the element's locator, text

        :param locator_type: it takes locator by type(id/xpath,..) string as parameter
        :param locator: it takes locator element as parameter
        :param timeout: this is the maximum time to wait for particular element
        :param poll_frequency: this is the time in which driver polls the DOM for availability of the element
        :param expected_text : text to be present in the element
        :return: it returns the boolean value according to the element located or not
        """
        element_status = None

        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)

            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for click of element located")
            text_element = WebDriverWait(self.driver,timeout,poll_frequency,
                                    ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException]).until(
                      EC.text_to_be_present_in_element_value((by_type,locator), expected_text))

            self.log.info("Element appeared with locator: " + locator +" locatorType: " + locator_type + "Expected Text: " + expected_text)

            element_status = text_element

        except Exception as ex:
            self.log.info("Element not appeared with locator: " + locator + " locatorType: " + locator_type + "Expected Text: " + expected_text)
            self.log.error("### Exception occurred:: ", ex)

        return element_status

    def get_element(self,locator_type,locator,poll_frequency=0.5,timeout = 30):
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)
            wait = WebDriverWait(self.driver,timeout,poll_frequency,ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException])
            element = wait.until(lambda driver: self.driver.find_element(by_type,locator))
            self.log.info("Element found with locator: " + locator +
                          " and  locatorType: " + locator_type)

        except NoSuchElementException as e:
            self.log.info("Element not found with locator: " + locator + " and  locatorType: " + locator_type)
            self.log.error("Exceptipon occurred is::::::::{}".format(e))
            #raise Exception("Element {0} not found".format(locator))
            element = None
        except Exception as e:
            self.log.info("Element not found with locator: " + locator + " and  locatorType: " + locator_type)
            self.log.error("### Exception occurred:: ", e)
            element = None

        return element

    def get_elements(self,locator_type,locator,poll_frequency=0.5,timeout = 30):
        elements = None

        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)
            wait = WebDriverWait(self.driver,timeout,poll_frequency,ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException])
            elements = wait.until(lambda driver: self.driver.find_elements(by_type,locator))
            self.log.info("Element found with locator: " + locator +
                          " and  locatorType: " + locator_type)
        except Exception as e:
            self.log.info("Element not found with locator: " + locator + " and  locatorType: " + locator_type)
            self.log.error("### Exception occurred:: ", e)

        return elements

    def get_elements_with_status(self,locator_type,locator,poll_frequency=0.5,timeout = 30):
        elements = None

        element_lists = None
        status = True

        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)
            wait = WebDriverWait(self.driver,timeout,poll_frequency,ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException])
            elements = wait.until(lambda driver: self.driver.find_elements(by_type,locator))
            self.log.info("Element found with locator: " + locator +
                          " and  locatorType: " + locator_type)
            element_lists = elements
            status = True
        except Exception as e:
            self.log.info("Element not found with locator: " + locator + " and  locatorType: " + locator_type)
            self.log.error("### Exception occurred:: ", e)
            element_lists = 0
            status = False

        return element_lists,status

    def get_visibility_all_elements_located(self, locator_type,locator,poll_frequency=0.5,timeout = 30):
        elements = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)

            elements = WebDriverWait(self.driver,timeout,poll_frequency,ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException]).until(
                EC.visibility_of_all_elements_located((by_type,locator)))
        except:
            self.log.info("Elements not found with locator: " + locator + " and  locatorType: " + locator_type)
            raise Exception("Element {0} not found".format(locator))

        return elements

    def get_cuurent_url(self):
        return self.driver.current_url

    def get_element_text(self,locator_type,locator):
        return self.get_element(locator_type,locator).text

    def page_back_navigation(self):
        self.driver.back()

    def wait_for_element_visible_located(self,locator_type,locator,poll_frequency=0.5,timeout = 30):
        """
        An expectation for checking that an element is present on the DOM of a page and visible. Visibility means that the element is not only displayed
        but also has a height and width that is greater than 0.

        :param locator_type: it takes locator by type(id/xpath,..) string as parameter
        :param locator: it takes locator element as parameter
        :param timeout: this is the maximum time to wait for particular element
        :param poll_frequency: this is the time in which driver polls the DOM for availability of the element
        :return: it returns the boolean value according to the element located or not
        """
        element_visible_returned = None

        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)

            self.log.info("Waiting for maximum :: " + str(timeout) +" :: seconds for visibility of element located")

            element = WebDriverWait(self.driver,timeout,poll_frequency,
                          ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException]).until(
                EC.visibility_of_element_located((by_type,locator)))
            self.log.info("Element appeared with locator: " + locator +" locatorType: " + locator_type)

            element_visible_returned = element

        except Exception as e:
            self.log.info("Element not appeared with locator: " + locator +" locatorType: " + locator_type)
            self.log.error("### Exception occurred:: ", e)
            print_stack()

        return element_visible_returned

    def wait_for_elements_visible_located(self,locator_type,locator,poll_frequency=0.5,timeout = 30):
        """
        An expectation for checking that an element is present on the DOM of a page and visible. Visibility means that the element is not only displayed
        but also has a height and width that is greater than 0.

        :param locator_type: it takes locator by type(id/xpath,..) string as parameter
        :param locator: it takes locator element as parameter
        :param timeout: this is the maximum time to wait for particular element
        :param poll_frequency: this is the time in which driver polls the DOM for availability of the element
        :return: it returns the boolean value according to the element located or not
        """
        element_visible_returned = None

        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)

            self.log.info("Waiting for maximum :: " + str(timeout) +" :: seconds for visibility of element located")

            element = WebDriverWait(self.driver,timeout,poll_frequency,
                          ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException]).until(
                EC.visibility_of_all_elements_located((by_type,locator)))
            self.log.info("Element appeared with locator: " + locator +" locatorType: " + locator_type)

            element_visible_returned = element

        except Exception as e:
            self.log.info("Element not appeared with locator: " + locator +" locatorType: " + locator_type)
            self.log.error("### Exception occurred:: ", e)
            print_stack()

        return element_visible_returned

    def wait_for_element_to_be_clickable(self,locator_type,locator,poll_frequency=0.5,timeout = 30):
        """
         An Expectation for checking an element is visible and enabled such that you can click it.

        :param locator_type: it takes locator by type(id/xpath,..) string as parameter
        :param locator: it takes locator element as parameter
        :param timeout: this is the maximum time to wait for particular element
        :param poll_frequency: this is the time in which driver polls the DOM for availability of the element
        :return: it returns the boolean value according to the element located or not
        """
        element_to_be_clickable = None

        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)

            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for click of element located")
            element = WebDriverWait(self.driver,timeout,poll_frequency,
                                    ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException]).until(
                      EC.element_to_be_clickable((by_type,locator)))

            self.log.info("Element appeared with locator: " + locator +" locatorType: " + locator_type)

            element_to_be_clickable = element

        except Exception as e:
            self.log.info("Element not appeared with locator: " + locator + " locatorType: " + locator_type)
            self.log.error("### Exception occurred:: ", e)
            print_stack()

        return element_to_be_clickable

    def wait_for_element_to_be_present(self,locator_type,locator,poll_frequency=0.5,timeout = 30):
        """
        A StaleElementReferenceException is thrown when the element you were interacting is destroyed and then recreated.
        Most complex web pages these days will move things about on the fly as the
        user interacts with it and this requires elements in the DOM to be destroyed and recreated.

        :param locator_type: it takes locator by type(id/xpath,..) string as parameter
        :param locator: it takes locator element as parameter
        :param timeout: this is the maximum time to wait for particular element
        :param poll_frequency: this is the time in which driver polls the DOM for availability of the element
        :return: it returns the boolean value according to the element located or not
        """
        element_to_be_returned = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_locator_by_type(locator_type)

            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for presence of the element")
            element = WebDriverWait(self.driver,timeout,poll_frequency,
                                    ignored_exceptions=[StaleElementReferenceException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException]).until(
                EC.presence_of_element_located((by_type,locator)))

            self.log.info("Element appeared with locator: " + locator +" locatorType: " + locator_type)

            element_to_be_returned = element

        except Exception as e:
            self.log.info("Element not appeared with locator: " + locator + " locatorType: " + locator_type)
            self.log.error("### Exception occurred:: ", e)
            print_stack()

        return element_to_be_returned



    '''
    def wait_for_element_to_be_displayed(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This function is used for explicit waits till element displayed
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element located or not
        """

        try:
            WebDriverWait(self.driver, max_time_out, ignored_exceptions=[StaleElementReferenceException]).until(
                EC.visibility_of_element_located((self.get_locator_type(locator_type), locator_properties))
            )
            return True
        except Exception as e:
            self.log.error("Exception occurred while waiting for element to be visible.")
            self.log.error("### Exception occurred:: ", e)
            return False

    def wait_for_element_to_be_invisible(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This function is used for explicit waits till element displayed
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element located or not
        """

        try:
            WebDriverWait(self.driver, max_time_out, ignored_exceptions=[StaleElementReferenceException]).until(
                EC.invisibility_of_element_located((self.get_locator_type(locator_type), locator_properties))
            )
            return True
        except:
            return False

    def is_element_present(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to return the boolean value for element present
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element present or not
        """

        flag = False
        try:
            if self.wait_for_element_to_be_present(locator_properties, locator_type, max_time_out):
                self.log.info(
                    "Element present with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
                flag = True
            else:
                self.log.error(
                    "Element not present with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
        except Exception as e:
            self.log.error("Exception occurred during element identification.")

        return flag

    def verify_element_not_present(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to return the boolean value for element present
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element present or not
        """

        flag = False
        try:
            if self.wait_for_element_to_be_invisible(locator_properties, locator_type, max_time_out):
                self.log.info(
                    "Element invisible with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
                flag = True
            else:
                self.log.error(
                    "Element is visible with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
        except Exception as e:
            self.log.error("Exception occurred during element to be invisible.")

        return flag

    def is_element_displayed(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to return the boolean value for element displayed
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element displayed or not
        """

        try:
            if self.wait_for_element_to_be_displayed(locator_properties, locator_type, max_time_out):
                self.log.info(
                    "Element found with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
                return True
            else:
                self.log.error(
                    "Element not found with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
                return False
        except Exception as e:
            self.log.error("Exception occurred during element identification.")
            return False

    def is_element_clickable(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to return the boolean value for element clickable
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element clickable or not
        """

        try:
            if self.wait_for_element_to_be_clickable(locator_properties, locator_type, max_time_out):
                self.log.info(
                    "Element is clickable with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
                return True
            else:
                self.log.error(
                    "Element is not clickable with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
                return False
        except Exception as e:
            self.log.error("Exception occurred during element identification.")
            return False

    def is_element_checked(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to return the boolean value for element checked/ selected
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element present or not
        """

        flag = False
        try:
            if self.is_element_present(locator_properties, locator_type, max_time_out):
                element = self.get_element(locator_properties, locator_type, max_time_out)
                if element.is_selected():
                    self.log.info(
                        "Element is selected/ checked with locator_properties: " +
                        locator_properties + " and locator_type: " + locator_type)
                    flag = True
                else:
                    self.log.error(
                        "Element is not selected/ checked with locator_properties: " +
                        locator_properties + " and locator_type: " + locator_type)
        except Exception as e:
            flag = False

        return flag

    def verify_elements_located(self, locator_dict, max_timeout=10):

        """
        This method is used to return the boolean value according to element presents on page
        :param locator_dict: this parameter takes the list of locator value and it's type
        :param max_timeout: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to element presents on page
        """

        flag = False
        result = []
        try:

            for locator_prop in locator_dict.keys():
                prop_type = locator_dict[locator_prop]
                if self.wait_for_element_to_be_present(locator_prop, prop_type, max_timeout):
                    self.log.info(
                        "Element found with locator_properties: " + locator_prop +
                        " and locator_type: " + locator_dict[locator_prop])
                    flag = True
                else:
                    self.log.error(
                        "Element not found with locator_properties: " + locator_prop +
                        " and locator_type: " + locator_dict[locator_prop])
                    flag = False
                result.append(flag)

        except Exception as ex:
            self.log.error("Exception occurred during element identification: ", ex)

        if False in result:
            return False
        else:
            return True


    def get_attribute_value_from_element(self, attribute_name, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to get the element's attribute value according to the locator type and property
        :param attribute_name: it takes the attribute name as parameter
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the element attribute value
        """

        attribute_value = ""
        try:
            element = self.get_element(locator_properties, locator_type, max_time_out)
            attribute_value = element.get_attribute(attribute_name)
            if attribute_value is not None:
                self.log.info(attribute_name.upper() + " value is: " + attribute_value)
            else:
                self.log.error(attribute_name.upper() + " value is empty.")
        except:
            self.log.error("Exception occurred during attribute value retrieval.")
        return attribute_value

    def mouse_click_action(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to perform mouse click action according to the locator type and property
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        """

        try:
            if self.is_element_clickable(locator_properties, locator_type, max_time_out):
                element = self.get_element(locator_properties, locator_type, max_time_out)
                element.click()
                self.log.info(
                    "Clicked on the element with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
            else:
                self.log.error("Unable to click on the element with locator_properties: "
                               + locator_properties + " and locator_type: " + locator_type)
        except:
            self.log.error("Exception occurred during mouse click action.")

    def mouse_click_action_on_element_present(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to perform mouse click action according to the locator type and property
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        """

        try:
            if self.is_element_present(locator_properties, locator_type, max_time_out):
                element = self.get_element(locator_properties, locator_type, max_time_out)
                element.click()
                self.log.info(
                    "Clicked on the element with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
            else:
                self.log.error("Unable to click on the element with locator_properties: "
                               + locator_properties + " and locator_type: " + locator_type)
        except:
            self.log.error("Exception occurred during mouse click action.")

    def move_to_element_and_click(self, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used when element is not receiving the direct click
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        """

        try:
            if self.is_element_clickable(locator_properties, locator_type, max_time_out):
                element = self.get_element(locator_properties, locator_type, max_time_out)
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                self.log.info(
                    "Clicked on the element with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
            else:
                self.log.error("Unable to click on the element with locator_properties: "
                               + locator_properties + " and locator_type: " + locator_type)
        except:
            self.log.error("Exception occurred during mouse click action.")

    def enter_text_action(self, text_value, locator_properties, locator_type="xpath", max_time_out=10):

        """
        This method is used to enter the value in text input field
        :param text_value: it takes input string as parameter
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        :return:
        """

        element = None

        try:
            element = self.get_element(locator_properties, locator_type, max_time_out)
            element.clear()
            element.send_keys(text_value)
            self.log.info(
                "Sent data to the element with locator_properties: " + locator_properties + " and locator_type: " + locator_type)
        except:
            self.log.error("Unable to send data on the element with locator_properties: "
                           + locator_properties + " and locator_type: " + locator_type)

        return element

    def verify_text_contains(self, actual_text, expected_text):

        """
        This method verifies that actual text in the expected string
        :param actual_text: it takes actual keyword/ substring
        :param expected_text: it takes the string value to search actual keyword in it
        :return: it return boolean value according to verification
        """

        self.log.info("Actual Text From Application Web UI --> :: " + actual_text)
        self.log.info("Expected Text From Application Web UI --> :: " + expected_text)

        if expected_text.lower() in actual_text.lower():
            self.log.info("### VERIFICATION TEXT CONTAINS !!!")
            return True
        else:
            self.log.info("### VERIFICATION TEXT DOES NOT CONTAINS !!!")
            return False

    def verify_text_match(self, actual_text, expected_text):

        """
        This method verifies the exact match of actual text and expected text
        :param actual_text: it takes actual string value
        :param expected_text: it takes the expected string value to match with
        :return: it return boolean value according to verification
        """

        self.log.info("Actual Text From Application Web UI --> :: " + actual_text)
        self.log.info("Expected Text From Application Web UI --> :: " + expected_text)

        if expected_text.lower() == actual_text.lower():
            self.log.info("### VERIFICATION TEXT MATCHED !!!")
            return True
        else:
            self.log.error("### VERIFICATION TEXT DOES NOT MATCHED !!!")
            return False

    def horizontal_scroll(self, scroll_view, class_name, text):
        """
        This function is used for horizontal scroll
        :param scroll_view: class name for scroll view
        :param class_name: class name for text view
        :param text: text of the element
        :return: this function returns nothing
        """
        try:
            self.driver.find_element_by_android_uiautomator(
                "new UiScrollable(new UiSelector().scrollable(true)" +
                ".className(\"" + scroll_view + "\")).setAsHorizontalList().scrollIntoView(new UiSelector()" +
                ".className(\"" + class_name + "\").text(\"" + text + "\"))")
            self.log.info("Horizontally scrolling into the view.")

        except Exception as ex:
            self.log.error("Exception occurred while horizontally scrolling into the view: ", ex)
    '''