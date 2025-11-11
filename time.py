def hours_case(h):
    h = h % 12
    if h == 1:
        padej = 'час'
    elif 2 <= h < 5:
        padej = 'часа'
    else:
        padej = 'часов'
    return padej
def minuts_case(m):
    rovno = m == 0
    if 5 <= m <= 20:
        padej = 'минут'
    else:
        last_cou = m % 10
        if last_cou == 1:
            padej = 'минута'
        elif last_cou == 0:
            padej = 'минут'
        elif last_cou < 5:
            padej = 'минуты'
        else:
            padej = 'минут'
    return rovno, padej
def times_of_day(h):
    if h == 0:
        return '12', 'ночи'
    elif 1 <= h <= 5:
        time, v_s = str(h), 'ночи'
    elif 6 <= h <= 11:
        time, v_s = str(h), 'утра'
    elif 12 == h:
        time, v_s = str(h), 'дня'
    elif 13 <= h <= 17:
        time, v_s = str(h % 12) , 'дня'
    else:
        time, v_s = str(h % 12) , 'вечера'
    return time, v_s
def err(x):
    lst = x.split()
    if len(lst) != 2:
        return True, 'Введите ровно два числа (часы и минуты) через пробел'
    err_h = not (lst[0].isdigit())
    err_m = not (lst[1].isdigit())
    if not err_m:
        minutes = int(lst[1])
        err_m = not (0 <= minutes <= 59)
    if not err_h:
        hours = int(lst[0])
        err_h = not (0 <= hours <= 23)
    is_err = err_m or err_h
    text = ''

    if is_err:
        input_h_err = 'часы должны быть от 0 до 23'
        input_m_err = 'минуты должны быть от 0 до 59'
        text = 'Введены недопустимые данные: '
        if err_h and err_m:
            text += f'{input_h_err}, {input_m_err}'
        elif err_m:
            text += input_m_err
        else:
            text += input_h_err

    return is_err, text
def ready_text(hours, minutes):
    padej_h = hours_case(hours)
    rovno, padej_m = minuts_case(minutes)
    new_hours, vrem_sut = times_of_day(hours)

    if hours == 0 and minutes == 0:
        return 'полночь'
    elif hours == 12 and minutes == 0:
        return 'полдень'
    if rovno:
        return f'{new_hours} {padej_h} {vrem_sut} ровно'
    else:
        return f'{new_hours} {padej_h} {minutes} {padej_m} {vrem_sut}'
def main():
    print('Введите время в формате: "часы минуты"')
    print()
    input_time = input('Ваше время: ')
    err_status, text = err(input_time)
    while err_status:
        print(text)
        print('Введите повторно время в формате: "часы минуты"')
        print()
        input_time = input('Ваше время: ')
        err_status, text = err(input_time)
    hours, minutes = map(int, input_time.split())
    print(ready_text(hours, minutes))

if __name__ == '__main__':
    main()
# Вот сводка по colorama https://pythonru.com/biblioteki/tsvetnoj-vyvod-teksta-v-python-colorama