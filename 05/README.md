# LAPORAN PRAKTIKUM MODUL 5

## Sistem Terdistribusi dan Terdesentralisasi

### Fault Tolerance

**Nama:** ........................................\
**NIM:** ........................................\
**Program Studi:** ........................................\
**Mata Kuliah:** Sistem Terdistribusi dan Terdesentralisasi

------------------------------------------------------------------------

## 1. Tujuan Praktikum

Praktikum ini bertujuan memahami penerapan *fault tolerance* melalui
Load Balancing, Heartbeat, Retry, dan Circuit Breaker pada sistem
terdistribusi.

## 2. Dasar Teori

### 2.1 Fault Tolerance

*Fault tolerance* adalah kemampuan sistem untuk tetap beroperasi atau
menangani gangguan ketika salah satu komponennya mengalami kegagalan.

### 2.2 Load Balancing

*Load balancing* adalah teknik membagi permintaan pengguna ke beberapa
instance aplikasi. Pada praktikum ini, Nginx digunakan sebagai proxy dan
Docker Compose digunakan untuk menjalankan dua instance aplikasi
Blacksheep.

### 2.3 Heartbeat

*Heartbeat* merupakan mekanisme untuk memantau apakah suatu komponen
masih aktif dan dapat dihubungi. Jika server tidak dapat dihubungi,
komponen tersebut dapat dianggap tidak aktif atau tidak responsif.

### 2.4 Retry

*Retry* adalah mekanisme mencoba kembali suatu permintaan ketika terjadi
kegagalan koneksi. Program praktikum menggunakan Tenacity dengan
maksimal lima percobaan dan jeda yang meningkat secara bertahap.

### 2.5 Circuit Breaker

*Circuit breaker* merupakan pola untuk mencegah aplikasi terus-menerus
mengirim permintaan ke layanan yang mengalami kegagalan. Terdapat tiga
status: - **Closed:** permintaan diizinkan dan kegagalan dipantau. -
**Open:** permintaan diblokir sementara setelah batas kegagalan
tercapai. - **Half-Open:** sejumlah permintaan percobaan diizinkan untuk
memeriksa apakah layanan sudah pulih.

## 3. Alat dan Bahan

1.  Laptop/komputer dengan Windows.
2.  Visual Studio Code.
3.  Docker Desktop dan Docker Compose.
4.  Python.
5.  Aplikasi Blacksheep.
6.  Nginx.
7.  Library Python `tenacity`, `pybreaker`, dan `requests`.

## 4. Langkah Kerja dan Hasil Praktikum

### 4.1 Load Balancing Aplikasi

**A. Menjalankan aplikasi**

Perintah yang digunakan:

``` cmd
docker compose up --build -d --scale bs_app=2
```

Perintah tersebut membangun image, menjalankan layanan di latar
belakang, dan membuat dua instance `bs_app`.

**B. Memeriksa container**

Perintah:

``` cmd
docker compose ps
```

Hasil pengamatan: - Container Nginx berjalan. - Instance
`load-balancing-bs_app-1` berjalan. - Instance `load-balancing-bs_app-2`
berjalan. - Nginx menyediakan akses melalui port 80.

**C. Memeriksa pembagian permintaan**

Perintah:

``` cmd
docker compose logs --tail=30 bs_app
```

Pada log terlihat kedua instance menerima permintaan HTTP dan memberikan
respons `200 OK`. Hal ini menunjukkan bahwa permintaan yang diteruskan
oleh Nginx mencapai kedua instance aplikasi.

Setelah pengujian selesai, container dihentikan menggunakan:

``` cmd
docker compose down
```

Hasilnya, container Nginx, kedua instance aplikasi, dan network Docker
Compose berhasil dihapus.

**Kesimpulan 4.1:** Load Balancing berhasil dijalankan. Dua instance
aplikasi berjalan di belakang Nginx dan keduanya menerima permintaan
berdasarkan log container.

### 4.2 Failure Detection

*Failure detection* merupakan proses untuk menentukan apakah suatu
komponen sistem mengalami kegagalan atau tidak dapat dihubungi.

#### 4.2.1 Heartbeat

Program yang digunakan adalah `heartbeat/check-server.py`. Program
menerima alamat host dan nomor port untuk mencoba membuat koneksi ke
server.

**Pengujian A -- Server tidak aktif**

Perintah:

``` cmd
python check-server.py 127.0.0.1 44777
```

Hasil:

``` text
Server down
```

**Analisis:** Server pada port 44777 belum berjalan sehingga koneksi
tidak berhasil dibuat. Program menampilkan `Server down`.

**Pengujian B -- Server aktif**

Aplikasi Blacksheep dijalankan menggunakan:

``` cmd
python dev.py
```

Server berjalan pada `http://localhost:44777/`. Kemudian pemeriksaan
dijalankan kembali:

``` cmd
python check-server.py 127.0.0.1 44777
```

Hasil:

``` text
Server up
```

**Analisis:** Server aktif dan dapat menerima koneksi pada port 44777.
Program menampilkan `Server up`.

**Kesimpulan Heartbeat:** Program berhasil membedakan kondisi server
yang tidak aktif dan server yang aktif.

#### 4.2.2 Retry

Program `failure-detection/check-retry.py` menggunakan library Tenacity
dan Requests. Kode menetapkan maksimal lima percobaan. Jeda
antarpercobaan menggunakan *exponential backoff* dengan nilai minimum
empat detik dan maksimum sepuluh detik.

**Pengujian A -- Server aktif**

Perintah:

``` cmd
python check-retry.py
```

Hasil:

``` text
Attempting to access http://localhost:44777...
Successfully accessed http://localhost:44777
```

**Analisis:** Permintaan berhasil pada percobaan pertama karena server
aktif. Program tidak perlu melakukan percobaan ulang.

**Pengujian B -- Server tidak aktif**

Server Blacksheep dihentikan dengan menekan `Ctrl + C` pada terminal
server. Selanjutnya program dijalankan kembali:

``` cmd
python check-retry.py
```

Hasil:

``` text
Attempting to access http://localhost:44777...
Attempting to access http://localhost:44777...
Attempting to access http://localhost:44777...
Attempting to access http://localhost:44777...
Attempting to access http://localhost:44777...
Failed to access URL after multiple retries: RetryError
```

**Analisis:** Program mencoba mengakses server sebanyak lima kali.
Karena server tidak aktif, semua percobaan gagal. Setelah mencapai batas
percobaan, program menampilkan pesan kegagalan.

**Kesimpulan Retry:** Retry memberikan kesempatan kepada aplikasi untuk
mencoba kembali ketika koneksi gagal. Jika server tetap tidak tersedia
sampai batas percobaan tercapai, proses dihentikan dan kegagalan
dilaporkan.

#### 4.2.3 Circuit Breaker

Program `failure-detection/check-circuit-breaker.py` menggunakan library
PyBreaker dengan konfigurasi:

``` python
breaker = pybreaker.CircuitBreaker(fail_max=4, reset_timeout=20)
```

Batas kegagalan yang dikonfigurasi adalah empat kali dan waktu tunggu
reset adalah 20 detik.

**Pengujian A -- Server tidak aktif**

Ketika server tidak aktif, program dijalankan:

``` cmd
python check-circuit-breaker.py
```

Hasil utama:

``` text
Attempting to access http://localhost:44777...
HTTPConnectionPool(host='localhost', port=44777): Max retries exceeded
ConnectionError
```

**Analisis:** Permintaan gagal karena server tidak dapat menerima
koneksi pada port 44777.

**Pengujian B -- Server aktif**

Server Blacksheep dijalankan kembali menggunakan:

``` cmd
python dev.py
```

Kemudian program Circuit Breaker dijalankan:

``` cmd
python check-circuit-breaker.py
```

Hasil:

``` text
Attempting to access http://localhost:44777...
Successfully accessed http://localhost:44777
```

**Analisis:** Ketika server aktif, permintaan berhasil dan program
menampilkan pesan bahwa URL berhasil diakses.

**Catatan hasil pengujian:** Pengujian yang dilakukan membuktikan satu
pemanggilan ketika server tidak aktif dan satu pemanggilan ketika server
aktif. Kondisi internal Open dan Half-Open belum diuji secara langsung.
Kode menetapkan `fail_max=4`, tetapi satu kali menjalankan program hanya
menghasilkan satu pemanggilan fungsi sehingga belum membuktikan
perpindahan status setelah empat kegagalan.

**Kesimpulan Circuit Breaker:** Circuit Breaker membantu membatasi
permintaan ke layanan yang mengalami kegagalan. Mekanisme ini memiliki
status Closed, Open, dan Half-Open. Pada praktikum ini, hasil akses saat
server aktif dan tidak aktif telah diamati, sedangkan perpindahan status
Open dan Half-Open belum diuji secara langsung.

## 5. Hasil dan Pembahasan

  -----------------------------------------------------------------------
  Bagian                  Kondisi                 Hasil pengamatan
  ----------------------- ----------------------- -----------------------
  Load Balancing          Dua instance aktif      Kedua instance menerima
                                                  permintaan melalui
                                                  Nginx

  Heartbeat               Server tidak aktif      `Server down`

  Heartbeat               Server aktif            `Server up`

  Retry                   Server aktif            Berhasil diakses pada
                                                  percobaan pertama

  Retry                   Server tidak aktif      Lima percobaan gagal

  Circuit Breaker         Server tidak aktif      Koneksi ditolak

  Circuit Breaker         Server aktif            Berhasil diakses
  -----------------------------------------------------------------------

Perbedaan fungsi setiap mekanisme: - Load Balancing membagi permintaan
ke beberapa instance aplikasi. - Heartbeat memeriksa apakah server dapat
dihubungi. - Retry mengulang permintaan ketika terjadi kegagalan
koneksi. - Circuit Breaker membatasi permintaan ketika layanan mengalami
kegagalan berulang.

## 6. Kesimpulan

Praktikum Modul 5 membahas penerapan *fault tolerance* pada sistem
terdistribusi. Melalui Load Balancing, dua instance aplikasi Blacksheep
berhasil dijalankan menggunakan Docker Compose dan Nginx. Melalui
Heartbeat, kondisi server aktif dan tidak aktif dapat dibedakan.
Mekanisme Retry berhasil melakukan lima percobaan ketika server tidak
tersedia, sedangkan Circuit Breaker menunjukkan perbedaan hasil akses
saat server aktif dan tidak aktif.

Dengan praktikum ini, dapat dipahami bahwa setiap mekanisme memiliki
fungsi yang berbeda dalam membantu menjaga keandalan sistem. Pengujian
lanjutan masih diperlukan untuk mengamati secara langsung perpindahan
status Circuit Breaker dari Closed ke Open dan Half-Open.

## 7. Dokumentasi

Tambahkan screenshot hasil praktikum pada bagian ini sesuai urutan:

1.  **Gambar 1.** Container Load Balancing aktif (`docker compose ps`).
2.  **Gambar 2.** Aplikasi dapat diakses melalui browser (`localhost`).
3.  **Gambar 3.** Log dua instance aplikasi menerima permintaan.
4.  **Gambar 4.** Container dihentikan (`docker compose down`).
5.  **Gambar 5.** Pengujian Heartbeat saat server tidak aktif
    (`Server down`).
6.  **Gambar 6.** Pengujian Heartbeat saat server aktif (`Server up`).
7.  **Gambar 7.** Pengujian Retry saat server aktif.
8.  **Gambar 8.** Pengujian Retry saat server tidak aktif.
9.  **Gambar 9.** Pengujian Circuit Breaker saat server tidak aktif.
10. **Gambar 10.** Pengujian Circuit Breaker saat server aktif.

