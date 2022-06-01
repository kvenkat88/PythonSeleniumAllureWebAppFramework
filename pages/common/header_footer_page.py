import logging
from utility.support.ui_helpers import UIHelpers
import utility.framework.logger_utility as log_utils
from locators.common.header_footer_page_locators import HeaderFooterPageLocators, HeaderFooterPageLocatorsStaticText
from locators.common.landing_sign_in_page_locator import LandingSignInPageLocators, LandingSignInPageLocatorsStaticText

class HeaderFooterPage(UIHelpers):
    """This class defines the method and element identifications forHeader Footer Sections."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, driver):
        self.driver = driver
        #self.ui_helpers = UIHelpers(driver)
        self.locator = HeaderFooterPageLocators()
        self.locator_page_static_text = HeaderFooterPageLocatorsStaticText()
        super(HeaderFooterPage, self).__init__(driver)

    def verify_header_section_after_user_login(self, user_first_name):
        """
        Verify the header section elements available after login
        :param user_first_name: user_first_name as str
        :return: True | False
        """
        result = True

        after_login_toolbar_user_name_el = self.get_element(*self.locator.after_login_toolbar_user_name, timeout=10)

        if after_login_toolbar_user_name_el is not None:
            if after_login_toolbar_user_name_el.text.strip() != "Welcome, {}!".format(user_first_name.strip()):
                self.log.info("Expected is {}".format(self.locator_page_static_text.footer_terms_of_use_text.strip()))
                self.log.error("Result mismatched and actual result is  -- {}".format(after_login_toolbar_user_name_el.text))
                result = False
        else:
            self.log.info("after_login_toolbar_user_name_el is not available for the screen name")
            result = False

        return result

    def verify_header_footer_section_elements_available(self, screen_name=None):
        """
        Verify the static text elements available
        :param screen_name:screen_name as str
        :return: True | False
        """
        result = True

        if screen_name == "after_login":
            branding_logo_after_sign_in_el = self.get_element(*self.locator.branding_logo_after_sign_in, timeout=10)

            if branding_logo_after_sign_in_el is not None:
                self.log.info("branding_logo_after_sign_in element is available")
            else:
                self.log.info("branding_logo_after_sign_in_el is not available")
                result = False
        else:
            site_header_left_logo_el = self.get_element(*self.locator.site_header_left_logo, timeout=10)

            if site_header_left_logo_el is None:
                self.log.info("site_header_left_logo_el is not available")
                result = False

        footer_terms_of_use_el = self.get_element(*self.locator.footer_terms_of_use, timeout=10)

        if footer_terms_of_use_el is not None:
            footer_terms_of_use_text_el = self.get_element(*self.locator.footer_terms_of_use_text, timeout=10)

            if footer_terms_of_use_text_el is not None:
                if footer_terms_of_use_text_el.text.strip() != self.locator_page_static_text.footer_terms_of_use_text.strip():
                    self.log.info("Expected is {}".format(self.locator_page_static_text.footer_terms_of_use_text.strip()))
                    self.log.error("Result mismatched and actual result is  -- {}".format(footer_terms_of_use_text_el.text))
                    result = False
            else:
                self.log.info("footer_terms_of_use_text_el is not available")
                result = False
        else:
            self.log.info("footer_terms_of_use_el is not None")
            result = False

        footer_privacy_policy_el = self.get_element(*self.locator.footer_privacy_policy, timeout=10)

        if footer_privacy_policy_el is not None:
            footer_privacy_policy_text_el = self.get_element(*self.locator.footer_privacy_policy_text, timeout=10)

            if footer_privacy_policy_text_el is not None:
                if footer_privacy_policy_text_el.text.strip() != self.locator_page_static_text.footer_privacy_policy_text.strip():
                    self.log.info("Expected is {}".format(self.locator_page_static_text.footer_privacy_policy_text.strip()))
                    self.log.error("Result mismatched and actual result is  -- {}".format(footer_privacy_policy_text_el.text))
                    result = False
            else:
                self.log.info("footer_privacy_policy_text_el is not available")
                result = False
        else:
            self.log.info("footer_privacy_policy_el is not None")
            result = False

        footer_cookie_policy_el = self.get_element(*self.locator.footer_cookie_policy, timeout=10)

        if footer_cookie_policy_el is not None:
            footer_cookie_policy_text_el = self.get_element(*self.locator.footer_cookie_policy_text, timeout=10)

            if footer_cookie_policy_text_el is not None:
                if footer_cookie_policy_text_el.text.strip() != self.locator_page_static_text.footer_cookie_policy_text.strip():
                    self.log.info("Expected is {}".format(self.locator_page_static_text.footer_cookie_policy_text.strip()))
                    self.log.error("Result mismatched and actual result is  -- {}".format(footer_cookie_policy_text_el.text))
                    result = False
            else:
                self.log.info("footer_cookie_policy_text_el is not available")
                result = False
        else:
            self.log.info("footer_cookie_policy_el is not None")
            result = False

        footer_help_link_el = self.get_element(*self.locator.help_link, timeout=10)

        if footer_help_link_el is not None:
            footer_help_link_text_el = self.get_element(*self.locator.help_link_text, timeout=10)

            if footer_help_link_text_el is not None:
                if footer_help_link_text_el.text.strip() != self.locator_page_static_text.help_link_text.strip():
                    self.log.info("Expected is {}".format(self.locator_page_static_text.help_link_text.strip()))
                    self.log.error("Result mismatched and actual result is  -- {}".format(footer_help_link_text_el.text))
                    result = False
            else:
                self.log.info("footer_help_link_text_el is not available")
                result = False
        else:
            self.log.info("footer_help_link_el is not None")
            result = False

        return result

    def verify_account_name_spinner_element_section(self, user_details):
        """
        Verify the Account Name availability
        :param user_details: user_details as a dict
        :return: True | False
        """
        result = True
        arrived_first_name = None

        logged_in_user_icon_el = self.get_element(*self.locator.logged_in_user_icon, timeout=10)

        if not logged_in_user_icon_el:
            self.log.error("User Icon element after login is not available")
            result = False

        after_login_header_profile_icon_spinner_btn_el = self.wait_for_element_to_be_present(*self.locator.after_login_header_profile_icon_spinner_btn, timeout=15)

        if after_login_header_profile_icon_spinner_btn_el is not None:
            if len(user_details['first_name']) > 4:
                arrived_first_name = "{}...".format(user_details['first_name'][0:4])
            else:
                arrived_first_name = user_details['first_name']

            arrived_last_name = user_details['last_name'][0]

            after_login_header_profile_name_el = self.get_element(*self.locator.after_login_header_profile_name, timeout=10)

            if after_login_header_profile_name_el is not None:
                if after_login_header_profile_name_el.text.strip()!= "{} {}.".format(arrived_first_name,arrived_last_name):
                    self.log.error("Username Framed is different compared with expected one - {}".format("{} {}.".format(arrived_first_name,arrived_last_name)))
                    self.log.info("Username Framed is different compared with expected one and available username is {}".format(after_login_header_profile_name_el.text.strip()))
                    result = False
            else:
                self.log.info("after_login_header_profile_name_el is not available")
                result = False
        else:
            self.log.info("after_login_header_profile_icon_spinner_btn_el is not available")
            result = False

        return result

    # def verify_account_name_spinner_selector_dropdown_availbility_and_its_options(self):
    #     """
    #     Verify the Account Name dropdown box availability and its options
    #     :return: True | False
    #     """
    #     result = True
    #
    #     click_spinner_element = self.wait_for_element_to_be_clickable(*self.header_footer_locator.username_dropdown_displayed_after_login)
    #     if not click_spinner_element:
    #         self.log.error("Unable to click on Account Spinner Dropdown")
    #
    #     click_spinner_element.click()
    #
    #     appointments_element_available = self.wait_for_element_visible_located(*self.header_footer_locator.spinner_appointments_option)
    #
    #     if appointments_element_available.text.strip() != self.header_footer_static_text.spinner_appointments_text.strip():
    #         self.log.info("Expected text is {}".format(self.header_footer_static_text.spinner_appointments_text))
    #         self.log.error("Actual text  is {}".format(appointments_element_available.text))
    #         result = False
    #
    #     my_account_element_available = self.wait_for_element_visible_located(*self.header_footer_locator.spinner_my_account_option)
    #
    #     if my_account_element_available.text.strip() != self.header_footer_static_text.spinner_my_account_option_text.strip():
    #         self.log.info("Expected text is {}".format(self.header_footer_static_text.spinner_my_account_option_text))
    #         self.log.error("Actual text  is {}".format(my_account_element_available.text))
    #         result = False
    #
    #     spinner_recommendations_option_element_available = self.wait_for_element_visible_located(*self.header_footer_locator.spinner_recommendations_option)
    #
    #     if spinner_recommendations_option_element_available.text.strip() != self.header_footer_static_text.spinner_recommendations_option_text.strip():
    #         self.log.info("Expected text is {}".format(self.header_footer_static_text.spinner_recommendations_option_text))
    #         self.log.error("Actual text  is {}".format(spinner_recommendations_option_element_available.text))
    #         result = False
    #
    #     sign_out_element_available = self.wait_for_element_visible_located(*self.header_footer_locator.spinner_sign_out_option)
    #
    #     if sign_out_element_available.text.strip() != self.header_footer_static_text.spinner_sign_out_option_text.strip():
    #         self.log.info("Expected text is {}".format(self.header_footer_static_text.spinner_sign_out_option_text))
    #         self.log.error("Actual text  is {}".format(sign_out_element_available.text))
    #         result = False
    #
    #     return result

    def fetch_header_name_greet_message(self):
        """
        Fetch the welcome greet message after login
        :return:
        """
        fetched = None
        try:
            el_available = self.get_element(*self.locator.after_login_toolbar_user_name, timeout=10)

            if el_available is not None:
                fetched = el_available.text.strip()

        except Exception as e:
            pass

        self.log.info("Value of fetched is {}".format(fetched))

        return fetched

    def fetch_header_patient_view_name(self, patient_name):
        """
        Fetch the patient view name available in the header
        :param patient_name: patient_name as str
        :return: Fetched values
        """
        result = True

        try:
            el_available = self.get_element(*self.locator.after_login_header_patient_name, timeout=10)

            if el_available is not None:
                fetched = el_available.text.strip()
                if "{} {}".format(fetched.split()[0].strip(),fetched.split()[1].strip()) == patient_name:
                    self.log.info("patient_name_fetched info is {}".format(fetched))
                    result = True
                else:
                    self.log.info("Failure Loop::patient_name_fetched info is {}".format(fetched))
                    result = False
            else:
                self.log.info("Element is not available")
                result = False

        except Exception as e:
            pass

        return result

    def verify_sign_out_functionality(self):
        """
        Verify the Sign Out functionality
        :return: True | False
        """
        result = True

        click_spinner_element = self.wait_for_element_to_be_clickable(*self.locator.after_login_header_profile_icon_spinner_btn,  timeout=10)

        if not click_spinner_element:
            self.log.error("Unable to click on Profile Account Spinner Dropdown")
            result = False
        else:
            click_spinner_element.click()

            sign_out_element_available = self.wait_for_element_visible_located(*self.locator.after_login_sign_out_link, timeout=10)

            if sign_out_element_available is None:
                self.log.error("Account Name Spinner Dropdown Box Sign Out option is not available")
                result = False
            else:
                sign_out_element_available.click()
                self.wait_for_sync(20)

                sign_in_page_title_text_el = self.get_element(*LandingSignInPageLocators().signin_title, timeout=10)

                if sign_in_page_title_text_el is not None:
                    if sign_in_page_title_text_el.text.strip() != LandingSignInPageLocatorsStaticText().login_btn_text.strip():
                        self.log.info("Expected Page redirection and Page Title is {}".format(LandingSignInPageLocatorsStaticText().login_btn_text))
                        self.log.error("Actual Page redirection and Page Title is {}".format(sign_in_page_title_text_el.text))
                        result = False
                else:
                    self.log.info("sign_in_page_title_text_el is not available")
                    result = False

        return result

