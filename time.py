def what_padej_hs(h):
    h = h % 12
    if h == 1:
        padej = 'час'
    elif 2 <= h < 5:
        padej = 'часа'
    else:
        padej = 'часов'
    return padej
def what_padej_ms(m):
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
def what_vrem_sut(h):
    if h == 0:
        return 12, 'ночи'
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
def main_fk(x):
    err_status, text = err(x)
    if err_status:
        return text
    hours, minutes = map(int, x.split())

    padej_h = what_padej_hs(hours)
    rovno, padej_m = what_padej_ms(minutes)
    new_hours, vrem_sut = what_vrem_sut(hours)

    if hours == 0 and minutes == 0:
        return 'полночь'
    elif hours == 12 and minutes ==0:
        return 'полдень'
    if rovno:
        return f'{new_hours} {padej_h} {vrem_sut} ровно'
    else:
        return f'{new_hours} {padej_h} {minutes} {padej_m} {vrem_sut}'

print(main_fk(input()))