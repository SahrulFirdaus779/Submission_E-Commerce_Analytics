# E-Commerce Data Analysis (Advanced)

Proyek ini merupakan *submission* tugas akhir kelas **DBS Foundation Dicoding** pada alur belajar (*learning path*) **Data Science**, khusus untuk penyelesaian modul **Belajar Fundamental Analisis Data**. Melalui proyek ini, dilakukan praktik ekstraksi data, transformasi, visualisasi, serta **analisis lanjutan (RFM & Manual Clustering)** menggunakan Python.

## Dicoding Collection Dashboard ✨

### Setup Environment - Anaconda
```shell
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal
```shell
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Run steamlit app
```shell
streamlit run dashboard.py
```

## Panduan Deploy ke Streamlit Cloud (Mengejar Bintang 5)
Agar dashboard bisa diakses online ikuti langkah berikut:
1. Pastikan folder ini sudah di-*push* ke repositori GitHub Anda (opsional tapi sangat disarankan: buat repositori baru yang hanya berisi root folder `submission` ini).
2. Login ke [Streamlit Community Cloud](https://share.streamlit.io/) dengan akun GitHub Anda.
3. Klik **New app**.
4. Pilih repository tempat Anda menyimpan file ini.
5. Pada bagian **Main file path**, ketik: `dashboard/dashboard.py`.
6. Klik **Deploy**.
7. Tunggu beberapa saat, lalu salin URL yang diberikan Streamlit Cloud dan masukkan / paste URL tersebut ke dalam berkas `url.txt`.
