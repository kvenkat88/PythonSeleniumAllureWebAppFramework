class HeaderFooterPageLocatorsStaticText:
    footer_terms_of_use_text = "Terms Of Use"
    footer_privacy_policy_text = "Privacy Policy"
    footer_cookie_policy_text = "Cookie Policy"
    help_link_text = "Help"

class HeaderFooterPageLocators:
    site_header_left_logo = ('id', "site_header_left_logo")
    footer_terms_of_use = ('id', "footer_btn_Terms of Use")
    footer_terms_of_use_text = ('xpath', "//button[@id='footer_btn_Terms of Use']/span")
    footer_privacy_policy = ('id', "footer_btn_Privacy Policy")
    footer_privacy_policy_text = ('xpath', "//button[@id='footer_btn_Privacy Policy']/span")
    footer_cookie_policy = ('id', "footer_btn_Cookie Policy")
    footer_cookie_policy_text = ('xpath', "//button[@id='footer_btn_Cookie Policy']/span")
    help_link = ('id', "footer_btn_Help")
    help_link_text = ('xpath', "//button[@id='footer_btn_Help']/span")

    # Header section after login - Common
    branding_logo_after_sign_in = ('id', "after_login_header1_left_logo_img")
    after_login_toolbar_user_name = ('xpath', "//h6[@id='after_login_header2_toolbar_user_name']/b")
    logged_in_user_icon = ('id', "logged-in-user-icon")
    after_login_header_profile_icon_spinner_btn = ('id', "after_login_header1_right_profile_iconbtn")
    after_login_header_profile_name = ('id', "after_login_header1_right_profile_name") #Andrew D. in home page after login for eg

    after_login_account_link = ('xpath', "")
    after_login_account_link_text = ('xpath', "")
    after_login_sign_out_link = ('xpath', "//li[@id='menu_item-signout-link']")
    after_login_sign_out_link_text = ('xpath', "//li[@id='menu_item-signout-link']/h6")

    # Header section after login - Physician Role
    current_time_clock = ('id', "currentTimeClock")
    after_login_header_clinic_name = ('id', "after_login_header2_toolbar_right_clinic_name")
    after_login_header_search_icon = ('id', "after_login_header1_right_search_icon")
    after_login_header_patient_search_btn_text = ('id', "after_login_header1_right_patient_search") #Patient Search text

    # Patient View Landing Screen
    after_login_header_patient_name = ('id', "after_login_header2_toolbar_patientname")
    after_login_header_patient_name_back_arrow_btn = ('id', "after_login_header2_toolbar_leftarrow_iconbtn")

