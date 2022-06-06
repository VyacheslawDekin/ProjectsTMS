#Генератор
def gen_geo(q):
    next_element = 1
    while True:
        next_element *= q
        yield next_element


gen = gen_geo(3)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))