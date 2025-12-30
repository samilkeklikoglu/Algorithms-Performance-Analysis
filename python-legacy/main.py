import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import sys
import tracemalloc  # Bellek ölçümü için Python'un yerleşik kütüphanesi

# --- SENİN MODÜLLERİN ---
import algorithms
import data_generator

# Recursion limit ayarı
sys.setrecursionlimit(200000)

# --- TEMA AYARLARI ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ProSortingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("AlgoAnalyze Ultimate - Sorting Performance Suite")
        self.geometry("1200x800")

        # Layout: Sol Sidebar + Sağ Ana Alan
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        # --- SOL MENÜ ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        # Başlık
        title_lbl = ctk.CTkLabel(self.sidebar, text="🚀 AlgoAnalyze", font=ctk.CTkFont(size=24, weight="bold"))
        title_lbl.grid(row=0, column=0, padx=20, pady=(30, 20))

        # 1. Veri Boyutu
        ctk.CTkLabel(self.sidebar, text="Veri Boyutu (N):", anchor="w").grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.size_entry = ctk.CTkEntry(self.sidebar, placeholder_text="1000")
        self.size_entry.insert(0, "1000")
        self.size_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # 2. Veri Tipi
        ctk.CTkLabel(self.sidebar, text="Veri Karakteristiği:", anchor="w").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.type_menu = ctk.CTkOptionMenu(self.sidebar, values=["Random", "Partially Sorted", "Reverse"])
        self.type_menu.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Çalıştır Butonu
        self.btn_run = ctk.CTkButton(self.sidebar, text="ANALİZİ BAŞLAT", fg_color="#E74C3C", hover_color="#C0392B", height=40, font=("Arial", 14, "bold"), command=self.start_thread)
        self.btn_run.grid(row=5, column=0, padx=20, pady=20)

        # Durum Çubuğu
        self.status_lbl = ctk.CTkLabel(self.sidebar, text="Durum: Hazır", text_color="gray")
        self.status_lbl.grid(row=6, column=0, padx=20, pady=10)

    def create_main_area(self):
        # --- SAĞ ANA EKRAN (TAB YAPISI) ---
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        # Sekmeler
        self.tab_dashboard = self.tabs.add("📈 Grafikler (Dashboard)")
        self.tab_table = self.tabs.add("📋 Karşılaştırma Tablosu")
        self.tab_logs = self.tabs.add("📝 Detaylı Loglar")

        # --- SEKME 1: DASHBOARD (Çift Grafik) ---
        self.setup_dashboard()

        # --- SEKME 2: TABLO ---
        self.setup_table()

        # --- SEKME 3: LOGLAR ---
        self.log_box = ctk.CTkTextbox(self.tab_logs, font=("Consolas", 13))
        self.log_box.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_dashboard(self):
        # Matplotlib ile 2 grafik yan yana (Time vs Memory)
        self.chart_frame = ctk.CTkFrame(self.tab_dashboard)
        self.chart_frame.pack(fill="both", expand=True)

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
        self.fig.patch.set_facecolor('#242424') # Arka plan rengi
        
        # Grafik 1: Zaman
        self.ax1.set_facecolor('#2b2b2b')
        self.ax1.set_title("Zaman Karmaşıklığı (Saniye)", color='white', fontsize=10)
        self.ax1.tick_params(colors='white', labelsize=8)
        self.ax1.spines['bottom'].set_color('white'); self.ax1.spines['left'].set_color('white')
        self.ax1.spines['top'].set_color('none'); self.ax1.spines['right'].set_color('none')

        # Grafik 2: Bellek
        self.ax2.set_facecolor('#2b2b2b')
        self.ax2.set_title("Bellek Kullanımı (Peak KB)", color='white', fontsize=10)
        self.ax2.tick_params(colors='white', labelsize=8)
        self.ax2.spines['bottom'].set_color('white'); self.ax2.spines['left'].set_color('white')
        self.ax2.spines['top'].set_color('none'); self.ax2.spines['right'].set_color('none')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def setup_table(self):
        # Tablo Başlıkları
        headers = ["Algoritma", "Süre (sn)", "Bellek (KB)", "Durum"]
        self.table_frame = ctk.CTkFrame(self.tab_table)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Grid sistemi ile tablo başlıklarını oluştur
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=text, font=("Arial", 16, "bold"), fg_color="#333", corner_radius=5)
            lbl.grid(row=0, column=col, sticky="ew", padx=2, pady=5, ipady=5)
            self.table_frame.grid_columnconfigure(col, weight=1)

        # Satırları dinamik ekleyeceğiz, şimdilik boş tutuyoruz
        self.table_rows = []

    def start_thread(self):
        self.btn_run.configure(state="disabled")
        self.status_lbl.configure(text="Durum: Analiz Yapılıyor...")
        self.log_box.delete("1.0", "end")
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        try:
            size = int(self.size_entry.get())
            dtype = self.type_menu.get()
        except:
            self.log_box.insert("end", "HATA: Geçersiz sayı girişi!\n")
            self.reset_ui()
            return

        self.log_box.insert("end", f"PARAMETRELER: N={size}, Tip={dtype}\n{'-'*50}\n")
        
        # Veri Üretimi
        try:
            self.log_box.insert("end", "Veri seti oluşturuluyor... ")
            original_data = data_generator.generate_data(size, dtype)
            self.log_box.insert("end", "TAMAMLANDI.\n\n")
        except Exception as e:
            self.log_box.insert("end", f"HATA: {e}\n")
            self.reset_ui()
            return

        # Algoritmalar
        algos = [
            ("Quick Sort", algorithms.quick_sort),
            ("Heap Sort", algorithms.heap_sort),
            ("Shell Sort", algorithms.shell_sort),
            ("Merge Sort", algorithms.merge_sort),
            ("Radix Sort", algorithms.radix_sort)
        ]

        time_results = {}
        memory_results = {}
        table_data = []

        for name, func in algos:
            arr_copy = original_data.copy()
            
            # --- ÖLÇÜM BAŞLANGICI ---
            tracemalloc.start() # Bellek takibini başlat
            start_time = time.time()
            
            error_msg = None
            try:
                func(arr_copy) # Algoritmayı çalıştır
            except Exception as e:
                error_msg = str(e)
            
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory() # Kullanılan belleği al
            tracemalloc.stop() # Bellek takibini durdur
            # --- ÖLÇÜM BİTİŞİ ---

            elapsed = end_time - start_time
            peak_kb = peak / 1024 # Byte'ı KB'a çevir

            if error_msg:
                self.log_box.insert("end", f"{name}: HATA -> {error_msg}\n")
                time_results[name] = 0
                memory_results[name] = 0
                table_data.append((name, "-", "-", "HATA"))
            else:
                self.log_box.insert("end", f"{name:12} | Süre: {elapsed:.5f}s | Bellek: {peak_kb:.2f} KB\n")
                time_results[name] = elapsed
                memory_results[name] = peak_kb
                table_data.append((name, f"{elapsed:.5f}", f"{peak_kb:.2f}", "BAŞARILI"))
            
            self.log_box.see("end")

        # Sonuçları Görselleştir
        self.update_dashboard(time_results, memory_results)
        self.update_table_view(table_data)
        
        self.log_box.insert("end", f"\n{'-'*50}\nTest Başarıyla Tamamlandı.")
        self.reset_ui()

    def update_dashboard(self, time_data, mem_data):
        # Grafik güncelleme ana thread'de olmalı
        self.after(0, lambda: self._draw_graphs(time_data, mem_data))

    def _draw_graphs(self, time_data, mem_data):
        names = list(time_data.keys())
        times = list(time_data.values())
        mems = list(mem_data.values())

        # Renk Paletleri
        colors_time = ['#3498db', '#3498db', '#3498db', '#3498db', '#3498db']
        colors_mem = ['#9b59b6', '#9b59b6', '#9b59b6', '#9b59b6', '#9b59b6']

        # 1. Zaman Grafiği Temizle ve Çiz
        self.ax1.clear()
        self.ax1.bar(names, times, color=colors_time, alpha=0.8)
        self.ax1.set_title("Zaman Karmaşıklığı (Daha az = Daha iyi)", color='white', pad=10)
        self.ax1.tick_params(axis='x', rotation=20, colors='white')
        
        # 2. Bellek Grafiği Temizle ve Çiz
        self.ax2.clear()
        self.ax2.bar(names, mems, color=colors_mem, alpha=0.8)
        self.ax2.set_title("Bellek Tüketimi (Daha az = Daha iyi)", color='white', pad=10)
        self.ax2.tick_params(axis='x', rotation=20, colors='white')

        self.fig.tight_layout()
        self.canvas.draw()

    def update_table_view(self, data):
        self.after(0, lambda: self._draw_table(data))

    def _draw_table(self, data):
        # Eski satırları temizle (başlık hariç)
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        # Yeni verileri ekle
        for i, row_data in enumerate(data):
            # Renklendirme (Alternatif satır)
            bg_color = "#2b2b2b" if i % 2 == 0 else "#3a3a3a"
            
            ctk.CTkLabel(self.table_frame, text=row_data[0], fg_color=bg_color).grid(row=i+1, column=0, sticky="ew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text=row_data[1], fg_color=bg_color).grid(row=i+1, column=1, sticky="ew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text=row_data[2], fg_color=bg_color).grid(row=i+1, column=2, sticky="ew", padx=2, pady=2)
            
            status_color = "#2ecc71" if row_data[3] == "BAŞARILI" else "#e74c3c"
            ctk.CTkLabel(self.table_frame, text=row_data[3], fg_color=bg_color, text_color=status_color).grid(row=i+1, column=3, sticky="ew", padx=2, pady=2)

    def reset_ui(self):
        self.after(0, lambda: self._enable_button())

    def _enable_button(self):
        self.btn_run.configure(state="normal")
        self.status_lbl.configure(text="Durum: Tamamlandı")

if __name__ == "__main__":
    app = ProSortingApp()
    app.mainloop()
