import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Fuzzy Traffic System", layout="centered")

# Fungsi Keanggotaan Manual untuk Jumlah Kendaraan
def fuzzy_membership_traffic(x):
    # Lancar (Trapesium: 0, 0, 200, 400)
    lancar = 0
    if x <= 200:
        lancar = 1
    elif 200 < x < 400:
        lancar = (400 - x) / (400 - 200)
    
    # Padat (Segitiga: 300, 500, 700)
    padat = 0
    if 300 < x <= 500:
        padat = (x - 300) / (500 - 300)
    elif 500 < x < 700:
        padat = (700 - x) / (700 - 500)
        
    # Macet (Trapesium: 600, 800, 1000, 1000)
    macet = 0
    if 600 < x < 800:
        macet = (x - 600) / (800 - 600)
    elif x >= 800:
        macet = 1
        
    return lancar, padat, macet

st.title("🚦 Sistem Logika Fuzzy: Tingkat Kemacetan")

# Input Section sesuai gaya slider kode kedua
input_val = st.slider("Masukkan Jumlah Kendaraan (Unit):", 0, 1000, 350, step=1)

# Hitung Nilai Fuzzifikasi Manual
mu_lancar, mu_padat, mu_macet = fuzzy_membership_traffic(input_val)

# Menentukan Hasil Akhir berdasarkan Nilai Maksimum (seperti kode beasiswa)
labels = ["Lancar", "Padat", "Macet"]
values = [mu_lancar, mu_padat, mu_macet]
idx_max = np.argmax(values)
status_akhir = labels[idx_max]

# --- TABEL DERAJAT KEANGGOTAAN ---
st.subheader("📊 Tabel Derajat Keanggotaan")
data_fuzzy = {
    "Himpunan Fuzzy": labels,
    "Derajat Keanggotaan (μ)": [f"{v:.4f}" for v in values]
}
st.table(pd.DataFrame(data_fuzzy))

# --- OUTPUT PERHITUNGAN ---
st.subheader("📝 Output Perhitungan")
st.write(f"Berdasarkan input jumlah kendaraan **{input_val}** unit, didapatkan nilai keanggotaan:")
st.latex(rf"\mu_{{\text{{Lancar}}}}({input_val}) = {mu_lancar:.4f}")
st.latex(rf"\mu_{{\text{{Padat}}}}({input_val}) = {mu_padat:.4f}")
st.latex(rf"\mu_{{\text{{Macet}}}}({input_val}) = {mu_macet:.4f}")

st.info(f"**Kesimpulan:** Nilai tertinggi adalah **{values[idx_max]:.4f}** pada kategori **{status_akhir}**.")

# --- GRAFIK ---
st.subheader("📈 Grafik Himpunan Fuzzy")
x_range = np.linspace(0, 1000, 1000)
y_plots = [[fuzzy_membership_traffic(i)[j] for i in x_range] for j in range(3)]
colors = ['green', 'orange', 'red']

fig, ax = plt.subplots()
for y, label, color in zip(y_plots, labels, colors):
    ax.plot(x_range, y, label=label, color=color)
ax.axvline(x=input_val, color='blue', linestyle='--', label=f'Input: {input_val}')
ax.set_ylabel("Degree of Membership")
ax.set_xlabel("Jumlah Kendaraan")
ax.legend()
st.pyplot(fig)
