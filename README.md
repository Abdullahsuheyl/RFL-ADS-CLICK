# Web Reklam Yerleştirme Simülasyonu

Bir web sitesine gelen genç, yetişkin ve kurumsal segmentlerine ve gece gündüz farkına göre en yüksek tıklanma oranına sahip reklamı otomatik olarak seçen bir ajan geliştirdim. Bu çalışma Reinforcement Learning prensiplerini kullanarak dinamik bir ortamda maksimum verimi elde etmeyi amaçlamaktadır.

## Kullanılan RL Bileşenleri

- **State:** Kullanıcı Segmenti + Günün Saati şeklinde tanımlanmıştır. Toplamda 6 farklı senaryo mevcuttur: (Genç-Gündüz, Genç-Gece, Yetişkin-Gündüz, Yetişkin-Gece, Kurumsal-Gündüz, Kurumsal-Gece).
- **Action:** Ajanın her adımda seçebileceği 3 seçenek vardır: Reklam A'yı Göster, Reklam B'yi Göster veya Reklam Gösterme.
- **Reward:** Performans ölçümü için tıklama gerçekleşirse **+50 puan**, tıklama olmazsa deneme maliyeti olarak **-1 puan** verilir.
- **Algoritma:** Epsilon-Greedy yaklaşımı kullanılmıştır. Ajan, zamanın %20'sinde rastgele seçimler yaparak yeni stratejiler keşfeder (Exploration), kalan %80'inde ise o ana kadar öğrendiği en yüksek değerli aksiyonu (Exploitation) seçer.

## Teknik İşleyiş ve Q-Learning Mantığı

Sistem arka planda bir **Q-Table** üzerinde çalışır. Başlangıçta tüm değerler sıfırdır ve ajan hangi reklamın kime hitap ettiğini bilmez. Her adımda aşağıdaki matematiksel güncelleme kuralı işletilir:

**Q(durum, eylem) = Q(durum, eylem) + alpha * (Ödül - Q(durum, eylem))**

Buradaki **alpha** öğrenme katsayısıdır. Ajan aldığı ödüllere göre tablodaki değerleri güncelleyerek her kullanıcı grubu için bir hafıza oluşturur.

## Strateji ve Isı Haritası Analizi

<img width="4800" height="1800" alt="analiz_isi_haritalari" src="https://github.com/user-attachments/assets/015fd4b9-e9bc-42e4-ba44-598cb658dd16" />

Bu tablo hangi durumdayken hangi reklamın tıklama aldığını gösterir. Örneğin **Genç-Gece** durumunda Reklam B'nin 3 tıklama alarak baskın olduğunu görüyoruz. 

Q-Değerleri tablosundaki sayılar ise ajanın tecrübesini temsil eder. Mesela **Genç-Gündüz** satırında Reklam A'nın değeri **13.72** ile en yüksektir. Bu değerin rakiplerinden büyük olması, ajanın bu kullanıcı geldiğinde Reklam A'yı göstermenin en karlı yol olduğuna karar verdiğini kanıtlar. Negatif değerler ise o reklamın o grupta başarısız olduğunu ve ajanın artık bu riski almaması gerektiğini ifade eder.

## Performans Eğrisi ve Eğitim Süreci

<img width="3600" height="3000" alt="analiz_performans_egrisi" src="https://github.com/user-attachments/assets/664b67c1-9933-4ed1-b4dc-98ccf1359800" />

Bu grafik ajanın zamanla nasıl akıllandığını göstermektedir:
1. **Toplam Kazanç (Reward):** Grafikteki kırılma noktaları ajanın yaptığı hataları ve aldığı ödülleri gösterir. Başlarda (ilk 100 adım) grafik daha yatay seyrederken, ajan çevreyi çözdükçe ve keşif aşamasını tamamladıkça 150. adımdan sonra dik bir tırmanışa geçmiştir.
2. **CTR Gelişimi:** Alttaki turuncu eğri tıklanma oranının zamanla daha kararlı hale geldiğini gösterir. Ajanın yanlış reklamları eleyip doğru reklamlara odaklandığının ispatıdır.

## Canlı Simülasyon Arayüzü

Aşağıdaki animasyonda ajanın anlık olarak kullanıcıyı nasıl tanımladığı, hangi reklamı yerleştirdiği ve karşılığında aldığı puan geri bildirimi görselleştirilmiştir.

<img width="1000" height="600" alt="reklam_simulasyonu" src="https://github.com/user-attachments/assets/b29b207c-9974-4d5c-b69a-e70e900be733" />
