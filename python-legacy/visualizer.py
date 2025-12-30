import matplotlib.pyplot as plt

def plot_performance(results_dict, test_type):
    """
    Zaman ve Bellek performansı için grafikler oluşturur.
    results_dict: {'Quick Sort': [0.1, 0.5, 1.2], ...}
    test_type: "Zaman (saniye)" veya "Bellek (MB)"
    """
    sizes = ["1.000", "10.000", "100.000"] # Önerilen test boyutları [cite: 26, 27, 28]
    
    plt.figure(figsize=(10, 6))
    for algo_name, values in results_dict.items():
        plt.plot(sizes, values, marker='o', label=algo_name)
    
    plt.title(f"Algoritma Karşılaştırması - {test_type}")
    plt.xlabel("Veri Boyutu")
    plt.ylabel(test_type)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"results_{test_type.split()[0].lower()}.png") # Grafiği kaydeder [cite: 40]
    plt.show()