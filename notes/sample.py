# decorator
def swap_dec(fn):
    def wrapper(n1,n2):
        if n1<n2:
            (n1,n2)=(n2,n1)
        return fn(n1,n2)
    return wrapper

@swap_dec
def smart_sub(n1,n2):
    return n1-n2
@swap_dec
def smart_div(n1,n2):
    return n1/n2
print(smart_sub(5,10))
print(smart_div(10,5))