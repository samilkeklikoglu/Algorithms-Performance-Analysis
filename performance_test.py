import time
import tracemalloc
from data_generator import create_dataset

def run_test(algorithm_func, data):
    # Bellek ölçümünü başlat [cite: 17]
    tracemalloc.start()
    
    # Zaman ölçümünü başlat [cite: 13]
    start_time = time.perf_counter()
    
    # Algoritmayı çalıştır (Verinin kopyasını gönderiyoruz ki orijinali bozulmasın)
    algorithm_func(data.copy())
    
    end_time = time.perf_counter()
    
    # Bellek kullanım verilerini al
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    duration = end_time - start_time
    memory_mb = peak / (1024 * 1024) # Byte'ı MB'a çevir
    
    return duration, memory_mb