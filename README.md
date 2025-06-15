Proyek Aplikasi Booking Tiket Wahana
1. Pendahuluan
Dokumen ini menjelaskan arsitektur dan logika dari aplikasi web "Booking Tiket Wahana", sebuah proyek purwarupa yang dibangun menggunakan Python dengan framework Flask. Aplikasi ini mensimulasikan sistem pemesanan tiket online untuk sebuah taman hiburan, lengkap dengan fitur-fitur canggih seperti autentikasi pengguna, manajemen wahana oleh admin, daftar tunggu (waiting list), dan fitur pembatalan aksi terakhir (undo).

Tujuan utama proyek ini adalah untuk mendemonstrasikan implementasi berbagai struktur data fundamental dalam sebuah aplikasi web yang fungsional dan terhubung ke database.

Teknologi Utama:

Backend: Python, Flask

Database: MySQL (via XAMPP)

ORM: Flask-SQLAlchemy

Keamanan: Passlib (untuk hashing password)

Frontend: HTML, CSS, Jinja2 (Templating From Flask)

2. Struktur Proyek
Proyek ini disusun dengan struktur folder yang rapi untuk memisahkan antara logika, tampilan, dan aset statis, sesuai dengan praktik terbaik pengembangan web.

/booking_wahana_final
|
|-- app.py              # File utama Flask (otak aplikasi)
|
|-- /templates          # Folder untuk file-file HTML
|   |-- layout.html         # Template dasar untuk semua halaman
|   |-- index.html          # Halaman utama (daftar wahana)
|   |-- wahana_detail.html  # Halaman detail wahana & booking
|   |-- riwayat.html        # Halaman riwayat booking pengguna
|   |-- daftar_tunggu.html  # Halaman daftar tunggu pengguna
|   |-- auth.html           # Halaman untuk Login & Registrasi
|   |-- /admin
|       |-- layout.html
|       |-- dashboard.html
|       |-- kelola_wahana.html
|       |-- form_wahana.html
|
|-- /static             # Folder untuk file CSS, JS, dan Gambar
    |-- /css/style.css
    |-- /images/ ...

3. Alur Kerja & Logika Backend (app.py)
File app.py adalah pusat dari seluruh aplikasi. Di sinilah semua logika bisnis, interaksi database, dan manajemen struktur data terjadi.

3.1. Inisialisasi dan Koneksi Database
Aplikasi dimulai dengan menginisialisasi Flask dan SQLAlchemy. Konfigurasi SQLALCHEMY_DATABASE_URI diatur untuk terhubung ke database MySQL yang berjalan di XAMPP.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/db_booking_wahana'
db = SQLAlchemy(app)

3.2. Implementasi Struktur Data
Proyek ini secara aktif menggunakan beberapa struktur data fundamental:

Record / Class / Struct (Database-backed):

Implementasi: Struktur data ini diimplementasikan menggunakan Model SQLAlchemy. Setiap class seperti Pengguna, Wahana, JadwalWahana, dll., berfungsi sebagai blueprint (sebuah Record atau Class) yang secara langsung memetakan atributnya ke kolom-kolom pada tabel di database MySQL. Ini adalah fondasi utama penyimpanan data permanen.

Contoh: class Wahana(db.Model): ...

Array (Database-backed):

Implementasi: Struktur data ini diwujudkan melalui query SQLAlchemy yang mengembalikan sebuah Python List. List berfungsi sebagai Array dinamis.

Contoh: Wahana.query.all() akan mengambil semua baris dari tabel wahana dan mengembalikannya sebagai sebuah List (Array) yang berisi objek-objek Wahana.

Queue / Antrian (Database-backed):

Implementasi: Fitur Waiting List diimplementasikan sebagai sebuah antrian (Queue) yang persisten menggunakan tabel waiting_list di database. Sifat "First-In, First-Out" (FIFO) dari antrian dicapai dengan mengurutkan data berdasarkan waktu_masuk.

Contoh: Saat tiket habis, sebuah data baru ditambahkan ke tabel waiting_list (proses enqueue). Saat tiket kembali tersedia (karena ada yang membatalkan), data yang paling lama (.order_by(WaitingList.waktu_masuk).first()) akan diambil dan dihapus (proses dequeue).

Stack / Tumpukan (Session-based):

Implementasi: Fitur "Undo Booking" menggunakan Python List yang disimpan di dalam session sebagai sebuah Stack.

Contoh: Setiap kali booking berhasil, ID pemesanan yang baru dibuat akan di-push (dengan .append()) ke puncak stack session['undo_stack']. Saat pengguna menekan tombol "Undo", data terakhir akan di-pop (dengan .pop()) dari stack untuk diproses pembatalannya. Penggunaan session memastikan bahwa stack ini bersifat sementara dan unik untuk setiap pengguna.

3.3. Logika Rute (Routing)
Aplikasi memiliki beberapa grup rute utama:

Rute Publik (/, /wahana/<id>): Dapat diakses oleh siapa saja untuk melihat daftar dan detail wahana.

Rute Autentikasi (/auth, /logout): Mengelola proses registrasi dan login. Saat login berhasil, informasi penting seperti user_id dan user_role disimpan ke dalam session.

Rute Pengguna Terdaftar (/booking, /riwayat, dll.): Memerlukan pengguna untuk login. Proses booking akan memvalidasi sisa tiket dan memutuskan apakah akan memproses pemesanan atau memasukkan pengguna ke Queue.

Rute Admin (/admin/...): Dilindungi oleh decorator @admin_required yang memeriksa apakah session['user_role'] adalah 'admin'. Jika tidak, pengguna akan dialihkan. Rute ini mengelola operasi CRUD (Create, Read, Update, Delete) untuk data wahana dan jadwalnya.

4. Cara Menjalankan Proyek
Prasyarat: Pastikan Anda telah menginstal Python, XAMPP (dengan Apache & MySQL berjalan), dan library yang dibutuhkan (pip install Flask Flask-SQLAlchemy mysql-connector-python passlib).

Database: Buka phpMyAdmin dan jalankan skrip SQL yang tersedia untuk membuat database db_booking_wahana beserta semua tabelnya.

Struktur Folder: Pastikan semua file (app.py, HTML, CSS, images) berada di dalam struktur folder yang benar.

Jalankan Server: Buka terminal, navigasi ke folder proyek (/booking_wahana_final), dan jalankan perintah:

python app.py

Akses Aplikasi: Buka browser web dan kunjungi http://127.0.0.1:5000/.

Saat pertama kali dijalankan, skrip akan secara otomatis membuat akun admin default (admin@wahana.com dengan password admin123) dan mengisi database dengan data wahana awal jika database tersebut kosong.