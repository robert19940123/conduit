from selenium import webdriver
import time

driver = webdriver.Chrome()


def test_adatkezeles():
    driver.get("http://localhost:1667/#/")

    try:

        def displayed(a):
            assert a.is_displayed()

        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        displayed(sign_in)
        sign_in.click()

        mail = driver.find_element_by_xpath("//input[@placeholder='Email']")
        password = driver.find_element_by_xpath("//input[@placeholder='Password']")

        def type_and_check(t, p, c):
            assert t.get_attribute("placeholder") == p
            t.send_keys(c)

        type_and_check(mail, "Email", "rob@freemail.hu")
        type_and_check(password, "Password", "Aaaa11111")

        green_button = driver.find_element_by_xpath("//button[@class='btn btn-lg btn-primary pull-xs-right']")
        assert sign_in.text == driver.find_element_by_xpath("//h1[@class='text-xs-center']").text == green_button.text
        green_button.click()
        time.sleep(1.0)

        driver.find_element_by_xpath("//a[@href='https://cookiesandyou.com/']").click()
        time.sleep(3.0)

        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1.0)

        driver.find_element_by_xpath(
            "//button[@class='cookie__bar__buttons__button cookie__bar__buttons__button--accept']").click()
        time.sleep(1.0)

    finally:
        driver.close()
