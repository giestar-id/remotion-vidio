# Workspace Guidelines: Video YouTube & Documentary Remotion

Petunjuk baku dan aturan kerja khusus untuk pembuatan video dokumenter & YouTube di repositori ini.

---

## Standar Baku Analisis Semantik Audio-Visual & Naskah

1. **Wajib Analisis Mendalam Sebelum Finalisasi Timeline**:
   - Jangan pernah mengandalkan potongan baris tabel mentah 1-ke-1 secara membabi buta.
   - Penulis naskah sering memotong satu kalimat narasi utuh ke dalam baris tabel berikutnya, sehingga subjek visual untuk adegan `Scene N` sering kali sudah mulai diucapkan pada klausa akhir baris `Scene N-1`.

2. **Transisi Maju Subjek Visual**:
   - Jika visual `Scene N` menggambarkan subjek yang sudah mulai diucapkan di akhir naskah `Scene N-1` (contoh: baris 2 *"dan padang pasir yang membakar, sebuah bangsa peradaban kuno"* di mana gambar benteng peradaban kuno adalah `Scene 3`), **WAJIB majukan kemunculan gambar `Scene N` tepat pada jeda napas (*speech pause*) saat subjek tersebut mulai diucapkan**.

3. **Invarian "Jangan Sampai Miss"**:
   - Seluruh adegan dari `Scene 1` hingga `Scene` terakhir **wajib tetap ada dan tampil berurutan**.
   - Adegan sebelumnya (`Scene N-1`) tidak boleh terlewat atau memiliki durasi terlalu pendek (pertahankan durasi minimal yang proporsional dan nyaman ditonton, >= 1,5 – 2,0 detik).

4. **Snap ke Jeda Napas Alami (*Natural Speech Pauses*)**:
   - Titik pergantian adegan harus selalu dikunci pada celah hening antarkata (gap audio >= 150–200 ms), bukan memotong kata atau fonem di tengah pengucapan.

5. **Kontinuitas Total 100% (*Zero Dead-Air*)**:
   - `timeline.json` harus 100% bersambung dari `0 ms` hingga akhir audio tanpa celah kosong (*gap*) maupun tumpang tindih (*overlap*).

6. **Branding & Identitas Visual Baku**:
   - Header kiri atas: Judul topik utama (misal: `SEJARAH PERSIA`, `SEJARAH ROMA`, `SEJARAH CHINA`).
   - Header kanan atas: `ZEELACUNA`.
   - Tanpa intro title card pembuka; langsung masuk ke scene 1.
   - Tanpa kartu era lower-third yang muncul berulang kali (`eraMarkers: []`).
