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


def test_adatlitazas_tobboldalas_lista_bejaras():
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

        new_article = driver.find_element_by_xpath("//a[@href='#/editor']")
        displayed(new_article)
        new_article.click()
        time.sleep(0.5)

        def clear_and_fill(xp, ph):
            element = driver.find_element_by_xpath(xp)
            assert element.get_attribute("placeholder") == ph
            element.clear()
            return element

        with open("../tc6_fill_in.csv", encoding="UTF-8") as csv_file:
            csv_reader = csv.reader(csv_file,
                                    delimiter='*')
            for row in csv_reader:
                for _ in range(6):
                    new_article = driver.find_element_by_xpath("//a[@href='#/editor']")
                    new_article.click()
                    art_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/button")
                    clear_and_fill("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[1]/input",
                                   "Article Title").send_keys(row[0])
                    clear_and_fill("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[2]/input",
                                   "What's this article about?").send_keys(row[1])
                    clear_and_fill("/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[3]/textarea",
                                   "Write your article (in markdown)").send_keys(row[2])
                    clear_and_fill(
                        "/html/body/div[1]/div/div/div/div/form/fieldset/fieldset[4]/div/div/ul/li/input",
                        "Enter tags").send_keys(row[3])
                    art_button.click()

        home = driver.find_element_by_xpath("//a[@href='#/']")
        displayed(home)
        home.click()
        time.sleep(0.5)

        assert len(driver.find_element_by_xpath("//div[@class='tag-list']").text) == 0

        driver.refresh()
        time.sleep(1.0)

        assert len(driver.find_element_by_xpath("//div[@class='tag-list']").text) != 0

        all_tags = driver.find_elements_by_xpath("//div[@class='tag-list']/a")
        art_count = []
        for tag in all_tags:
            if "Bulletin of Atomic Scientists" in tag.text:
                art_count.append(tag.text)
        assert len(art_count) == 7

        driver.find_element_by_xpath('//div/a[@href="#/tag/Bulletin of Atomic Scientists"]').click()
        time.sleep(0.5)

        check_and_click("Atom", '//li/a[@href="#/tag/Bulletin%20of%20Atomic%20Scientists"]',
                        "Bulletin of Atomic Scientists")

        pages = driver.find_elements_by_xpath("//ul[@class='pagination']/li/a")
        page_count = 0
        for page in pages:
            page.click()
            page_count += 1
            time.sleep(0.5)
        assert str(page_count) == pages[-1].text

    finally:
        driver.close()
