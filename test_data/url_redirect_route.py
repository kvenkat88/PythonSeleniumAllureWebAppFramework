import logging
from utility.support.ui_helpers import UIHelpers
import utility.framework.logger_utility as log_utils
import time

class URLRedirectRouter(UIHelpers):
    """This class defines the method and element identifications for UI Route to different screens"""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, driver):
        self.driver = driver
        super(URLRedirectRouter, self).__init__(driver)

    def route_to_patients_specific_patient_view(self,base_url,patient_id):
        """
        Navigate to specific patient_id view using the relative path
        :param base_url: base_url as str
        :param patient_id: patient_id as str
        :return: framed path
        """
        # file:///C:/Venkatesh/gitlab_push/DigitalHospital/Patients/PatientView/794d7217-5f11-44c4-8cb8-1386a27c7a47/patient_view.html
        # self.driver.get("{}/{}?{}".format(base_url,relative_path, patient_id))

        self.driver.get("{}\\PatientView\\{}\\patient_view.html".format(base_url,patient_id))
        self.wait_for_sync(15)

    def route_to_patients_roster_screen(self,base_url):
        """
        Navigate to Patients Roster screen using the relative path
        :param base_url: base_url as str
        :return: framed path
        """
        self.driver.get("{}\\Patients\\patient_roster.html".format(base_url))
        self.wait_for_sync(15)