# 1. Функция: Сортировка выбором
# Получение списка A из n элементов
# Для i от 0 до n-2:
#     min_index <= i
#     Для j от i+1 до n-1:
#         Если A[j] < A[min_index]:
#             min_index <= j
#     Если min_index ≠ i:
#         Поменять местами A[i] и A[min_index]
#         Увеличить счётчик перестановок
#     Увеличивать счётчик сравнений при каждом сравнении
# Вывод списка



# 2. Функция: Сортировка пузырьком
# Получение списка A из n элементов
# Для i от 0 до n-2:
#     swapped <= ЛОЖЬ
#     Для j от 0 до n-2-i:
#         Если A[j] > A[j+1]:
#             Поменять местами A[j] и A[j+1]
#             swapped <= ИСТИНА
#             Увеличить счётчик перестановок
#         Увеличить счётчик сравнений
#     Если swapped = ЛОЖЬ:
#         Прервать цикл (список уже отсортирован)
# Вывод списка


# 3. Функция: Дополнительный метод — сортировка вставками
# Получение списка A из n элементов
# Для i от 1 до n-1:
#     key - A[i]
#     j <= i - 1
#     Пока j ≥ 0 и A[j] > key:
#         A[j+1] <= A[j]
#         j <= j - 1
#         Увеличить счётчик сравнений
#         Увеличить счётчик перестановок
#     A[j+1] <= key
# Вывод списка

# Главная программа
# НАЧАЛО
#
# Вывести:
#     "Выберите режим работы:"
#     "1 — Демонстративный"
#     "2 — Интерактивный"
#
# Ввести mode

# Демонстративный режим
# ЕСЛИ mode = 1 ТО
#     Задать размер списка n (например, n = 10)
#     Создать список A из n случайных чисел от 0 до 99
#
#     Вывести "Исходный список:"
#     Вывести A
#
#     Скопировать A в A1
#     Вызвать сортировку выбором для A1
#     Вывести отсортированный список и количество сравнений и перестановок
#
#     Скопировать A в A2
#     Вызвать сортировку пузырьком для A2
#     Вывести отсортированный список и количество сравнений и перестановок
#
#     Скопировать A в A3
#     Вызвать сортировку вставками для A3
#     Вывести отсортированный массив и количество сравнений и перестановок
# КОНЕЦ ЕСЛИ

# Интерактивный режим
# ЕСЛИ mode = 2 ТО
#     Ввести размер список n
#     Создать список A
#
#     Вывести:
#         "1 — Ввести список вручную"
#         "2 — Заполнить список случайными числами"
#
#     Ввести choice
#
#     ЕСЛИ choice = 1 ТО
#         Для i от 0 до n-1:
#             Ввести A[i]
#     ИНАЧЕ
#         Заполнить A случайными числами от 0 до 99
#     КОНЕЦ ЕСЛИ

# Меню действий (интерактивный режим)
# ПОКА
# ИСТИНА:
# Вывести:
# "Выберите действие:"
# "1 — Вывести массив"
# "2 — Сортировка выбором"
# "3 — Сортировка пузырьком"
# "4 — Сортировка вставками"
# "5 — Изменить массив (полностью или часть)"
# "0 — Выход"
#
# Ввести
# action

# Обработка действий
#         ЕСЛИ action = 1 ТО
#             Вывести A
#
#         ЕСЛИ action = 2 ТО
#             Вызвать сортировку выбором для A
#             Вывести массив и статистику
#
#         ЕСЛИ action = 3 ТО
#             Вызвать сортировку пузырьком для A
#             Вывести массив и статистику
#
#         ЕСЛИ action = 4 ТО
#             Вызвать сортировку вставками для A
#             Вывести массив и статистику
#
#         ЕСЛИ action = 5 ТО
#             Вывести:
#                 "1 — Изменить весь массив"
#                 "2 — Изменить один элемент"
#
#             Ввести edit_choice
#
#             ЕСЛИ edit_choice = 1 ТО
#                 Для i от 0 до n-1:
#                     Ввести A[i]
#
#             ЕСЛИ edit_choice = 2 ТО
#                 Ввести индекс k
#                 Ввести новое значение
#                 A[k] <= новое значение
#             КОНЕЦ ЕСЛИ
#
#         ЕСЛИ action = 0 ТО
#             ВЫХОД ИЗ ЦИКЛА
#     КОНЕЦ ПОКА
# КОНЕЦ ЕСЛИ
#
# Завершение программы
# КОНЕЦ




import random

# 1. Функция: Сортировка выбором
def selection_sort(A):
    n = len(A)
    comparisons = 0
    swaps = 0

    for i in range(0, n - 1):
        min_index = i
        for j in range(i + 1, n):
            comparisons += 1
            if A[j] < A[min_index]:
                min_index = j
        if min_index != i:
            A[i], A[min_index] = A[min_index], A[i]
            swaps += 1

    return A, comparisons, swaps


# 2. Функция: Сортировка пузырьком
def bubble_sort(A):
    n = len(A)
    comparisons = 0
    swaps = 0

    for i in range(0, n - 1):
        swapped = False
        for j in range(0, n - 1 - i):
            comparisons += 1
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return A, comparisons, swaps


# 3. Функция: Сортировка вставками
def insertion_sort(A):
    n = len(A)
    comparisons = 0
    swaps = 0

    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            comparisons += 1
            A[j + 1] = A[j]
            swaps += 1
            j -= 1
        A[j + 1] = key

    return A, comparisons, swaps


def table(s1, p1, s2, p2, s3, p3):
    # Определяем заголовки
    h_name = "Метод сортировки"
    h_comp = "Сравнения"
    h_swap = "Перестановки"
    print()
    print()

    # Рисуем шапку
    print("-" * 50)
    # Названия методов выровняем по левому краю (.ljust),
    # а числа — по правому (.rjust), чтобы они стояли ровными колонками
    print(f"{h_name.ljust(20)} | {h_comp.rjust(12)} | {h_swap.rjust(12)}")
    print("-" * 50)

    # Строки данных
    # Используем str(val).rjust(12) для выравнивания чисел
    print(f"{'Выбором'.ljust(20)} | {str(s1).rjust(12)} | {str(p1).rjust(12)}")
    print(f"{'Пузырьком'.ljust(20)} | {str(s2).rjust(12)} | {str(p2).rjust(12)}")
    print(f"{'Вставками'.ljust(20)} | {str(s3).rjust(12)} | {str(p3).rjust(12)}")

    print("-" * 50)


# Главная программа
print("Выберите режим работы:")
print("1 — Демонстративный")
print("2 — Интерактивный")

mode = int(input())

# Демонстративный режим
if mode == 1:
    n = 10
    A = [random.randint(0, 99) for _ in range(n)]

    print("Исходный список:")
    print(A)

    A1 = A.copy()
    sorted_A1, c1, s1 = selection_sort(A1)
    print("\nСортировка выбором:")
    print(sorted_A1)

    A2 = A.copy()
    sorted_A2, c2, s2 = bubble_sort(A2)
    print("\nСортировка пузырьком:")
    print(sorted_A2)

    A3 = A.copy()
    sorted_A3, c3, s3 = insertion_sort(A3)
    print("\nСортировка вставками:")
    print(sorted_A3)

    table(c1, s1, c2, s2, c3, s3)


# Интерактивный режим
elif mode == 2:
    n = int(input("Введите размер списка: "))
    A = [0] * n

    print("1 — Ввести список вручную")
    print("2 — Заполнить список случайными числами")
    choice = int(input())

    if choice == 1:
        for i in range(n):
            A[i] = int(input())
    else:
        A = [random.randint(0, 99) for _ in range(n)]

    while True:
        print("\nВыберите действие:")
        print("1 — Вывести массив")
        print("2 — Сортировка выбором")
        print("3 — Сортировка пузырьком")
        print("4 — Сортировка вставками")
        print("5 — Изменить массив")
        print("6 - Сортировка 3-мя способами")
        print("0 — Выход")

        action = int(input())

        if action == 1:
            print(A)

        elif action == 2:
            A, c, s = selection_sort(A)
            print(A)
            print("Сравнения:", c, "Перестановки:", s)

        elif action == 3:
            A, c, s = bubble_sort(A)
            print(A)
            print("Сравнения:", c, "Перестановки:", s)

        elif action == 4:
            A, c, s = insertion_sort(A)
            print(A)
            print("Сравнения:", c, "Перестановки:", s)

        elif action == 5:
            print("1 — Изменить весь массив")
            print("2 — Изменить один элемент")
            edit_choice = int(input())

            if edit_choice == 1:
                for i in range(n):
                    A[i] = int(input())
            elif edit_choice == 2:
                k = int(input("Введите индекс: "))
                value = int(input("Введите новое значение: "))
                A[k] = value


        elif action == 6:
            A1 = A.copy()
            sorted_A1, c1, s1 = selection_sort(A1)
            print("\nСортировка выбором:")
            print(sorted_A1)

            A2 = A.copy()
            sorted_A2, c2, s2 = bubble_sort(A2)
            print("\nСортировка пузырьком:")
            print(sorted_A2)

            A3 = A.copy()
            sorted_A3, c3, s3 = insertion_sort(A3)
            print("\nСортировка вставками:")
            print(sorted_A3)

            table(c1, s1, c2, s2, c3, s3)


        elif action == 0:
            break
