import time
from selenium import webdriver
## ---- Use for type hint ---- ##
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
## --------------------------- ##
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


AMAZON_US_URL = 'https://amazon.com'
AMAZON_CUSTOMER_REVIEWS_URL_FORMAT = 'https://www.amazon.com/product-reviews/{product_id}?sortBy={sort_by}&pageNumber={page_number}&filterByStar={review_type}'

def create_firefox_web_driver_conection() -> WebDriver:
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options= firefox_options)
    return driver

def open_url(driver, url: str):
    driver.get(url)

def close_driver_conection(driver):
    driver.close()


def search_product_amazon(driver: WebDriver, product_name: str):
    try:
        search_bar_input = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
            )
    except TimeoutException as e:
        print(' #####  searching with the fallback option  #####')
        search_bar_input = search_product_amazon_fallback(driver, product_name)

    search_bar_input.send_keys(product_name + Keys.ENTER)


def search_product_amazon_fallback(driver: WebDriver, product_name: str) -> WebElement:
    try:
        search_bar_input = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//form[@name="site-search"]//input'))
            )
        
        return search_bar_input

    except TimeoutException as e:
        raise e



def get_amazon_choice_product_id(driver: WebDriver) -> str | None:
    try:
        amazon_choice = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[id$="amazons-choice-label"]'))
            )
    except TimeoutException:
        return get_firts_amazon_display_poroduct_id(driver= driver)

    product_id = amazon_choice.get_attribute('id').split('-')[0]

    return product_id


def get_firts_amazon_display_poroduct_id(driver: WebDriver) -> str | None:
    try:
        element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"][1]'))
            )
    except TimeoutException:
        return None

    product_id = element.get_attribute('data-asin')

    return product_id


def get_amazon_product_reviews_url(product_id:str,
                                   review_type:str,
                                   sort_by:str = 'recent',
                                   page_number:int = 1,
                                   reviews_url_format:str = AMAZON_CUSTOMER_REVIEWS_URL_FORMAT
                                   ) -> str:

    return reviews_url_format.format(product_id= product_id,
                                     sort_by= sort_by,
                                     page_number= page_number,
                                     review_type= review_type
                                     )


def get_product_comments(driver: WebDriver, reviews_url: str) -> list[str] | None:

    driver.get(reviews_url)
    try:
        span_tags = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, '//span[\
                                                contains(@class, "a-size-base")\
                                                 and contains(@class, "review-text")\
                                                 and contains(@class, "review-text-content")]\
                                                //span'
                                                )
                                            )
            )
    except TimeoutException:
        return None

    comments = []
    for span_tag in span_tags:
        comments.append(span_tag.text)

    return comments


def get_amazon_product_url_by_id(product_id: str) -> str:
    return f'https://amazon.com/dp/{product_id}/'


if __name__ == '__main__':
    
    driver = create_firefox_web_driver_conection()

    busca = input('search: ')


    open_url(driver, AMAZON_US_URL)
    search_product_amazon(driver, busca)
    product_id = get_amazon_choice_product_id(driver)
    product_url = get_amazon_product_url_by_id(product_id)

    print(product_id)

    review_url = get_amazon_product_reviews_url(product_id= product_id, review_type= 'positive')
    coments = get_product_comments(driver, review_url)


    review_url_2 = get_amazon_product_reviews_url(product_id= product_id, review_type= 'critical')
    coments_critical = get_product_comments(driver, review_url_2)

    print(product_url)
    # print(len(coments), " - ", len(coments_critical))

    cnt = 0
    for c in coments:
        if len(c)==0:
            cnt+= 1
        
        print(c)

    print(cnt)
    print('\n ########################################## \n')

    for c in coments_critical:
        print(c)

    driver.quit()