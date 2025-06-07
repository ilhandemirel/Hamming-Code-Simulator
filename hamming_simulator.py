# Hamming SEC-DED Kodlama Simülatörü
# Bu program, Hamming kodlamasının SEC-DED (Single Error Correction - Double Error Detection) versiyonunu simüle eder
# Veri bitlerine parity bitleri ekleyerek hata düzeltme ve tespit etme işlemlerini gerçekleştirir

import tkinter as tk
from tkinter import messagebox, font, ttk
import tkinter.font as tkfont

# --- 1. Çekirdek Mantık Sınıfı ---
# Bu sınıf Hamming kodlamasının temel mantığını içerir
# Veri bitlerini kodlar ve hataları düzeltir
class HammingSEC_DED:
    def __init__(self, d_bits):
        # d_bits: veri biti sayısı
        self.d_bits = d_bits
        # Gerekli parity bit sayısını hesapla
        self.p_bits = self._calculate_p_bits(d_bits)
        # Toplam bit sayısı = veri bitleri + parity bitleri
        self.total_bits = self.d_bits + self.p_bits

    def _calculate_p_bits(self, d):
        # Parity bit sayısını hesaplayan yardımcı fonksiyon
        # 2^p >= d + p + 1 eşitsizliğini sağlayan en küçük p değerini bulur
        p = 0
        while (2 ** p) < (d + p + 1):
            p += 1
        return p

    def encode(self, data_str):
        # Veriyi Hamming koduna dönüştürür
        # data_str: kodlanacak veri bitleri (0 ve 1'lerden oluşan string)
        if len(data_str) != self.d_bits or not all(c in '01' for c in data_str):
            raise ValueError(f"Veri {self.d_bits} bit uzunluğunda ve sadece '0' ve '1' içermelidir.")
        
        # Kodlanmış veriyi tutacak liste
        code = [None] * (self.total_bits + 1)
        data_idx = 0
        
        # Veri bitlerini yerleştir
        for i in range(1, self.total_bits + 1):
            if (i & (i - 1)) == 0:  # 2'nin kuvveti olan pozisyonlar parity bitleri için
                code[i] = '0'
            else:
                code[i] = data_str[data_idx]
                data_idx += 1
        
        # Parity bitlerini hesapla
        for p in range(self.p_bits):
            p_pos = 2 ** p
            parity = 0
            for i in range(1, self.total_bits + 1):
                if i & p_pos:
                    parity ^= int(code[i])
            code[p_pos] = str(parity)
        
        # Genel parity bitini hesapla (P0)
        overall_parity = sum(int(bit) for bit in code[1:]) % 2
        return str(overall_parity) + ''.join(code[1:])

    def check_and_correct(self, received_code_str):
        # Alınan kodu kontrol eder ve hataları düzeltir
        # received_code_str: alınan kod (0 ve 1'lerden oluşan string)
        
        # P0 bitini kontrol et
        p0_received = int(received_code_str[0])
        code = list(received_code_str[1:])
        syndrome = 0
        
        # Sendrom hesapla
        for p in range(self.p_bits):
            p_pos = 2 ** p
            parity = 0
            for i in range(1, self.total_bits + 1):
                if i & p_pos and i != p_pos:
                    parity ^= int(code[i-1])
            if parity != int(code[p_pos-1]):
                syndrome += p_pos
        
        # Gerçek P0 değerini hesapla
        p_actual = sum(int(bit) for bit in code) % 2
        
        # Hata durumlarını kontrol et
        if syndrome == 0:
            if p_actual == p0_received:
                return {"status": "Hata Yok", "error_pos": 0, "corrected_code": ''.join(code)}
            else:
                return {"status": "P0 Düzeltildi", "error_pos": -1, "corrected_code": ''.join(code)}
        else:
            if p_actual != p0_received:
                error_pos = syndrome
                if 1 <= error_pos <= len(code):
                    code[error_pos - 1] = '1' if code[error_pos - 1] == '0' else '0'
                return {"status": f"Tek Hata Düzeltildi (Bit {error_pos})", "error_pos": error_pos, "corrected_code": ''.join(code)}
            else:
                return {"status": "Çift Hata Tespit Edildi (Düzeltilemez)", "error_pos": -2, "corrected_code": ''.join(code)}

# --- 2. Klasik Görsel Arayüz Sınıfı ---
# Bu sınıf programın kullanıcı arayüzünü oluşturur
class SimulatorApp:
    def __init__(self, root):
        # Ana pencere ayarları
        self.root = root
        self.root.title("Hamming SEC-DED Simülatörü")
        self.root.geometry("1200x900")
        self.root.configure(bg="#f0f0f0")

        # Değişkenler
        self.hamming_logic = None
        self.original_encoded_code = ""
        self.corrupted_code = []
        self.bit_labels = []
        self.corrected_bit_labels = []
        self.error_indices = set()  # Hatalı bitlerin indeksleri

        # Stil ayarları
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat")
        self.style.configure("TLabel", background="#f0f0f0")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("Error.TFrame", background="#ffeeee")
        self.style.configure("Corrected.TFrame", background="#eeffee")
        self.create_widgets()

    def create_widgets(self):
        # Arayüz bileşenlerini oluşturur
        # Fontlar
        title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        subtitle_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        default_font = tkfont.Font(family="Helvetica", size=12)
        bit_font = tkfont.Font(family="Consolas", size=14, weight="bold")

        # Ana container
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill="both", expand=True)

        # Başlık
        title_label = ttk.Label(main_container, 
                              text="Hamming SEC-DED Simülatörü", 
                              font=title_font)
        title_label.pack(pady=(0, 20))

        # --- Üst Kontrol Çerçevesi ---
        control_frame = ttk.Frame(main_container)
        control_frame.pack(fill="x", pady=(0, 20))

        # Veri girişi bölümü
        input_frame = ttk.LabelFrame(control_frame, text="1. Veri Girişi", padding="10")
        input_frame.pack(fill="x", padx=5, pady=5)

        # Veri girişi alanları
        ttk.Label(input_frame, text="Veri:", font=default_font).pack(side="left", padx=5)
        self.data_entry = ttk.Entry(input_frame, width=35, font=default_font)
        self.data_entry.pack(side="left", padx=5)
        ttk.Label(input_frame, text="Bit Sayısı:", font=default_font).pack(side="left", padx=5)
        self.data_size_var = tk.StringVar(value="8")
        size_combo = ttk.Combobox(input_frame, 
                                 textvariable=self.data_size_var,
                                 values=["8", "16", "32"],
                                 state="readonly",
                                 width=5)
        size_combo.pack(side="left", padx=5)
        
        # Kodlama butonu
        self.encode_button = ttk.Button(input_frame, 
                                      text="KODLA",
                                      command=self.encode_data)
        self.encode_button.pack(side="left", padx=10)

        # Örnek veri butonları
        example_frame = ttk.Frame(input_frame)
        example_frame.pack(side="left", padx=20)
        ttk.Button(example_frame, text="8-bit örnek", 
                  command=lambda: self.set_example("10110010", "8")).pack(side="left", padx=2)
        ttk.Button(example_frame, text="16-bit örnek", 
                  command=lambda: self.set_example("1100110011001100", "16")).pack(side="left", padx=2)
        ttk.Button(example_frame, text="32-bit örnek", 
                  command=lambda: self.set_example("10101010110011001100110010101010", "32")).pack(side="left", padx=2)
        
        # Hamming rehberi butonu
        guide_btn = ttk.Button(example_frame, text="Hamming Code Nasıl Oluşur?", command=self.open_hamming_guide)
        guide_btn.pack(side="left", padx=10)

        # --- Sonuç Çerçeveleri ---
        results_frame = ttk.Frame(main_container)
        results_frame.pack(fill="both", expand=True)

        # Kodlanmış Veri gösterimi
        encoded_frame = ttk.LabelFrame(results_frame, 
                                     text="2. Kodlanmış Veri (Hata oluşturmak için bit'e tıklayın)", 
                                     padding="10")
        encoded_frame.pack(fill="x", pady=10)
        self.encoded_frame = ttk.Frame(encoded_frame)
        self.encoded_frame.pack(fill="x", padx=5, pady=5)

        # Hata Durumu gösterimi
        status_frame = ttk.LabelFrame(results_frame, 
                                    text="3. Hata Durum Analizi", 
                                    padding="10")
        status_frame.pack(fill="x", pady=10)
        self.status_label = ttk.Label(status_frame, 
                                    text="Durum: Bekleniyor...", 
                                    font=default_font,
                                    foreground="blue")
        self.status_label.pack(anchor="w", padx=5)
        self.syndrome_label = ttk.Label(status_frame, 
                                      text="Sendrom: -", 
                                      font=default_font)
        self.syndrome_label.pack(anchor="w", padx=5)

        # Düzeltilmiş Veri gösterimi
        corrected_frame = ttk.LabelFrame(results_frame, 
                                       text="4. Hata Düzeltildikten Sonraki Kod", 
                                       padding="10")
        corrected_frame.pack(fill="x", pady=10)
        self.corrected_frame = ttk.Frame(corrected_frame)
        self.corrected_frame.pack(fill="x", padx=5, pady=5)

        # Bilgi paneli
        info_frame = ttk.LabelFrame(main_container, 
                                  text="Renk Kodlaması ve Bilgiler", 
                                  padding="10")
        info_frame.pack(fill="x", pady=10)
        info_text = """• P0 (Genel Parity): Kırmızı\n• Kontrol Bitleri (P1, P2, P4, P8...): Mavi  \n• Veri Bitleri: Siyah\n• Hatalı Bit: Turuncu arka plan\n• Düzeltilen Bit: Yeşil arka plan\n\nNot: Herhangi bir bite tıklayarak hata oluşturabilirsiniz. Tek hatalar düzeltilir, çift hatalar tespit edilir."""
        info_label = ttk.Label(info_frame, 
                             text=info_text, 
                             font=default_font,
                             justify="left")
        info_label.pack(anchor="w", padx=5)

    def set_example(self, data, size):
        # Örnek veri setlerini yükler
        self.data_size_var.set(size)
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, data)

    def encode_data(self):
        # Veriyi kodlar ve arayüzde gösterir
        try:
            data_size = int(self.data_size_var.get())
            data_str = self.data_entry.get().strip()
            
            # Veri kontrolü
            if len(data_str) != data_size:
                messagebox.showerror("Hata", f"Lütfen {data_size} bit uzunluğunda veri girin.")
                return
            if not all(c in '01' for c in data_str):
                messagebox.showerror("Hata", "Veri sadece '0' ve '1' içermelidir.")
                return
            
            # Hamming kodlaması
            self.hamming_logic = HammingSEC_DED(data_size)
            self.original_encoded_code = self.hamming_logic.encode(data_str)
            self.corrupted_code = list(self.original_encoded_code)
            
            # Arayüzü güncelle
            self.display_bits(self.encoded_frame, self.corrupted_code, self.bit_labels, self.flip_bit)
            self.reset_status()
        except ValueError as e:
            messagebox.showerror("Giriş Hatası", str(e))
        except Exception as e:
            messagebox.showerror("Beklenmedik Hata", str(e))

    def display_bits(self, frame, code_list, label_list, click_handler, highlight_index=None, highlight_color=None, error_indices=None):
        # Bitleri görsel olarak gösterir
        # Eski etiketleri temizle
        for label in label_list:
            if hasattr(label, 'master'):
                label.master.destroy()
            else:
                label.destroy()
        label_list.clear()
        for widget in frame.winfo_children():
            widget.destroy()
            
        # Yeni bit container'ı oluştur
        bit_container = tk.Frame(frame, bg="#f0f0f0")
        bit_container.pack(fill="x", pady=5)
        bit_font = tkfont.Font(family="Consolas", size=14, weight="bold")
        
        # Her bit için etiket oluştur
        for i, bit in enumerate(code_list):
            # Bit tipine göre renk belirle
            is_p0 = (i == 0)
            is_parity = (i > 0) and ((i & (i - 1)) == 0)
            color = "red" if is_p0 else ("#007FFF" if is_parity else "black")
            
            # Bit frame'i oluştur
            bit_frame = tk.Frame(bit_container, bg="#f0f0f0")
            bit_frame.pack(side="left", padx=2)
            
            # Bit numarası etiketi
            num_text = "P0" if i == 0 else str(i)
            num_label = tk.Label(bit_frame, 
                                 text=num_text, 
                                 font=("Helvetica", 8),
                                 fg="gray", bg="#f0f0f0")
            num_label.pack()
            
            # Bit değeri etiketi
            bg = "#fff"
            if error_indices and i in error_indices:
                bg = "#ffe0b2"
            if highlight_index is not None and i == highlight_index:
                bg = highlight_color
                
            label = tk.Label(bit_frame, 
                             text=bit, 
                             font=bit_font,
                             fg=color,
                             bg=bg,
                             padx=8, pady=8,
                             cursor="hand2")
            label.pack()
            
            # Tıklama olayını ekle
            if click_handler:
                label.bind("<Button-1>", lambda e, index=i: click_handler(index))
            label_list.append(label)

    def flip_bit(self, index):
        # Bit değerini değiştirir ve hata kontrolü yapar
        if not self.corrupted_code:
            return
            
        # Bit değerini değiştir
        current_val = self.corrupted_code[index]
        self.corrupted_code[index] = '0' if current_val == '1' else '1'
        
        # Hata indekslerini güncelle
        if index in self.error_indices:
            self.error_indices.remove(index)
        else:
            self.error_indices.add(index)
            
        # Arayüzü güncelle
        self.display_bits(self.encoded_frame, self.corrupted_code, self.bit_labels, self.flip_bit, error_indices=self.error_indices)
        self.check_for_errors()

    def check_for_errors(self):
        # Hataları kontrol eder ve düzeltir
        code_str = "".join(self.corrupted_code)
        
        # Çift hata kontrolü
        if len(self.error_indices) >= 2:
            status_text = "❌ Çift Hata Tespit Edildi (Düzeltilemez)"
            status_color = "#d32f2f"  # kırmızı
            syndrome_text = "Sendrom: Çift hata tespit edildi"
            self.status_label.config(text=f"Durum: {status_text}", foreground=status_color)
            self.syndrome_label.config(text=syndrome_text)
            corrected_list = list(self.corrupted_code)
            self.display_bits(self.corrected_frame, corrected_list, self.corrected_bit_labels, None)
            return
            
        # Hata düzeltme
        result = self.hamming_logic.check_and_correct(code_str)
        status_text = result['status']
        
        # Durum rengini belirle
        if status_text.startswith("✅ Tek Hata Düzeltildi"):
            status_color = "#388e3c"  # yeşil
        elif status_text.startswith("❌"):
            status_color = "#d32f2f"  # kırmızı
        elif status_text.startswith("✅"):
            status_color = "#388e3c"  # yeşil
        else:
            status_color = "#1976d2"  # mavi
            
        # Arayüzü güncelle
        self.status_label.config(text=f"Durum: {status_text}", foreground=status_color)
        
        # Sendrom bilgisini güncelle
        if result['error_pos'] > 0:
            syndrome_text = f"Sendrom (Hata Pozisyonu): {result['error_pos']}"
        elif result['error_pos'] == -1:
            syndrome_text = "Sendrom: P0'da hata"
        elif result['error_pos'] == -2:
            syndrome_text = "Sendrom: Çift hata tespit edildi"
        else:
            syndrome_text = "Sendrom: Hata yok"
        self.syndrome_label.config(text=syndrome_text)
        
        # Düzeltilmiş kodu göster
        corrected_list = list(result['corrected_code'])
        highlight_index = None
        if result['error_pos'] > 0:
            highlight_index = result['error_pos']
        elif result['error_pos'] == -1:
            highlight_index = 0
        self.display_bits(self.corrected_frame, corrected_list, self.corrected_bit_labels, None, highlight_index=highlight_index, highlight_color="#b9f6ca")

    def reset_status(self):
        # Durum bilgilerini sıfırlar
        self.status_label.config(text="Durum: Kodlandı. Hata oluşturmak için bir bite tıklayın.",
                               foreground="#1976d2")
        self.syndrome_label.config(text="Sendrom: -")
        for label in self.corrected_bit_labels:
            if hasattr(label, 'master'):
                label.master.destroy()
        self.corrected_bit_labels.clear()
        self.error_indices = set()

    def open_hamming_guide(self):
        # Hamming kodlama rehberini açar
        HammingGuideWindow(self)

# --- Hamming Code Nasıl Oluşur? Penceresi ---
# Bu sınıf Hamming kodlamasının nasıl oluştuğunu adım adım gösterir
class HammingGuideWindow:
    def __init__(self, app):
        # Rehber penceresi ayarları
        self.app = app
        self.step = 0
        self.window = tk.Toplevel(app.root)
        self.window.title("Hamming Code Nasıl Oluşur?")
        self.window.geometry("880x560")
        self.window.grab_set()
        
        # Canvas ve bilgi etiketi
        self.canvas = tk.Canvas(self.window, bg="#f4f6fb")
        self.canvas.pack(fill="both", expand=True)
        self.info_label = tk.Label(self.window, text="", font=("Helvetica", 11), bg="#f4f6fb", anchor="w", justify="left")
        self.info_label.pack(fill="x", padx=20, pady=(0,10))
        
        # Kontrol butonları
        btn_frame = tk.Frame(self.window, bg="#f4f6fb")
        btn_frame.pack(pady=10)
        self.prev_btn = ttk.Button(btn_frame, text="Geri", command=self.prev_step)
        self.prev_btn.pack(side="left", padx=5)
        self.next_btn = ttk.Button(btn_frame, text="İleri", command=self.next_step)
        self.next_btn.pack(side="left", padx=5)
        self.restart_btn = ttk.Button(btn_frame, text="Baştan Başlat", command=self.restart)
        self.restart_btn.pack(side="left", padx=5)
        
        # Rehberi başlat
        self.draw_hamming_guide()

    def draw_hamming_guide(self):
        # Rehber adımlarını çizer
        self.canvas.delete("all")
        
        # 8 bitlik örnek veri
        data_bits = list("10110010")
        d = 8
        p = 0
        while 2**p < d + p + 1:
            p += 1
        total = d + p
        
        # Görsel parametreler
        x0 = 100
        y0 = 120
        box_w = 55
        box_h = 55
        bit_labels = []
        parity_positions = [2**i-1 for i in range(p)]
        
        # Başlık
        step_titles = [
            "Bitlerin Yerleşimi",
            "Parity Bitlerinin Kontrolü",
            "Genel Parity (P0) Hesabı",
            "Hamming Kodunun Son Hali"
        ]
        self.canvas.create_text(440, 50, text=step_titles[min(self.step,3)], font=("Helvetica", 18, "bold"), fill="#1976d2")
        
        # Adımları çiz
        if self.step == 0:
            # Bitlerin yerleşimi
            for i in range(total):
                if i in parity_positions:
                    label = f"P{i+1}"
                    color = "#b3e5fc"
                else:
                    label = f"D{len(bit_labels)+1}"
                    color = "#c8e6c9"
                self.canvas.create_rectangle(x0+i*box_w, y0, x0+i*box_w+box_w, y0+box_h, fill=color, outline="#0288d1", width=3)
                self.canvas.create_text(x0+i*box_w+box_w//2, y0+box_h//2, text=label, font=("Consolas", 18, "bold"))
                bit_labels.append(label)
            self.info_label.config(text="Adım 1: Parity ve veri bitlerinin yerleşimi.\nMavi kutular parity bitlerini, yeşil kutular veri bitlerini gösterir.")
            self.canvas.create_text(440, y0+box_h+30, text="Neden? Parity bitleri (P1, P2, ...) 2'nin kuvveti olan pozisyonlara yerleştirilir. Diğer pozisyonlara veri bitleri konur.", font=("Helvetica", 12), fill="#333")
            
        elif self.step <= p:
            # Parity bitlerinin kontrolü
            pi = self.step-1
            for i in range(total):
                if i == parity_positions[pi]:
                    color = "#b3e5fc"
                elif (i+1) & (2**pi):
                    color = "#ffe082"
                elif i in parity_positions:
                    color = "#b3e5fc"
                else:
                    color = "#c8e6c9"
                label = f"P{i+1}" if i in parity_positions else f"D{[j for j in range(total) if j not in parity_positions].index(i)+1}"
                self.canvas.create_rectangle(x0+i*box_w, y0, x0+i*box_w+box_w, y0+box_h, fill=color, outline="#0288d1", width=3)
                self.canvas.create_text(x0+i*box_w+box_w//2, y0+box_h//2, text=label, font=("Consolas", 18, "bold"))
            involved = [i+1 for i in range(total) if (i+1) & (2**pi)]
            form = f"P{2**pi} = " + " ⊕ ".join([f"Bit {idx}" for idx in involved])
            self.info_label.config(text=f"Adım {self.step+1}: P{2**pi} parity biti hesaplanıyor.\nSarı kutular P{2**pi}'nin kontrol ettiği bitleri gösterir.\nFormül: {form}")
            self.canvas.create_text(440, y0+box_h+30, text=f"Neden? P{2**pi} parity biti, pozisyonunda 1 olan tüm bitleri kontrol eder.", font=("Helvetica", 12), fill="#333")
            
        elif self.step == p+1:
            # Genel parity (P0) hesabı
            for i in range(total):
                color = "#b3e5fc" if i in parity_positions else "#c8e6c9"
                label = f"P{i+1}" if i in parity_positions else f"D{[j for j in range(total) if j not in parity_positions].index(i)+1}"
                self.canvas.create_rectangle(x0+i*box_w, y0, x0+i*box_w+box_w, y0+box_h, fill=color, outline="#0288d1", width=3)
                self.canvas.create_text(x0+i*box_w+box_w//2, y0+box_h//2, text=label, font=("Consolas", 18, "bold"))
            self.canvas.create_rectangle(x0+total*box_w, y0, x0+total*box_w+box_w, y0+box_h, fill="#ffccbc", outline="#d84315", width=3)
            self.canvas.create_text(x0+total*box_w+box_w//2, y0+box_h//2, text="P0", font=("Consolas", 18, "bold"))
            self.info_label.config(text=f"Adım {self.step+1}: Genel parity (P0) hesaplanıyor.\nTüm bitlerin toplamı alınır, çiftse 0, tekse 1 olur.")
            self.canvas.create_text(440, y0+box_h+30, text="Neden? P0, tüm kodun çift/tek olup olmadığını kontrol eder.", font=("Helvetica", 12), fill="#333")
            
        elif self.step == p+2:
            # Son hali
            for i in range(total):
                color = "#b3e5fc" if i in parity_positions else "#c8e6c9"
                label = f"P{i+1}" if i in parity_positions else f"D{[j for j in range(total) if j not in parity_positions].index(i)+1}"
                self.canvas.create_rectangle(x0+i*box_w, y0, x0+i*box_w+box_w, y0+box_h, fill=color, outline="#0288d1", width=3)
                self.canvas.create_text(x0+i*box_w+box_w//2, y0+box_h//2, text=label, font=("Consolas", 18, "bold"))
            self.canvas.create_rectangle(x0+total*box_w, y0, x0+total*box_w+box_w, y0+box_h, fill="#ffccbc", outline="#d84315", width=3)
            self.canvas.create_text(x0+total*box_w+box_w//2, y0+box_h//2, text="P0", font=("Consolas", 18, "bold"))
            self.info_label.config(text=f"Adım {self.step+1}: Hamming kodunun tamamı oluştu!\nKullanıcı verisi ve parity bitleriyle birlikte kod hazır.")
            self.canvas.create_text(440, y0+box_h+30, text="Artık bu kod bellek veya iletim için hazır!", font=("Helvetica", 12), fill="#333")
            
        # Buton durumlarını güncelle
        self.prev_btn.config(state="normal" if self.step > 0 else "disabled")
        if self.step >= (p+2):
            self.next_btn.config(state="disabled")
        else:
            self.next_btn.config(state="normal")

    def next_step(self):
        # Sonraki adıma geç
        self.step += 1
        self.draw_hamming_guide()

    def prev_step(self):
        # Önceki adıma dön
        if self.step > 0:
            self.step -= 1
            self.draw_hamming_guide()

    def restart(self):
        # Rehberi baştan başlat
        self.step = 0
        self.draw_hamming_guide()

if __name__ == "__main__":
    # Programı başlat
    main_window = tk.Tk()
    main_window.state('zoomed')  # Otomatik tam ekran başlat
    app = SimulatorApp(main_window)
    main_window.mainloop()