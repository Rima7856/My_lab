def hours_case(h):
    h_12 = h % 12
    if h_12 == 1:
        padej = 'час'
    elif 2 <= h_12 < 5:
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
        elif 2 <= last_cou < 5:
            padej = 'минуты'
        else:
            padej = 'минут'
    return rovno, padej
def times_of_day(h):
    if 0 <= h <= 5:
        v_s = 'ночи'
    elif 6 <= h <= 11:
        v_s = 'утра'
    elif 12 <= h <= 17:
        v_s = 'дня'
    else:
        v_s = 'вечера'
    return v_s
def err(x):
    lst = x.split()
    if len(lst) != 2:
        return True, 'Введите ровно два числа (часы и минуты) через пробел'
    err_h = not (lst[0].isdigit()) or '-' in lst[0]
    err_m = not (lst[1].isdigit()) or '-' in lst[1]
    if not err_m:
        minutes = int(lst[1])
        err_m = not (0 <= minutes <= 59)
    if not err_h:
        hours = int(lst[0])
        err_h = not (0 <= hours <= 23)
    is_err = err_m or err_h
    text = ''

    if is_err:
        text = 'Введены недопустимые данные: '
        errors = []

        if err_h:
            errors.append('часы должны быть от 0 до 23')
        if err_m:
            errors.append('минуты должны быть от 0 до 59')
        text += ', '.join(errors)

    return is_err, text
def ready_text(hours, minutes):
    if hours == 0 and minutes == 0:
        return 'полночь'
    elif hours == 12 and minutes == 0:
        return 'полдень'

    padej_h = hours_case(hours)
    rovno, padej_m = minuts_case(minutes)
    vrem_sut = times_of_day(hours)

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
