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
  
