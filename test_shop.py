"""
Протестируйте классы из модуля homework/models.py
"""
import random

import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product2():
    return Product("notebook", 1000, "This is a notebook", 100)


@pytest.fixture
def cart(product):
    return Cart()


count_add_product = random.randint(10, 20)
count_add_product2 = random.randint(10, 20)
count_remove_product = random.randint(1, 10)
count_remove_product2 = random.randint(1, 10)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(product.quantity - 1)
        assert product.check_quantity(product.quantity)
        assert not product.check_quantity(product.quantity + 1)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        initial_quantity = product.quantity
        count_product = random.randint(0, 100)
        product.buy(count_product)
        assert product.quantity == initial_quantity - count_product, (f"Количество товара должно уменьшиться на "
                                                                      f"{count_product}")

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match=f"Недостаточно {product.name} на складе"):
            product.buy(random.randint(product.quantity + 1, product.quantity + 100))


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        cart.add_product(product, count_add_product)
        assert cart.products[product] == count_add_product, "Неожидаемое количество товаров в корзине"

    def test_add_multiple_products(self, cart, product, product2):
        cart.add_product(product, count_add_product)
        cart.add_product(product2, count_add_product2)
        assert cart.products[product] == count_add_product, "Неожидаемое количество товаров в корзине"
        assert cart.products[product2] == count_add_product2, "Неожидаемое количество товаров в корзине"

    def test_remove_product(self, cart, product):
        expected_result = count_add_product - count_remove_product
        cart.add_product(product, count_add_product)
        cart.remove_product(product, count_remove_product)
        assert cart.products[product] == expected_result

    def test_remove_multiple_products(self, cart, product, product2):
        expected_result_product = count_add_product - count_remove_product

        cart.add_product(product, count_add_product)
        cart.add_product(product2, count_add_product2)
        cart.remove_product(product, count_remove_product)
        cart.remove_product(product2, count_add_product2)
        assert cart.products[product] == expected_result_product
        assert product2 not in cart.products

    def test_remove_product_more_than_available(self, cart, product):
        cart.add_product(product, count_add_product)
        cart.remove_product(product, count_add_product + 1)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, count_add_product)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product, product2):
        cart.add_product(product, count_add_product)
        expected_result = count_add_product * product.price
        assert cart.get_total_price() == expected_result

        cart.add_product(product2, count_add_product2)
        expected_result += count_add_product2 * product2.price
        assert cart.get_total_price() == expected_result

    def test_buy_successful(self, cart, product):
        expected_result = product.quantity - count_add_product

        cart.add_product(product, count_add_product)
        cart.buy()
        assert len(cart.products) == 0
        assert product.quantity == expected_result

    def test_buy_insufficient_stock(self, cart, product):
        value_product = product.quantity + count_add_product
        cart.add_product(product, value_product)
        with pytest.raises(ValueError, match=f"Недостаточно товара '{product.name}' на складе для покупки "
                                             f"{value_product} единиц."):
            cart.buy()
