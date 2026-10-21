LAPORAN PRAKTIKUM
SISTEM TERDISTRIBUSI DAN TERDESENTRALISASI
MODUL 3
SINKRONISASI PADA SISTEM TERDISTRIBUSI

Disusun untuk memenuhi tugas praktikum

Disusun oleh:

Nama: Rafael Natalino Soumokil

NIM: 255410022

Program Studi Informatika

UNIVERSITAS TEKNOLOGI DIGITAL INDONESIA

Yogyakarta

2026

Catatan: halaman sampul ini merupakan draft. Pastikan logo sesuai dengan logo resmi kampus sebelum laporan dikumpulkan.
KATA PENGANTAR
Puji syukur kepada Tuhan Yang Maha Esa karena atas rahmat-Nya, laporan Praktikum Sistem Terdistribusi dan Terdesentralisasi Modul 3 yang berjudul “Sinkronisasi pada Sistem Terdistribusi” dapat disusun.

Laporan ini dibuat untuk memenuhi tugas praktikum serta menambah pemahaman mengenai sinkronisasi waktu, vector clock, permasalahan pada sistem tanpa sinkronisasi, dan algoritma Raft. Melalui praktikum ini, mahasiswa diharapkan dapat memahami cara kerja sinkronisasi dan penerapannya menggunakan program Python.

Penulis menyadari bahwa laporan ini masih memiliki kekurangan. Oleh karena itu, kritik dan saran diperlukan untuk perbaikan laporan selanjutnya.

Yogyakarta, Oktober 2026

Penulis
DAFTAR ISI
1. BAB I Pendahuluan
2. BAB II Dasar Teori
3. BAB III Pelaksanaan Praktikum
   - 3.1 Sinkronisasi Waktu
   - 3.2 Vector Clock
   - 3.3 Problem Tanpa Sinkronisasi
   - 3.3.1 Data Race / Race Conditions
   - 3.3.2 Deadlock
   - 3.4 Algoritma Raft
4. BAB IV Penutup
5. Daftar Pustaka
6. Lampiran Dokumentasi

BAB I — PENDAHULUAN
1.1 Latar Belakang
Sistem terdistribusi merupakan sistem yang terdiri dari beberapa komputer atau proses yang saling berkomunikasi untuk menjalankan suatu pekerjaan. Dalam sistem ini, sinkronisasi diperlukan agar proses dapat berjalan dengan teratur dan data tetap konsisten.

Tanpa sinkronisasi yang baik, sistem dapat mengalami berbagai masalah, seperti perbedaan waktu, data race, dan deadlock. Selain itu, sistem terdistribusi juga membutuhkan mekanisme untuk menentukan pemimpin atau leader agar koordinasi antarproses dapat dilakukan dengan baik.

Oleh karena itu, praktikum Modul 3 membahas sinkronisasi waktu, vector clock, permasalahan akibat tidak adanya sinkronisasi, serta algoritma Raft untuk memahami penerapan konsep tersebut.
1.2 Tujuan Praktikum
1. Memahami proses sinkronisasi waktu menggunakan protokol NTP.
2. Memahami cara kerja vector clock untuk mengurutkan event.
3. Mengamati perbedaan keluaran program multithread.
4. Memahami penyebab dan pencegahan data race.
5. Memahami penyebab dan pencegahan deadlock.
6. Memahami cara kerja algoritma Raft dalam pemilihan leader.
7. Membuat modul Python dan contoh penggunaannya sesuai tugas pada modul.
1.3 Manfaat Praktikum
Praktikum ini memberikan pemahaman dasar tentang koordinasi proses pada sistem terdistribusi. Mahasiswa juga dapat melatih kemampuan menggunakan Python untuk mempelajari sinkronisasi, pengelolaan thread, dan simulasi pemilihan leader.
BAB II — DASAR TEORI
2.1 Sinkronisasi Waktu
Sinkronisasi waktu merupakan proses menyamakan waktu pada komputer dengan sumber waktu yang dijadikan acuan. Modul menjelaskan dua protokol yang biasa digunakan, yaitu NTP (Network Time Protocol) dan PTP (Precision Time Protocol).

Pada sistem Windows, modul menggunakan NetTime sebagai perangkat lunak untuk melakukan sinkronisasi dengan server NTP. Pada Linux, BSD, atau macOS, modul mengarahkan penggunaan Chrony.
2.2 Vector Clock
Vector clock merupakan metode untuk membantu menentukan hubungan urutan antar-event dalam sistem terdistribusi. Setiap proses memiliki nilai clock yang diperbarui ketika suatu event terjadi. Ketika pesan dikirim atau diterima, informasi clock digunakan untuk memperbarui hubungan waktu logis antarproses.

Berbeda dari jam biasa, vector clock membantu menunjukkan hubungan sebab-akibat antar-event tanpa harus bergantung pada kesamaan waktu fisik seluruh komputer.
2.3 Problem Tanpa Sinkronisasi
Pada sistem yang menjalankan beberapa thread atau proses secara bersamaan, urutan penyelesaian pekerjaan tidak selalu dapat diprediksi. Modul membahas dua masalah utama, yaitu data race atau race condition dan deadlock.
2.4 Data Race / Race Condition
Data race atau race condition dapat terjadi ketika beberapa thread mengakses atau mengubah data yang sama tanpa pengaturan sinkronisasi yang tepat. Hasil akhir dapat berbeda bergantung pada urutan eksekusi setiap thread.

Penggunaan mekanisme sinkronisasi, seperti lock, dapat membantu mengatur akses ke data bersama.
2.5 Deadlock
Deadlock adalah kondisi ketika beberapa thread atau proses saling menunggu sumber daya yang sedang dipegang oleh pihak lain. Akibatnya, proses yang terlibat tidak dapat melanjutkan pekerjaannya.

Pengaturan urutan pengambilan lock dan pengelolaan sumber daya yang tepat dapat mengurangi risiko terjadinya deadlock.
2.6 Algoritma Raft
Raft adalah algoritma konsensus yang digunakan untuk membantu beberapa node dalam sistem terdistribusi mencapai kesepakatan. Salah satu bagian pentingnya adalah pemilihan leader yang bertugas mengoordinasikan proses tertentu dalam cluster.

Dokumen Word sudah dibuat dan bisa kamu edit langsung.

Draft Laporan Praktikum Modul 3

Word (.docx) · Bisa diedit

Berisi sampul, kata pengantar, dasar teori, pembahasan setiap praktik, kesimpulan, dan lampiran dokumentasi.


Download Draft Laporan Modul 3 (.docx)

Bagian yang perlu kamu lengkapi
- Sinkronisasi waktu: screenshot NetTime atau Chrony dan hasil sinkronisasi.
- Vector Clock: screenshot keluaran program, perhitungan manual, serta kode modul Python.
- Multithread dan data race: screenshot hasil program dan visualisasi manual.
- Deadlock: screenshot kedua program dan gambar penjelasan prosesnya.
- Algoritma Raft: screenshot simulasi, gambar pemilihan leader, dan kode modul Python.
Catatan: dokumen ini masih berupa draft laporan. Hasil eksekusi dan screenshot belum dimasukkan karena harus sesuai dengan program yang benar-benar dijalankan.
