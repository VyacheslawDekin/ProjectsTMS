#1
number = input("Введите число: ")
try:
    number = float(number)
    if number == 0:
        print("Число равно нулю")
    elif number > 0:
        print("Число положительное")
    else:
        print("Число отрицательное")
except ValueError:
    print("Введите число!")

#2 Подсчитывает только количество БУКВ>
string = input("Введите строку для вывода в таблицу: ")
set_str = {_ for _ in string if _.isalpha()}
max_len = 0
list_couples = []
for _ in set_str:
    len_str = string.count(_)
    max_len = max(len(str(len_str)), max_len)
    list_couples.append((_, len_str))

for letter, count in list_couples:
    print(f'| {letter} | {count:<{max_len}} |')
    print(max_len)