def check_input():
    #Ввод и проверка ввода

    while True: #бесконечный цикл проверки
        userInput = input("Введите время в формате часы минуты: ").split() #запрос ввода и преобразование ввода в список
        
        if len(userInput) == 1 and (userInput[0]).lower() == "выход": #если длина списка = 1 и строчные символы строки = "выход" -> возвращаем "exit" и "exit"
            return "exit", "exit"
        
        if len(userInput) == 2: #проверка, является длина ввода двум - если нет, выводим ошибку и просим ввод заново
            hours = userInput[0]
            minutes = userInput[1]
            
            if hours.isdigit() and minutes.isdigit(): #если часы и минуты являются числами - преобразуем часы и минуты в int значение
                hours = int(hours) 
                minutes = int(minutes)

                checkHours = (0 <= hours < 24)
                checkMinutes = (0 <= minutes < 60)

                if checkHours and checkMinutes: #если часы и минуты находятся в допустимых значения - конец цикла проверки
                    return hours, minutes
                if not checkHours and checkMinutes: #если часы не находятся в допустимых значение - выводим ошибку и просим ввод заново
                    print("Введены недопустимые данные: часы должны быть от 0 до 23.")
                
                if checkHours and not checkMinutes:
                    print("Введены недопустимые данные: минуты должны быть от 0 до 59.") #если минуты не находятся в допустимых значениях - выводим ошибку и просим ввод заново
                
                if not checkHours and not checkMinutes:
                    print("Введены недопустимые данные: часы должны быть от 0 до 23, минуты должны быть от 0 до 59.") #если и часы и минуты не находятся в допустимых значениях - выводим ошибку и просим ввод заново
            
            else:
                print("Ошибка ввода: введите ровно два целых числа, разделенные пробелом.") #ввод не является числами или не являются положительными - выводим ошибку
        else:
            print("Ошибка ввода: введите ровно два целых числа, разделенные пробелом.") #длина ввода не равна двум - выводим ошибку


def padezh_hours(hours):
    # функция падежа для часов
    # преобразовываем часы в 12 часовой формат
    # если часы = 0 -> "часов"
    # если часы = 1, то присваем переменной "час"
    # если часы от 2 до 4, то присваем переменной "часа"
    # в остальных случаях присваем "часов"
    # возвращаем падеж
    twelve_format_hours = hours % 12
    
    padezh_h = ""
    
    if twelve_format_hours == 0:
        padezh_h = "часов"
    
    elif twelve_format_hours == 1:
        padezh_h = "час"
    
    elif 2 <= twelve_format_hours < 5:
        padezh_h = "часа"
    
    else:
        padezh_h = "часов"
    
    return padezh_h

def padezh_minutes(minutes):
    # функция падежа для минут
    # если минуты от 10 до 20 -> "минут"
    # если минуты = 0 -> "ровно"
    # в остальных случаях: выбираем последнюю минуту, если она = 1 -> "минута", если от 2 до 4 -> "минуты", в остальных случаях -> "минут"
    # возвращаем падеж
    padezh_m = ""

    if 10 <= minutes < 21:
        padezh_m = "минут"
    
    elif minutes == 0:
        padezh_m = "ровно"

    else:
        last_minute = int(str(minutes)[-1])

        if last_minute == 1:
            padezh_m = "минута"
            
        elif 2 <= last_minute < 5:
            padezh_m = "минуты"

        else:
            padezh_m = "минут"
    return padezh_m

def time_clock(hours):
    # функция определения времени суток
    # если часы от 0 до 5 -> "ночи"
    # если часы от 6 до 11 -> "утра"
    # если часы от 12 до 17 -> "дня"
    # в остальных случаях -> "вечера"
    # возвращаем время суток
    clock = ""

    if 0 <= hours < 6:
        clock = "ночи"
    
    elif 6 <= hours < 12:
        clock = "утра"

    elif 12 <= hours < 18:
        clock = "дня"

    else:
        clock = "вечера"

    return clock

def full_time_output(hours, minutes, padezh_h, padezh_m, clock):
    # функция составления итогового результата
    # смотрим особый случай: если часы != 12 -> переводим в строковый формат 12 часовой формат часов, иначе -> переводим в строковый формат просто часы
    # смотрим особые случаи: если время 00:00 -> "полночь", если время 12:00 -> "полдень"
    # в остальных случаях: если минуты = 0 -> часы + пробел + падеж часов + пробел + время суток + пробел + падеж минут, 
    # в остальных случаях -> часы + пробел + падеж часов + пробел + минуты + пробел + падеж минут + пробел + время суток
    # возвращаем итоговый результат
    time_output = ""

    hours_twelve_format = hours % 12
    
    if hours != 12:
        hours_s = str(hours_twelve_format)

    else:
        hours_s = str(hours)

    minutes_s = str(minutes)

    space = " "

    if hours == 0 and minutes == 0:
        time_output = "полночь"
    
    elif hours == 12 and minutes == 0:
        time_output = "полдень"
    
    elif minutes == 0:
        time_output = hours_s + space + padezh_h + space + clock + space + padezh_m

    else:
        time_output = hours_s + space + padezh_h + space + minutes_s + space + padezh_m + space + clock

    return time_output

   
def main():
    print("Для выхода из программы напишите 'выход'") # выводим пользователю инструкцию, как выйти из программы
    
    while True:
        hours, minutes = check_input() # проверяем ввод
        
        if (hours and minutes) == "exit": # если возврат часов и минут = "exit" -> сообщаем пользователю об выходе из программы и завершаем программу
            print("Выход из программы")
            break
        
        padezh_h = padezh_hours(hours) # определяем падеж часов
        padezh_m = padezh_minutes(minutes) # определяем падеж минут
        
        clock = time_clock(hours) # определяем время суток

        time_output = full_time_output(hours, minutes, padezh_h, padezh_m, clock) #определяем готовый результат

        print(time_output) # вывод результата


if __name__ == "__main__":
    main()
