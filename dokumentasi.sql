-- Langkah 1: Buat database baru jika belum ada
CREATE DATABASE db_booking_wahana CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Langkah 2: Gunakan database yang baru dibuat
USE db_booking_wahana;

-- Langkah 3: Buat tabel 'pengguna' (dengan kolom 'role')
CREATE TABLE pengguna (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_lengkap VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Langkah 4: Buat tabel 'wahana'
CREATE TABLE wahana (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_wahana VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    lokasi VARCHAR(50),
    kapasitas INT,
    gambar_url VARCHAR(255)
);

-- Langkah 5: Buat tabel 'jadwal_wahana'
CREATE TABLE jadwal_wahana (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wahana_id INT NOT NULL,
    waktu_mulai DATETIME NOT NULL,
    waktu_selesai DATETIME NOT NULL,
    sisa_tiket INT NOT NULL,
    FOREIGN KEY (wahana_id) REFERENCES wahana(id) ON DELETE CASCADE
);

-- Langkah 6: Buat tabel 'pemesanan'
CREATE TABLE pemesanan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pengguna_id INT NOT NULL,
    tanggal_pemesanan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_harga DECIMAL(10, 2) NOT NULL,
    status_pembayaran ENUM('Menunggu', 'Lunas', 'Gagal') DEFAULT 'Lunas',
    FOREIGN KEY (pengguna_id) REFERENCES pengguna(id)
);

-- Langkah 7: Buat tabel 'tiket'
CREATE TABLE tiket (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pemesanan_id INT NOT NULL,
    jadwal_id INT NOT NULL,
    kode_booking VARCHAR(20) NOT NULL UNIQUE,
    status ENUM('Aktif', 'Digunakan', 'Batal') DEFAULT 'Aktif',
    FOREIGN KEY (pemesanan_id) REFERENCES pemesanan(id),
    FOREIGN KEY (jadwal_id) REFERENCES jadwal_wahana(id)
);

-- Langkah 8: Buat tabel 'waiting_list'
CREATE TABLE waiting_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jadwal_id INT NOT NULL,
    pengguna_id INT NOT NULL,
    waktu_masuk TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (jadwal_id) REFERENCES jadwal_wahana(id),
    FOREIGN KEY (pengguna_id) REFERENCES pengguna(id)
);



-- Langkah 1: Buat database baru

CREATE DATABASE db_booking_wahana CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



-- Langkah 2: Gunakan database yang baru dibuat

USE db_booking_wahana;



-- Langkah 3: Buat tabel 'pengguna'

CREATE TABLE pengguna (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nama_lengkap VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Langkah 4: Buat tabel 'wahana'

CREATE TABLE wahana (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nama_wahana VARCHAR(100) NOT NULL,

    deskripsi TEXT,

    lokasi VARCHAR(50),

    kapasitas INT,

    gambar_url VARCHAR(255)

);



-- Langkah 5: Buat tabel 'jadwal_wahana'

CREATE TABLE jadwal_wahana (

    id INT AUTO_INCREMENT PRIMARY KEY,

    wahana_id INT NOT NULL,

    waktu_mulai DATETIME NOT NULL,

    waktu_selesai DATETIME NOT NULL,

    sisa_tiket INT NOT NULL,

    FOREIGN KEY (wahana_id) REFERENCES wahana(id) ON DELETE CASCADE

);



-- Langkah 6: Buat tabel 'pemesanan' (transaksi)

CREATE TABLE pemesanan (

    id INT AUTO_INCREMENT PRIMARY KEY,

    pengguna_id INT NOT NULL,

    tanggal_pemesanan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    total_harga DECIMAL(10, 2) NOT NULL,

    status_pembayaran ENUM('Menunggu', 'Lunas', 'Gagal') DEFAULT 'Menunggu',

    FOREIGN KEY (pengguna_id) REFERENCES pengguna(id)

);



-- Langkah 7: Buat tabel 'tiket'

-- Satu pemesanan bisa memiliki banyak tiket

CREATE TABLE tiket (

    id INT AUTO_INCREMENT PRIMARY KEY,

    pemesanan_id INT NOT NULL,

    jadwal_id INT NOT NULL,

    kode_booking VARCHAR(20) NOT NULL UNIQUE,

    status ENUM('Aktif', 'Digunakan', 'Batal') DEFAULT 'Aktif',

    FOREIGN KEY (pemesanan_id) REFERENCES pemesanan(id),

    FOREIGN KEY (jadwal_id) REFERENCES jadwal_wahana(id)

);



-- (Opsional) Langkah 8: Buat tabel 'waiting_list' jika Anda ingin menyimpannya di DB

CREATE TABLE waiting_list (

    id INT AUTO_INCREMENT PRIMARY KEY,

    jadwal_id INT NOT NULL,

    pengguna_id INT NOT NULL,

    waktu_masuk TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (jadwal_id) REFERENCES jadwal_wahana(id),

    FOREIGN KEY (pengguna_id) REFERENCES pengguna(id)

);