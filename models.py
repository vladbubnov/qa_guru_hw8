from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return self.quantity >= quantity

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        # raise NotImplementedError
        if self.check_quantity(quantity):
            self.quantity -= quantity
        else:
            raise ValueError(f"Недостаточно {self.name} на складе")

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        # raise NotImplementedError
        if product in self.products:
            # Если продукт уже есть в корзине, увеличиваем количество
            self.products[product] += buy_count
        else:
            # Если продукта нет в корзине, добавляем его с указанным количеством
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products:
            if remove_count is None or remove_count >= self.products[product]:
                del self.products[product]
            else:
                self.products[product] -= remove_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        total_price = 0.0
        for product, quantity in self.products.items():
            total_price += product.price * quantity
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError(f"Недостаточно товара '{product.name}' на складе для покупки {quantity} единиц.")

        # Если все товары доступны, уменьшаем количество на складе
        for product, quantity in self.products.items():
            product.buy(quantity)

        # Очищаем корзину после успешной покупки
        self.products.clear()
