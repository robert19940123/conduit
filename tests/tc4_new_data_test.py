from selenium import webdriver
import time
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_new_data():
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
        new_article.click()
        time.sleep(0.5)

        # Fill input fields
        title = driver.find_element_by_xpath('//fieldset/input[@placeholder="Article Title"]')
        about = driver.find_element_by_xpath('//fieldset/input[@class="form-control"]')
        my_article = driver.find_element_by_xpath(
            '//fieldset/textarea[@placeholder="Write your article (in markdown)"]')
        tags = driver.find_element_by_xpath('//li/input[@placeholder="Enter tags"]')
        art_button = driver.find_element_by_xpath('//form/button[@class="btn btn-lg pull-xs-right btn-primary"]')

        type_and_check(title, "Article Title", "Random Article")
        type_and_check(about, "What's this article about?", "The Great Race to Rule Streaming TV")
        type_and_check(my_article, "Write your article (in markdown)",
                       "Three giant telecoms are gonna make and own all the content, and they’re not gonna want anyone "
                       "else to make it.")
        type_and_check(tags, "Enter tags", "riptheaters")
        time.sleep(0.5)

        displayed(art_button)
        check_and_click('//form/button[@class="btn btn-lg pull-xs-right btn-primary"]', "Publish Article")

        # Make a comment
        comment = driver.find_element_by_xpath('//div/textarea[@placeholder="Write a comment..."]')
        comment_button = driver.find_element_by_xpath('//div[@class="card-footer"]/button')

        type_and_check(comment, "Write a comment...", "Already outdated!")

        displayed(comment_button)
        check_and_click('//div[@class="card-footer"]/button', "Post Comment")

        # Delete created comment
        trash = driver.find_element_by_xpath('//span/i[@class="ion-trash-a"]')
        displayed(trash)
        trash.click()
        time.sleep(0.5)

        # Check that created comment is deleted
        assert len(driver.find_elements_by_xpath('//div[@class="card"]')) == 0

        # Edit created article
        check_and_click('//span/a[@href="#/editor/random-article"]', " Edit Article")

        my_article.clear()
        tags.clear()
        time.sleep(1.0)

        check_and_click('//form/button[@class="btn btn-lg pull-xs-right btn-primary"]', "Publish Article")

        # Delete created article
        check_and_click('//span/button[@class="btn btn-outline-danger btn-sm"]', " Delete Article")

        # Alert message appears (error when deleting article), accept it
        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Oops!"
        check_and_click("//button[@class='swal-button swal-button--confirm']", "OK")

        check_and_click("//a[@href='#/@robert07134/']", "robert07134")

        # Check number of articles
        number_of_art(11)

    finally:
        driver.close()
