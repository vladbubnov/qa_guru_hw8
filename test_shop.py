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
def cart(product):
    return Cart()


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
        count_product = random.randint(1, 10)
        cart.add_product(product, count_product)
        assert cart.products[product] == count_product, "Неожидаемое количество товаров в корзине"

    def test_remove_product(self, cart, product):
        count_add_product = random.randint(10, 20)
        count_remove_product = random.randint(1, 10)
        expected_result = count_add_product - count_remove_product

        cart.add_product(product, count_add_product)
        cart.remove_product(product, count_remove_product)
        assert cart.products[product] == expected_result

    @pytest.mark.parametrize("count_add_product, count_remove_product", [
        random.randint(10, 20)
    ])
    def test_remove_product_entirely_and_more_than_available(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_product_more_than_available(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 10)
        assert product not in cart.products
