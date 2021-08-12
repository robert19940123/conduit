from selenium import webdriver
import time
import random
import string
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_data_entry_from_data_source():
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

        # Check number of articles
        def number_of_art(y):
            element = driver.find_elements_by_xpath("//a[@class='preview-link']")
            assert len(element) == y

        number_of_art(11)

        new_article = driver.find_element_by_xpath("//a[@href='#/editor']")
        displayed(new_article)

        # Upload data from tc6_fill_in.csv
        def clear_and_fill(xp, ph):
            element = driver.find_element_by_xpath(xp)
            assert element.get_attribute("placeholder") == ph
            element.clear()
            return element

        with open("tc6_fill_in.csv", encoding="UTF-8") as csv_file:
            csv_reader = csv.reader(csv_file,
                                    delimiter='*')
            for row in csv_reader:
                new_article.click()
                time.sleep(0.5)
                clear_and_fill('//fieldset/input[@placeholder="Article Title"]',
                               "Article Title").send_keys(row[0])
                clear_and_fill('//fieldset/input[@class="form-control"]',
                               "What's this article about?").send_keys(row[1])
                clear_and_fill('//fieldset/textarea[@placeholder="Write your article (in markdown)"]',
                               "Write your article (in markdown)").send_keys(row[2])
                clear_and_fill('//li/input[@placeholder="Enter tags"]', "Enter tags").send_keys(row[3])
                check_and_click('//form/button[@class="btn btn-lg pull-xs-right btn-primary"]', "Publish Article")

        check_and_click("//a[@href='#/@robert07134/']", "robert07134")

        # Check number of articles
        number_of_art(16)

        # Delete previously uploaded data
        for x in reversed(range(16)):
            articles = driver.find_elements_by_xpath("//a[@class='preview-link']")
            articles[x].click()
            time.sleep(0.5)
            if len(driver.find_elements_by_xpath("//button[@class='btn btn-outline-danger btn-sm']")) != 0:
                driver.find_element_by_xpath("//button[@class='btn btn-outline-danger btn-sm']").click()
                time.sleep(1.0)
                assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Oops!"
                check_and_click("//button[@class='swal-button swal-button--confirm']", "OK")
            check_and_click("//a[@href='#/@robert07134/']", "robert07134")

        # Check number of articles
        number_of_art(11)

    finally:
        driver.close()
