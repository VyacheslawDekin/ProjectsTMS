#1
(lambda x: print("Четное") if x % 2 == 0 else print("Нечетное"))(7)

#2
list1 = [1, 2, 3, 4, 5, 6, 7, 8]
print(
    list(map(lambda x: str(x), list1))
)

#3
tuple1 = ('ага', 'привет', 'done', 'fork', 'rever')
print(tuple(filter(lambda x: x == x[::-1], tuple1)))