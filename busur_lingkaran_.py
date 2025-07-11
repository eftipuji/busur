import streamlit as st
import math
import time
import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Fungsi Inti Perhitungan ---
def hitung_busur_juring(radius, sudut_derajat):
    """
    Menghitung panjang busur dan luas juring lingkaran.
    Mengembalikan tuple (panjang_busur, luas_juring) atau (None, None) jika input tidak valid.
    """
    if radius <= 0:
        return None, None # Jari-jari harus positif

    sudut_radian = math.radians(sudut_derajat)
    panjang_busur = radius * sudut_radian
    luas_juring = 0.5 * (radius**2) * sudut_radian
    return panjang_busur, luas_juring

# --- Fungsi untuk Membuat Visualisasi Lingkaran ---
def plot_lingkaran_juring(radius, sudut_derajat):
    fig = go.Figure()

    # Gambar Lingkaran Penuh
    theta_full = np.linspace(0, 2 * np.pi, 100)
    x_full = radius * np.cos(theta_full)
    y_full = radius * np.sin(theta_full)
    fig.add_trace(go.Scatter(x=x_full, y=y_full, mode='lines', name='Lingkaran',
                             line=dict(color='lightgray', width=2)))

    # Gambar Juring
    if sudut_derajat != 0 and radius > 0:
        sudut_radian = math.radians(sudut_derajat)
        
        # Batasi sudut agar tidak terlalu berputar dalam visualisasi jika melebihi 360
        # Untuk visualisasi, kita hanya peduli bentuknya, bukan berapa kali putaran
        visual_sudut_radian = sudut_radian % (2 * math.pi)
        if visual_sudut_radian < 0: # Mengatasi sudut negatif jika diizinkan (saat ini min_value slider = 0)
            visual_sudut_radian += 2 * math.pi

        # Titik-titik untuk juring
        # Mulai dari (0,0), lalu ke (r,0), ikuti busur, lalu kembali ke (0,0)
        theta_juring = np.linspace(0, visual_sudut_radian, 50)
        x_juring_busur = radius * np.cos(theta_juring)
        y_juring_busur = radius * np.sin(theta_juring)

        x_juring = np.concatenate([[0], x_juring_busur, [0]])
        y_juring = np.concatenate([[0], y_juring_busur, [0]])

        fig.add_trace(go.Scatter(x=x_juring, y=y_juring, mode='lines', fill='toself', name='Juring',
                                 fillcolor='rgba(100, 149, 237, 0.5)', # Warna biru muda transparan
                                 line=dict(color='cornflowerblue', width=2)))
        
        # Garis radius
        fig.add_trace(go.Scatter(x=[0, radius * math.cos(0)], y=[0, radius * math.sin(0)],
                                 mode='lines', name='Radius 1', line=dict(color='darkblue', width=2)))
        if visual_sudut_radian > 0:
             fig.add_trace(go.Scatter(x=[0, radius * math.cos(visual_sudut_radian)], y=[0, radius * math.sin(visual_sudut_radian)],
                                 mode='lines', name='Radius 2', line=dict(color='darkblue', width=2)))

    # Pengaturan layout
    max_val = radius * 1.2 # Beri sedikit ruang di sekitar lingkaran
    fig.update_xaxes(range=[-max_val, max_val], showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(range=[-max_val, max_val], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(title='Visualisasi Lingkaran dan Juring', showlegend=False,
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)') # Transparan

    return fig


# --- Halaman Menu 1: Kalkulator Busur & Juring ---
def kalkulator_menu():
    st.title("📏 Kalkulator Panjang Busur & Luas Juring Lingkaran 📐")
    st.markdown("""
    Selamat datang di kalkulator interaktif! Masukkan nilai **jari-jari** lingkaran dan **sudut** juring
    (dalam derajat) untuk menemukan panjang busur dan luas juringnya.
    **Visualisasi akan berubah secara *real-time*!**
    """)

    st.write("---")

    st.header("⚙️ Masukkan Data Lingkaran")

    col1, col2 = st.columns(2)

    with col1:
        radius = st.number_input(
            "Masukkan Jari-jari Lingkaran (r)",
            min_value=0.01,
            value=10.0,
            format="%.2f",
            help="Jari-jari lingkaran harus bernilai positif."
        )
    with col2:
        sudut_derajat = st.slider(
            "Pilih Sudut Juring (derajat)",
            min_value=0.0,
            max_value=720.0,
            value=90.0,
            step=0.5,
            format="%.1f",
            help="Sudut juring dalam derajat. 360 derajat adalah satu lingkaran penuh."
        )

    st.write("---")
    
    st.header("👁️ Visualisasi")
    # Tampilkan plot secara real-time
    fig_lingkaran = plot_lingkaran_juring(radius, sudut_derajat)
    st.plotly_chart(fig_lingkaran, use_container_width=True)


    st.header("✨ Hasil Perhitungan ✨")

    # Langsung hitung dan tampilkan hasil tanpa tombol terpisah
    # Hasil akan update otomatis saat slider digerakkan
    panjang_busur, luas_juring = hitung_busur_juring(radius, sudut_derajat)

    if panjang_busur is not None:
        colors = ["#4CAF50", "#2196F3", "#FFC107", "#9C27B0", "#E91E63"]
        selected_color = random.choice(colors)

        st.markdown(f"""
        <div style="background-color:{selected_color}; padding: 25px; border-radius: 12px; text-align: center; margin-top: 20px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
            <h3 style="color: white; margin-bottom: 15px; font-size: 28px;">✅ Hasil Ditemukan! ✅</h3>
            <p style="font-size: 22px; font-weight: normal; color: white;">
                Dengan Jari-jari **{radius:.2f}** dan Sudut **{sudut_derajat:.1f}°**:
            </p>
            <p style="font-size: 36px; font-weight: bolder; color: white; margin-top: 15px;">
                Panjang Busur: <span style="color: yellow;">{panjang_busur:.4f}</span> unit
            </p>
            <p style="font-size: 36px; font-weight: bolder; color: white;">
                Luas Juring: <span style="color: yellow;">{luas_juring:.4f}</span> unit²
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info(f"""
        * **Panjang Busur ($s$)**: $s = r \\times \\theta_{{radian}}$
        * **Luas Juring ($A$)**: $A = \\frac{{1}}{{2}} r^2 \\times \\theta_{{radian}}$
        * Dimana $\\theta_{{radian}} = \\text{{sudut dalam derajat}} \\times \\frac{{\\pi}}{{180}}$
        """)
        st.info(f"Untuk kasus Anda, sudut dalam radian adalah: **{math.radians(sudut_derajat):.4f} radian**.")

    else:
        st.error("❌ Input tidak valid! Jari-jari harus lebih besar dari nol.")
    
    st.markdown("---")


# --- Halaman Menu 2: Penjelasan Rumus ---
def penjelasan_rumus_menu():
    st.title("💡 Penjelasan Rumus Kalkulator 💡")
    st.markdown("""
    Di bagian ini, kita akan membahas lebih dalam mengenai rumus matematika yang digunakan
    dalam kalkulator ini untuk menghitung panjang busur dan luas juring lingkaran.
    """)

    st.write("---")

    st.header("1. Panjang Busur Lingkaran ($s$)")
    st.markdown("""
    Panjang busur adalah bagian dari keliling lingkaran yang dibatasi oleh dua titik pada lingkaran
    dan sudut pusat tertentu. Bayangkan Anda memotong sepotong "kue pizza" dari lingkaran,
    panjang busur adalah panjang kulit luarnya.
    """)
    st.latex(r'''s = r \times \theta_{radian}''')
    st.markdown("""
    Di mana:
    * $s$ = Panjang Busur
    * $r$ = Jari-jari lingkaran (jarak dari pusat ke tepi lingkaran)
    * $\\theta_{radian}$ = Sudut pusat juring dalam satuan **radian**

    **Penting:** Jika sudut yang Anda miliki dalam **derajat**, Anda harus mengubahnya terlebih dahulu ke radian menggunakan rumus konversi:
    """)
    st.latex(r'''\theta_{radian} = \text{sudut dalam derajat} \times \frac{\pi}{180}''')

    st.header("2. Luas Juring Lingkaran ($A$)")
    st.markdown("""
    Luas juring adalah luas daerah yang dibatasi oleh dua jari-jari dan busur lingkaran.
    Ini adalah luas dari potongan "kue pizza" itu sendiri.
    """)
    st.latex(r'''A = \frac{1}{2} r^2 \times \theta_{radian}''')
    st.markdown("""
    Di mana:
    * $A$ = Luas Juring
    * $r$ = Jari-jari lingkaran
    * $\\theta_{radian}$ = Sudut pusat juring dalam satuan **radian**

    Sama seperti panjang busur, jika sudut Anda dalam **derajat**, Anda perlu mengonversinya ke radian terlebih dahulu.
    """)

    st.write("---")
    st.info("""
    **Mengapa Menggunakan Radian?**
    Dalam banyak rumus matematika yang melibatkan lingkaran dan trigonometri, penggunaan radian menyederhanakan perhitungan dan secara alami sesuai dengan definisi turunan dan integral fungsi trigonometri. Satu radian adalah sudut ketika panjang busur sama dengan jari-jari lingkaran.
    """)
    st.markdown(f"Untuk nilai $\\pi$ (pi) yang digunakan di sini, sekitar **{math.pi:.6f}**.")

# --- Halaman Menu 3: Lembar Kerja Praktikum ---
def lembar_kerja_menu():
    st.title("📄 Lembar Kerja Praktikum Virtual 📄")
    st.markdown("""
    Selamat datang di lembar kerja praktikum virtual geometri lingkaran!
    Gunakan menu **'Kalkulator Busur & Juring'** untuk melakukan percobaan dan mengisi tabel di bawah.
    """)

    st.write("---")

    st.header("📚 Tujuan Pembelajaran")
    st.markdown("""
    Setelah menyelesaikan praktikum virtual ini, Anda diharapkan mampu:
    * Memahami konsep **jari-jari**, **busur**, dan **juring** lingkaran.
    * Menghitung **panjang busur** dan **luas juring** lingkaran menggunakan kalkulator virtual.
    * Menganalisis hubungan antara jari-jari, sudut, panjang busur, dan luas juring.
    * Menerapkan rumus panjang busur dan luas juring dalam berbagai skenario.
    """)

    st.header("🛠️ Alat dan Bahan")
    st.markdown("""
    * Komputer/Laptop/Tablet/Smartphone
    * Akses internet stabil
    * Aplikasi ini (Kalkulator Busur & Juring Lingkaran)
    """)

    st.header("📝 Prosedur Praktikum")
    st.markdown("""
    **Langkah 1: Akses Aplikasi Virtual Lab**
    >1.  Pastikan Anda berada di aplikasi ini.
    >2.  Gunakan **sidebar** di kiri untuk beralih antara menu.

    **Langkah 2: Eksplorasi Pengaruh Jari-jari**
    >1.  Pindah ke menu **'Kalkulator Busur & Juring'**.
    >2.  Atur **Sudut Juring** ke nilai tetap, misalnya **90.0 derajat**.
    >3.  Ubah nilai **Jari-jari Lingkaran (r)** secara bertahap dan catat hasilnya pada Tabel 1 di bawah ini.
    >    * Coba nilai **r**: **5.0, 10.0, 15.0, 20.0**.
    >    * **Tips:** Langsung masukkan jari-jari di kalkulator, lihat hasilnya, dan catat di tabel yang ada di bawah ini.

    **Langkah 3: Eksplorasi Pengaruh Sudut**
    >1.  Pada menu **'Kalkulator Busur & Juring'**, atur **Jari-jari Lingkaran (r)** ke nilai tetap, misalnya **10.0 unit**.
    >2.  Ubah nilai **Sudut Juring (derajat)** secara bertahap dan catat hasilnya pada Tabel 2 di bawah ini.
    >    * Coba nilai **sudut**: **30.0, 60.0, 90.0, 180.0, 360.0, 450.0**.
    >    * **Tips:** Sama seperti sebelumnya, gunakan kalkulator untuk mendapatkan hasil dan catat.

    **Langkah 4: Eksplorasi Kasus Khusus**
    >1.  Coba masukkan nilai **jari-jari negatif** atau **nol** di kalkulator. Apa yang terjadi dengan hasil perhitungannya?
    >2.  Coba masukkan sudut yang sangat kecil (misal **0.1 derajat**) atau sangat besar (misal **1000.0 derajat**). Apa yang bisa Anda simpulkan?
    """)

    st.header("📊 Data Pengamatan")
    st.markdown("Isi tabel di bawah ini dengan hasil yang Anda dapatkan dari **Kalkulator Busur & Juring**.")

    st.subheader("Tabel 1: Pengaruh Perubahan Jari-jari (Sudut Tetap = 90.0°)")
    # Menggunakan session_state untuk menyimpan nilai input tabel simulasi
    if 'table1_data' not in st.session_state:
        st.session_state.table1_data = {
            'No.': [1, 2, 3, 4],
            'Jari-jari (r)': [5.0, 10.0, 15.0, 20.0],
            'Sudut (derajat)': [90.0, 90.0, 90.0, 90.0],
            'Panjang Busur (unit)': [' ', ' ', ' ', ' '],
            'Luas Juring (unit²)': [' ', ' ', ' ', ' ']
        }
    
    # Tampilkan DataFrame yang bisa diisi menggunakan st.data_editor
    # Ini jauh lebih interaktif daripada text_input per sel
    edited_df1 = st.data_editor(pd.DataFrame(st.session_state.table1_data), 
                                num_rows="fixed", 
                                column_config={
                                    "No.": st.column_config.NumberColumn("No.", disabled=True),
                                    "Jari-jari (r)": st.column_config.NumberColumn("Jari-jari (r)", disabled=True),
                                    "Sudut (derajat)": st.column_config.NumberColumn("Sudut (derajat)", disabled=True),
                                    "Panjang Busur (unit)": st.column_config.TextColumn("Panjang Busur (unit)"),
                                    "Luas Juring (unit²)": st.column_config.TextColumn("Luas Juring (unit²)")
                                },
                                hide_index=True,
                                key="df1_editor")
    st.session_state.table1_data = edited_df1.to_dict('list') # Update session state


    st.subheader("Tabel 2: Pengaruh Perubahan Sudut (Jari-jari Tetap = 10.0 unit)")
    if 'table2_data' not in st.session_state:
        st.session_state.table2_data = {
            'No.': [1, 2, 3, 4, 5, 6],
            'Jari-jari (r)': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
            'Sudut (derajat)': [30.0, 60.0, 90.0, 180.0, 360.0, 450.0],
            'Panjang Busur (unit)': [' ', ' ', ' ', ' ', ' ', ' '],
            'Luas Juring (unit²)': [' ', ' ', ' ', ' ', ' ', ' ']
        }

    edited_df2 = st.data_editor(pd.DataFrame(st.session_state.table2_data), 
                                num_rows="fixed", 
                                column_config={
                                    "No.": st.column_config.NumberColumn("No.", disabled=True),
                                    "Jari-jari (r)": st.column_config.NumberColumn("Jari-jari (r)", disabled=True),
                                    "Sudut (derajat)": st.column_config.NumberColumn("Sudut (derajat)", disabled=True),
                                    "Panjang Busur (unit)": st.column_config.TextColumn("Panjang Busur (unit)"),
                                    "Luas Juring (unit²)": st.column_config.TextColumn("Luas Juring (unit²)")
                                },
                                hide_index=True,
                                key="df2_editor")
    st.session_state.table2_data = edited_df2.to_dict('list') # Update session state


    st.header("❓ Analisis Data dan Pertanyaan")
    st.markdown("""
    Setelah mengisi tabel di atas, jawablah pertanyaan-pertanyaan berikut di tempat yang telah disediakan:
    """)
    
    st.subheader("Pertanyaan 1:")
    st.markdown("1. Bagaimana hubungan antara **jari-jari** dengan **panjang busur** jika sudut dijaga tetap? Jelaskan mengapa demikian!")
    st.text_area("Jawaban Pertanyaan 1", key="jawaban_q1", height=100)

    st.subheader("Pertanyaan 2:")
    st.markdown("2. Bagaimana hubungan antara **jari-jari** dengan **luas juring** jika sudut dijaga tetap? Jelaskan mengapa demikian!")
    st.text_area("Jawaban Pertanyaan 2", key="jawaban_q2", height=100)
    
    st.subheader("Pertanyaan 3:")
    st.markdown("3. Bagaimana hubungan antara **sudut** dengan **panjang busur** jika jari-jari dijaga tetap? Jelaskan mengapa demikian!")
    st.text_area("Jawaban Pertanyaan 3", key="jawaban_q3", height=100)

    st.subheader("Pertanyaan 4:")
    st.markdown("4. Bagaimana hubungan antara **sudut** dengan **luas juring** jika jari-jari dijaga tetap? Jelaskan mengapa demikian!")
    st.text_area("Jawaban Pertanyaan 4", key="jawaban_q4", height=100)

    st.subheader("Pertanyaan 5:")
    st.markdown("5. Apa yang terjadi pada panjang busur dan luas juring jika sudut yang dimasukkan lebih dari 360 derajat? Berikan contoh nyata di mana konsep ini bisa diterapkan (misalnya, roda berputar).")
    st.text_area("Jawaban Pertanyaan 5", key="jawaban_q5", height=100)

    st.subheader("Pertanyaan 6:")
    st.markdown("6. Aplikasi memiliki menu 'Penjelasan Rumus'. Jelaskan mengapa sudut harus diubah ke **radian** sebelum digunakan dalam rumus perhitungan.")
    st.text_area("Jawaban Pertanyaan 6", key="jawaban_q6", height=100)

    st.subheader("Pertanyaan 7:")
    st.markdown("7. Bagaimana Virtual Lab ini membantu Anda memahami konsep geometri lingkaran dibandingkan dengan hanya membaca buku?")
    st.text_area("Jawaban Pertanyaan 7", key="jawaban_q7", height=100)

    st.header("✅ Kesimpulan")
    st.markdown("""
    Tuliskan kesimpulan Anda mengenai hubungan antara jari-jari, sudut, panjang busur, dan luas juring berdasarkan hasil praktikum virtual ini.
    """)
    st.text_area("Tulis Kesimpulan Anda di sini...", key="kesimpulan_akhir", height=150, help="Anda bisa menyalin dan menempel kesimpulan Anda setelah menulisnya.")

    st.markdown("---")
    st.caption("Lembar kerja ini dirancang untuk memandu pembelajaran Anda. Selamat belajar!")


# --- Main Aplikasi Streamlit ---
def main():
    # Konfigurasi halaman umum
    st.set_page_config(
        page_title="Aplikasi Geometri Lingkaran Interaktif 🌌",
        page_icon="🧭",
        layout="wide", # Layout lebar sangat cocok untuk visualisasi dan lembar kerja
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("Navigasi Aplikasi")
    menu_selection = st.sidebar.radio(
        "Pilih Menu:",
        ["Kalkulator Busur & Juring", "Penjelasan Rumus", "Lembar Kerja Praktikum"]
    )

    if menu_selection == "Kalkulator Busur & Juring":
        kalkulator_menu()
    elif menu_selection == "Penjelasan Rumus":
        penjelasan_rumus_menu()
    elif menu_selection == "Lembar Kerja Praktikum":
        lembar_kerja_menu()

    current_time = time.strftime("%A, %d %B %Y", time.localtime()) # Current time is Monday, July 7, 2025 at 11:15:05 AM WIB.
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Versi Aplikasi v2.0. Dibuat dengan ❤️ di Pekalongan, {current_time}.")

if __name__ == "__main__":
    main()
