from selenium import webdriver
import time

driver = webdriver.Chrome()


def test_login_logout():
    driver.get("http://localhost:1667/#/")

    try:

        def displayed(a):
            assert a.is_displayed()

        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        displayed(sign_in)
        sign_in.click()

        green_button = driver.find_element_by_xpath("//button[@class='btn btn-lg btn-primary pull-xs-right']")
        green_button.click()
        time.sleep(1.0)

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Login failed!"
        driver.find_element_by_xpath("//button[@class='swal-button swal-button--confirm']").click()

        mail = driver.find_element_by_xpath("//input[@placeholder='Email']")
        password = driver.find_element_by_xpath("//input[@placeholder='Password']")

        def type_and_check(t, p, c):
            assert t.get_attribute("placeholder") == p
            t.send_keys(c)

        type_and_check(mail, "Email", "rob@freemail.hu")
        type_and_check(password, "Password", "Aaaa11111")

        assert sign_in.text == driver.find_element_by_xpath("//h1[@class='text-xs-center']").text == green_button.text
        green_button.click()
        time.sleep(1.0)

        log_out = driver.find_element_by_xpath("//a[@active-class='active']")
        displayed(log_out)
        log_out.click()

        displayed(sign_in)

    finally:
        driver.close()
