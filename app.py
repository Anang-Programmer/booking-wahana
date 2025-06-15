from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import time
from passlib.hash import sha256_crypt
import random, string
from functools import wraps
import os
from werkzeug.utils import secure_filename


# --- Inisialisasi & Konfigurasi ---
app = Flask(__name__)
# app.secret_key = 'kunci_rahasia_super_aman_12345'
app.secret_key = 'project_data_structure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/db_booking_wahana'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# === IMPLEMENTASI STRUKTUR DATA: RECORD/CLASS ===
# Model SQLAlchemy ini adalah implementasi nyata dari konsep Record/Class/Struct.
# Setiap class di bawah ini memetakan ke sebuah tabel di database MySQL,
# dan setiap objek dari class ini adalah sebuah record data.
class Pengguna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    tanggal_daftar = db.Column(db.DateTime, default=datetime.utcnow)
    pemesanans = db.relationship('Pemesanan', backref='pengguna', lazy=True)
    waiting_lists = db.relationship('WaitingList', backref='pengguna', lazy=True)
class Wahana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_wahana = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text)
    lokasi = db.Column(db.String(50))
    kapasitas = db.Column(db.Integer)
    gambar_url = db.Column(db.String(255))
    jadwals = db.relationship('JadwalWahana', backref='wahana', lazy=True, cascade="all, delete-orphan")

class JadwalWahana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wahana_id = db.Column(db.Integer, db.ForeignKey('wahana.id'), nullable=False)
    waktu_mulai = db.Column(db.DateTime, nullable=False)
    waktu_selesai = db.Column(db.DateTime, nullable=False)
    sisa_tiket = db.Column(db.Integer, nullable=False)
    tikets = db.relationship('Tiket', backref='jadwal', lazy=True)
    waiting_lists = db.relationship('WaitingList', backref='jadwal', lazy=True)

class Pemesanan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengguna_id = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)
    tanggal_pemesanan = db.Column(db.DateTime, default=datetime.utcnow)
    total_harga = db.Column(db.DECIMAL(10, 2), nullable=False, default=0)
    status_pembayaran = db.Column(db.Enum('Menunggu', 'Lunas', 'Gagal'), default='Lunas')
    tikets = db.relationship('Tiket', backref='pemesanan', lazy=True)

class Tiket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pemesanan_id = db.Column(db.Integer, db.ForeignKey('pemesanan.id'), nullable=False)
    jadwal_id = db.Column(db.Integer, db.ForeignKey('jadwal_wahana.id'), nullable=False)
    kode_booking = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Enum('Aktif', 'Digunakan', 'Batal'), default='Aktif')

# === IMPLEMENTASI STRUKTUR DATA: QUEUE (ANTRIAN) ===
# Kelas WaitingList di bawah ini, bersama dengan logika pemrosesannya, adalah implementasi
# dari struktur data Queue (Antrian) dengan prinsip First-In, First-Out (FIFO).
# - Enqueue (Menambah ke antrian): Terjadi saat pengguna booking tiket yang habis.
#   Sebuah record baru ditambahkan ke tabel WaitingList.
# - Dequeue (Mengambil dari antrian): Terjadi saat tiket kembali tersedia (karena
#   pembatalan atau penambahan oleh admin). Pengguna terdepan dalam antrian
#   (berdasarkan 'waktu_masuk' paling awal) akan diproses lebih dulu.
class WaitingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jadwal_id = db.Column(db.Integer, db.ForeignKey('jadwal_wahana.id'), nullable=False)
    pengguna_id = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)
    waktu_masuk = db.Column(db.DateTime, default=datetime.utcnow)
    
# --- Konfigurasi Baru untuk Upload File ---
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(), 'timedelta': timedelta}    
# === Fungsi Bantuan ===
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# === DECORATOR UNTUK OTORISASI ADMIN ===
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'admin':
            flash('Anda tidak memiliki izin untuk mengakses halaman ini.', 'error')
            return redirect(url_for('halaman_utama'))
        return f(*args, **kwargs)
    return decorated_function

# === RUTE AUTENTIKASI (DIPERBARUI) ===

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Jika pengguna sudah login, langsung arahkan ke halaman utama
    if 'logged_in' in session:
        return redirect(url_for('halaman_utama'))

    error = None  # Siapkan variabel untuk menampung pesan error

    if request.method == 'POST':
        email = request.form.get('email')
        password_candidate = request.form.get('password')

        if not email or not password_candidate:
            error = 'Email dan password harus diisi.'
        else:
            user = Pengguna.query.filter_by(email=email).first()

            if user and sha256_crypt.verify(password_candidate, user.password_hash):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['user_nama'] = user.nama_lengkap
                session['user_role'] = user.role
                
                flash('Anda berhasil login.', 'success')

                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('halaman_utama'))
            else:
                error = 'Email atau password salah. Silakan coba lagi.'

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = Pengguna.query.filter_by(email=email).first()
        if existing_user:
            flash('Email sudah terdaftar, silakan login.', 'error')
            return redirect(url_for('register'))

        password_hash = sha256_crypt.hash(password)
        pengguna_baru = Pengguna(nama_lengkap=nama, email=email, password_hash=password_hash)
        db.session.add(pengguna_baru)
        db.session.commit()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda berhasil logout.', 'info')
    return redirect(url_for('halaman_utama'))

# --- Rute Pengguna Biasa ---

# === IMPLEMENTASI STRUKTUR DATA: ARRAY ===
# Variabel 'daftar_wahana' di bawah ini adalah implementasi dari struktur data Array.
# Saat kita memanggil `Wahana.query.all()`, SQLAlchemy mengembalikan sebuah List Python
# yang berisi objek-objek (records) dari kelas Wahana. List ini berfungsi sebagai
# array dinamis yang menyimpan kumpulan data terurut yang dapat diakses melalui iterasi.
@app.route('/')
def halaman_utama():
    query = request.args.get('q', '')
    if query:
        daftar_wahana = Wahana.query.filter(Wahana.nama_wahana.ilike(f'%{query}%')).all()
    else:
        daftar_wahana = Wahana.query.all()
    return render_template('index.html', daftar_wahana=daftar_wahana)

@app.route('/wahana/<int:id_wahana>')
def detail_wahana(id_wahana):
    wahana = Wahana.query.get_or_404(id_wahana)
    relevant_waiting_lists = {j.id: WaitingList.query.filter_by(jadwal_id=j.id).order_by(WaitingList.waktu_masuk).all() for j in wahana.jadwals}
    return render_template('wahana_detail.html', wahana=wahana, waiting_lists=relevant_waiting_lists)

@app.route('/booking', methods=['POST'])
def proses_booking():
    if not session.get('logged_in'):
        flash('Anda harus login untuk melakukan booking.', 'error')
        return redirect(url_for('auth'))

    id_jadwal = int(request.form['jadwal'])
    jumlah_tiket = int(request.form['jumlah_tiket'])

    jadwal = JadwalWahana.query.get(id_jadwal)

    if jadwal and jadwal.sisa_tiket >= jumlah_tiket:
        jadwal.sisa_tiket -= jumlah_tiket

        pemesanan_baru = Pemesanan(pengguna_id=session['user_id'], total_harga=0)
        db.session.add(pemesanan_baru)
        db.session.commit()

        for _ in range(jumlah_tiket):
            kode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            tiket_baru = Tiket(pemesanan_id=pemesanan_baru.id, jadwal_id=id_jadwal, kode_booking=kode)
            db.session.add(tiket_baru)

        # === IMPLEMENTASI STRUKTUR DATA: STACK (TUMPUKAN) ===
        # Bagian 'undo_stack' ini adalah implementasi dari struktur data Stack
        # dengan prinsip Last-In, First-Out (LIFO).
        # - Push (Mendorong): Terjadi saat sebuah booking berhasil. Data booking
        #   ditambahkan ke akhir list menggunakan `.append()`.
        # - Pop (Mengambil): Fitur undo yang lengkap akan mengambil elemen terakhir
        #   dari stack ini (misalnya dengan `.pop()`) untuk membatalkan aksi terakhir.
        if 'undo_stack' not in session:
            session['undo_stack'] = []
        undo_data = {'pemesanan_id': pemesanan_baru.id, 'timestamp': time.time()}
        temp_stack = session.get('undo_stack', [])
        temp_stack.append(undo_data)
        session['undo_stack'] = temp_stack

        db.session.commit()
        flash(f'Booking {jumlah_tiket} tiket berhasil!', 'success')
        return redirect(url_for('detail_wahana', id_wahana=jadwal.wahana_id))
    else:
        # Cek apakah sudah mengantri
        sudah_mengantri = WaitingList.query.filter_by(jadwal_id=id_jadwal, pengguna_id=session['user_id']).first()
        if sudah_mengantri:
            flash('Anda sudah ada dalam daftar tunggu untuk jadwal ini.', 'warning')
            return redirect(url_for('detail_wahana', id_wahana=jadwal.wahana_id))

        antrian = WaitingList(jadwal_id=id_jadwal, pengguna_id=session['user_id'], waktu_masuk=datetime.utcnow())
        db.session.add(antrian)
        db.session.commit()
        flash('Tiket habis! Anda telah ditambahkan ke daftar tunggu.', 'info')
        return redirect(url_for('detail_wahana', id_wahana=jadwal.wahana_id))


@app.route('/batal/<int:pemesanan_id>', methods=['POST'])
def batal_booking(pemesanan_id):
    if not session.get('logged_in'):
        return redirect(url_for('auth'))

    pemesanan = Pemesanan.query.get_or_404(pemesanan_id)

    if pemesanan.pengguna_id != session['user_id']:
        flash('Anda tidak memiliki izin untuk membatalkan pesanan ini.', 'error')
        return redirect(url_for('riwayat_booking'))

    BATAS_WAKTU_DETIK = 120
    selisih_waktu = datetime.utcnow() - pemesanan.tanggal_pemesanan

    if selisih_waktu < timedelta(seconds=BATAS_WAKTU_DETIK):
        jumlah_tiket = len(pemesanan.tikets)
        jadwal = pemesanan.tikets[0].jadwal
        jadwal.sisa_tiket += jumlah_tiket

        # Distribusi tiket ke antrian
        antrian_list = WaitingList.query.filter_by(jadwal_id=jadwal.id).order_by(WaitingList.waktu_masuk).limit(jumlah_tiket).all()
        tiket_tersedia = jumlah_tiket

        for antrian in antrian_list:
            if tiket_tersedia <= 0:
                break

            pengguna_id = antrian.pengguna_id
            nama_pengguna = antrian.pengguna.nama_lengkap  # Akses nama lengkap dari relasi

            pemesanan_baru = Pemesanan(pengguna_id=pengguna_id, total_harga=0)
            db.session.add(pemesanan_baru)
            db.session.commit()

            kode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            tiket_baru = Tiket(pemesanan_id=pemesanan_baru.id, jadwal_id=jadwal.id, kode_booking=kode)
            db.session.add(tiket_baru)

            db.session.delete(antrian)
            jadwal.sisa_tiket -= 1
            tiket_tersedia -= 1

            flash(f'Tiket otomatis diberikan ke {nama_pengguna}', 'info')


        # Hapus semua tiket & pesanan pembatal
        for tiket in pemesanan.tikets:
            db.session.delete(tiket)
        db.session.delete(pemesanan)

        db.session.commit()
        flash(f'Pemesanan dibatalkan. {jumlah_tiket} tiket dikembalikan.', 'success')
    else:
        flash('Batas waktu untuk membatalkan pesanan telah habis.', 'error')

    return redirect(url_for('riwayat_booking'))

@app.route('/riwayat')
def riwayat_booking():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    pemesanan_user = Pemesanan.query.filter_by(pengguna_id=session['user_id']).order_by(Pemesanan.tanggal_pemesanan.desc()).all()
    return render_template('riwayat.html', riwayat=pemesanan_user)


@app.route('/tiket/<int:id>')
def cetak_tiket(id):
    if not session.get('logged_in'):
        flash('Anda harus login untuk melihat tiket.', 'error')
        return redirect(url_for('login'))

    tiket = Tiket.query.get_or_404(id)

    if tiket.pemesanan.pengguna_id != session['user_id'] and session.get('user_role') != 'admin':
        flash('Anda tidak memiliki izin untuk mengakses tiket ini.', 'error')
        return redirect(url_for('halaman_utama'))

    return render_template('tiket.html', tiket=tiket)

@app.route('/daftar_tunggu')
def daftar_tunggu_saya():
    if not session.get('logged_in'):
        return redirect(url_for('auth'))

    # ambil antrian yang masih ada (belum diproses)
    daftar_tunggu_user = (
        WaitingList.query
        .filter_by(pengguna_id=session['user_id'])
        .join(JadwalWahana)
        .order_by(WaitingList.waktu_masuk)
        .all()
    )

    return render_template('daftar_tunggu.html', daftar_tunggu=daftar_tunggu_user)


# === RUTE KHUSUS ADMIN ===
@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_wahana = Wahana.query.count()
    total_pengguna = Pengguna.query.filter_by(role='user').count()
    total_booking = Pemesanan.query.count()
    return render_template('admin/dashboard.html', total_wahana=total_wahana, total_pengguna=total_pengguna, total_booking=total_booking)

@app.route('/admin/wahana')
@admin_required
def admin_kelola_wahana():
    semua_wahana = Wahana.query.all()
    return render_template('admin/kelola_wahana.html', daftar_wahana=semua_wahana)

@app.route('/admin/wahana/tambah', methods=['GET', 'POST'])
@admin_required
def admin_tambah_wahana():
    if request.method == 'POST':
        # --- Logika Upload Gambar Dimulai Di Sini ---
        gambar_file = request.files['gambar_file']
        filename = ''
        if gambar_file and allowed_file(gambar_file.filename):
            filename = secure_filename(gambar_file.filename)
            gambar_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # --- Logika Upload Gambar Selesai ---

        wahana_baru = Wahana(
            nama_wahana=request.form['nama_wahana'],
            deskripsi=request.form['deskripsi'],
            lokasi=request.form['lokasi'],
            kapasitas=request.form['kapasitas'],
            gambar_url=filename  # Simpan nama file ke database
        )
        db.session.add(wahana_baru)
        db.session.commit()
        flash('Wahana baru berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_kelola_wahana'))
    return render_template('admin/form_wahana.html', form_title='Tambah Wahana Baru', wahana=None)

@app.route('/admin/wahana/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_wahana(id):
    wahana = Wahana.query.get_or_404(id)
    if request.method == 'POST':
        # --- Logika Upload Gambar untuk Edit ---
        gambar_file = request.files['gambar_file']
        if gambar_file and allowed_file(gambar_file.filename):
            filename = secure_filename(gambar_file.filename)
            gambar_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Update nama file gambar jika ada file baru yang diupload
            wahana.gambar_url = filename
        
        # Update data lainnya
        wahana.nama_wahana = request.form['nama_wahana']
        wahana.deskripsi = request.form['deskripsi']
        wahana.lokasi = request.form['lokasi']
        wahana.kapasitas = request.form['kapasitas']
        db.session.commit()
        flash('Data wahana berhasil diperbarui!', 'success')
        return redirect(url_for('admin_kelola_wahana'))
    return render_template('admin/form_wahana.html', form_title='Edit Wahana', wahana=wahana)

@app.route('/admin/wahana/hapus/<int:id>', methods=['POST'])
@admin_required
def admin_hapus_wahana(id):
    wahana = Wahana.query.get_or_404(id)
    db.session.delete(wahana)
    db.session.commit()
    flash('Wahana berhasil dihapus.', 'success')
    return redirect(url_for('admin_kelola_wahana'))

@app.route('/admin/jadwal/tambah/<int:id_wahana>', methods=['POST'])
@admin_required
def admin_tambah_jadwal(id_wahana):
    jadwal_baru = JadwalWahana(
        wahana_id=id_wahana,
        waktu_mulai=datetime.strptime(request.form['waktu_mulai'], '%Y-%m-%dT%H:%M'),
        waktu_selesai=datetime.strptime(request.form['waktu_selesai'], '%Y-%m-%dT%H:%M'),
        sisa_tiket=request.form['sisa_tiket'])
    db.session.add(jadwal_baru)
    db.session.commit()
    flash('Jadwal baru berhasil ditambahkan.', 'success')
    return redirect(url_for('admin_edit_wahana', id=id_wahana))

@app.route('/admin/jadwal/edit/<int:id>', methods=['POST'])
@admin_required
def admin_edit_jadwal(id):
    jadwal = JadwalWahana.query.get_or_404(id)
    
    try:
        jadwal.waktu_mulai = datetime.strptime(request.form['waktu_mulai'], '%Y-%m-%dT%H:%M')
        jadwal.waktu_selesai = datetime.strptime(request.form['waktu_selesai'], '%Y-%m-%dT%H:%M')
        sisa_tiket_baru = int(request.form['sisa_tiket'])

        # Hitung selisih tiket yang ditambahkan
        selisih_tiket = sisa_tiket_baru - jadwal.sisa_tiket
        jadwal.sisa_tiket = sisa_tiket_baru

        db.session.commit()
        flash('Jadwal berhasil diperbarui.', 'success')

        # Jika ada tiket yang ditambahkan, distribusikan ke daftar tunggu
        if selisih_tiket > 0:
            antrian_list = (
                WaitingList.query
                .filter_by(jadwal_id=jadwal.id)
                .order_by(WaitingList.waktu_masuk)
                .limit(selisih_tiket)
                .all()
            )

            tiket_tersedia = selisih_tiket
            for antrian in antrian_list:
                if tiket_tersedia <= 0:
                    break

                pengguna_id = antrian.pengguna_id
                nama_pengguna = antrian.pengguna.nama_lengkap

                pemesanan_baru = Pemesanan(pengguna_id=pengguna_id, total_harga=0)
                db.session.add(pemesanan_baru)
                db.session.commit()

                kode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                tiket_baru = Tiket(pemesanan_id=pemesanan_baru.id, jadwal_id=jadwal.id, kode_booking=kode)
                db.session.add(tiket_baru)

                db.session.delete(antrian)
                jadwal.sisa_tiket -= 1
                tiket_tersedia -= 1

                flash(f'Tiket otomatis diberikan ke {nama_pengguna} dari daftar tunggu.', 'info')

            db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui jadwal: {e}', 'error')

    return redirect(url_for('admin_edit_wahana', id=jadwal.wahana_id))


@app.route('/admin/jadwal/hapus/<int:id>', methods=['POST'])
@admin_required
def admin_hapus_jadwal(id):
    jadwal = JadwalWahana.query.get_or_404(id)
    id_wahana = jadwal.wahana_id
    db.session.delete(jadwal)
    db.session.commit()
    flash('Jadwal berhasil dihapus.', 'success')
    return redirect(url_for('admin_edit_wahana', id=id_wahana))

# --- RUTE BARU UNTUK MANAJEMEN PENGGUNA ---
@app.route('/admin/pengguna')
@admin_required
def admin_kelola_pengguna():
    """Menampilkan daftar semua pengguna."""
    daftar_pengguna = Pengguna.query.order_by(Pengguna.tanggal_daftar.desc()).all()
    return render_template('admin/kelola_pengguna.html', daftar_pengguna=daftar_pengguna)

# --- RUTE BARU UNTUK MANAJEMEN PEMESANAN ---
@app.route('/admin/pemesanan')
@admin_required
def admin_kelola_pemesanan():
    """Menampilkan daftar semua pemesanan."""
    semua_pemesanan = Pemesanan.query.order_by(Pemesanan.tanggal_pemesanan.desc()).all()
    return render_template('admin/kelola_pemesanan.html', semua_pemesanan=semua_pemesanan)

@app.route('/admin/pemesanan/<int:id>')
@admin_required
def admin_detail_pemesanan(id):
    """Menampilkan detail tiket dari sebuah pemesanan."""
    pemesanan = Pemesanan.query.get_or_404(id)
    return render_template('admin/detail_pemesanan.html', pemesanan=pemesanan)

# --- Fungsi Inisialisasi Database ---
def init_db():
    with app.app_context():
        db.create_all()
        # Cek jika user admin belum ada, maka buat.
        if not Pengguna.query.filter_by(email='admin@wahana.com').first():
            admin_hash = sha256_crypt.hash('admin123')
            new_admin = Pengguna(nama_lengkap='Admin', email='admin@wahana.com', password_hash=admin_hash, role='admin')
            db.session.add(new_admin)
            print("Akun admin berhasil dibuat.")

        # Cek jika wahana kosong, maka isi data awal
        if Wahana.query.count() == 0:
            wahana_data = [
                Wahana(nama_wahana='Roller Coaster Halilintar', deskripsi='Rasakan kecepatan kilat.', lokasi='Zona Adrenalin', kapasitas=20, gambar_url='coaster.jpg'),
                Wahana(nama_wahana='Istana Boneka Nusantara', deskripsi='Perjalanan magis budaya Indonesia.', lokasi='Zona Anak', kapasitas=30, gambar_url='doll_palace.jpg'),
                Wahana(nama_wahana='Arung Jeram Niagara', deskripsi='Terjang ombak.', lokasi='Zona Air', kapasitas=8, gambar_url='rafting.jpg')
            ]
            db.session.bulk_save_objects(wahana_data)
            db.session.commit()
            
            jadwal_data = [    
                JadwalWahana(wahana_id=1, waktu_mulai=datetime.strptime('2025-07-15 10:00', '%Y-%m-%d %H:%M'), waktu_selesai=datetime.strptime('2025-07-15 10:30', '%Y-%m-%d %H:%M'), sisa_tiket=1),
                JadwalWahana(wahana_id=1, waktu_mulai=datetime.strptime('2025-07-15 10:30', '%Y-%m-%d %H:%M'), waktu_selesai=datetime.strptime('2025-07-15 11:00', '%Y-%m-%d %H:%M'), sisa_tiket=10),
                JadwalWahana(wahana_id=2, waktu_mulai=datetime.strptime('2025-07-15 11:00', '%Y-%m-%d %H:%M'), waktu_selesai=datetime.strptime('2025-07-15 11:20', '%Y-%m-%d %H:%M'), sisa_tiket=0)
            ]
            db.session.bulk_save_objects(jadwal_data)
            print("Data awal wahana & jadwal telah diinisialisasi.")
        
        db.session.commit()

if __name__ == '__main__':
    # Memindahkan init_db ke dalam blok ini memastikan konteks aplikasi sudah ada
    init_db()
    app.run(debug=True, host='0.0.0.0')