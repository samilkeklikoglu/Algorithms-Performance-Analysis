import tkinter as tk
from tkinter import ttk, messagebox
from data_generator import create_dataset
from performance_test import run_test
import algorithms as algos
from visualizer import plot_performance

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritma Performans Analizi [2025]") # [cite: 1]
        self.root.geometry("400x300")
        
        # UI Elemanları
        tk.Label(root, text="Veri Boyutu Seçiniz:", font=('Arial', 10, 'bold')).pack(pady=10)
        self.size_var = tk.StringVar(value="1000")
        ttk.Combobox(root, textvariable=self.size_var, values=["1000", "10000", "100000"]).pack() # [cite: 25]
        
        tk.Label(root, text="Veri Karakteristiği:", font=('Arial', 10, 'bold')).pack(pady=10)
        self.type_var = tk.StringVar(value="random")
        ttk.Combobox(root, textvariable=self.type_var, values=["random", "partially", "reverse"]).pack() # [cite: 20]
        
        tk.Button(root, text="Analizi Başlat ve Grafik Çiz", command=self.start_full_analysis, 
                  bg="green", fg="white", font=('Arial', 10, 'bold')).pack(pady=20)

    def start_full_analysis(self):
        try:
            size = int(self.size_var.get())
            mode = self.type_var.get()
            data = create_dataset(size, mode)
            
            # Analiz edilecek algoritmalar listesi [cite: 4]
            target_algos = {
                "Quick Sort": algos.quick_sort,
                "Heap Sort": algos.heap_sort,
                "Shell Sort": algos.shell_sort,
                "Merge Sort": algos.merge_sort,
                "Radix Sort": algos.radix_sort
            }
            
            time_results = {}
            for name, func in target_algos.items():
                duration, memory = run_test(func, data)
                time_results[name] = duration
                print(f"{name} bitti: {duration:.4f}s")
            
            messagebox.showinfo("Başarılı", "Analiz tamamlandı! Konsol çıktılarını kontrol edin.")
            # Not: Gerçek bir grafikte 3 farklı size için döngü kurmalısınız.
            
        except Exception as e:
            messagebox.showerror("Hata", f"Bir sorun oluştu: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()