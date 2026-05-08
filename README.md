Bir web sitesine gelen genç, yetişkin ve kurumsal segmentlerine  ve gece gündüz farkına göre en yüksek tıklanma oranına sahip reklamı otomatik olarak seçen bir ajan geliştirdim.

## Kullanılan RL Bileşenleri
State: Kullanıcı Segmenti + Günün Saati (Toplam 6 farklı senaryo)
Action: Reklam A, Reklam B veya Reklam Gösterme 
Reward: Tıklama olursa +50, tıklama olmazsa -1 puan
Algoritma: Greedy, zamanın %20'sinde rastgele seçimler yaparak yeni şeyler keşfeder, %80'inde ise o ana kadar öğrendiği en iyi veriyi kullanır.
<img width="4800" height="1800" alt="analiz_isi_haritalari" src="https://github.com/user-attachments/assets/015fd4b9-e9bc-42e4-ba44-598cb658dd16" />

Bu tablo hangi durumdayken hangi reklamın tıklama aldığını gösterir. Örneğin Genç-Gece durumunda Reklam B'nin 3 tıklama alarak baskın olduğunu görüyoruz.
Q-Değerleri ise Buradaki sayılar ajanın tecrübesini temsil eder. Mesela Genç-Gündüz satırında Reklam A'nın değeri 13.72 ile en yüksektir. Bu da ajanın kullanıcı gelirse kesinlikle Reklam A'yı göstermeliyim kararına vardığını kanıtlar.

<img width="3600" height="3000" alt="analiz_performans_egrisi" src="https://github.com/user-attachments/assets/664b67c1-9933-4ed1-b4dc-98ccf1359800" />
Bu grafik ajanın zamanla nasıl akıllandığını gösteriyor. Grafikteki kırılma noktaları ajanın yaptığı hataları ve aldığı ödülleri gösterir. Başlarda grafik daha yatay veya aşağı yönlüyken, 150. adımdan sonra dik bir tırmanışa geçmiştir.
<img width="1000" height="600" alt="reklam_simulasyonu" src="https://github.com/user-attachments/assets/b29b207c-9974-4d5c-b69a-e70e900be733" />
