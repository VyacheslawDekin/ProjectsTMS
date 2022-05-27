def check(number):
    try:
        number = float(number)
    except ValueError:
        print("Введите число!")
        return

    if number == 0:
        print("Число равно нулю")
    elif number > 0:
        print("Число положительное")
    else:
        print("Число отрицательное")


number = input("Введите число: ")
check(number)

