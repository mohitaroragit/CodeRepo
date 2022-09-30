def f(k):
    var =k ** 2
    return g(k + 1) + var
def g(k):
    var = k + 1
    return var + 1
print(f(3))