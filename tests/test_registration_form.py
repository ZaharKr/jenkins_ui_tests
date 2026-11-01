import allure

from pages.registration_page import RegistrationPage


@allure.title("Successful fill form")
@allure.label("owner", "ZaharKr")
@allure.feature("Student Registration Form")
def test_successful(setup_browser):
    page = RegistrationPage(setup_browser)
    first_name = "Alex"
    last_name = "Egorov"

    with allure.step("Open registration form"):
        page.open()

    with allure.step("Fill form"):
        page.fill_first_name(first_name)
        page.fill_last_name(last_name)
        page.fill_email("alex@egorov.com")
        page.select_gender_other()
        page.fill_mobile("1231231230")
        page.fill_subjects("Maths")
        page.select_hobby_sports()
        page.fill_current_address("Some street 1")
        page.select_state("NCR")
        page.select_city("Delhi")
        page.submit()

    with allure.step("Check form results"):
        page.should_have_submitted()
        page.should_have_result(f"{first_name} {last_name}")
        page.should_have_result("alex@egorov.com")
        page.should_have_result("Other")
        page.should_have_result("1231231230")
        page.should_have_result("Maths")
        page.should_have_result("Sports")
        page.should_have_result("Some street 1")
        page.should_have_result("NCR Delhi")
