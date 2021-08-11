from selenium import webdriver
import time
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_registration():
    driver.get("http://localhost:1667/#/")

    try:

        def check_and_click(a, b, c):
            a = driver.find_element_by_xpath(b)
            assert a.text == c
            a.click()
            time.sleep(1.0)

        def displayed(a):
            assert a.is_displayed()

        def type_and_check(t, p, c):
            t.clear()
            assert t.get_attribute("placeholder") == p
            t.send_keys(c)

        def random_email_address(domain='gmail.com'):
            random_data = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            return random_data + '@' + domain

        sign_up = driver.find_element_by_xpath("//a[@href='#/register']")
        displayed(sign_up)
        sign_up.click()

        green_button = driver.find_element_by_xpath("//button[@class='btn btn-lg btn-primary pull-xs-right']")
        green_button.click()
        time.sleep(1.0)

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Registration failed!"
        check_and_click("confirm", "//button[@class='swal-button swal-button--confirm']", "OK")

        username = driver.find_element_by_xpath("//input[@placeholder='Username']")
        mail = driver.find_element_by_xpath("//input[@placeholder='Email']")
        password = driver.find_element_by_xpath("//input[@placeholder='Password']")

        type_and_check(username, "Username", "robert07134")
        type_and_check(mail, "Email", random_email_address())
        type_and_check(password, "Password", "Aaaa11111")

        assert sign_up.text == driver.find_element_by_xpath(
            "//h1[@class='text-xs-center']").text == green_button.text == "Sign up"
        green_button.click()
        time.sleep(3.0)

        assert driver.find_element_by_xpath("//div[@class='swal-text']").text == "Your registration was successful!"
        check_and_click("confirm", "//button[@class='swal-button swal-button--confirm']", "OK")

        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == "robert07134"

    finally:
        driver.close()
