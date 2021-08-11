from selenium import webdriver
import time
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_adatmodositas_torles():
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

        settings = driver.find_element_by_xpath("//a[@href='#/settings']")
        displayed(settings)
        settings.click()
        time.sleep(0.5)

        user_name = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[2]/input")
        bio = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[3]/textarea")
        upd_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset/button")

        type_and_check(user_name, "Your username", "robert0123")
        type_and_check(bio, "Short bio about you", "Hard work, pays off")

        displayed(upd_button)
        check_and_click("update_butt", "/html/body/div[1]/div/div/div/div/form/fieldset/button", "Update Settings")

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Update successful!"
        check_and_click("confirm", "//button[@class='swal-button swal-button--confirm']", "OK")

        check_and_click("my_page", "//a[@href='#/@robert0123/']", "robert0123")

        assert driver.find_element_by_xpath("//a[@href='#/@robert0123/']").text == driver.find_element_by_xpath(
            "/html/body/div/div/div[1]/div/div/div/h4").text == "robert0123"
        # annak vizsgálata hogy jól lefrissült e a fejlécben és a saját cikkeknél található felhasználónév

        assert driver.find_element_by_xpath("/html/body/div/div/div[1]/div/div/div/p").text == "Hard work, pays off"
        # megjelenő bio vizsgálata
        check_and_click("edit_profile", "/html/body/div/div/div[1]/div/div/div/div/a", "Edit Profile Settings")

        assert user_name.get_attribute("value") == driver.find_element_by_xpath("//a[@href='#/@robert0123/']").text

        type_and_check(user_name, "Your username", "robert07134")
        type_and_check(bio, "Short bio about you", "")

        assert user_name.get_attribute("value") == driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text

        displayed(upd_button)
        check_and_click("update", "/html/body/div[1]/div/div/div/div/form/fieldset/button", "Update Settings")

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Update successful!"
        check_and_click("confirm", "//button[@class='swal-button swal-button--confirm']", "OK")

        check_and_click("my_page", "//a[@href='#/@robert07134/']", "robert07134")

        driver.refresh()
        # szükséges az oldalt frissíteni, különben a 2. változtatás után nem frissíti magától a saját cikkek fülön
        # található adatokat
        time.sleep(1.0)

        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == driver.find_element_by_xpath(
            "/html/body/div/div/div[1]/div/div/div/h4").text == "robert07134"

        assert driver.find_element_by_xpath("/html/body/div/div/div[1]/div/div/div/p").text == ""

    finally:
        driver.close()
