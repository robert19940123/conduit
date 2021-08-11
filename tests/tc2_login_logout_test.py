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

        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        displayed(sign_in)
        sign_in.click()

        main_window = driver.window_handles[0]
        driver.execute_script("window.open('', 'newwin', 'height=800, width=1200')")
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        driver.get("http://localhost:1667/#/")

        sign_up = driver.find_element_by_xpath("//a[@href='#/register']")
        displayed(sign_up)
        sign_up.click()

        username = driver.find_element_by_xpath("//input[@placeholder='Username']")
        mail = driver.find_element_by_xpath("//input[@placeholder='Email']")
        password = driver.find_element_by_xpath("//input[@placeholder='Password']")

        type_and_check(username, "Username", "robert07134")
        type_and_check(mail, "Email", random_email_address())
        type_and_check(password, "Password", "Aaaa11111")

        green_button = driver.find_element_by_xpath("//button[@class='btn btn-lg btn-primary pull-xs-right']")
        assert sign_up.text == driver.find_element_by_xpath(
            "//h1[@class='text-xs-center']").text == green_button.text == "Sign up"
        green_button.click()
        time.sleep(3.0)

        assert driver.find_element_by_xpath("//div[@class='swal-text']").text == "Your registration was successful!"
        check_and_click("confirm", "//button[@class='swal-button swal-button--confirm']", "OK")

        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == "robert07134"

        settings = driver.find_element_by_xpath("//a[@href='#/settings']")
        displayed(settings)
        settings.click()
        time.sleep(0.5)

        my_random_email = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[4]/input").get_attribute("value")

        driver.switch_to.window(main_window)

        sign_in_button = driver.find_element_by_xpath(
            "/html/body/div/div/div/div/div/form/button")
        sign_in_button.click()
        time.sleep(1.0)

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Login failed!"
        check_and_click("confirm", "//button[@class='swal-button swal-button--confirm']", "OK")

        sign_in_mail = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset[1]/input")
        sign_in_password = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset[2]/input")

        type_and_check(sign_in_mail, "Email", my_random_email)
        type_and_check(sign_in_password, "Password", "Aaaa11111")

        assert sign_in.text == driver.find_element_by_xpath("//h1[@class='text-xs-center']").text == sign_in_button.text
        sign_in_button.click()
        time.sleep(3.0)

        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == "robert07134"

        log_out = driver.find_element_by_xpath("/html/body/div[1]/nav/div/ul/li[5]/a")
        displayed(log_out)
        log_out.click()
        time.sleep(1.0)

        displayed(sign_in)

    finally:
        driver.quit()
