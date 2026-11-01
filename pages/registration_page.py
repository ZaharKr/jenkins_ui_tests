import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RegistrationPage:
    URL = "https://demoqa.com/automation-practice-form"

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_OTHER = (By.XPATH, "//*[@id='genterWrapper']//*[text()='Other']")
    MOBILE = (By.ID, "userNumber")
    SUBJECTS = (By.ID, "subjectsInput")
    HOBBIES_SPORTS = (By.XPATH, "//*[@id='hobbiesWrapper']//*[text()='Sports']")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    SUBMIT_BUTTON = (By.ID, "submit")
    RESULT_TITLE = (By.CSS_SELECTOR, "#example-modal-sizes-title-lg")
    RESULT_TABLE = (By.CSS_SELECTOR, ".table-responsive")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Open url /automation-practice-form")
    def open(self):
        self.driver.get(self.URL)
        wrapper = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".practice-form-wrapper"))
        )
        assert "Student Registration Form" in wrapper.text
        self.driver.execute_script(
            "document.querySelectorAll('footer').forEach(el => el.remove())"
        )
        self.driver.execute_script("document.getElementById('fixedban')?.remove()")
        return self

    @allure.step("Fill first name field with {first_name}")
    def fill_first_name(self, first_name):
        element = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        element.clear()
        element.send_keys(first_name)
        return self

    @allure.step("Fill last name field with {last_name}")
    def fill_last_name(self, last_name):
        element = self.driver.find_element(*self.LAST_NAME)
        element.clear()
        element.send_keys(last_name)
        return self

    @allure.step("Fill email field with {email}")
    def fill_email(self, email):
        element = self.driver.find_element(*self.EMAIL)
        element.clear()
        element.send_keys(email)
        return self

    @allure.step("Select gender Other")
    def select_gender_other(self):
        element = self.wait.until(EC.element_to_be_clickable(self.GENDER_OTHER))
        self.driver.execute_script("arguments[0].click();", element)
        return self

    @allure.step("Fill mobile with {mobile}")
    def fill_mobile(self, mobile):
        element = self.driver.find_element(*self.MOBILE)
        element.clear()
        element.send_keys(mobile)
        return self

    @allure.step("Fill subjects with {subject}")
    def fill_subjects(self, subject):
        element = self.driver.find_element(*self.SUBJECTS)
        element.send_keys(subject)
        element.send_keys(Keys.ENTER)
        return self

    @allure.step("Select hobby Sports")
    def select_hobby_sports(self):
        element = self.wait.until(EC.presence_of_element_located(self.HOBBIES_SPORTS))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        clickable = self.wait.until(EC.element_to_be_clickable(self.HOBBIES_SPORTS))
        self.driver.execute_script("arguments[0].click();", clickable)
        return self

    @allure.step("Fill current address with {address}")
    def fill_current_address(self, address):
        element = self.driver.find_element(*self.CURRENT_ADDRESS)
        element.clear()
        element.send_keys(address)
        return self

    @allure.step("Select state {state}")
    def select_state(self, state):
        self.driver.find_element(*self.STATE).click()
        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[@id='stateCity-wrapper']//*[text()='{state}']")
            )
        )
        self.driver.execute_script("arguments[0].click();", option)
        return self

    @allure.step("Select city {city}")
    def select_city(self, city):
        self.driver.find_element(*self.CITY).click()
        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[@id='stateCity-wrapper']//*[text()='{city}']")
            )
        )
        self.driver.execute_script("arguments[0].click();", option)
        return self

    @allure.step("Submit form")
    def submit(self):
        button = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)
        return self

    @allure.step("Check success modal")
    def should_have_submitted(self):
        title = self.wait.until(EC.visibility_of_element_located(self.RESULT_TITLE))
        assert "Thanks for submitting the form" in title.text
        return self

    @allure.step("Check result contains {text}")
    def should_have_result(self, text):
        table = self.wait.until(EC.visibility_of_element_located(self.RESULT_TABLE))
        assert text in table.text
        return self
