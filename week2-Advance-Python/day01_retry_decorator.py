import time
import random
def retry(func):
    def wrapper(*args, **kwargs):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                if attempt == max_attempts - 1:
                    raise
                time.sleep(1)
    return wrapper


@retry
def flaky_function():
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success!"

result = flaky_function()
print(f"Final result: {result}")