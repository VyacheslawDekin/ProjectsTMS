#Генератор
def gen_geo(q):
    start = 1
    while True:
        start *= q
        yield start

gen = gen_geo(3)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))