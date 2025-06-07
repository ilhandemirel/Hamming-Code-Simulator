# Python ile Hamming (SEC-DED) Kodlama Simülatörü

Bu proje, **Hamming kodlamasının** Tek Hata Düzeltme ve Çift Hata Tespit (SEC-DED) prensiplerini görselleştirmek amacıyla Python ve Tkinter kütüphanesi kullanılarak geliştirilmiş bir masaüstü uygulamasıdır. Kullanıcıların veri bitlerini girerek bu bitlerin nasıl kodlandığını, hataların nasıl oluşturulduğunu ve sistemin bu hataları nasıl tespit edip düzelttiğini adım adım gözlemlemesini sağlar.


---

## 📺 Demo Videosu

Uygulamanın nasıl çalıştığını, temel özelliklerini ve kullanımını gösteren videoya aşağıdaki linkten ulaşabilirsiniz.
[![Hamming Simülatör Demo](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID)

---

## 📝 Proje Raporu

Projenin tüm detaylarını, teorik altyapısını, tasarım kararlarını, kodun yapısını ve elde edilen sonuçları içeren proje anlatım dokümanına (raporuna) aşağıdaki linkten erişebilirsiniz.

- **[Proje Raporunu Görüntülemek İçin Tıklayın](./BLM230_Proje_AdSoyad_OgrenciNo.pdf)**

---

## 🚀 Temel Özellikler

- **İnteraktif Arayüz:** Tkinter ile geliştirilmiş kullanıcı dostu ve modern bir arayüz.
- **Değişken Veri Boyutları:** 8, 16 ve 32 bitlik veri girişlerini destekler.
- **Otomatik Kodlama:** Girilen veri bitlerini Hamming (SEC-DED) standardına göre otomatik olarak kodlar.
- **Hata Simülasyonu:** Kullanıcı, kodlanmış bitlerden herhangi birine tıklayarak **tek veya çift bitlik hatalar** oluşturabilir.
- **Anlık Analiz:**
  - **Tek Hata Düzeltme (SEC):** Oluşturulan tek bitlik hatalar anında tespit edilir, hata konumu (sendrom) hesaplanır ve otomatik olarak düzeltilir.
  - **Çift Hata Tespiti (DED):** Oluşturulan çift bitlik hataların düzeltilemez olduğu tespit edilir ve kullanıcıya bildirilir.
- **Görsel Geri Bildirim:**
  - Parity bitleri, veri bitleri, hatalı bit ve düzeltilen bit farklı renklerle vurgulanır.
  - Hata durumu ve sendrom değeri anlık olarak gösterilir.
- **Eğitici Rehber:** "Hamming Code Nasıl Oluşur?" bölümü, kodlama mantığını adım adım ve görsel olarak anlatır.

---

## ⚙️ Nasıl Çalıştırılır?

Proje, ek bir kütüphane kurulumu gerektirmez. Sisteminizde Python 3 yüklü olması yeterlidir.

1.  **Depoyu Klonlayın:** Bu depoyu bilgisayarınıza indirin.
    ```bash
    git clone [https://github.com/](https://github.com/)[KULLANICI-ADIN]/[REPO-ADIN].git
    ```
2.  **Dizine Gidin:** Proje klasörünün içine girin.
    ```bash
    cd [REPO-ADIN]
    ```
3.  **Simülatörü Başlatın:** Aşağıdaki komut ile uygulamayı çalıştırın.
    ```bash
    python hamming_simulator.py
    ```

Uygulama penceresi açılacaktır. Veri girişi yaparak simülasyonu başlatabilirsiniz.
