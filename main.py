import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import seaborn as sns
import pandas as pd

# --- 1. AYARLAR VE PARAMETRELER ---
segments = ["Genç", "Yetişkin", "Kurumsal"]
times = ["Gündüz", "Gece"]
actions = ["Reklam A", "Reklam B", "Reklam Yok"]
state_names = [f"{s}-{t}" for s in segments for t in times]

# Gerçek tıklama olasılıkları (Ajanın çözmeye çalıştığı "gizli" veriler)
true_ctr = np.array([
    [0.18, 0.02, 0.00], [0.01, 0.20, 0.00], # Genç
    [0.05, 0.05, 0.00], [0.02, 0.12, 0.00], # Yetişkin
    [0.01, 0.01, 0.00], [0.15, 0.03, 0.00]  # Kurumsal
])

q_table = np.zeros((6, 3))
epsilon = 0.2  # Keşif oranı
alpha = 0.2    # Öğrenme hızı
rewards = []
data_log = []

# --- 2. CANLI ANİMASYON VE GIF KAYDI ---
fig_anim = plt.figure(figsize=(10, 6))
gs = fig_anim.add_gridspec(2, 2)
ax_web = fig_anim.add_subplot(gs[0, 0]) 
ax_stats = fig_anim.add_subplot(gs[0, 1]) 
ax_graph_live = fig_anim.add_subplot(gs[1, :]) 

def update(frame):
    global q_table
    state_idx = np.random.randint(0, 6)
    seg_idx, time_idx = divmod(state_idx, 2)
    
    # Aksiyon Seçimi
    action_idx = np.random.randint(0, 3) if np.random.rand() < epsilon else np.argmax(q_table[state_idx])
    
    # Simülasyon
    clicked = np.random.rand() < true_ctr[state_idx, action_idx]
    reward = 50 if clicked else -1
    
    rewards.append(reward)
    data_log.append({'Durum': state_names[state_idx], 'Reklam': actions[action_idx], 'Tıklama': 1 if clicked else 0})
    q_table[state_idx, action_idx] += alpha * (reward - q_table[state_idx, action_idx])
    
    # Görselleştirme
    for ax in [ax_web, ax_stats, ax_graph_live]: ax.clear()
    
    ax_web.set_title("Canlı Simülasyon")
    color = '#27ae60' if clicked else ('#c0392b' if action_idx != 2 else '#95a5a6')
    ax_web.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, color='#f0f0f0', ec='black'))
    ax_web.add_patch(plt.Rectangle((0.2, 0.3), 0.6, 0.3, color=color, alpha=0.6))
    ax_web.text(0.5, 0.85, f"{segments[seg_idx]}\n{times[time_idx]}", ha='center', weight='bold')
    ax_web.text(0.5, 0.45, f"{actions[action_idx]}", ha='center', va='center', weight='bold')
    ax_web.axis('off')
    
    ax_stats.bar(actions, q_table[state_idx], color=['#2980b9', '#8e44ad', '#7f8c8d'])
    ax_stats.set_title("Ajanın Mevcut Hafızası")
    ax_stats.set_ylim(-5, 55)

    ax_graph_live.plot(np.cumsum(rewards), color='green')
    ax_graph_live.set_title("Kümülatif Ödül Artışı")

print("Eğitim başlıyor, GIF kaydediliyor...")
ani = FuncAnimation(fig_anim, update, frames=200, interval=50, repeat=False)
ani.save("reklam_simulasyonu.gif", writer=PillowWriter(fps=10))
plt.close()

# --- 3. AYRI AYRI ANALİZ GÖRSELLERİNİ OLUŞTURMA ---

def create_final_plots():
    df = pd.DataFrame(data_log)
    q_df = pd.DataFrame(q_table, index=state_names, columns=actions)
    
    # GÖRSEL 1: STRATEJİ ANALİZİ (Isı Haritaları Beraber)
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    click_pivot = df.pivot_table(index='Durum', columns='Reklam', values='Tıklama', aggfunc='sum', fill_value=0)
    sns.heatmap(click_pivot, annot=True, cmap="YlGn", fmt='d', ax=ax1)
    ax1.set_title("Gerçekleşen Tıklama Sayıları")
    
    sns.heatmap(q_df, annot=True, cmap="Blues", fmt='.2f', ax=ax2)
    ax2.set_title("Ajanın Öğrendiği Q-Değerleri (Strateji)")
    
    plt.tight_layout()
    plt.savefig("analiz_isi_haritalari.png", dpi=300)
    print("Isı haritaları kaydedildi.")

    # GÖRSEL 2: PERFORMANS ANALİZİ (Eğriler Beraber)
    fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Ödül Eğrisi
    ax3.plot(np.cumsum(rewards), color='#16a085', lw=2)
    ax3.set_title("Eğitim Süreci: Toplam Kazanç Gelişimi")
    ax3.grid(True, alpha=0.3)
    
    # CTR Eğrisi
    clicks_list = [d['Tıklama'] for d in data_log]
    ctr_evolution = [sum(clicks_list[:i+1])/(i+1) for i in range(len(clicks_list))]
    ax4.plot(ctr_evolution, color='#e67e22', lw=2)
    ax4.set_title("Tıklama Oranı (CTR) Zamanla Değişimi")
    ax4.set_xlabel("Adım")
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("analiz_performans_egrisi.png", dpi=300)
    print("Performans grafikleri kaydedildi.")
    
    # ÖZET METİN
    with open("final_ozet_raporu.txt", "w") as f:
        f.write(f"SİMÜLASYON ÖZETİ\n")
        f.write(f"{'='*20}\n")
        f.write(f"Toplam Gösterim: {len(data_log)}\n")
        f.write(f"Toplam Tıklama: {sum(clicks_list)}\n")
        f.write(f"Final CTR: %{(sum(clicks_list)/len(data_log))*100:.2f}\n")
    
    plt.show()

create_final_plots()