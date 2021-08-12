from selenium import webdriver
import time
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_data_modify_delete():
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

        settings = driver.find_element_by_xpath("//a[@href='#/settings']")
        displayed(settings)
        settings.click()
        time.sleep(0.5)

        # Edit profile
        user_name = driver.find_element_by_xpath('//fieldset/input[@placeholder="Your username"]')
        bio = driver.find_element_by_xpath('//fieldset/textarea[@placeholder="Short bio about you"]')
        upd_button = driver.find_element_by_xpath('//fieldset/button[@class="btn btn-lg btn-primary pull-xs-right"]')

        type_and_check(user_name, "Your username", "robert0123")
        type_and_check(bio, "Short bio about you", "Hard work, pays off")

        displayed(upd_button)
        check_and_click('//fieldset/button[@class="btn btn-lg btn-primary pull-xs-right"]', "Update Settings")

        # Checking correct alert message
        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Update successful!"
        check_and_click("//button[@class='swal-button swal-button--confirm']", "OK")

        check_and_click("//a[@href='#/@robert0123/']", "robert0123")

        # Checking texts
        assert driver.find_element_by_xpath("//a[@href='#/@robert0123/']").text == driver.find_element_by_xpath(
            '//div[@class="col-xs-12 col-md-10 offset-md-1"]/h4').text == "robert0123"

        assert driver.find_element_by_xpath(
            '//div[@class="col-xs-12 col-md-10 offset-md-1"]/p').text == "Hard work, pays off"

        check_and_click('//div/a[@href="#/settings"]', "Edit Profile Settings")

        assert user_name.get_attribute("value") == driver.find_element_by_xpath("//a[@href='#/@robert0123/']").text

        # Edit profile
        type_and_check(user_name, "Your username", "robert07134")
        type_and_check(bio, "Short bio about you", "Changed again")

        # Checking texts
        assert user_name.get_attribute("value") == driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text

        displayed(upd_button)
        check_and_click('//fieldset/button[@class="btn btn-lg btn-primary pull-xs-right"]', "Update Settings")

        # Checking correct alert message
        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Update successful!"
        check_and_click("//button[@class='swal-button swal-button--confirm']", "OK")

        check_and_click("//a[@href='#/@robert07134/']", "robert07134")

        # Refresh required to show the changes
        driver.refresh()
        time.sleep(2.0)

        # Checking texts
        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == driver.find_element_by_xpath(
            '//div[@class="col-xs-12 col-md-10 offset-md-1"]/h4').text == "robert07134"

        # Changes in "bio" don't show correctly, even after a refresh
        assert driver.find_element_by_xpath('//div[@class="col-xs-12 col-md-10 offset-md-1"]/p').text != "Changed again"

    finally:
        driver.close()
