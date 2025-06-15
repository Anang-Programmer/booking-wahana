document.addEventListener('DOMContentLoaded', () => {
    // Cari semua sel di tabel yang memiliki data waktu pembatalan
    const actionCells = document.querySelectorAll('.cancellation-cell');

    if (actionCells.length > 0) {
        // Jalankan fungsi update setiap detik
        const intervalId = setInterval(() => {
            let activeTimersCount = 0;

            actionCells.forEach(cell => {
                const endTimeISO = cell.dataset.cancellationEnd;
                if (!endTimeISO) return;

                const endTime = new Date(endTimeISO);
                const now = new Date();
                
                // Hitung sisa waktu dalam detik
                const remainingSeconds = Math.round((endTime - now) / 1000);

                const form = cell.querySelector('form');
                const timerText = cell.querySelector('.timer-text');
                const expiredText = cell.querySelector('.status-expired');

                // Jika masih ada sisa waktu
                if (remainingSeconds > 0) {
                    activeTimersCount++;
                    const minutes = Math.floor(remainingSeconds / 60);
                    const seconds = remainingSeconds % 60;
                    
                    // Format tampilan menjadi MM:SS
                    timerText.textContent = `Bisa dibatalkan dalam: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                    
                    // Tampilkan form dan timer, sembunyikan teks expired
                    if (form) form.style.display = 'block';
                    if (timerText) timerText.style.display = 'block';
                    if (expiredText) expiredText.style.display = 'none';

                } else {
                    // Jika waktu sudah habis
                    if (form) form.style.display = 'none';
                    if (timerText) timerText.style.display = 'none';
                    if (expiredText) expiredText.style.display = 'block';
                }
            });
            
            // Hentikan interval jika semua timer sudah selesai
            if (activeTimersCount === 0) {
                clearInterval(intervalId);
            }

        }, 1000);
    }
});
