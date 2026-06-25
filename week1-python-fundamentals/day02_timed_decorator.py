import time

def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return result
    return wrapper

@timed
def slow_add(a, b):
    time.sleep(1)
    return a + b  
@timed
def slow_multiply(a,b):
    time.sleep(1)
    return a * b  

print(slow_add(5, 9))
print(slow_multiply(5,9))