from selenium import webdriver
import time

driver = webdriver.Chrome()


def test_adatmodositas_torles():
    driver.get("http://localhost:1667/#/")

    try:

        def check_and_click(a, b, c):
            a = driver.find_element_by_xpath(b)
            assert a.text == c
            a.click()
            time.sleep(0.5)

        def type_and_check(t, p, c):
            assert t.get_attribute("placeholder") == p
            t.send_keys(c)

        def displayed(a):
            assert a.is_displayed()

        sign_in = driver.find_element_by_xpath("//a[@href='#/login']")
        displayed(sign_in)
        sign_in.click()

        green_button = driver.find_element_by_xpath("//button[@class='btn btn-lg btn-primary pull-xs-right']")
        time.sleep(1.0)

        mail = driver.find_element_by_xpath("//input[@placeholder='Email']")
        password = driver.find_element_by_xpath("//input[@placeholder='Password']")

        type_and_check(mail, "Email", "rob@freemail.hu")
        type_and_check(password, "Password", "Aaaa11111")

        assert sign_in.text == driver.find_element_by_xpath("//h1[@class='text-xs-center']").text == green_button.text
        green_button.click()
        time.sleep(1.0)

        check_and_click("my_page", "//a[@href='#/@robert07134/']", "robert07134")

        assert driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[12]/div/div/a").text == "robert07134"
        check_and_click("my_prev_art", "/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[12]/a/h1",
                        "Random Article")

        check_and_click("edit_art", "/html/body/div[1]/div/div[1]/div/div/span/a/span", " Edit Article")

        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[3]/textarea").clear()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[2]/input").clear()
        time.sleep(1.0)

        check_and_click("art_button", "/html/body/div[1]/div/div/div/div/form/button", "Publish Article")

        check_and_click("delete_button", "/html/body/div[1]/div/div[1]/div/div/span/button/span", " Delete Article")
        time.sleep(1.0)

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Oops!"
        driver.find_element_by_xpath("//button[@class='swal-button swal-button--confirm']").click()

        check_and_click("my_page", "//a[@href='#/@robert07134/']", "robert07134")

        if len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[12]/a/h1")) == 0:
            print('Article delete function actually works!')

    finally:
        driver.close()
