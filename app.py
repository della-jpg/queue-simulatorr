import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Optimasi Produksi (LP)", layout="centered")
st.title("📈 Aplikasi Optimasi Produksi (Linear Programming)")

st.markdown("Masukkan data berikut untuk memaksimalkan keuntungan produksi dua produk.")

# Input
c1 = st.number_input("Keuntungan per unit Produk A (Rp)", value=30000)
c2 = st.number_input("Keuntungan per unit Produk B (Rp)", value=50000)

b1 = st.number_input("Total bahan baku tersedia (kg)", value=100.0)
a11 = st.number_input("Bahan baku per unit Produk A", value=2.0)
a12 = st.number_input("Bahan baku per unit Produk B", value=4.0)

b2 = st.number_input("Total waktu kerja tersedia (jam)", value=80.0)
a21 = st.number_input("Waktu kerja per unit Produk A", value=3.0)
a22 = st.number_input("Waktu kerja per unit Produk B", value=2.0)

# Fungsi objektif (negatif karena linprog meminimalkan)
c = [-c1, -c2]

# Matriks kendala dan RHS
A = [[a11, a12],
     [a21, a22]]
b = [b1, b2]

# Batasan variabel x >= 0
x_bounds = (0, None)
bounds = [x_bounds, x_bounds]

# Optimasi
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

if res.success:
    x1, x2 = res.x
    total_profit = -res.fun
    st.success("✅ Solusi Optimal Ditemukan:")
    st.write(f"Produksi Produk A: {x1:.2f} unit")
    st.write(f"Produksi Produk B: {x2:.2f} unit")
    st.write(f"Total Keuntungan: Rp {total_profit:,.0f}")
else:
    st.error("❌ Tidak ditemukan solusi optimal. Coba ubah parameter.")

# Visualisasi feasible region
st.subheader("📉 Visualisasi Area Feasible")

x = np.linspace(0, max(b1/a11, b2/a21), 400)
y1 = (b1 - a11 * x) / a12
y2 = (b2 - a21 * x) / a22

plt.figure(figsize=(6, 5))
plt.plot(x, y1, label="Batas Bahan Baku")
plt.plot(x, y2, label="Batas Waktu")
plt.fill_between(x, 0, np.minimum(y1, y2), where=(y1 > 0) & (y2 > 0), color='lightblue', alpha=0.5)
plt.xlim(left=0)
plt.ylim(bottom=0)
if res.success:
    plt.plot(x1, x2, 'ro', label="Solusi Optimal")
plt.xlabel("Produk A")
plt.ylabel("Produk B")
plt.legend()
plt.grid(True)
st.pyplot(plt)
