class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price == other.price

    def __repr__(self):
        return f"{self.name}: {self.price} руб."

products = [
    Product("Кофе", 350),
    Product("Чай", 150),
    Product("Печенье", 150),
    Product("Шоколад", 200),
]

products.sort()
print('Отсортированный список:')
print(*products, sep='\n')

has_duplicates = False
for i in range(len(products) - 1):
    if products[i] == products[i+1]:
        print(f"Одинаковая цена: {products[i]} и {products[i+1]}")
        has_duplicates = True

if not has_duplicates:
    print("Одинаковой цены нет.")
