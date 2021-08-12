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


def test_data_listing_and_multi_page():
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
                for _ in range(4):
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

        # Go to home page
        home = driver.find_element_by_xpath("//a[@href='#/']")
        displayed(home)
        home.click()
        time.sleep(0.5)

        # Check that tag list isn't visible before a refresh
        assert len(driver.find_element_by_xpath("//div[@class='tag-list']").text) == 0

        driver.refresh()
        time.sleep(2.0)

        # Check that tag list is visible now
        assert len(driver.find_element_by_xpath("//div[@class='tag-list']").text) != 0

        # Count the number of a created tag (I created 4, and 1 is stored as a "directory" for them)
        all_tags = driver.find_elements_by_xpath("//div[@class='tag-list']/a")
        art_count = []
        for tag in all_tags:
            if "Bulletin of Atomic Scientists" in tag.text:
                art_count.append(tag.text)
        assert len(art_count) == 5

        # List the articles by a specific tag (it doesn't work)
        driver.find_element_by_xpath('//div/a[@href="#/tag/Bulletin of Atomic Scientists"]').click()
        time.sleep(0.5)

        check_and_click('//li/a[@href="#/tag/Bulletin%20of%20Atomic%20Scientists"]',
                        "Bulletin of Atomic Scientists")

        # Go through the available pages and check the page counts are okay
        pages = driver.find_elements_by_xpath("//ul[@class='pagination']/li/a")
        page_count = 0
        for page in pages:
            page.click()
            page_count += 1
            time.sleep(0.5)
        assert str(page_count) == pages[-1].text

    finally:
        driver.close()
