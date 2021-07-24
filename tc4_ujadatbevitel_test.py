from selenium import webdriver
import time

driver = webdriver.Chrome()


def test_ujadatbevitel():
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
        art_button.click()
        time.sleep(0.5)

        comment = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/form/div[1]/textarea")
        comment_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/form/div[2]/button")

        type_and_check(comment, "Write a comment...", "Already outdated!")

        displayed(comment_button)
        comment_button.click()
        time.sleep(0.5)

        trash = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div[2]/span[2]/i")
        displayed(trash)
        trash.click()
        time.sleep(0.5)

    finally:
        driver.close()
