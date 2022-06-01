import logging
import pytest
import allure
import sys
import test_data.global_variables as gv
import utility.framework.logger_utility as log_utils
from utility.framework.execution_status_utility import ExecutionStatus
from utility.framework.data_reader_utility import DataReader
from pages.physician_role.ed_hospitalization.patients.patient_view.patient_view_specific_patient_landing_home_page import PatientViewSpecificPatientLandingHome
from pages.common.header_footer_page import HeaderFooterPage
from test_data.url_redirect_route import URLRedirectRouter
"""
    TODO:: TestCases Pending
    1. Logo Image cross check/Image Validation
    2. To and back page navigation
    3. Header and Footer section Validation
    4. Fields exception message validations
"""
#unittest.defaultTestLoader.sortTestMethodsUsing = None

@pytest.mark.usefixtures("test_setup")
@allure.story('[XXX_Hospital Web App] - Automate the Specific Patient View Screen Functionality')
@allure.feature('XXX_Hospital Web App - Specific Patient View Screen')
@pytest.mark.incremental
class TestPatientsSpecificPatientViewFlow(object):
    """
    This class contains the executable test cases.
    """
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(autouse=True) # Fixture to get configuration items from command line
    def _request_get_config_params(self, get_config_params):
        self._config_params = get_config_params

    @pytest.fixture(autouse=True)
    def objectSetup(self, test_setup):
        self.data_reader = DataReader()
        self.pat_view_page = PatientViewSpecificPatientLandingHome(self.driver)
        self.header_footer = HeaderFooterPage(self.driver)
        self.exe_status = ExecutionStatus(self.driver)
        self.url_router = URLRedirectRouter(self.driver)

        self.fetched_pat_for_view = self.data_reader.fetch_patient_info_based_on_patient_cat(
            region_country_name=self._config_params['region']['country'], patient_cat=self._config_params['patient'])

        self.fetched_patient_record,self.record_list_length = self.data_reader.fetch_load_specific_patient_info_excel_as_json(
            patient_name="{} {}".format(self.fetched_pat_for_view['first_name'], self.fetched_pat_for_view['last_name']))

        if self.record_list_length == 1:
            self.log.info("Record Length is {}".format(self.record_list_length))
            self.fetched_patient_record_latest = self.fetched_patient_record[0]

        elif self.record_list_length > 1:
            self.log.info("Record Length is {}".format(self.record_list_length))
            self.fetched_patient_record_latest = self.fetched_patient_record[-1]

    @allure.testcase("Verify Patient view header and menu section static and dynamic elements")
    @allure.id("TC_DIGITAL_HOSPITAL_WEB_PATIENTS_PATIENT_VIEW_SCREEN_001")
    @allure.severity(allure.severity_level.NORMAL)
    #@pytest.mark.run(order=1)
    def test_01_verify_patient_view_landing_page_header_menu_static_dynamic_elements(self):
        """
        This test is validating the presence of Sign In Screen Elements.
        :return: return test status
        """
        ## Determining the name of the Current Function
        test_name = sys._getframe().f_code.co_name

        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        self.url_router.route_to_patients_specific_patient_view(base_url=gv.base_url_fetched, patient_id=self.fetched_pat_for_view['pat_id'])

        with allure.step("Verify Patient view header and menu section static and dynamic elements"):
            result = self.pat_view_page.patient_view_landing_page_header_menu_static_dynamic_elements(patient_name="{} {}".format(self.fetched_patient_record_latest['First name'],self.fetched_patient_record_latest['Last name']))
            self.exe_status.mark_final(test_step="Verify Patient view header and menu section static and dynamic elements", result=result)