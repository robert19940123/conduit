from selenium import webdriver
import time
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_login_logout():
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

        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        displayed(sign_in)
        sign_in.click()

        # Taking the random email address from a separate registration, in a new window

        main_window = driver.window_handles[0]
        # Switching to a new window
        driver.execute_script("window.open('', 'newwin', 'height=800, width=1200')")
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        driver.get("http://localhost:1667/#/")

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

        # Checking texts
        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == "robert07134"

        settings = driver.find_element_by_xpath("//a[@href='#/settings']")
        displayed(settings)
        settings.click()
        time.sleep(0.5)

        # Saving the random email address
        my_random_email = driver.find_element_by_xpath("//fieldset/input[@placeholder='Email']").get_attribute("value")

        # Switching back to the original window
        driver.switch_to.window(main_window)

        sign_in_button = driver.find_element_by_xpath(
            '//form/button[@class="btn btn-lg btn-primary pull-xs-right"]')
        sign_in_button.click()
        time.sleep(1.0)

        # Checking correct alert message
        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Login failed!"
        check_and_click("//button[@class='swal-button swal-button--confirm']", "OK")

        # Fill input fields
        sign_in_mail = driver.find_element_by_xpath("//fieldset/input[@placeholder='Email']")
        sign_in_password = driver.find_element_by_xpath("//fieldset/input[@placeholder='Password']")

        type_and_check(sign_in_mail, "Email", my_random_email)
        type_and_check(sign_in_password, "Password", "Aaaa11111")

        # Checking texts
        assert sign_in.text == driver.find_element_by_xpath("//h1[@class='text-xs-center']").text == sign_in_button.text
        sign_in_button.click()
        time.sleep(3.0)

        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == "robert07134"

        # Checking displayed elements
        log_out = driver.find_element_by_xpath('//li/a[@active-class="active"]')
        displayed(log_out)
        log_out.click()
        time.sleep(1.0)

        displayed(sign_in)

    finally:
        driver.quit()
