import logging
# from traceback import print_stack
# from utility.support.ui_helpers import UIHelpers
# from configparser import ConfigParser
import utility.framework.logger_utility as log_utils
import imaplib
import email
import re
import datetime
from PIL import Image, ImageDraw
import json, sys, os
from utility.framework.data_reader_utility import DataReader

def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare

'''
usage in module before start of the class
    ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare

https://codereview.stackexchange.com/questions/122532/controlling-the-order-of-unittest-testcases
'''
#class BaseHelpers(UIHelpers):
class BaseHelpers(object):
    """
    This class includes basic reusable base_helpers.
    """
    log = log_utils.custom_logger(logging.INFO)

    # def __init__(self, driver):
    #     super().__init__(driver)
    #     self.driver = driver

    def identify_space_in_sentence(self, text):
        """
        Identify whether space is available in the text or not
        :param text: text as string
        :return: space count
        """
        count=0
        for a in text:
            if (a.isspace()) == True:
                count += 1

        return count

    def generate_random_integer(self, rnge=9999):
        """
        Generate the random integer from the range
        :param rnge: rnge as int
        :return: int
        """
        import random
        return random.randint(0, rnge)

    def get_date(self,days=0):
        """
        Fetch current day date as form of new date format based upon timedelta
        :param days: days in int
        :return: date object in formatted string
        """
        return (datetime.date.today() + datetime.timedelta(days=days)).strftime("%b %d")

    def get_usa_date_format(self, days=0):
        """
        Fetch USA current day date as form of new date format based upon timedelta
        :param days: days in int
        :return: date object in formatted string
        """
        return (datetime.date.today() + datetime.timedelta(days=days)).strftime("%m/%d/%Y")

    def format_date_and_produce_day(self,date_with_month_fetched_from_app,year=DataReader().fetch_current_year()):
        """
        Get the date as input and return the day(weekday)
        :param date_with_month_fetched_from_app: date_with_month_fetched_from_app in string like Oct 10
        :param year: year in int
        :return: for today => Today, tomorrow => Tomorrow and further days => Thursday,Monday, etc
        """
        full_weekday_name = None

        if (datetime.date.today() + datetime.timedelta(days=0)).strftime("%b %d") == date_with_month_fetched_from_app:
            full_weekday_name = "Today"

        elif (datetime.date.today() + datetime.timedelta(days=1)).strftime("%b %d") == date_with_month_fetched_from_app:
            full_weekday_name = "Tomorrow"

        else:
            date_string = "{} {}".format(date_with_month_fetched_from_app, year)
            date_object = datetime.datetime.strptime(date_string, "%b %d %Y")
            print("date_object =", date_object)
            full_weekday_name = date_object.strftime("%A")

        return full_weekday_name

    def format_date_and_produce_day_for_apptmt_booking(self,date_with_month_fetched_from_app,year=DataReader().fetch_current_year()):
        """
        Get the date as input and return the day(weekday)
        :param date_with_month_fetched_from_app: date_with_month_fetched_from_app in string like Oct 10
        :param year: year in int
        :return: for today => Today, tomorrow => Tomorrow and further days => Thursday,Monday, etc
        """
        full_weekday_name = None

        if (datetime.date.today() + datetime.timedelta(days=0)).strftime("%b %d") == date_with_month_fetched_from_app:
            full_weekday_name = "Today"

        elif (datetime.date.today() + datetime.timedelta(days=1)).strftime("%b %d") == date_with_month_fetched_from_app:
            full_weekday_name = "Tomorrow"

        else:
            date_string = "{} {}".format(date_with_month_fetched_from_app, year)
            date_object = datetime.datetime.strptime(date_string, "%b %d %Y")
            print("date_object =", date_object)
            full_weekday_name = date_object.strftime("%A")

        return full_weekday_name


    def is_time_format(self,string):
        """
        This method is used to validate the time format available while booking the appointment
        :param string: string as str like 8:00 am or 12:56 pm or 08:34 am
        :return: True | False
        """
        time_re = re.compile(r'(^0?\d|1[0-2]):[0-5]\d\s*(?:am|pm)', re.M | re.I)
        return bool(time_re.match(string))

    def is_doctor_name_format(self,string):
        """
        This method is used to validate the doctor name format available while booking the appointment
        :param string: string as str like "Dr. Venkatesh Miller, MD"
        :return: True | False
        """
        #doctor_name_re = re.compile(r'(?:Dr|Mr)\.\s+[a-z\s]+\,\s*(?:MD|MBBS)', re.M | re.I)
        doctor_name_re = re.compile(r'[a-z\s]+\,\s*(?:MD|MBBS|BSN|HWC)', re.M | re.I)
        return bool(doctor_name_re.match(string))

    def is_payment_price_format(self, string):
        """
        This method is used to validate the payment price format available
        :param string: string as str like "$50.00"
        :return: True | False
        """
        payment_price_re = re.compile(r'(\$)(?:\d+\.)?\d+', re.M | re.I)
        return bool(payment_price_re.match(string))

    def is_estimated_time_value_format(self, string):
        """
        This method is used to validate the estimated time value format available
        :param string: string as str like "30 min/ 30 minutes"
        :return: True | False
        """
        #estimated_time = re.compile(r'(?:\d+)\s+(min)', re.M | re.I)
        estimated_time = re.compile(r'(?:\d+\s+Hour).*|(?:\d+\s+Minutes)', re.M | re.I) # Still have to optimize this regex
        return bool(estimated_time.match(string))

    def is_mobile_number_format(self, string):
        """
        This method is used to validate the mobile no format available
        :param string: string as str like (555) 123-4567
        :return: True | False
        """
        mobile_no = re.compile(r'^\(\d{1,3}\)\s+\d{1,3}\-\d{1,4}$', re.M | re.I)
        return bool(mobile_no.match(string))

    def is_date_format(self, string):
        """
        This method is used to validate the date format available
        :param string: string as str like 03/11/2020
        :return: True | False
        """
        # date_provided = re.compile(r'^(0[1-9]|1[0-2])\/(3[01]|[12][0-9]|0[1-9])\/[0-9]{4}$', re.M | re.I)
        # return bool(date_provided.match(string))

        try:
            datetime.datetime.strptime(string, '%m/%d/%Y')
            return True
        except ValueError:
            return False

    def no_of_clinics_available_format_with_zipcode(self, string):
        """
        This method is used to validate the text present in clinic locator
        :param string: string as str like 5 clinics near 92618
        :return: True | False
        """
        str_format = re.compile(r'(\d+\s+clinics near\s\d\w{0,4})', re.M | re.I)
        return bool(str_format.match(string))

    def no_of_providers_available_format_advanced_serach(self, service_type,string):
        """
        This method is used to validate the text present in Advanced Provider Search
        :param string: string as str like 5 Medical Providers
        :param service_type: service_type as str like Medical, Dental
        :return: True | False
        """
        str_format = re.compile(r'(\d+\s+{}\s Providers)'.format(service_type), re.M | re.I)
        return bool(str_format.match(string))

    def no_of_clinics_available_format(self, string, service_type):
        """
        This method is used to validate the text present in clinic locator
        :param string: string as str like 5 Clinics With Medical Services
        :param service_type: service_type as str like Medical, Dental
        :return: True | False
        """
        str_format = re.compile(r'(\d+\s+Clinics near {} Services)'.format(service_type), re.M | re.I)
        return bool(str_format.match(string))

    def no_of_articles_available_format(self, string, search_term):
        """
        This method is used to validate the articles text available
        :param string: string as str like 69 articles for Covid 19
        :param search_term: search_term as str like Covid 19, Diabetes
        :return: True | False
        """
        # 69 articles for Covid 19
        str_format = re.compile(r'(\d+\s+articles for {})'.format(search_term), re.M | re.I)
        return bool(str_format.match(string))

    def no_of_articles_results_in_detailed_load_more_results(self, string, search_term):
        """
        This method is used to validate the no of full articles
        :param string: string as str like 3 Results for
        :param search_term: search_term as str like Covid 19, Diabetes
        :return: True | False
        """
        # 69 articles for Covid 19
        str_format = re.compile(r'(\d+\s+articles for {})'.format(search_term), re.M | re.I)
        return bool(str_format.match(string))

    def clinic_miles_text_format(self, string):
        """
        This method is used to validate the miles (3.7 mi)text present in clinic locator address list
        :param string: string as str like 3.7 mi
        :return: True | False
        """
        # str_format = re.compile(r'^(\d+.\d\s+mi)$', re.M | re.I)
        str_format = re.compile(r'^[0-9]{1,11}(?:\.[0-9]{1,3})?\s+mi$', re.M | re.I)
        return bool(str_format.match(string))

    def parse_timezone_comparision_info(self, comparison_text):
        """
        This method is used to fetch and parse the timezone and comparison hours info
        :param comparison_text: comparison_text as str like Hours are shown in this clinic's local time (America/Los_Angeles), which is 12 hours 30 minutes later than your current local time (Asia/Calcutta).
        :return:
        """
        splitted_comp_text = comparison_text.replace(')', '').split('(')
        self.log.info("Splitted Comparison text info is {}".format(splitted_comp_text))
        self.log.info({'clinic_local_timezone': splitted_comp_text[1].split(',')[0].strip(), 'timezone_diff_clinic_local': splitted_comp_text[1].split(',')[1].strip(), 'device_timezone': splitted_comp_text[2].replace('.', '').strip()})
        return {'clinic_local_timezone': splitted_comp_text[1].split(',')[0].strip(), 'timezone_diff_clinic_local': splitted_comp_text[1].split(',')[1].strip(), 'device_timezone': splitted_comp_text[2].replace('.', '').strip()}

    def provide_tz_database_time_zones(self, timezone_info):
        """
        Fetch the TZ timezone information by accepting the full timezone info. Ref URL :: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        :param timezone_info: timezone_info as string and example is Indian Standard Time
        :return: Time Zone info like Asia/Calcutta
        """
        fetched_tz_timezone = None

        if timezone_info in ('Indian Standard Time','India Standard Time', 'India Daylight Time'):
            fetched_tz_timezone = "Asia/Calcutta"

        elif timezone_info in ('Pacific Standard Time','Pacific Daylight Time', 'Pacific Time'):
            fetched_tz_timezone = "US/Pacific"

        elif timezone_info in ('Eastern Standard Time','Eastern Daylight Time', 'Eastern Time'):
            fetched_tz_timezone = "US/Eastern"

        elif timezone_info in ('Mountain Standard Time','Mountain Daylight Time', 'Mountain Time'):
            fetched_tz_timezone = "US/Mountain"

        elif timezone_info in ('Central Standard Time','Central Daylight Time', 'Central Time'):
            fetched_tz_timezone = "US/Central"

        else:
            fetched_tz_timezone = None

        return fetched_tz_timezone

    # https://stackabuse.com/how-to-get-the-current-date-and-time-in-python/
    def timezone_date_identify_compare(self, timezone1, timezone2):
        """
        Method to compare and verify whether two timezones date is equal or not
        :param timezone1: timezone1 as string .Eg America/Los_Angeles
        :param timezone2: timezone1 as string Eg Asia/Calcutta
        :return:
        """
        flag = None
        import pytz
        from datetime import datetime

        tz = datetime.now(pytz.timezone(self.provide_tz_database_time_zones(timezone1))).date()
        tz1 = datetime.now(pytz.timezone(self.provide_tz_database_time_zones(timezone2))).date()

        self.log.info("Timezone1 date is {} and Timezone2 date is {}".format(tz, tz1))
        print("Timezone1 date is {} and Timezone2 date is {}".format(tz, tz1))

        if tz == tz1:
            self.log.info("Timezone1 date - {} and Timezone2 date - {} are equal".format(tz, tz1))
            # print("Timezone1 date - {} and Timezone2 date - {} are equal".format(tz, tz1))
            flag = True
        else:
            self.log.info("Timezone1 date - {} and Timezone2 date - {} are not equal".format(tz, tz1))
            flag = False

        return flag

    def fetch_timezone_by_abbreviation(self, timezone_abbreviation):
        """
        Method to fetch the timezone using the abbreviated timezone form
        :param timezone_abbreviation: timezone_abbreviation as string .Eg IST
        :return:
        """

        timezone_info = None

        if timezone_abbreviation == "IST":
            timezone_info = "India Standard Time"

        elif timezone_abbreviation == "GST":
            # This timezone is for Dubai/Gulf Standard Time. Windows doesn't have GST listed.So AST is same as GST
            timezone_info = "Arabian Standard Time"

        elif timezone_abbreviation == "PST":
            timezone_info = "Pacific Standard Time"

        elif timezone_abbreviation == "Hawaii":
            timezone_info = "Hawaiian Standard Time"

        elif timezone_abbreviation == "Alaska":
            timezone_info = "Alaskan Standard Time"

        elif timezone_abbreviation == "MST":
            timezone_info = "Mountain Standard Time"

        elif timezone_abbreviation == "CST":
            timezone_info = "Central Standard Time"

        elif timezone_abbreviation == "EST":
            timezone_info = "Eastern Standard Time"

        elif timezone_abbreviation == "WAST":
            timezone_info = "W. Australia Standard Time"

        elif timezone_abbreviation == "CAST":
            timezone_info = "Cen. Australia Standard Time"

        elif timezone_abbreviation == "ACST":
            timezone_info = "AUS Central Standard Time"

        else:
            # Setting to default timezone of India
            timezone_info = "India Standard Time"

        return timezone_info

    def fetch_timezone_by_expanded_form(self, timezone_retrieved):
        """Method to fetch the timezone abbreviation by giving the expaned form """

        timezone_abbreviation = None

        if timezone_retrieved in ('India Standard Time', 'India Daylight Time'):
            timezone_abbreviation = 'IST'

        elif timezone_retrieved in ('Arabian Standard Time', 'Arabian Daylight Time'):
            timezone_abbreviation = 'GST'

        elif timezone_retrieved in ('Pacific Standard Time', 'Pacific Daylight Time'):
            timezone_abbreviation = 'PST'

        elif timezone_retrieved in ('Hawaiian Standard Time', 'Hawaiian Daylight Time'):
            timezone_abbreviation = 'Hawaii'

        elif timezone_retrieved in ('Alaskan Standard Time', 'Alaskan Daylight Time'):
            timezone_abbreviation = 'Alaska'

        elif timezone_retrieved in ('Mountain Standard Time', 'Mountain Daylight Time'):
            timezone_abbreviation = 'MST'

        elif timezone_retrieved in ('Central Standard Time', 'Central Daylight Time'):
            timezone_abbreviation = 'CST'

        elif timezone_retrieved in ('Eastern Standard Time', 'Eastern Daylight Time'):
            timezone_abbreviation = 'EST'

        elif timezone_retrieved in ('W. Australia Standard Time', 'W. Australia Daylight Time'):
            timezone_abbreviation = 'WAST'

        elif timezone_retrieved in ('Cen. Australia Standard Time', 'Cen. Australia Daylight Time'):
            timezone_abbreviation = 'CAST'

        elif timezone_retrieved in ('AUS Central Standard Time', 'AUS Central Daylight Time'):
            timezone_abbreviation = 'ACST'

        else:
            timezone_abbreviation = None

        return timezone_abbreviation

    def identify_provide_day(self,day_count):
        """
        Get the days in integer and identify the day for appointment booking
        :param day_count: day_count in int
        :return: for today => Today, tomorrow => Tomorrow and further days => Thursday,Monday, etc
        """
        day_identified = None

        fetched_date_day = (datetime.date.today() + datetime.timedelta(days=day_count)).strftime("%b %d")
        today_info_fetched = datetime.date.today()

        if fetched_date_day == datetime.date.today().strftime("%b %d"):
            if today_info_fetched.strftime("%A") not in ('Sunday', 'Saturday'):
                self.log.info("Current Day is Today")
                day_identified = "Today"
            else:
                self.log.info("Current Day is {} and hence not taken into consideration".format(today_info_fetched.strftime("%A")))

                if datetime.date.today().strftime("%A") == "Saturday":
                    self.log.info("Day to be passed is {}".format("Monday"))
                    day_identified = "Monday"
                else:
                    self.log.info("Day to be passed is {}".format("Tomorrow"))
                    day_identified = "Tomorrow"

        if fetched_date_day != datetime.date.today().strftime("%b %d"):
            self.log.info("Current Day is {} and given day is {}".format(today_info_fetched.strftime("%A"), fetched_date_day))
            diff = (datetime.date.today() + datetime.timedelta(days=day_count)) - datetime.date.today()
            self.log.info("Day difference is {}".format(diff.days))

            if diff.days == 1 and today_info_fetched.strftime("%A") not in ('Sunday', 'Saturday'):
                self.log.info("Tomorrow")
                day_identified = "Tomorrow"

            elif diff.days == 1 and today_info_fetched.strftime("%A") == "Saturday":
                self.log.info("Monday")
                day_identified = "Monday"

            elif diff.days == 1 and today_info_fetched.strftime("%A") == "Sunday":
                self.log.info("Tomorrow")
                day_identified = "Tomorrow"

            else:
                if (datetime.date.today() + datetime.timedelta(days=day_count)).strftime("%A") == "Saturday":
                    self.log.info("Day to be passed is {}".format("Monday"))
                    day_identified = "Monday"

                elif (datetime.date.today() + datetime.timedelta(days=day_count)).strftime("%A") == "Sunday":
                    self.log.info("Day to be passed is {}".format("Tomorrow"))
                    day_identified = "Tomorrow"
                else:
                    day_to_be_passed = (datetime.date.today() + datetime.timedelta(days=day_count)).strftime("%A")
                    self.log.info("Day to be passed is {}".format(day_to_be_passed))
                    day_identified = day_to_be_passed

        return day_identified

    def timezone_date_identify_compare_v2(self, country):
        """
        Method to compare and verify whether two timezones date is equal or not
        :param country: country as string .Eg USA
        :return: Date list
        """
        import pytz
        from datetime import datetime
        date_collector = []

        if country == "USA":
            for tz in ["US/Pacific", "US/Eastern", "US/Mountain", "US/Central"]:
                date_collector.append(datetime.now(pytz.timezone(tz)).date().strftime("%b %d"))

        self.log.info("Available date for the {} Country is {}".format(country, date_collector))

        return date_collector

    # def validate_other_clinic_timeslot_info_format(self, time_slot, hospital_name, hour_min_info, mile_info, actual_string):
    def validate_other_clinic_timeslot_info_format(self, hospital_name, actual_string):
        """
        This method is used to validate the text present(08:00 AM at Irvine General Hosptal 5 mins (1.6 mi) away.)
        :param time_slot: time_slot as str like 08:00 AM | 17:00 AM
        :param hospital_name: hospital_name as str
        :param hour_min_info: hour_min_info as str like 0 mins/ 1 hour 30 mins
        :param mile_info: mile_info as str like 1.6/9 mi
        :return: True | False
        """
        str_format = re.compile(r'(^[0-2]?\d|1[0-2]):[0-5]\d\s*(?:AM|PM)\s+at\s+{}\s+((?:\d+\s+hour).*|(?:\d+\s+mins)\s+{}{})'.format(hospital_name,"/\([0-9]{1,11}(?:\.[0-9]{1,3})?\s+mi\)/\s+","away."), re.M | re.I)
        return bool(str_format.match(actual_string))

# b = BaseHelpers()
# print(b.generate_random_integer())
# print(b.identify_space_in_sentence("972-535-1111"))
# print(b.timezone_date_identify_compare_v2("USA"))
# print(b.validate_other_clinic_timeslot_info_format("Irvine General Hosptal","17:00 PM at Irvine General Hosptal 5 mins (1.6 mi) away."))

# print(b.identify_provide_day(day_count=2))