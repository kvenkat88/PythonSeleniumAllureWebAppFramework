class LandingSignInPageLocatorsStaticText:
    welcome_to_text = "Welcome To Clinical 360"
    signin_title_text = "Sign In"
    username_text_fld_placeholder_text = "Username"
    password_text_fld_placeholder_text = "Password"
    login_btn_text = "Sign In"
    or_text = "OR"
    sso_btn_txt = "Signin with your Organization"

class LandingSignInPageLocators:
    welcome_to_text = ('xpath', "//h6[@id='before_login_secondary_toolbar_title']/b")
    signin_title = ('id', "signin_title")
    username_text_fld = ('id', "username_input")
    password_text_fld = ('id', "password_input")
    or_text = ('xpath', "//div[@id='or_']")
    login_btn = ('id', "login_btn")
    login_btn_text = ('id', "login_btn_txt")
    sso_btn = ('xpath', "//button[@id='sso_btn']")
    sso_btn_text = ('xpath', "//button[@id='sso_btn']//h6[@id='sso_btn_txt']")