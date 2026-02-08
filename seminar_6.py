# Семинар 6

# Задача 5
# Начало программы
# Создание массива из 25 элементов со значением элементов [0, 10]
# 
# Выводим массив в строку 
# 
# Создаем новый словарь
# Создаём счётчики количества оценок marks и количества хороших оценок good_marks
# Начало перебора значений элементов (num) по массиву
#   Если num нет в словаре, то:
#       Добавляем в словарь число num с счетиком количества значений этого элемента (cou), равное 1
#   Иначе:
#       прибавляем к cou этого num нового словаря 1
#   Если num >=6:
#       прибавляет к good_marks 1
#   прибавляем к marks 1
#
# Конец цикла
# 
# По ключам ищем максимальное значение счётчика оценок в словаре
# Выводим ключ максимального счетчика словаря
# Выводим целое(good_marks/marks*100)
# Конец программы

import random

arr = [random.randint(0, 10) for _ in range(25)]

print("Массив оценок:", ' '.join(map(str, arr)))

freq_dict = {}
marks = 0
good_marks = 0

for num in arr:
    if num not in freq_dict:
        freq_dict[num] = 1
    else:
        freq_dict[num] += 1
    
    if num >= 6:
        good_marks += 1
    marks += 1

max_value = 0
max_key = None
for key, value in freq_dict.items():
    if value > max_value:
        max_value = value
        max_key = key

print(f"Наиболее частая оценка: {max_key} (встречается {max_value} раз)")

if marks > 0:
    percentage = int(good_marks / marks * 100)
    print(f"Процент удовлетворительных оценок (>=6): {percentage}%")
else:
    print("Массив пуст")



    
# Задача 3
# Начало программы 
# Генерация массива из 10 случайных мизел диапазоне [1,50】
# Вывести массив
# создания пустого нового массива
# Начало цикла с перебором значения от 0 до 9
#   Если оно четное 
#      умножаем его на 2 и добавляем в новый список
#   Иначе 
#      делим 1 на 2 и добавляем в новый список
# Конец цикла
# Вывести этот массив
# Конец программы
# Конец программы

import random

arr = [random.randint(1, 50) for _ in range(10)]
print("Исходный массив:", arr)

new_arr = []
for i in range(10):
    if arr[i] % 2 == 0:
        new_arr.append(arr[i] * 2)
    else:
        new_arr.append(arr[i] // 2)

print("Новый массив:", new_arr)
