import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Fuzzy Traffic System", layout="centered")
st.title("🚦 Sistem Logika Fuzzy: Tingkat Kemacetan")

# 1. Definisi Variabel Fuzzy
jumlah_kendaraan = ctrl.Antecedent(np.arange(0, 1001, 1), 'jumlah_kendaraan')
kemacetan = ctrl.Consequent(np.arange(0, 101, 1), 'kemacetan')

# 2. Fungsi Keanggotaan
jumlah_kendaraan['lancar'] = fuzz.trapmf(jumlah_kendaraan.universe, [0, 0, 200, 400])
jumlah_kendaraan['padat'] = fuzz.trimf(jumlah_kendaraan.universe, [300, 500, 700])
jumlah_kendaraan['macet'] = fuzz.trapmf(jumlah_kendaraan.universe, [600, 800, 1000, 1000])

kemacetan['lancar'] = fuzz.trimf(kemacetan.universe, [0, 0, 50])
kemacetan['padat'] = fuzz.trimf(kemacetan.universe, [30, 50, 70])
kemacetan['macet'] = fuzz.trimf(kemacetan.universe, [50, 100, 100])

# 3. Aturan Fuzzy
rule1 = ctrl.Rule(jumlah_kendaraan['lancar'], kemacetan['lancar'])
rule2 = ctrl.Rule(jumlah_kendaraan['padat'], kemacetan['padat'])
rule3 = ctrl.Rule(jumlah_kendaraan['macet'], kemacetan['macet'])

traffic_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
traffic_sim = ctrl.ControlSystemSimulation(traffic_ctrl)

# 4. Input Section
st.subheader("📍 Masukkan Data Lalu Lintas")
container = st.container(border=True)
with container:
    mode_input = st.radio("Pilih Metode Input:", ("Slider", "Input Manual (Ketik)"), horizontal=True)
    if mode_input == "Input Manual (Ketik)":
        input_val = st.number_input("Jumlah Kendaraan (Unit)", min_value=0, max_value=1000, value=350, step=1)
    else:
        input_val = st.slider("Geser Jumlah Kendaraan", 0, 1000, 350)

# 5. Perhitungan Derajat Keanggotaan (Fuzzifikasi)
d_lancar = fuzz.interp_membership(jumlah_kendaraan.universe, jumlah_kendaraan['lancar'].mf, input_val)
d_padat = fuzz.interp_membership(jumlah_kendaraan.universe, jumlah_kendaraan['padat'].mf, input_val)
d_macet = fuzz.interp_membership(jumlah_kendaraan.universe, jumlah_kendaraan['macet'].mf, input_val)

# 6. Simulasi & Defuzzifikasi
traffic_sim.input['jumlah_kendaraan'] = input_val
traffic_sim.compute()
output_val = traffic_sim.output['kemacetan']

# 7. Status Hasil
if output_val <= 40:
    status = "Lancar"
elif 40 < output_val <= 70:
    status = "Padat"
else:
    status = "Macet"

# 8. Tampilan Antarmuka Utama
st.divider()
st.subheader("📊 Hasil Analisis")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Nilai Defuzzifikasi (Centroid)", value=f"{output_val:.2f}")
with col2:
    if status == "Lancar":
        st.success(f"Kondisi: **{status}**")
    elif status == "Padat":
        st.warning(f"Kondisi: **{status}**")
    else:
        st.error(f"Kondisi: **{status}**")

# Tabel Detail Perhitungan
st.write("**Tabel Derajat Keanggotaan & Perhitungan:**")
data_keanggotaan = {
    "Himpunan Fuzzy": ["Lancar", "Padat", "Macet"],
    "Fungsi Keanggotaan": ["Trapmf (0,0,200,400)", "Trimf (300,500,700)", "Trapmf (600,800,1000,1000)"],
    "Derajat Keanggotaan (μ)": [f"{d_lancar:.4f}", f"{d_padat:.4f}", f"{d_macet:.4f}"],
    "Alpha-Predicate": [f"Rule 1: {d_lancar:.4f}", f"Rule 2: {d_padat:.4f}", f"Rule 3: {d_macet:.4f}"]
}
df_fuzzy = pd.DataFrame(data_keanggotaan)
st.table(df_fuzzy)

# Grafik dan Detail
tab1, tab2 = st.tabs(["📈 Grafik Himpunan", "📝 Logika Aturan"])

with tab1:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(jumlah_kendaraan.universe, jumlah_kendaraan['lancar'].mf, 'g', label='Lancar')
    ax.plot(jumlah_kendaraan.universe, jumlah_kendaraan['padat'].mf, 'y', label='Padat')
    ax.plot(jumlah_kendaraan.universe, jumlah_kendaraan['macet'].mf, 'r', label='Macet')
    ax.vlines(input_val, 0, 1, colors='blue', linestyles='dashed', label=f'Input ({input_val})')
    ax.set_title("Kurva Keanggotaan Jumlah Kendaraan")
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.info("**Basis Aturan (Rules) & Inferensi:**")
    st.latex(fr"\alpha_{{1}} = \mu_{{Lancar}}({input_val}) = {d_lancar:.4f}")
    st.latex(fr"\alpha_{{2}} = \mu_{{Padat}}({input_val}) = {d_padat:.4f}")
    st.latex(fr"\alpha_{{3}} = \mu_{{Macet}}({input_val}) = {d_macet:.4f}")
    st.write("---")
    st.write("1. IF kendaraan **Lancar** THEN kemacetan **Lancar**")
    st.write("2. IF kendaraan **Padat** THEN kemacetan **Padat**")
    st.write("3. IF kendaraan **Macet** THEN kemacetan **Macet**")
    st.write(f"\n**Metode Defuzzifikasi:** Centroid")
