from selenium import webdriver
import time

driver = webdriver.Chrome()


def test_registration():
    driver.get("http://localhost:1667/#/")

    try:
        sign_up = driver.find_element_by_xpath("//a[@href='#/register']")
        sign_up.click()

        green_button = driver.find_element_by_xpath("//button[@class='btn btn-lg btn-primary pull-xs-right']")
        green_button.click()
        time.sleep(1.0)

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Registration failed!"
        driver.find_element_by_xpath("//button[@class='swal-button swal-button--confirm']").click()

        username = driver.find_element_by_xpath("//input[@placeholder='Username']")
        mail = driver.find_element_by_xpath("//input[@placeholder='Email']")
        password = driver.find_element_by_xpath("//input[@placeholder='Password']")

        def type_and_check(t, p, c):
            assert t.get_attribute("placeholder") == p
            t.send_keys(c)

        type_and_check(username, "Username", "robert07134")
        type_and_check(mail, "Email", "rob@freemail.hu")
        type_and_check(password, "Password", "Aaaa11111")

        assert sign_up.text == driver.find_element_by_xpath("//h1[@class='text-xs-center']").text == green_button.text
        green_button.click()
        time.sleep(3.0)

        assert driver.find_element_by_xpath("//div[@class='swal-text']").text == "Your registration was successful!"
        driver.find_element_by_xpath("//button[@class='swal-button swal-button--confirm']").click()

        assert driver.find_element_by_xpath("//a[@href='#/@robert07134/']").text == "robert07134"

    finally:
        time.sleep(1.0)
        driver.close()
