# Функция обработки ошибок
# Если введенного тарифа нет в списке, вывести "Неверный тариф"
# Проверка на натуральные числа в цене
# Выодим текст ошибки и код ошибки (есть ошибка или нет)

# Функция выдачи сдачи
# Вычитаем из суммы денег, которую ввёл пользователь, цену тарифа
# Делим нацело это число на 10 - число 10-рублевых монет
# Получаем остаток от 10 для этого числа
# Делим нацело на 5, полученное число - число 5-рублевых монет
# Получаем остаток от 5 для этого числа
# Делим нацело на 2, полученное число - число 2-рублевых монет
# Получаем остаток от 2 для этого числа
# Полученнное число - число 1-рублевых монет

# Вывести информацию для пользователя
# Ввод данных пользователя (тариф. затем цена)
# Проверка на корректность входных данных --> функция обработки ошибок
# Если денег не хватает на тариф:
# Вывести "Недостаточно средств для оплаты выбранного тарифа".
# Если денег хватает на тариф:
# Рассчитать сдачу --> функция выдачи сдачи
# Вывести сообщение: "Оплачен тариф '[тариф]'. Ваша сдача: A по 10 руб., B по 5 руб., C по 2 руб., D по 1 руб."


tarifs = ['1 час', '2 часа', '5 часов']
pricese_for_tarifs = [60, 110, 250]


def errors(tarif, price):
    if tarif not in tarifs:
        return True, 'Неверный тариф'
    if not price.isdigit() or '-' in price:
        return True, 'Ошибка в цене (напишите целое число)'
    return False, ''


def change(price, tarif_price):  # change - сдача на английском
    this_change = price - tarif_price
    ten_change = this_change // 10
    this_change %= 10
    five_change = this_change // 5
    this_change %= 5
    two_change = this_change // 2
    this_change %= 2
    one_change = this_change
    return ten_change, five_change, two_change, one_change


tarif = input("Введите тариф (1 час, 2 часа, 5 часов): ").strip()
price = input("Введите целое число — сумму денег, которую Вы вносите в купюроприемник: ")

has_error, error_text = errors(tarif, price)

if has_error:
    print(error_text)
else:
    price = int(price)
    tarif_price = pricese_for_tarifs[tarifs.index(tarif)]

    if tarif_price > price:
        print('Недостаточно средств для оплаты выбранного тарифа')

    else:
        ten_change, five_change, two_change, one_change = change(price, tarif_price)
        print(f"Оплачен тариф '{tarif}'. Ваша сдача: {ten_change} по 10 руб., {five_change} по 5 руб., {two_change} по 2 руб., {one_change} по 1 руб.")
