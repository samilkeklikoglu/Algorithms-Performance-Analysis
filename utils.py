import random
import time

def generate_data(size, data_type="random"):
    if data_type == "random":
        return [random.randint(0, size * 10) for _ in range(size)]
    elif data_type == "reverse":
        return list(range(size, 0, -1))
    elif data_type == "partially":
        data = list(range(size))
        for _ in range(size // 10): # %10'unu karıştır
            idx1, idx2 = random.randint(0, size-1), random.randint(0, size-1)
            data[idx1], data[idx2] = data[idx2], data[idx1]
        return data

def measure_time(func, data):
    start = time.perf_counter()
    func(data.copy())
    return time.perf_counter() - start