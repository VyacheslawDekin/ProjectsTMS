import math

#Программа будет работать только если вводить положительные значения чисел. Все остальное соответсвует условиям задачи


def execute_operation(number1, number2, operator):
    number1 = string_in_number(number1)
    number2 = string_in_number(number2)

    if number1 is None or number2 is None:
        return None
    try:
        if operator == "+":
            return number1 + number2
        elif operator == "-":
            return number1 - number2
        elif operator == "/":
            return number1 / number2
        elif operator == "*":
            return number1 * number2
        elif operator == "-/":
            return math.sqrt(number1)
        elif operator == "^":
            return math.pow(number1, number2)
        elif operator == "!":
            return math.factorial(int(number1))

    except ZeroDivisionError:
        print("Деление на ноль")
        return None
    except:
        print("Неверное выражение")
        return None


def string_in_number(string):
    try:
        if string == "pi":
            return math.pi
        elif string == "e":
            return math.e
        else:
            return float(string)
    except:
        print("Для вычисления необходимо ввести числовые значения")
        return None


operation_symbols = ["+", "-", "*", "/", "^", "!"]

# 3 + 5
res = 0
while True:
    input_string = input("Введите выражение: ")
    input_string = input_string.replace(" ", "")

    operations_in_string = [x for x in input_string if x in operation_symbols]
    # если был корень -/, то найден - и /. Поэтому проверка на два оператора или ни одного.
    if len(operations_in_string) == 0 or len(operations_in_string) > 2:
        print("Неверное выражение")
        continue

    it_sqrt = len(operations_in_string) == 2 and "-" in operations_in_string and "/" in operations_in_string
    if len(operations_in_string) == 2 and not it_sqrt:
        print("Неверное выражение")
        continue

    operator = "".join(operations_in_string)
    if it_sqrt:
        number_string = "".join([x for x in input_string if x.isdigit()])
        result = execute_operation(number_string, 0, operator)
        if not (result is None):
            res = result
            print(result)
        continue

    # вычисление факториала
    if operator == "!":
        number_string = "".join([x for x in input_string if x.isdigit()])
        result = execute_operation(number_string, 0, operator)
        if not (result is None):
            res = result
            print(result)
        continue

    numbers = [x for x in input_string.split(operator) if
               x != ""]  # формируем список чисел и удаляем пустые строки, если оператор стоял в начале или конце
    if len(numbers) != 2:
        print("Необходимо ввести только 2 числа")
        continue

    list_numbers = [res if x == "res" else x for x in numbers]
    result = execute_operation(*list_numbers, operator)
    if not result is None:
        res = result
        print(result)
