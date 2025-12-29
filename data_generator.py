# Dosya Adı: data_generator.py
import random

def generate_data(size, data_type):
    # Temel veri: 0'dan size'a kadar sayılar
    data = list(range(size))
    
    if data_type == "Random":
        # Tamamen karıştırılmış veri
        random.shuffle(data)
        
    elif data_type == "Reverse":
        # Ters sıralı veri (Büyükten küçüğe)
        data.sort(reverse=True)
        
    elif data_type == "Partially Sorted":
        # Kısmen sıralı veri
        # Önce sırala, sonra %10'luk kısmını rastgele boz
        data.sort()
        swaps = int(size * 0.1) # %10 oranında bozulma
        for _ in range(swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            data[i], data[j] = data[j], data[i]
            
    return data
