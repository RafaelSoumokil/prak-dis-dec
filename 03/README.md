LAPORAN PRAKTIKUM
SISTEM TERDISTRIBUSI DAN TERDESENTRALISASI
MODUL 3
SINKRONISASI PADA SISTEM TERDISTRIBUSI
Disusun oleh:

Rafael Natalino Soumokil

NIM: 255410022

Program Studi Informatika

Universitas Teknologi Digital Indonesia

2026


BAB I. PENDAHULUAN
1.1 Latar Belakang
Sistem terdistribusi merupakan sistem yang terdiri dari beberapa komputer atau proses yang saling berkomunikasi untuk menjalankan suatu tugas. Dalam sistem ini, sinkronisasi sangat penting agar proses dapat berjalan dengan teratur dan data tetap konsisten.

Tanpa sinkronisasi yang baik, sistem dapat mengalami masalah seperti race condition dan deadlock. Selain itu, sistem terdistribusi membutuhkan metode untuk mengurutkan kejadian, menyamakan waktu, dan menentukan koordinator ketika beberapa komputer bekerja bersama.

Pada praktikum Modul 3 ini, mahasiswa mempelajari sinkronisasi waktu, vector clock, masalah sinkronisasi pada program multithread, serta algoritma Raft untuk pemilihan pemimpin atau leader.
1.2 Tujuan Praktikum
1. Memahami proses sinkronisasi waktu menggunakan NTP.
2. Memahami cara kerja vector clock untuk mengurutkan kejadian.
3. Mengetahui penyebab terjadinya race condition dan deadlock.
4. Memahami penggunaan mekanisme sinkronisasi untuk mencegah masalah pada program multithread.
5. Memahami cara kerja algoritma Raft dalam pemilihan leader.
6. Membuat modul Python sederhana berdasarkan program yang dipelajari.
1.3 Manfaat Praktikum
1. Menambah pemahaman mengenai konsep sinkronisasi dalam sistem terdistribusi.
2. Melatih kemampuan menjalankan dan menganalisis program Python.
3. Mengetahui cara mengatasi masalah yang terjadi akibat proses berjalan secara bersamaan.
4. Memahami dasar pemilihan koordinator dalam sistem terdistribusi.
   <img width="757" height="539" alt="image" src="https://github.com/user-attachments/assets/839b06e9-2314-4ecb-869f-c3905fded9be" />


BAB II. DASAR TEORI
2.1 Sinkronisasi Waktu
Sinkronisasi waktu adalah proses menyamakan waktu pada beberapa komputer agar memiliki acuan waktu yang sesuai. Dalam sistem terdistribusi, sinkronisasi waktu diperlukan untuk membantu pencatatan aktivitas dan pengurutan kejadian.

Dua protokol yang digunakan untuk sinkronisasi waktu adalah:
- NTP (Network Time Protocol): protokol untuk menyinkronkan waktu komputer melalui jaringan.
- PTP (Precision Time Protocol): protokol yang dirancang untuk sinkronisasi waktu dengan tingkat presisi tinggi.
Pada sistem operasi Windows, praktikum menggunakan aplikasi NetTime. Sementara itu, Linux, BSD, dan macOS dapat menggunakan Chrony sesuai petunjuk modul.
2.2 Vector Clock
Vector clock merupakan metode untuk mengetahui urutan kejadian dalam sistem terdistribusi. Setiap proses memiliki vektor yang menyimpan informasi logis mengenai kejadian yang telah berlangsung.

Ketika suatu kejadian terjadi, nilai pada vektor diperbarui. Ketika proses menerima pesan dari proses lain, nilai vektor dibandingkan dan diperbarui untuk menggambarkan hubungan antarkejadian.

Dengan metode ini, kita dapat mengetahui apakah suatu kejadian terjadi sebelum kejadian lain atau kedua kejadian tersebut tidak memiliki hubungan urutan yang pasti.
2.3 Masalah Tanpa Sinkronisasi
Pada sistem yang menjalankan beberapa proses secara bersamaan, urutan eksekusi tidak selalu dapat dipastikan. Hal ini dapat menimbulkan beberapa masalah.
2.3.1 Data Race / Race Condition
Race condition terjadi ketika beberapa thread mengakses atau mengubah data yang sama secara bersamaan sehingga hasil program dapat bergantung pada urutan eksekusi thread.

Salah satu cara untuk mengatasinya adalah menggunakan mekanisme penguncian (lock), sehingga bagian program yang mengakses data bersama tidak dijalankan secara bersamaan oleh thread yang berbeda.
2.3.2 Deadlock
Deadlock merupakan keadaan ketika dua atau lebih proses saling menunggu sumber daya yang sedang dikunci oleh proses lainnya. Akibatnya, proses-proses tersebut tidak dapat melanjutkan pekerjaannya.

Deadlock dapat dicegah dengan pengaturan penggunaan lock yang konsisten dan pengendalian urutan pengambilan sumber daya.
2.4 Algoritma Raft
Raft merupakan algoritma konsensus yang digunakan untuk membantu beberapa node dalam sistem terdistribusi mencapai kesepakatan.

Raft menggunakan tiga peran utama:
1. Follower: menerima informasi dan mengikuti pemimpin.
2. Candidate: mengajukan diri menjadi pemimpin ketika pemimpin tidak tersedia.
3. Leader: mengoordinasikan proses dan komunikasi dengan node lainnya.
Pemilihan pemimpin dilakukan melalui proses pemungutan suara (election). Candidate yang memperoleh dukungan mayoritas sesuai ketentuan Raft dapat menjadi leader.
BAB III. ALAT DAN BAHAN
Alat dan bahan yang digunakan dalam praktikum ini meliputi:
No.	Alat dan bahan	Keterangan
1	Laptop atau komputer	Menjalankan praktikum
2	Sistem operasi Windows atau Linux	Lingkungan praktikum
3	Python	Menjalankan program praktikum
4	Editor kode	Visual Studio Code atau editor sejenis
5	Koneksi internet	Diperlukan untuk sinkronisasi NTP
6	Modul Praktikum 3	Panduan pengerjaan
7	Aplikasi NetTime atau Chrony	Sinkronisasi waktu sesuai sistem operasi

BAB IV. LANGKAH KERJA DAN PEMBAHASAN
4.1 Praktik 1 — Sinkronisasi Waktu
Langkah kerja
1. Menyiapkan komputer dan koneksi internet.
2. Mengunduh serta memasang NetTime apabila menggunakan Windows.
3. Membuka aplikasi NetTime dan menentukan server NTP sesuai konfigurasi yang tersedia.
4. Menjalankan proses sinkronisasi waktu.
5. Mengamati status sinkronisasi dan mencatat hasilnya.
6. Mengambil screenshot sebagai bukti praktikum.
Penjelasan hasil praktikum:

Sinkronisasi waktu dilakukan dengan menghubungkan komputer ke server NTP. Komputer memperoleh informasi waktu dari server tersebut, kemudian menyesuaikan jam sistem berdasarkan hasil sinkronisasi. Proses ini membantu komputer menggunakan acuan waktu yang lebih konsisten.

4.2 Praktik 2 — Vector Clock
Langkah kerja
1. Menyiapkan Python dan file vclocks.py dari modul.
2. Menjalankan program menggunakan terminal.
3. Mengamati perubahan nilai vector clock pada setiap proses.
4. Mencatat keluaran program.
5. Membandingkan hasil program dengan perhitungan vector clock secara manual.
Penjelasan hasil praktikum:

Program vector clock digunakan untuk menunjukkan perkembangan kejadian pada beberapa proses. Setiap kejadian menyebabkan perubahan nilai vektor sesuai aturan algoritma. Saat pesan diterima, informasi vektor dari proses pengirim digunakan untuk memperbarui vektor penerima.

Dibandingkan dengan perhitungan manual, program membantu melakukan pembaruan nilai vektor secara otomatis. Perhitungan manual tetap dapat digunakan untuk memeriksa apakah perubahan nilai yang dihasilkan program sudah sesuai dengan aturan algoritma.

Tugas: Membuat modul Python VectorClock
Modul dapat dibuat dengan menyimpan class VectorClock dalam file terpisah. Contoh berikut merupakan implementasi sederhana yang dapat digunakan untuk mempelajari konsepnya.

File vector_clock.py:
class VectorClock:    def __init__(self, jumlah_proses):        self.clock = [0] * jumlah_proses    def increment(self, proses):        self.clock[proses] += 1    def update(self, clock_lain):        self.clock = [            max(a, b)            for a, b in zip(self.clock, clock_lain)        ]    def tampil(self):        print(self.clock)



Contoh penggunaan, simpan sebagai main.py:
from vector_clock import VectorClockvc = VectorClock(3)vc.increment(0)vc.increment(1)print("Vector clock:")vc.tampil()



Keluaran yang diharapkan:
Vector clock:
[1, 1, 0]


Implementasi ini merupakan contoh sederhana untuk memahami class vector clock. Jika tugas mengharuskan modul mengikuti class VectorClock pada file asli vclocks.py, nama metode dan aturan pembaruannya perlu disesuaikan dengan kode tersebut.
4.3 Praktik 3 — Problem Tanpa Sinkronisasi
4.3.1 Program Multithread
Langkah kerja:
1. Membuka file multithreaded-example.py.
2. Menjalankan program beberapa kali.
3. Mengamati perbedaan keluaran pada setiap eksekusi.
4. Mengambil screenshot keluaran yang berbeda.
Penjelasan hasil praktikum:

Program multithread menjalankan beberapa thread yang dapat bekerja secara bersamaan. Urutan eksekusi thread dapat berubah pada setiap percobaan karena pengaturan waktu oleh sistem operasi dan kondisi eksekusi program.

Akibatnya, keluaran program dapat berbeda walaupun kode yang digunakan tetap sama. Hal ini menunjukkan bahwa program multithread tidak selalu menghasilkan urutan eksekusi yang sama.

4.3.2 Data Race / Race Condition
Langkah kerja:
1. Membuka file race-conditions-01.py.
2. Menjalankan program dan mengamati hasilnya.
3. Membuat gambar ilustrasi alur dua thread yang mengakses data bersama.
4. Membuka file race-conditions-02.py.
5. Menjalankan program kedua dan membandingkan hasilnya.
Penjelasan hasil praktikum:

Pada program pertama, dua thread dapat mengakses atau mengubah data yang sama tanpa pengaturan akses yang tepat. Akibatnya, perubahan data dapat saling memengaruhi dan menghasilkan nilai akhir yang tidak sesuai harapan.

Pada program kedua, mekanisme sinkronisasi digunakan untuk mengatur akses terhadap data bersama. Dengan demikian, bagian program yang dilindungi lock dapat dijalankan secara bergantian sehingga risiko race condition berkurang.

Ilustrasi manual yang perlu dibuat:
- Gambar dua thread yang mengakses variabel yang sama.
- Tunjukkan urutan membaca dan menulis data.
- Berikan keterangan bahwa perubahan oleh satu thread dapat tertimpa oleh thread lain.

4.3.3 Deadlock
Langkah kerja:
1. Membuka file deadlock-01.py.
2. Menjalankan program dan mengamati perilakunya.
3. Membuat ilustrasi hubungan antarproses dan sumber daya.
4. Membuka file deadlock-02.py.
5. Menjalankan program kedua dan membandingkan hasilnya.
Penjelasan hasil praktikum:

Deadlock dapat terjadi ketika dua thread memegang lock yang berbeda dan masing-masing menunggu lock yang sedang dipegang oleh thread lainnya. Karena kedua thread terus menunggu, tidak ada thread yang dapat melanjutkan prosesnya.

Program kedua pada modul digunakan untuk mempelajari cara menghindari kondisi tersebut. Penjelasan akhirnya harus disesuaikan dengan teknik pencegahan yang benar-benar diterapkan pada kode deadlock-02.py.

Ilustrasi manual yang perlu dibuat:

Gambarkan dua thread dan dua lock. Tunjukkan bahwa Thread A menunggu Lock B, sedangkan Thread B menunggu Lock A. Beri tanda panah untuk memperlihatkan hubungan menunggu yang membentuk deadlock.

4.4 Praktik 4 — Algoritma Raft
Langkah kerja
1. Membuka file raft.py sesuai modul.
2. Menjalankan program menggunakan Python.
3. Mengamati proses pemilihan leader.
4. Mencatat perubahan status node dan hasil pemungutan suara.
5. Membuat ilustrasi manual proses pemilihan leader.
6. Mengembangkan program menjadi modul Python dan membuat contoh penggunaannya.
Penjelasan hasil praktikum:

Algoritma Raft menggunakan proses pemilihan leader untuk menentukan node yang bertugas mengoordinasikan sistem. Ketika pemilihan dimulai, sebuah node dapat berubah menjadi candidate dan meminta suara dari node lainnya.

Apabila candidate mendapatkan dukungan mayoritas yang diperlukan, node tersebut menjadi leader. Node lainnya bertindak sebagai follower. Leader kemudian mengoordinasikan komunikasi sesuai mekanisme Raft.

Hasil pemilihan yang sebenarnya harus mengikuti keluaran program raft.py yang dijalankan.

Ilustrasi manual yang perlu dibuat:
1. Follower

Belum ada leader yang aktif

2. Candidate

Memulai pemilihan dan meminta suara

3. Pemungutan Suara

Memeriksa apakah dukungan mayoritas tercapai

4. Leader

Mengkoordinasikan node lainnya


Ilustrasi konsep untuk digambar ulang secara manual sesuai instruksi modul.
Tugas: Membuat modul Python Raft
Struktur program dapat dipisahkan menjadi dua file:
praktikum_raft/
├── raft_module.py
└── main.py


File raft_module.py berisi class atau fungsi untuk menjalankan simulasi Raft. File main.py digunakan untuk mengimpor modul dan menjalankan simulasi.

Implementasi perlu mengikuti kode raft.py pada modul asli agar proses pemilihan, jumlah node, dan aturan pemungutan suara tidak berubah.

Bukti praktikum:

BAB V. KESIMPULAN
Berdasarkan materi Modul 3, sinkronisasi merupakan bagian penting dalam sistem terdistribusi. Sinkronisasi waktu membantu komputer menggunakan acuan waktu yang sesuai, sedangkan vector clock digunakan untuk mempelajari urutan kejadian pada beberapa proses.

Pada program multithread, kurangnya pengaturan akses dapat menimbulkan race condition. Sementara itu, deadlock terjadi ketika proses saling menunggu sumber daya sehingga tidak dapat melanjutkan pekerjaan. Kedua masalah tersebut dapat dikurangi melalui mekanisme sinkronisasi yang tepat.

Algoritma Raft digunakan untuk memilih leader melalui proses pemungutan suara. Melalui praktikum ini, mahasiswa diharapkan memahami konsep sinkronisasi dan mampu menerapkannya melalui program Python sederhana.
