from selenium import webdriver
import time
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_cookie_management():
    driver.get("http://localhost:1667/#/")

    try:

        def check_and_click(b, c):
            element = driver.find_element_by_xpath(b)
            assert element.text == c
            element.click()
            time.sleep(1.0)

        def displayed(a):
            assert a.is_displayed()

        def type_and_check(t, p, c):
            t.clear()
            assert t.get_attribute("placeholder") == p
            t.send_keys(c)

        # random email address generator
        def random_email_address(domain='gmail.com'):
            random_data = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            return random_data + '@' + domain

        sign_up = driver.find_element_by_xpath("//a[@href='#/register']")
        displayed(sign_up)
        sign_up.click()

        # Fill input fields
        username = driver.find_element_by_xpath("//input[@placeholder='Username']")
        mail = driver.find_element_by_xpath("//input[@placeholder='Email']")
        password = driver.find_element_by_xpath("//input[@placeholder='Password']")

        type_and_check(username, "Username", "robert07134")
        type_and_check(mail, "Email", random_email_address())
        type_and_check(password, "Password", "Aaaa11111")

        # Checking texts
        green_button = driver.find_element_by_xpath("//button[@class='btn btn-lg btn-primary pull-xs-right']")
        assert sign_up.text == driver.find_element_by_xpath(
            "//h1[@class='text-xs-center']").text == green_button.text == "Sign up"
        green_button.click()
        time.sleep(3.0)

        # Checking correct alert message
        assert driver.find_element_by_xpath("//div[@class='swal-text']").text == "Your registration was successful!"
        check_and_click("//button[@class='swal-button swal-button--confirm']", "OK")

        check_and_click("//a[@href='#/@robert07134/']", "robert07134")

        # Go to the cookie website
        check_and_click("//a[@href='https://cookiesandyou.com/']", "Learn More...")

        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1.0)

        # Check that the given cookie doesn't exist
        assert driver.get_cookie("vue-cookie-accept-decline-cookie-policy-panel") is None

        # Accept the cookie
        ok_button = driver.find_element_by_xpath(
            "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--accept']")
        displayed(ok_button)
        check_and_click("//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--accept']",
                        "I accept!")

        # Check that the given cookie exist
        assert driver.get_cookie("vue-cookie-accept-decline-cookie-policy-panel") is not None

    finally:
        driver.close()
