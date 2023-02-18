global a
a = 1
 
def test():
    global a
    #a = 3
    b = 2
 
    return a + b
 
 
print(test())
print(a)