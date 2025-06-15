# 🎠 Ride On - Sistem Booking Wahana

**Ride On** adalah aplikasi web lengkap berbasis Flask untuk sistem manajemen pemesanan tiket wahana di sebuah taman hiburan. Aplikasi ini memungkinkan pengguna melihat daftar wahana, memesan tiket berdasarkan jadwal, dan masuk ke dalam daftar tunggu jika tiket habis. Admin memiliki dashboard untuk mengelola semua data wahana, jadwal, pengguna, dan pemesanan.

🌐 **Lihat Aplikasi Live**: [https://cumlaude28.pythonanywhere.com](https://cumlaude28.pythonanywhere.com)

---

## ✨ Fitur Utama

### 👤 Untuk Pengguna
- 🔍 **Pencarian Wahana**: Cari wahana favorit dengan mudah.
- 📋 **Katalog Detail**: Lihat deskripsi, lokasi, dan jadwal setiap wahana.
- 🎟️ **Sistem Booking**: Pesan tiket untuk jadwal yang tersedia.
- 🕒 **Daftar Tunggu (Waiting List)**: Otomatis masuk antrian jika tiket habis.
- 📜 **Riwayat Pemesanan**: Lihat dan kelola riwayat tiket yang pernah dipesan.
- ❌ **Pembatalan Terbatas**: Batalkan pesanan dalam waktu tertentu setelah booking.
- 🧾 **Cetak Tiket**: Lihat detail tiket dengan kode booking unik.

### 🛠️ Untuk Admin
- 📊 **Dashboard Admin**: Statistik total wahana, pengguna, dan pemesanan.
- 🎡 **Manajemen Wahana (CRUD)**: Tambah, lihat, edit, dan hapus wahana (termasuk unggah gambar).
- 📅 **Manajemen Jadwal (CRUD)**: Kelola jadwal dan kuota tiket. Sistem otomatis memberi tiket pada daftar tunggu saat kuota bertambah.
- 👥 **Manajemen Pengguna & Pesanan**: Lihat daftar pengguna dan semua detail pemesanan.

---

## 🔬 Implementasi Struktur Data

- **Record / Class**: Menggunakan model SQLAlchemy seperti `User`, `Wahana`, `Pemesanan`, dll.
- **Array**: Menggunakan list Python saat menampilkan data (`Wahana.query.all()`).
- **Queue (Antrian)**: Fitur daftar tunggu menggunakan konsep FIFO (First In, First Out).
- **Stack (Tumpukan)**: Fitur undo booking berbasis LIFO (Last In, First Out), disimpan dalam session.

---

## 🚀 Cara Menjalankan Secara Lokal

### 1. Prasyarat
- Python 3.x
- Git
- MySQL Server

### 2. Clone Repository
```bash
git clone https://github.com/Anang-Programmer/booking-wahana.git
cd booking-wahana
```

### 3. Buat dan Aktifkan Virtual Environment
```bash
# Membuat virtual environment
python -m venv venv

# Aktifkan venv
# Windows
venv\Scripts\activate

# MacOS / Linux
source venv/bin/activate
```

### 4. Install Dependensi
```bash
pip install -r requirements.txt
```

### 5. Setup Database
- Buat database MySQL baru, contoh: `db_booking_wahana`
- Impor file `db_booking_wahana.sql` dari repo ke database tersebut

### 6. Konfigurasi Koneksi Database
Buka file `app.py` dan ubah baris berikut:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://USERNAME:PASSWORD@localhost/NAMA_DATABASE'
```

### 7. Jalankan Aplikasi
```bash
py app.py
```

Akses di: `http://127.0.0.1:5000`

---

## 💻 Teknologi yang Digunakan
- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: PythonAnywhere
- **Lainnya**: Jinja2 (Template Engine), Passlib (Password Hashing)

---

## 👥 Tim Pengembang (Kelompok 1 Struktur Data)

- 👨‍💻 Jaka Perdana  
- 👩‍💻 Firda Nabilah  
- 👩‍💻 Hasanah Nur Aini  
- 👩‍💻 Anggina Pertiwi Nasution  
- 👩‍💻 Azri Anggia Putri
