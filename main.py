import tkinter as tk
from tkinter import messagebox
from utils import generate_data, measure_time
from algorithms import quick_sort

def run_analysis():
    try:
        size = int(entry_size.get())
        data = generate_data(size, "random")
        duration = measure_time(quick_sort, data)
        lbl_result.config(text=f"Quick Sort Süre: {duration:.4f} saniye")
    except Exception as e:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")

root = tk.Tk()
root.title("Algoritma Analizi")
root.geometry("300x200")

tk.Label(root, text="Veri Boyutu:").pack(pady=5)
entry_size = tk.Entry(root)
entry_size.pack()

tk.Button(root, text="Analizi Başlat", command=run_analysis).pack(pady=10)
lbl_result = tk.Label(root, text="")
lbl_result.pack()

root.mainloop()