# E-Commerce Data Analysis (Advanced)

Proyek ini merupakan *submission* tugas akhir untuk mempelajari dasar-dasar ekstraksi data, transformasi, visualisasi, serta **analisis lanjutan (RFM & Manual Clustering)** menggunakan Python.

## Setup Lingkungan (Lokal)
```shell
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

## Panduan Deploy ke Streamlit Cloud (Mengejar Bintang 5)
Agar dashboard bisa diakses online dan mendapat nilai sempurna, ikuti langkah berikut:
1. Pastikan folder ini sudah di-*push* ke repositori GitHub Anda (opsional tapi sangat disarankan: buat repositori baru yang hanya berisi root folder `submission` ini).
2. Login ke [Streamlit Community Cloud](https://share.streamlit.io/) dengan akun GitHub Anda.
3. Klik **New app**.
4. Pilih repository tempat Anda menyimpan file ini.
5. Pada bagian **Main file path**, ketik: `dashboard/dashboard.py`.
6. Klik **Deploy**.
7. Tunggu beberapa saat, lalu salin URL yang diberikan Streamlit Cloud dan masukkan / paste URL tersebut ke dalam berkas `url.txt`.
