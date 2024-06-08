import requests
from allure_commons._allure import step
from selene import browser
from selene.support.conditions import have
from utils import attach

API_URL = "https://demowebshop.tricentis.com/addproducttocart"
CART_URL = "https://demowebshop.tricentis.com/cart"


def test_add_one_product_to_cart():
    url = API_URL + "/details/72/1"
    Quantity = 55

    payload = {
        "product_attribute_72_5_18": 53,
        "product_attribute_72_6_19": 54,
        "product_attribute_72_3_20": 57,
        "addtocart_72.EnteredQuantity": Quantity
    }

    with step("Шаг добавления товара метод POST API"):
        response = requests.post(url=url, data=payload)
        attach.request_url_and_body(response)
        attach.response_json_and_cookies(response)
        attach.logging_response(response)

    with step("Получаем cookie"):
        cookie = response.cookies.get("Nop.customer")

    with step("Устанавливаем cookie"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("Проверяем корзину в UI"):
        attach.add_screenshot(browser)
        browser.element(".cart-qty").should(have.text(f"({Quantity})"))


def test_add_two_products_to_cart():
    books_url = API_URL + "/details/"
    id_first_book = 45
    id_second_book = 22
    Quantity_first_book = 55
    Quantity_second_book = 100

    payload_fiction = {
        f"addtocart_{id_first_book}.EnteredQuantity": Quantity_first_book
    }

    payload_health = {
        f"addtocart_{id_second_book}.EnteredQuantity": Quantity_second_book
    }

    with step("Шаг добавления первой книги метод POST API"):
        response_first_book = requests.post(url=books_url + f'{id_first_book}/1', data=payload_fiction)
        attach.request_url_and_body(response_first_book)
        attach.response_json_and_cookies(response_first_book)
        attach.logging_response(response_first_book)

    with step("Шаг добавления второй книги метод POST API"):
        response_second_book = requests.post(url=books_url + f'{id_second_book}/1', data=payload_health,
                                             cookies=response_first_book.cookies)
        attach.request_url_and_body(response_second_book)
        attach.response_json_and_cookies(response_second_book)
        attach.logging_response(response_second_book)

    with step("Получаем cookie"):
        cookie = response_second_book.cookies.get("Nop.customer")

    with step("Устанавливаем cookie"):
        browser.open(CART_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(CART_URL)

    with step("Проверяем корзину в UI"):
        attach.add_screenshot(browser)
        browser.element(".cart-qty").should(have.text(f"({Quantity_first_book + Quantity_second_book})"))
