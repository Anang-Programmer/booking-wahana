document.addEventListener('DOMContentLoaded', () => {
    // Cek apakah kita berada di halaman detail wahana
    if (typeof WAHANA_ID !== 'undefined') {
        const jadwalSelect = document.getElementById('jadwal');
        
        // Ambil data jadwal dari API yang sudah kita buat di Flask
        fetch(`/api/jadwal/${WAHANA_ID}`)
            .then(response => response.json())
            .then(data => {
                // Hapus opsi "Memuat jadwal..."
                jadwalSelect.innerHTML = '';
                
                if (data.error) {
                    jadwalSelect.innerHTML = `<option value="">${data.error}</option>`;
                    return;
                }
                
                // Tambahkan setiap jadwal ke dalam dropdown
                data.forEach(jadwal => {
                    const option = document.createElement('option');
                    option.value = jadwal.jadwal_id;
                    option.textContent = `${jadwal.waktu} (Sisa: ${jadwal.sisa_tiket} tiket)`;
                    jadwalSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching jadwal:', error);
                jadwalSelect.innerHTML = '<option value="">Gagal memuat jadwal</option>';
            });
    }
});