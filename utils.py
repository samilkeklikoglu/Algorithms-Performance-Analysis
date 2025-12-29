import random
import time
import tracemalloc

def generate_data(size, data_type="random"):
    """Proje gereksinimi olan 3 farklı veri tipini üretir."""
    if data_type == "random":
        return [random.randint(0, 1000000) for _ in range(size)]
    elif data_type == "partially_sorted":
        data = sorted([random.randint(0, 1000000) for _ in range(size)])
        # Verinin küçük bir kısmını karıştırarak 'kısmen sıralı' yapıyoruz
        for _ in range(size // 20):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            data[i], data[j] = data[j], data[i]
        return data
    elif data_type == "reverse":
        return list(range(size, 0, -1))

def measure_performance(sort_func, data):
    """Zaman ve bellek kullanımını ölçer."""
    data_copy = data.copy() # Orijinal veriyi bozmamak için kopya alıyoruz
    tracemalloc.start()
    start_time = time.perf_counter()
    
    sort_func(data_copy)
    
    end_time = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Süre (saniye), Bellek (MB)
    return (end_time - start_time), (peak / (1024 * 1024))