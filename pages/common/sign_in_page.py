import logging
from utility.support.ui_helpers import UIHelpers
import utility.framework.logger_utility as log_utils
from locators.common.landing_sign_in_page_locator import LandingSignInPageLocatorsStaticText, LandingSignInPageLocators

class LandingSignInPage(UIHelpers):
    """This class defines the method and element identifications for Sign In Screen."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, driver):
        self.driver = driver
        #self.ui_helpers = UIHelpers(driver)
        self.locator = LandingSignInPageLocators()
        self.locator_page_static_text = LandingSignInPageLocatorsStaticText()
        super(LandingSignInPage, self).__init__(driver)

    def verify_page_title(self):
        """
        Verify Sign In Page Title
        :return: True | False
        """
        result = True

        element_text = self.get_element(*self.locator.signin_title, timeout=10)

        if element_text is not None:
            if element_text.text.strip() != self.locator_page_static_text.signin_title_text.strip():
                self.log.info("Expected is {}".format(self.locator_page_static_text.signin_title_text))
                self.log.error("Result mismatched and actual result is  -- {}".format(element_text.text))
                result = False
        else:
            self.log.info("Sign In page is not available")
            result = False

        return result

    def verify_static_text_elements_available(self):
        """
        Verify the static text elements available
        :return: True | False
        """
        result = True

        welcome_to_text_el = self.get_element(*self.locator.welcome_to_text, timeout=10)

        if welcome_to_text_el is not None:
            if welcome_to_text_el.text.strip() != self.locator_page_static_text.welcome_to_text.strip():
                self.log.info("Expected is {}".format(self.locator_page_static_text.welcome_to_text.strip()))
                self.log.error("Result mismatched and actual result is  -- {}".format(welcome_to_text_el.text))
                result = False
        else:
            self.log.info("welcome_to_text_el is not available")
            result = False

        signin_title_el = self.get_element(*self.locator.signin_title, timeout=10)

        if signin_title_el is not None:
            if signin_title_el.text.strip() != self.locator_page_static_text.signin_title_text.strip():
                self.log.info("Expected is {}".format(self.locator_page_static_text.signin_title_text.strip()))
                self.log.error("Result mismatched and actual result is  -- {}".format(signin_title_el.text))
                result = False
        else:
            self.log.info("signin_title_el is not available")
            result = False

        username_text_fld_el = self.get_element(*self.locator.username_text_fld, timeout=10)

        if username_text_fld_el is not None:
            if username_text_fld_el.get_attribute('placeholder') != self.locator_page_static_text.username_text_fld_placeholder_text.strip():
                self.log.info("Expected is {}".format(self.locator_page_static_text.username_text_fld_placeholder_text.strip()))
                self.log.error("Result mismatched and actual result is  -- {}".format(username_text_fld_el.get_attribute('placeholder')))
                result = False
        else:
            self.log.info("username_text_fld_el placeholder is not available")
            result = False

        password_text_fld_el = self.get_element(*self.locator.password_text_fld, timeout=10)

        if password_text_fld_el is not None:
            if password_text_fld_el.get_attribute('placeholder') != self.locator_page_static_text.password_text_fld_placeholder_text.strip():
                self.log.info("Expected is {}".format(self.locator_page_static_text.password_text_fld_placeholder_text.strip()))
                self.log.error("Result mismatched and actual result is  -- {}".format(password_text_fld_el.get_attribute('placeholder')))
                result = False
        else:
            self.log.info("password_text_fld_el placeholder is not available")
            result = False

        login_btn_el = self.get_element(*self.locator.login_btn, timeout=10)

        if login_btn_el is not None:
            login_btn_text_el = self.get_element(*self.locator.login_btn_text, timeout=10)

            if login_btn_text_el is not None:
                if login_btn_text_el.text.strip() != self.locator_page_static_text.login_btn_text.strip():
                    self.log.info("Expected is {}".format(self.locator_page_static_text.login_btn_text.strip()))
                    self.log.error("Result mismatched and actual result is  -- {}".format(login_btn_text_el.text))
                    result = False
            else:
                self.log.info("login_btn_text_el is not available")
                result = False
        else:
            self.log.info("login_btn_el is not available")
            result = False

        or_text_el = self.get_element(*self.locator.or_text, timeout=10)

        if or_text_el is not None:
            if or_text_el.text.strip() != self.locator_page_static_text.or_text.strip():
                self.log.info("Expected is {}".format(self.locator_page_static_text.or_text.strip()))
                self.log.error("Result mismatched and actual result is  -- {}".format(or_text_el.text))
                result = False
        else:
            self.log.info("or_text_el is not available")
            result = False

        sso_btn_el = self.get_element(*self.locator.sso_btn, timeout=10)

        if sso_btn_el is not None:
            sso_btn_text_el = self.get_element(*self.locator.sso_btn_text, timeout=10)

            if sso_btn_text_el is not None:
                if sso_btn_text_el.text.strip() != self.locator_page_static_text.sso_btn_txt.strip():
                    self.log.info("Expected is {}".format(self.locator_page_static_text.sso_btn_txt.strip()))
                    self.log.error("Result mismatched and actual result is  -- {}".format(sso_btn_text_el.text))
                    result = False
            else:
                self.log.info("sso_btn_text_el is not available")
                result = False
        else:
            self.log.info("sso_btn_el is not available")
            result = False

        return result

    def click_sign_in_btn(self):
        """
        click sign in button
        :return: NA
        """
        self.get_element(*self.locator.login_btn, timeout=10).click()
        self.wait_for_sync(30)

    def click_sso_btn(self):
        """
        click SSO Sign In button
        :return: NA
        """
        self.get_element(*self.locator.sso_btn, timeout=10).click()
        self.wait_for_sync(30)

    def verify_enter_login_credentials_redirection(self, login_data_record):
        """
        Verify redirection to Appointment Type screen once logged in with valid credentials
        :param login_data_record: login_data_record as json/dict
        :return: True | False
        """
        result = True

        username_text_fld_el = self.get_element(*self.locator.username_text_fld, timeout=10)

        if username_text_fld_el is not None:
            username_text_fld_el.clear()
            username_text_fld_el.send_keys(login_data_record['username'])
        else:
            self.log.info("username_text_fld_el is not available")
            result = False

        password_text_fld_el = self.get_element(*self.locator.password_text_fld, timeout=10)

        if password_text_fld_el is not None:
            # password_text_fld_el.clear()
            password_text_fld_el.send_keys(login_data_record['password'])
        else:
            self.log.info("password_text_fld_el is not available")
            result = False

        login_btn_element_available = self.wait_for_element_to_be_clickable(*self.locator.login_btn, timeout=15)

        if login_btn_element_available is not None:
            login_btn_element_available.click()
            self.wait_for_sync(25)
        else:
            self.log.error("Sign In button element is not clickable")
            result = False

        return result