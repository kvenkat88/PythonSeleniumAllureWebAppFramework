import logging
import utility.framework.logger_utility as log_utils
import datetime
import os
import traceback
from collections import Counter
import pyexcel as exc
import json
from collections import OrderedDict
import pandas as pd
from datetime import datetime


class DataReader:
    """
    This class includes basic reusable data helpers.
    """
    log = log_utils.custom_logger(logging.INFO)

    def __init__(self):
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.join(self.cur_path, r"../../test_data/TestData.xlsx")
        self.json_file_path = os.path.join(self.cur_path, r"../../test_data/user_info.json")
        self.general_data_json_file_path = os.path.join(self.cur_path, r"../../test_data/general_info.json")

    def load_excel_data(self):
        """
        This methods is used for loading excel file data
        :return: it returns excel records
        """
        records = None

        # noinspection PyBroadException

        try:
            if self.file_path is not None:
                records = exc.iget_records(file_name=self.file_path)
        except Exception as ex:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(ex))

        return records

    def get_data(self, tc_name, column_name):
        """
        This method is used for returning column data specific to test case name
        :param tc_name: it takes test case name as input parameter
        :param column_name: it takes the name of the column for which value has to be returned
        :return:
        """
        value = None
        excel_records = self.load_excel_data()

        # noinspection PyBroadException

        try:
            if excel_records is not None:
                for record in excel_records:
                    if record['TC_Name'] == tc_name:
                        value = record[column_name]
                        break
                    else:
                        continue

        except Exception as ex:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(ex))

        return value

    def pie_chart_percentage_covered(self, actual_record_count, total_record_count):
        """
        Calculate the pie chart coverage angle/degree
        :param actual_record_count: actual_record_count as int
        :param total_record_count: total_record_count as int
        :return: covered angle
        """
        # return "{}deg".format(int((((actual_record_count/total_record_count)/100)*360)*100))
        return "{}deg".format(int((actual_record_count/total_record_count)*360))

    def load_general_info_json(self):
        """
        This method is used for loading json file data. Through this we can modify the json file also
        :return: it returns json records
        # https://stackoverflow.com/questions/44587621/how-to-make-python-write-json-read-and-write-same-file-for-each-cicle
        """
        records = None

        # noinspection PyBroadException

        try:
            if self.general_data_json_file_path is not None:
                with open(self.general_data_json_file_path,'r') as json_file:
                    records = json.load(json_file)
        except Exception as ex:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(ex))

        return records

    def load_json(self):
        """
        This method is used for loading json file data. Through this we can modify the json file also
        :return: it returns json records
        # https://stackoverflow.com/questions/44587621/how-to-make-python-write-json-read-and-write-same-file-for-each-cicle
        """
        records = None

        # noinspection PyBroadException

        try:
            if self.json_file_path is not None:
                #records = exc.iget_records(file_name=self.file_path)
                with open(self.json_file_path,'r+') as json_file:
                    # I use OrderedDict to keep the same order of key/values in the source file
                    records = json.load(json_file,object_pairs_hook=OrderedDict)
        except Exception as ex:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(ex))

        return records

    def fetch_load_brand_test_data_json(self, brand_name):
        """
        This method is used to fetch and retrieve the information from {brand}_medical_center_test_data.json
        :param brand_name: brand_name as a string
        :return: it returns json records
        """
        records = None

        # noinspection PyBroadException

        try:
            self.brand_test_data_path = os.path.join(self.cur_path, r"../../test_data/brands_test_data/{}_medical_center_test_data.json".format(brand_name))

            if self.brand_test_data_path is not None:
                with open(self.brand_test_data_path,'r+') as json_file:
                    # I use OrderedDict to keep the same order of key/values in the source file
                    records = json.load(json_file,object_pairs_hook=OrderedDict)

            # with open("C:\Venkatesh\gitlab_push\clinical-experience-app-android\/appium_tests\clinicalX_android_mobile_automation\/test_data\/medical_center_brands_test_data\irvine_rosslyn_medical_center_test_data.json",'r+') as json_file:
            #     records = json.load(json_file)

        except Exception as ex:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(ex))

        return records

    def fetch_appointment_type_info_list_category(self, apptment_type, brand_name):
        """
        This method is used to fetch the Appointment Type Category's all information
        :param apptment_type: apptment_type as a string
        :param brand_name: brand_name as a string
        :return: appointment type neccessary info as list
        """

        fetched_record = None

        json_loaded = self.fetch_load_brand_test_data_json(brand_name)

        for index, element in enumerate(json_loaded["apptmt_info_data"]['appointment_type_info_list']):
            if apptment_type == json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_type']:
                fetched_record = json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]
                break
        return fetched_record

    def fetch_clinic_details(self, brand_name):
        """
        THis method is used to fetch the clinic details available for appointment booking
        :param medical_center_name: brand_name as a string (say irvine)
        :return: medical center all informations
        """

        fetched_record = None

        self.log.info("Medical Center Name passed is {}".format(brand_name))
        json_loaded = self.fetch_load_brand_test_data_json(brand_name)

        if json_loaded['clinic_provider_details']:
            fetched_record = json_loaded['clinic_provider_details']

        return fetched_record

    def generalized_fetch_clinic_details(self, medical_center_name,apptmt_type, apptmt_type_list_fetched_from_brand_on_ui_load = None):
        """
        THis method is used to fetch the clinic apptmt_type details available for appointment booking generally
        :param medical_center_name: medical_center_name as a string
        :param apptmt_type: apptmt_type as a string
        :param apptmt_type_list_fetched_from_brand_on_ui_load: apptmt_type_list_fetched_from_brand_on_ui_load as a list
        :return: medical appointment type info
        """
        apptmt_type_needed = None

        if apptmt_type in self.fetch_clinic_details(medical_center_name)['apptmt_types']:
            apptmt_type_needed = apptmt_type

        if apptmt_type not in self.fetch_clinic_details(medical_center_name)['apptmt_types']:
            if (apptmt_type_list_fetched_from_brand_on_ui_load != None) and (len(apptmt_type_list_fetched_from_brand_on_ui_load) != 0):
                apptmt_type_needed = apptmt_type_list_fetched_from_brand_on_ui_load[0]

        return apptmt_type_needed

    def fetch_appointment_type_info_list_category_bulk_records(self, brand_name):
        """
        This method is used to fetch the Appointment Type Category's all information(bulk)
        :param brand_name: brand_name as a string
        :return: all appointment type category info as list
        """
        json_loaded = self.fetch_load_brand_test_data_json(brand_name)
        return json_loaded

    def fetch_current_year(self):
        """
        Fetch the current year for appointment booking
        :return: current year
        """
        now = datetime.datetime.now()
        return now.year

    def fetch_partner_brands_list(self):
        """
        Fetch the partner brands from test_data.json file
        :return: partner brands
        """
        json_loaded = self.load_general_info_json()
        return json_loaded['partners']

    def fetch_apptmt_type_provider_time_slot_info(self, session_name):
        """
        Fetch the session_name from general_info.json file
        :param session_name: session_name as a string
        :return: session slot info list
        """
        json_loaded = self.load_general_info_json()
        fetched_info = None

        if session_name == "Morning":
            fetched_info = json_loaded['morning_time_slots']

        elif session_name == "Afternoon":
            fetched_info = json_loaded['afternoon_time_slots']

        elif session_name == "Evening":
            fetched_info = json_loaded['evening_time_slots']

        else:
            fetched_info = None

        return fetched_info

    def fetch_24_hr_to_12_hr_conversion_time_slot(self, time_slot):
        """
        Fetch the time_slot from general_info.json file
        :param time_slot: time_slot as a string
        :return: time_slot info
        """
        json_loaded = self.load_general_info_json()
        fetched_info = None

        for key,value in json_loaded['24_hr_12_hr_time_slot_conversion'].items():
            if key == time_slot:
                fetched_info = value
                break

        return fetched_info

    def fetch_24_hr_12_hr_with_AM_PM_am_pm_time_slot_conversion(self, time_slot):
        """
        Fetch the time_slot from general_info.json file
        :param time_slot: time_slot as a string
        :return: time_slot info
        """
        json_loaded = self.load_general_info_json()
        fetched_info = None

        for key,value in json_loaded['24_hr_12_hr_with_AM_PM_am_pm_time_slot_conversion'].items():
            if value == time_slot:
                fetched_info = key
                break

        return fetched_info

    def fetch_12_hr_with_AM_PM_am_pm_time_slot_conversion(self, time_slot):
        """
        Fetch the time_slot from general_info.json file
        :param time_slot: time_slot as a string
        :return: time_slot info
        """
        json_loaded = self.load_general_info_json()
        fetched_info = None

        for key,value in json_loaded['12_hr_with_AM_PM_am_pm_time_slot_conversion'].items():
            if value == time_slot:
                fetched_info = key
                break

        return fetched_info

    def fetch_24_hr_to_12_hr_conversion_time_slot_retrieve_keys(self):
        """
        Fetch the time_slot keys from general_info.json file
        :return: keys info list
        """
        json_loaded = self.load_general_info_json()
        return list(json_loaded['24_hr_12_hr_time_slot_conversion'].keys())

    def fetch_apptmt_type_provider_speciality_conversion_info(self, apptmnt_type):
        """
        Fetch the partner brands from test_data.json file
        :param apptmnt_type: apptmnt_type as a string
        :return: Speciality Name for the apptment_type provided
        """
        json_loaded = self.load_general_info_json()
        return json_loaded['apptmt_type_provider_speciality_conversion'][apptmnt_type]

    def fetch_registered_user_data_from_json_file(self, user_category=None):
        """
        This method is used to fetch the user details
        :param user_category: user_category as a string and it would hold details like mfa_disabled, mfa_enabled,etc
        :param user_name_type:  user_name_type as a string and it would hold details like self,dependent
        :return: self user related info
        """
        fetched_record = None

        json_loaded = self.load_json()
        self.log.info("Length of the retrieved user details list is {}".format(len(json_loaded['role']['registered'][user_category])))
        for i in range(len(json_loaded['role']['registered'][user_category])):
            if 'profile' in json_loaded['role']['registered'][user_category][i]:
                fetched_record = json_loaded['role']['registered'][user_category][i]['profile']
                break

        return fetched_record

    def fetch_medication_history_by_med_name(self,med_name,med_his_list):
        """
        This method is to fetch the specific medication history records based upon the med name provided
        :param med_name: med_name as string
        :param med_his_list: med_his_list as list
        :return: medication record as dict
        """
        fetched_dict = None
        # med_his_list = self.fetch_registered_user_data_from_json_file(user_category="mfa_disabled", user_name_type="self", brand_name="irvine")['medication_history']
        # print(med_his_list)
        for his_ind in range(len(med_his_list)):
            # print(med_his_list[his_ind]['history']['medication_otc_drug_supplement'])
            if med_name == med_his_list[his_ind]['history']['medication_otc_drug_supplement']:
                fetched_dict = {'drug_name': med_his_list[his_ind]['history']['medication_otc_drug_supplement'],
                                'strength': med_his_list[his_ind]['history']['strength'],
                                'dose': med_his_list[his_ind]['history']['dose'],
                                'frequency': med_his_list[his_ind]['history']['frequency'],
                                'prescription_date': med_his_list[his_ind]['history']['prescription_date'],
                                'start_date': med_his_list[his_ind]['history']['start_date'],
                                'end_date': med_his_list[his_ind]['history']['end_date'],
                                'taking_status': med_his_list[his_ind]['history']['taking_status'],
                                'notes': med_his_list[his_ind]['history']['notes']
                                }
                break
        return fetched_dict

    def fetch_allergy_history_by_allergy_name(self,allergy_name,allergy_his_list):
        """
        This method is to fetch the specific allergy history records based upon the med name provided
        :param allergy_name: allergy_name as string
        :param allergy_his_list: allergy_his_list as list
        :return: allergy record as dict
        """
        fetched_dict = None
        for his_ind in range(len(allergy_his_list)):
            if allergy_name == allergy_his_list[his_ind]['history']['allergy_info']:
                fetched_dict = {'allergy_info': allergy_his_list[his_ind]['history']['allergy_info'],
                                'reactions': allergy_his_list[his_ind]['history']['reactions'],
                                'notes': allergy_his_list[his_ind]['history']['notes']
                                }
                break
        return fetched_dict

    def fetch_observation_history_by_obs_name(self,obs_name,obs_his_list):
        """
        This method is to fetch the specific observation history records based upon the obs name provided
        :param obs_name: obs_name as string
        :param obs_his_list: obs_his_list as list
        :return: observation record as dict
        """
        fetched_dict = None
        for his_ind in range(len(obs_his_list)):
            if obs_name == obs_his_list[his_ind]['history']['test_name']:
                fetched_dict = {'test_name': obs_his_list[his_ind]['history']['test_name'],
                                'result_value': obs_his_list[his_ind]['history']['result_value'],
                                'units': obs_his_list[his_ind]['history']['units'],
                                'test_date': obs_his_list[his_ind]['history']['test_date'],
                                'result_date': obs_his_list[his_ind]['history']['result_date'],
                                'notes': obs_his_list[his_ind]['history']['notes']
                                }
                break
        self.log.info("fetched_dict value is {}".format(fetched_dict))
        return fetched_dict

    def fetch_appointment_type_timeslot_info(self, apptment_type, brand_name, day, session):
        """
        This method is used to fetch the Appointment Type timeslot information for booking an appointment
        :param apptment_type: apptment_type as a string
        :param brand_name: brand_name as a string
        :param day: day as a string
        :param session: session as a string
        :param time: time as a string
        :return: appointment type timeslot neccessary info
        """

        fetched_record = None

        json_loaded = self.fetch_load_brand_test_data_json(brand_name)
        self.log.info("Values passed for apptment_type, brand_name, day, session is {},{},{},{}".format(apptment_type, brand_name, day, session))
        for index, element in enumerate(json_loaded["apptmt_info_data"]['appointment_type_info_list']):
            if apptment_type == json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_type']:
                for a in range(len(json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_book_details'])):
                    for b in range(len(json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_book_details'][a]['details'])):
                        if json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_book_details'][a]['day'] == day and \
                            json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_book_details'][a]['details'][b]['session'] == session:
                            fetched_record = {
                                "day": json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_book_details'][a]['day'],
                                "session": json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_book_details'][a]['details'][b]['session'],
                                "time": json_loaded["apptmt_info_data"]['appointment_type_info_list'][index]['apptmt_book_details'][a]['details'][b]['time_slot']
                            }

                            break
                # break

        return fetched_record

    def fetch_clinic_details_by_medical_center_name(self, brand, medical_center_name):
        """
        THis method is used to fetch the clinic details available for appointment booking
        :param medical_center_name: brand_name as a string (say irvine)
        :return: medical center all informations
        """

        fetched_record = None

        self.log.info("Medical Center Name passed is {}".format(medical_center_name))
        json_loaded = self.fetch_load_brand_test_data_json(brand)

        if json_loaded['clinic_provider_details']['medical_center_name'] == medical_center_name:
            fetched_record = json_loaded['clinic_provider_details']

        return fetched_record

    def fetch_load_c360_deployed_json(self):
        """
        This method is used to fetch and retrieve the information from dh_deployed.json
        :return: it returns json records
        """
        records = None

        # noinspection PyBroadException

        try:
            self.c360_deployed_data_path = os.path.join(self.cur_path,
                                                        r"../../test_data/region_specific_data/dh_deployed.json")

            if self.c360_deployed_data_path is not None:
                with open(self.c360_deployed_data_path,'r+') as json_file:
                    # I use OrderedDict to keep the same order of key/values in the source file
                    records = json.load(json_file,object_pairs_hook=OrderedDict)
        except Exception as ex:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(ex))

        return records

    def fetch_provider_clinic_names_from_c360_deployed_json(self, country_name, state_territory_name):
        """
        This method is used to fetch the clinic provider names list from c360 deployed json
        :param country_name: country_name as a string
        :param state_territory_name: state_territory_name as a string
        :return: clinic provider names as list
        """

        fetched_record = None

        json_loaded = self.fetch_load_c360_deployed_json()

        try:
            if country_name in json_loaded['deployed_geo']:
                fetched_record = json_loaded['deployed_geo'][country_name][state_territory_name]['clinic_provider_names']

        except Exception as ex:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(ex))

        return fetched_record

    def fetch_load_region_specific_data_json(self, region_country_name):
        """
        This method is used to fetch and retrieve the information from {region_country_name}_region.json.json
        :param region_country_name: region_country_name as str
        :return: it returns json records
        """
        records = None

        # noinspection PyBroadException
        try:
            self.region_data_path = os.path.join(self.cur_path,
                                                     r"../../test_data/region_specific_data/{}_region.json".format(
                                                         region_country_name))

            if self.region_data_path is not None:
                with open(self.region_data_path,'r+') as json_file:
                    # I use OrderedDict to keep the same order of key/values in the source file
                    records = json.load(json_file,object_pairs_hook=OrderedDict)
        except Exception as e:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(e))

        return records

    def fetch_info_from_region_specific_data_json(self, region_country_name, state_name, provider_short_name):
        """
        This method is used to fetch the info from {country_name}_region.json
        :param region_country_name: region_country_name as a string
        :param state_name: state_name as a string
        :param provider_short_name: provider_short_name as a string
        :return: clinic_info as dict data

        Output::
        			{
				"clinic_info": {
					"partner_name": "irvine_rosslyn",
					"partner_id": "12345",
					"clinic_provider_full_name": "",
					"county": "",
					"area": "",
					"launch_url": "https://c360-5-test.healthpointe-solutions-cloud.com"
				}
			}

        """

        fetched_record = None

        json_loaded = self.fetch_load_region_specific_data_json(region_country_name)

        try:
            if json_loaded is not None:
                if len(json_loaded['state'][state_name]) != 0:
                    # print(json_loaded['state'][state_name])
                    for a in range(len(json_loaded['state'][state_name])):
                        if json_loaded['state'][state_name][a]['clinic_info']['partner_name'] == provider_short_name:
                            # fetched_record = json_loaded['state'][state_name][a]['clinic_info']['partner_name']
                            fetched_record = json_loaded['state'][state_name][a]['clinic_info']
                            break
        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            fetched_record = None

        return fetched_record

    def fetch_all_launch_urls_from_json_for_specific_state(self, region_country_name, state_name):
        """
        This method is used to fetch the info from {country_name}_region.json and retrieve the launch_urls by using region_country_name and state_name
        :param region_country_name: region_country_name as a string
        :param state_name: state_name as a string
        :return: list
        """
        fetched_record = []

        json_loaded = self.fetch_load_region_specific_data_json(region_country_name)

        try:
            if json_loaded is not None:
                if len(json_loaded['state'][state_name]) != 0:
                    # print(json_loaded['state'][state_name])
                    for a in range(len(json_loaded['state'][state_name])):
                        fetched_record.append(json_loaded['state'][state_name][a]['clinic_info']['launch_url'])
        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            # fetched_record = None

        return fetched_record

    def fetch_all_launch_urls_from_json_for_country(self, region_country_name):
        """
        This method is used to fetch the info from {country_name}_region.json and retrieve the launch_urls by using region_country_name
        :param region_country_name: region_country_name as a string
        :return: list
        """
        fetched_record = []

        json_loaded = self.fetch_load_region_specific_data_json(region_country_name)

        try:
            if json_loaded is not None:
                if 'state' in json_loaded:
                    states_list_fetched = list(json_loaded['state'].keys())
                    for state in states_list_fetched:
                        for a in range(len(json_loaded['state'][state])):
                            fetched_record.append(json_loaded['state'][state][a]['clinic_info']['launch_url'])
        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            # fetched_record = None

        return fetched_record

    def fetch_info_based_on_county_from_region_json(self, region_country_name, state_name, county_name):
        """
        This method is used to fetch the info from {country_name}_region.json based upon the county_name
        :param region_country_name: region_country_name as a string
        :param state_name: state_name as a string
        :param county_name: county_name as a string
        :return: clinic_info as dict data
        """

        fetched_record = []

        json_loaded = self.fetch_load_region_specific_data_json(region_country_name)

        try:
            if json_loaded is not None:
                if len(json_loaded['state'][state_name]) != 0:
                    # print(json_loaded['state'][state_name])
                    for a in range(len(json_loaded['state'][state_name])):
                        if json_loaded['state'][state_name][a]['clinic_info']['county'] == county_name:
                            fetched_record.append(json_loaded['state'][state_name][a]['clinic_info'])

        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            fetched_record = None

        return fetched_record

    def fetch_load_patient_info_data_json(self, region_country_name):
        """
        This method is used to fetch and retrieve the patient information from {region_country_name}_patient.json
        :param region_country_name: region_country_name as str
        :return: it returns json records
        """
        records = None

        # noinspection PyBroadException
        try:
            self.region_data_path = os.path.join(self.cur_path,
                                                     r"../../test_data/patient_data/{}_patient.json".format(
                                                         region_country_name))

            if self.region_data_path is not None:
                with open(self.region_data_path,'r+') as json_file:
                    # I use OrderedDict to keep the same order of key/values in the source file
                    records = json.load(json_file,object_pairs_hook=OrderedDict)
        except Exception as e:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(e))

        return records

    def fetch_patient_info_based_on_patient_cat(self, region_country_name, patient_cat):
        """
        This method is used to fetch the patient info based upon patient_cat
        :param region_country_name: region_country_name as a string
        :param patient_id: patient_id as a string
        :return: patient info as dict data
        """
        fetched_record = None

        json_loaded = self.fetch_load_patient_info_data_json(region_country_name)

        try:
            if json_loaded['patient_info'] is not None and len(json_loaded['patient_info']) != 0:
                for a in range(len(json_loaded['patient_info'])):
                    if json_loaded['patient_info'][a]['patient']['pat_cat'] == patient_cat:
                        fetched_record = json_loaded['patient_info'][a]['patient']
                        break

        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            fetched_record = None

        return fetched_record

    def fetch_patient_info_based_on_patient_id(self, region_country_name, patient_id):
        """
        This method is used to fetch the patient info based upon patient_id
        :param region_country_name: region_country_name as a string
        :param patient_id: patient_id as a string
        :return: patient info as dict data
        """
        fetched_record = None

        json_loaded = self.fetch_load_patient_info_data_json(region_country_name)

        try:
            if json_loaded['patient_info'] is not None and len(json_loaded['patient_info']) != 0:
                for a in range(len(json_loaded['patient_info'])):
                    if json_loaded['patient_info'][a]['patient']['pat_id'] == patient_id:
                        fetched_record = json_loaded['patient_info'][a]['patient']
                        break

        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            fetched_record = None

        return fetched_record

    def fetch_patient_id_based_on_patient_cat(self, region_country_name, patient_cat):
        """
        This method is used to fetch the patient info based upon patient_cat
        :param region_country_name: region_country_name as a string
        :param patient_cat: patient_cat as a string
        :return: patient id as str
        """
        fetched_record = None

        json_loaded = self.fetch_load_patient_info_data_json(region_country_name)
        print(json_loaded)

        try:
            if json_loaded['patient_info'] is not None and len(json_loaded['patient_info']) != 0:
                for a in range(len(json_loaded['patient_info'])):
                    if json_loaded['patient_info'][a]['patient']['pat_cat'] == patient_cat:
                        fetched_record = json_loaded['patient_info'][a]['patient']['pat_id']
                        break

        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            fetched_record = None

        self.log.info("fetched_record info available are {}".format(fetched_record))

        return fetched_record

    def fetch_all_patient_id_based_on_patient_cat(self, region_country_name):
        """
        This method is used to fetch the patient info based upon patient_id
        :param region_country_name: region_country_name as a string
        :return: patient id as str
        """
        fetched_record = []

        json_loaded = self.fetch_load_patient_info_data_json(region_country_name)

        try:
            if json_loaded['patient_info'] is not None and len(json_loaded['patient_info']) != 0:
                for a in range(len(json_loaded['patient_info'])):
                    fetched_record.append(json_loaded['patient_info'][a]['patient']['pat_id'])

        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            fetched_record = None

        self.log.info("fetched_record info available are {}".format(fetched_record))

        return fetched_record

    def provide_patient_id_infos(self, region_country_name, fetch_patient_cat):
        """
        Fetch the specific patient id or all patient ids available
        :param region_country_name: region_country_name as str
        :param fetch_patient_cat: fetch_patient_cat as str
        :return: fetched
        """
        print("region_country_name, fetch_patient_cat values are ", region_country_name, fetch_patient_cat)

        if fetch_patient_cat == "all":
            return self.fetch_all_patient_id_based_on_patient_cat(region_country_name)
        else:
            return self.fetch_patient_id_based_on_patient_cat(region_country_name, fetch_patient_cat)

    def fetch_all_patient_cat(self, region_country_name):
        """
        This method is used to fetch the patient info based upon patient category available
        :param region_country_name: region_country_name as a string
        :return: patient id as str
        """
        fetched_record = []

        json_loaded = self.fetch_load_patient_info_data_json(region_country_name)

        try:
            if json_loaded['patient_info'] is not None and len(json_loaded['patient_info']) != 0:
                for a in range(len(json_loaded['patient_info'])):
                    fetched_record.append(json_loaded['patient_info'][a]['patient']['pat_cat'])

        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            fetched_record = None

        return fetched_record

    def fetch_load_excel_as_json(self):
        """
        This method is used to fetch and retrieve the records
        :return: it returns json records. length of records
        """
        fetched_df = None

        # noinspection PyBroadException
        try:
            self.excel_data_path = os.path.join(self.cur_path,
                                                r"../../test_data/patient_data/patient_data_source.xlsx")

            with pd.ExcelFile(self.excel_data_path) as xls:
                data = pd.read_excel(xls, "Sheet1", na_values=["NA", "?", "Nil"])

            fetched_df = pd.DataFrame(data)

            # if len(fetched_df.index) != 0 and len(fetched_df.columns) != 0:
            #     print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_df.index),len(fetched_df.columns)))
            #     self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_df.index),len(fetched_df.columns)))
            #     # print(fetched_df.Patient_GMID.unique()) # returns list of patient_ids
            #     # print(fetched_df.Patient_GMID.nunique(dropna=True)) #returns length of the columns
            #
            # else:
            #     self.log.info("Length may be zero")
            #     print("Length may be zero")

        except Exception as e:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(e))

        return fetched_df

    def fetch_unique_patient_records_length(self):
        """
        This method is used to fetch and retrieve the records length
        :return: Length of records
        """
        fetched_record = self.fetch_load_excel_as_json()
        length = None

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                # print(fetched_record.Patient_GMID.unique()) # returns list of patient_ids
                # print(fetched_record.Patient_GMID.nunique(dropna=True)) #returns length of the columns
                length = len(fetched_record.Patient_GMID.unique())
            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        self.log.info("fetch_unique_patient_records_length is {}".format(length))
        return length

    def fetch_unique_patient_records_location(self):
        """
        This method is used to fetch and retrieve the location records
        :return: records as dict
        """
        fetched_record = self.fetch_load_excel_as_json()
        final_location_counts = None

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                fetched_non_duplicate_records = unique_records_fetched.to_dict(orient='records')
                final_location_counts = Counter([a['Location'] for a in fetched_non_duplicate_records])
                self.log.info("fetched final_location_counts is {}".format(final_location_counts))
                print("fetched final_location_counts is {}".format(final_location_counts))

            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return final_location_counts

    def fetch_unique_patient_records_organization(self):
        """
        This method is used to fetch and retrieve the organization records
        :return: records as dict
        """
        fetched_record = self.fetch_load_excel_as_json()
        final_organization_counts = None

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                fetched_non_duplicate_records = unique_records_fetched.to_dict(orient='records')
                final_organization_counts = Counter([a['Organization'] for a in fetched_non_duplicate_records])
                self.log.info("fetched final_organization_counts is {}".format(final_organization_counts))
                print("fetched final_organization_counts is {}".format(final_organization_counts))

            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return final_organization_counts

    def fetch_unique_patient_records_hospital(self):
        """
        This method is used to fetch and retrieve the hospital records
        :return: records as dict
        """
        fetched_record = self.fetch_load_excel_as_json()
        final_hospital_counts = None

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                fetched_non_duplicate_records = unique_records_fetched.to_dict(orient='records')
                final_hospital_counts = Counter([a['Hospital'] for a in fetched_non_duplicate_records])
                self.log.info("fetched final_hospital_counts is {}".format(final_hospital_counts))
                print("fetched final_hospital_counts is {}".format(final_hospital_counts))

            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return final_hospital_counts

    def fetch_unique_patient_records_service_line(self):
        """
        This method is used to fetch and retrieve the service line records
        :return: records as dict
        """
        fetched_record = self.fetch_load_excel_as_json()
        final_service_line_counts = None

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                fetched_non_duplicate_records = unique_records_fetched.to_dict(orient='records')
                final_service_line_counts = Counter([a['Service Line'] for a in fetched_non_duplicate_records])
                self.log.info("fetched final_service_line_counts is {}".format(final_service_line_counts))
                print("fetched final_service_line_counts is {}".format(final_service_line_counts))
            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return final_service_line_counts

    def fetch_unique_patient_records_leaders(self):
        """
        This method is used to fetch and retrieve the leaders records
        :return: records as dict
        """
        fetched_record = self.fetch_load_excel_as_json()
        final_leaders_counts = None

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                fetched_non_duplicate_records = unique_records_fetched.to_dict(orient='records')
                final_leaders_counts = Counter([a['Leaders'] for a in fetched_non_duplicate_records])
                self.log.info("fetched final_leaders_counts is {}".format(final_leaders_counts))
                print("fetched final_leaders_counts is {}".format(final_leaders_counts))

            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return final_leaders_counts

    def fetch_unique_patient_records_department(self):
        """
        This method is used to fetch and retrieve the department records
        :return: records as dict
        """
        fetched_record = self.fetch_load_excel_as_json()
        final_department_counts = None

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                fetched_non_duplicate_records = unique_records_fetched.to_dict(orient='records')
                final_department_counts = Counter([a['Department'] for a in fetched_non_duplicate_records])
                self.log.info("fetched final_department_counts is {}".format(final_department_counts))
                print("fetched final_department_counts is {}".format(final_department_counts))

            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return final_department_counts

    def fetch_unique_patient_records_timeframe_based_upon_date(self, time_range):
        """
        This method is used to fetch and retrieve the timeframe records
        :return: Length of records
        """
        import datetime

        fetched_record = self.fetch_load_excel_as_json()
        filtered_records, filtered_records_length = None,0
        start_date,end_date = None,None

        self.log.info("Excecuting for timeframe - {}".format(time_range))
        print("Excecuting for timeframe - {}".format(time_range))

        try:
            if fetched_record is not None:
                if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                    print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                    self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))

                    fetched_record_updated = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')

                    if time_range == "Past 3 days":
                        start_date = (datetime.date.today() + datetime.timedelta(days=-3)).strftime("%Y-%m-%dT%H:%M:%SZ")
                        end_date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y-%m-%dT%H:%M:%SZ")

                        filtered_records = fetched_record_updated.loc[fetched_record_updated["Current Day"].between(start_date, end_date)]
                        filtered_records_length = len(filtered_records.index)

                    if time_range == "Past 7 days":
                        start_date = (datetime.date.today() + datetime.timedelta(days=-7)).strftime("%Y-%m-%dT%H:%M:%SZ")
                        end_date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y-%m-%dT%H:%M:%SZ")

                        filtered_records = fetched_record_updated.loc[fetched_record_updated["Current Day"].between(start_date, end_date)]
                        filtered_records_length = len(filtered_records.index)

                    if time_range == "Past month":
                        start_date = (datetime.date.today() + datetime.timedelta(days=-31)).strftime("%Y-%m-%dT%H:%M:%SZ")
                        end_date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y-%m-%dT%H:%M:%SZ")

                        filtered_records = fetched_record_updated.loc[fetched_record_updated["Current Day"].between(start_date, end_date)]
                        filtered_records_length = len(filtered_records.index)

                    if time_range == "Past 3 months":
                        start_date = (datetime.date.today() + datetime.timedelta(days=-91)).strftime("%Y-%m-%dT%H:%M:%SZ")
                        end_date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y-%m-%dT%H:%M:%SZ")

                        filtered_records = fetched_record_updated.loc[fetched_record_updated["Current Day"].between(start_date, end_date)]
                        filtered_records_length = len(filtered_records.index)

                    if time_range == "Past year":
                        start_date = (datetime.date.today() + datetime.timedelta(days=-365)).strftime("%Y-%m-%dT%H:%M:%SZ")
                        end_date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y-%m-%dT%H:%M:%SZ")

                        filtered_records = fetched_record_updated.loc[fetched_record_updated["Current Day"].between(start_date, end_date)]
                        filtered_records_length = len(filtered_records.index)

                    if time_range == "Past 3 years":
                        start_date = (datetime.date.today() + datetime.timedelta(days=-1095)).strftime("%Y-%m-%dT%H:%M:%SZ")
                        end_date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y-%m-%dT%H:%M:%SZ")

                        filtered_records = fetched_record_updated.loc[fetched_record_updated["Current Day"].between(start_date, end_date)]
                        filtered_records_length = len(filtered_records.index)

                else:
                    self.log.info("Length may be zero")
                    print("Length may be zero")
            else:
                self.log.info("fetched df may be none")

        except (Exception) as e:
            self.log.info("Exception Occured:: {}".format(e))

        return filtered_records, filtered_records_length

    def fetch_unique_patient_records_timeframe_length(self):
        """
        This method is used to fetch and retrieve the timeframe records
        :return: dict records
        """
        final_records = {}
        for d in ["Past 3 days", "Past 7 days", "Past month", "Past 3 months", "Past year", "Past 3 years"]:
            filtered_records, filtered_records_length = self.fetch_unique_patient_records_timeframe_based_upon_date(d)
            final_records.update({d:filtered_records_length})
        return final_records


    def fetch_unique_patient_records_timeframe_dummy(self):
        """
        This method is used to fetch and retrieve the timeframe records
        :return: Length of records
        """
        fetched_record = self.fetch_load_excel_as_json()
        final_timeframe_counts = None
        final_timeframe_info_not_available = {}

        import datetime

        # now = datetime.now()
        # dt_string = now.strftime('%Y-%m-%dT%H:%M:%SZ')

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))

                fetched_record = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')

                start_date = (datetime.date.today() + datetime.timedelta(days=-7)).strftime("%Y-%m-%dT%H:%M:%SZ")
                end_date = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%Y-%m-%dT%H:%M:%SZ")

                final_timeframe_counts = fetched_record.loc[fetched_record["Current Day"].between(start_date, end_date)]
                # print(df2)

                # unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                # fetched_non_duplicate_records = unique_records_fetched.to_dict(orient='records')

                # days_pre_processed = [{"days":(datetime.strptime(dt_string,'%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(k['date'],'%Y-%m-%dT%H:%M:%SZ')).days,"Name":k['First name'] }for k in [{"date":fetched_non_duplicate_records[i]['Current Day'], "First name":fetched_non_duplicate_records[i]['First name']} for i in range(len(fetched_non_duplicate_records))]]
                # print(days_pre_processed)
                # self.log.info("days_pre_processed with user info values are {}".format(days_pre_processed))
                #
                # days = [(datetime.strptime(dt_string,'%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(k,'%Y-%m-%dT%H:%M:%SZ')).days for k in [fetched_non_duplicate_records[i]['Current Day'] for i in range(len(fetched_non_duplicate_records))]]
                # print(days)
                # self.log.info("days with user info values are {}".format(days))
                #
                # dateDifference = list()
                # for day in days:
                #     if day <= 3:
                #         dateDifference.append("Past 3 days")
                #
                #     elif day <=7: # "Past 7 days"
                #         dateDifference.append("Past 7 days")
                #
                #     elif day <= 31: # "Past month"
                #         dateDifference.append("Past month")
                #
                #     elif day <= 91: # "Past 3 months"
                #         dateDifference.append("Past 3 months")
                #
                #     elif day <= 365: # "Past year"
                #         dateDifference.append("Past year")
                #
                #     elif day <= 1095: # "Past 3 years"
                #         dateDifference.append("Past 3 years")
                #
                # print(dateDifference)
                # self.log.info("dateDifference values are {}".format(dateDifference))
                # final_timeframe_counts = Counter([a for a in dateDifference])
                # print(final_timeframe_counts)
                # self.log.info("final_timeframe_counts values are {}".format(final_timeframe_counts))

                # if 'Past 3 days' not in dateDifference:
                #     final_timeframe_info_not_available.update({"Past 3 days": 0})
                #
                # if 'Past 7 days' not in dateDifference:
                #     final_timeframe_info_not_available.update({"Past 7 days": 0})
                #
                # if 'Past month' not in dateDifference:
                #     final_timeframe_info_not_available.update({"Past month": 0})
                #
                # if 'Past 3 months' not in dateDifference:
                #     final_timeframe_info_not_available.update({"Past 3 months": 0})
                #
                # if 'Past year' not in dateDifference:
                #     final_timeframe_info_not_available.update({"Past year": 0})
                #
                # if 'Past 3 years' not in dateDifference:
                #     final_timeframe_info_not_available.update({"Past 3 years": 0})
                #
                # count_available_items = [{k:v} for k,v in final_timeframe_counts.items()]
                # print({final_timeframe_info_not_available.update(k) for k in count_available_items})

            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return final_timeframe_counts

    def fetch_load_specific_patient_info_excel_as_json(self, patient_name):
        """
        This method is used to fetch and retrieve the patient information
        :param patient_name: patient_name as str
        :return: it returns json records. length of records
        """
        fetched_record = None
        record_list_length = 0

        # noinspection PyBroadException
        try:
            self.excel_data_path = os.path.join(self.cur_path,
                                                r"../../test_data/patient_data/patient_data_source.xlsx")

            with pd.ExcelFile(self.excel_data_path) as xls:
                data = pd.read_excel(xls, "Sheet1", na_values=["NA", "?", "Nil"])

            df = pd.DataFrame(data)

            fetched_dataframe = df[df['First name'] + ' ' + df['Last name'] == patient_name]

            if len(fetched_dataframe) != 0:
                json_records = fetched_dataframe.to_json(orient='records')
                fetched_record = json.loads(json_records)
                record_list_length = len(fetched_record)
            else:
                print("Unable to find the record for user - {}".format(patient_name))

        except Exception as e:
            # traceback.print_exc(ex)
            self.log.info("Exception Occurred :: {}".format(e))

        return fetched_record,record_list_length

    def fetch_provider_action_status_record_action_category(self, json_loaded, action_type):
        """
        This method is used to fetch the Provider Action Status's action category (like Add to Watch List, etc)
        :param json_loaded: json_loaded as a json
        :param action_type: action_type as a string
        :return: list
        """
        fetched_record = []

        try:
            if len(json_loaded['LatestStatus']) != 0:
                for a in range(len(json_loaded['LatestStatus'])):
                    if json_loaded['LatestStatus'][a]['ActionType'] == action_type:
                        fetched_record.append(json_loaded['LatestStatus'][a]['Action'])
        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            # fetched_record = None

        return fetched_record

    def fetch_provider_action_status_record_based_on_condition(self, json_loaded, action_type, action):
        """
        This method is used to fetch the Provider Action Status under the Actions Section in Summary Main Menu
        :param json_loaded: json_loaded as a json
        :param action_type: action_type as a string
        :param action: action as a string
        :return: dict
        """
        fetched_record = None

        try:
            if len(json_loaded['LatestStatus']) != 0:
                for a in range(len(json_loaded['LatestStatus'])):
                    if json_loaded['LatestStatus'][a]['ActionType'] == action_type and json_loaded['LatestStatus'][a]['Action'] == action:
                        fetched_record = json_loaded['LatestStatus'][a]
                        break
        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            # fetched_record = None

        return fetched_record

    def fetch_provider_action_status_history_record_based_on_condition(self, patient_record, action_type, action):
        """
        This method is used to fetch the Provider Action Status History under the Actions Section in Summary Main Menu
        :param patient_record: patient_record as a json
        :param action_type: action_type as a string
        :param action: action as a string
        :return: list,no_history_check
        """
        fetched_record = []
        history_check = None

        try:
            provider_action_history_record = json.loads(patient_record['Provider Action History'])

            provider_action_history_record_length = 0

            if action in provider_action_history_record:
                if len(provider_action_history_record[action]) != 0:
                    provider_action_history_record_length = len(provider_action_history_record[action])
                else:
                    self.log.info("provider_action_history_record_length is {}".format(provider_action_history_record_length))
            else:
                self.log.info("{} key is not available in provider_action_history_record - {}".format(action, provider_action_history_record))
                provider_action_history_record_length = 0

            if provider_action_history_record_length != 0:
                for a in range(len(provider_action_history_record[action])):
                    if provider_action_history_record[action][a]['ActionType'] == action_type and provider_action_history_record[action][a]['Action'] == action:
                        fetched_record.append(provider_action_history_record[action][a]['Data']['Note'])

        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            import traceback
            traceback.print_exc()
            # fetched_record = None

        if len(fetched_record) != 0:
            calculated_sum = sum([0 if len(c) == 0 else len(c) for c in fetched_record])
            if calculated_sum == 0:
                history_check = "No History"
            else:
                history_check = "History Available"
        else:
            history_check = "Exception_in_History_Calculation"

        return fetched_record, history_check

    def fetch_past_history_record_based_on_condition(self, json_loaded, action_type, action):
        """
        This method is used to fetch the Past Actions under the Actions Section in Summary Main Menu
        :param patient_record: patient_record as a json
        :param action_type: action_type as a string
        :param action: action as a string
        :return: dict
        """
        fetched_record = []

        try:
            if len(json_loaded['LatestAction']) != 0:
                for a in range(len(json_loaded['LatestAction'])):
                    if json_loaded['LatestAction'][a]['ActionType'] == action_type and json_loaded['LatestAction'][a]['Action'] == action:
                        fetched_record.append(json_loaded['LatestAction'][a])
        except Exception as e:
            self.log.info("Exception Occurred :: {}".format(e))
            # fetched_record = None

        return fetched_record

    def fetch_unique_patient_records(self,filter_list):
        """
        This method is used to fetch and retrieve the patient records
        :param filter_list: filter_list as list
        :return: Length of records
        """
        fetched_record = self.fetch_load_excel_as_json()
        fetched_records_dict = None
        if not isinstance(filter_list, list):
            filter_list = []

        if fetched_record is not None:
            if len(fetched_record.index) != 0 and len(fetched_record.columns) != 0:
                print("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                self.log.info("Before Unique Records Identification::Length of the rows - {} and Length of the columns - {}".format(len(fetched_record.index),len(fetched_record.columns)))
                unique_records_fetched = fetched_record.drop_duplicates(subset=['Patient_GMID'],keep='last')
                # fetched_full_name_df = unique_records_fetched.loc[:, ['First name', 'Last name']]
                fetched_full_name_df = unique_records_fetched.loc[:, filter_list]
                fetched_records_dict = fetched_full_name_df.to_dict(orient='records')
                # print(fetched_records_dict)
            else:
                self.log.info("Length may be zero")
                print("Length may be zero")
        else:
            self.log.info("fetched df may be none")

        return fetched_records_dict

    def fetch_specific_pat_records_based_upon_pat_name(self, patient_name):
        fetched_record = None
        try:
            parsed_df_dict = self.fetch_unique_patient_records(
                filter_list=['Total Risk', 'First name', 'Last name', 'Admit date', 'Hospital', 'Department',
                                                                               'EncounterStatus','Age', 'Gender', 'Race/Ethnicity','First Listed Diagnosis',
                                                                               'First Listed Diagnosis Type','Latest Diagnosis Status','Latest Procedure Category',
                                                                               'RxHCCs','ER Visits','progress'])
            if parsed_df_dict is not None:
                for a in parsed_df_dict:
                    if "{} {}".format(a["First name"],a["Last name"]) == patient_name:
                        fetched_record = a
                        break

        except (Exception) as e:
            self.log.info("Exception Occurred :: {}".format(e))

        return fetched_record

# d = DataReader()
# rec = d.fetch_unique_patient_records(filter_list=['Total Risk','First name','Last name','Admit date','Hospital', 'Department',
#                                                                    'EncounterStatus','Age', 'Gender', 'Race/Ethnicity','First Listed Diagnosis',
#                                                                    'First Listed Diagnosis Type','Latest Diagnosis Status','Latest Procedure Category',
#                                                                    'RxHCCs','ER Visits','progress'])

# rec = d.fetch_specific_pat_records_based_upon_pat_name(patient_name="Lolly Palfree")
# print(rec)







