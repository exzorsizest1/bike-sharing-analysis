# Proyek Analisis Data: Bike Sharing Dataset

Proyek akhir kelas Belajar Fundamental Analisis Data (Dicoding).

- **Nama:** Moh Reza
- **Email:** mohreza2455@gmail.com
- **ID Dicoding:** DS323B6Y1011

## Deskripsi
Analisis data penyewaan sepeda (Bike Sharing Dataset, 2011-2012) untuk menjawab dua pertanyaan bisnis:
1. Bagaimana tren penyewaan sepeda per bulan selama 2011-2012, kapan puncak dan titik terendahnya, serta berapa pertumbuhan 2012 dibanding 2011?
2. Pada jam berapa penyewaan tertinggi di hari kerja dibandingkan akhir pekan/libur?

Analisis lanjutan: binning suhu dan manual grouping level permintaan harian.

## Dashboard
Dashboard interaktif (Streamlit): https://URL-APLIKASI-KAMU.streamlit.app

## Struktur Folder
```
submission-analisis-data/
├── dashboard/
│   ├── dashboard.py
│   ├── main_data.csv
│   └── hour_clean.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Cara Menjalankan Dashboard di Lokal
1. Clone repository dan masuk ke foldernya:
   ```
   git clone https://github.com/exzorsizest1/bike-sharing-analysis.git
   cd bike-sharing-analysis
   ```
2. Buat dan aktifkan virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Pasang library:
   ```
   pip install -r requirements.txt
   ```
4. Jalankan dashboard:
   ```
   streamlit run dashboard/dashboard.py
   ```

## Sumber Data
[Bike Sharing Dataset (Kaggle)](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)