# Задача 2
#
# Функция: Сортировка выбором
# Получение списка A из n элементов
# Для i от 0 до n-2:
#     min_index <= i
#     Для j от i+1 до n-1:
#         Если A[j] < A[min_index]:
#             min_index <= j
#     Если min_index ≠ i:
#         Поменять местами A[i] и A[min_index]
#         Выводим на экран состояние массива
#         Увеличить счётчик перестановок
#     Увеличивать счётчик сравнений при каждом сравнении
# Вывод списка
#
#
#
# Создание списока из 7 случайных целых чисел в диапазоне от 50 до 500 (ежедневные расходы в условных единицах)
# Выводим сгенерированный список с сообщением: Сгенерирован список расходов: список
# Сортируем этот список по убыванию методом сортировки простым выбором --- функция сортировки простым выбором

# Выводим окончательный отсортированный массив


import random

def selection_sort_desc(a):
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        max_index = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] > a[max_index]:
                max_index = j
        if max_index != i:
            a[i], a[max_index] = a[max_index], a[i]
            swaps += 1
            print(a)
    # print(a)

expenses = [random.randint(50, 500) for _ in range(7)]
print("Сгенерирован список расходов:", expenses)
selection_sort_desc(expenses)
print(expenses, 'конечный список')


# Задача 1
#
# Функция: Сортировка пузырьком
# Получение списка A из n элементов
# Для i от 0 до n-2:
#     swapped <= ЛОЖЬ
#     Для j от 0 до n-2-i:
#         Если A[j] > A[j+1]:
#             Поменять местами A[j] и A[j+1]
#             swapped <= ИСТИНА
#             Увеличить счётчик перестановок
#         Выводим на экран состояние массива
#         Увеличить счётчик сравнений
#     Если swapped = ЛОЖЬ:
#         Прервать цикл (список уже отсортирован)
# Вывод списка
# Запрашиваем у пользователя количество участников `n`, а затем `n` целых чисел (их баллы)
# Сортируем полученный список по убыванию методом сортировки пузырьком --- функция сортировки пузырьком

# Выводим окончательный отсортированный массив и первые три элемента, если участников не менее трех


def bubble_sort_desc(a):
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if a[j] < a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
            print(a)
        if not swapped:
            break
    return a

n = int(input())
scores = [int(input()) for _ in range(n)]
bubble_sort_desc(scores)
print(scores, 'конечный список')
if n >= 3:
    print(scores[0], scores[1], scores[2])