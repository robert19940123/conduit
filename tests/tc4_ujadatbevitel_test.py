from selenium import webdriver
import time
import random
import string
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def test_ujadatbevitel():
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

        check_and_click("my_page", "//a[@href='#/@robert07134/']", "robert07134")

        new_article = driver.find_element_by_xpath("//a[@href='#/editor']")
        displayed(new_article)
        new_article.click()
        time.sleep(0.5)

        title = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[1]/input")
        about = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[2]/input")
        my_article = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[3]/textarea")
        tags = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[4]/div/div/ul/li/input")
        art_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/button")

        type_and_check(title, "Article Title", "Random Article")
        type_and_check(about, "What's this article about?", "The Great Race to Rule Streaming TV")
        type_and_check(my_article, "Write your article (in markdown)",
                       "Three giant telecoms are gonna make and own all the content, and they’re not gonna want anyone "
                       "else to make it.")
        type_and_check(tags, "Enter tags", "riptheaters")
        time.sleep(0.5)

        displayed(art_button)
        check_and_click("ark_butt_push", "/html/body/div[1]/div/div/div/div/form/button", "Publish Article")

        comment = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/form/div[1]/textarea")
        comment_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/form/div[2]/button")

        type_and_check(comment, "Write a comment...", "Already outdated!")

        displayed(comment_button)
        check_and_click("comment_click", "/html/body/div[1]/div/div[2]/div[2]/div/div/form/div[2]/button",
                        "Post Comment")

        trash = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div[2]/span[2]/i")
        displayed(trash)
        trash.click()
        time.sleep(0.5)

        assert len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[2]")) == 0

        check_and_click("edit_art", "/html/body/div[1]/div/div[1]/div/div/span/a/span", " Edit Article")

        my_article.clear()
        tags.clear()
        time.sleep(1.0)

        check_and_click("art_button", "/html/body/div[1]/div/div/div/div/form/button", "Publish Article")

        check_and_click("delete_button", "/html/body/div[1]/div/div[1]/div/div/span/button/span", " Delete Article")

        assert driver.find_element_by_xpath("//div[@class='swal-title']").text == "Oops!"
        check_and_click("confirm", "//button[@class='swal-button swal-button--confirm']", "OK")

        check_and_click("my_page", "//a[@href='#/@robert07134/']", "robert07134")

        assert len(
            driver.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div[12]/a/h1")) == 0

    finally:
        driver.close()
