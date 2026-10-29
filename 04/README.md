
DRAFT LAPORAN DAN PANDUAN PRAKTIKUM MODUL 4

Konsistensi dan Replikasi pada Sistem Terdistribusi

Nama: Rafael Natalino Soumokil

NIM: 255410022

Program Studi: Informatika

Mata Kuliah: Sistem Terdistribusi dan Terdesentralisasi

Catatan: Isi laporan ini adalah draft. Bagian hasil, tanggal, dan screenshot harus disesuaikan dengan hasil praktikum yang benar-benar dijalankan.

A. Tujuan Praktikum

Memahami replikasi streaming PostgreSQL dengan satu server primary dan satu server replica.

Menjalankan dan memeriksa container PostgreSQL menggunakan Docker Compose.

Menguji apakah perubahan data pada primary diteruskan ke replica.

Memahami replikasi master-master pada cluster Apache Ignite yang terdiri dari tiga node.

Mendokumentasikan konfigurasi, perintah, hasil pengujian, dan kesimpulan di GitHub.

B. Aplikasi dan Lingkungan Kerja

Visual Studio Code: membuat dan mengedit file YAML, SQL, serta README.md.

Docker Desktop dengan dukungan WSL 2: menjalankan container pada Windows.

Ubuntu di WSL 2: menjalankan perintah Linux/Docker yang digunakan dalam modul.

Browser dan GitHub: mengunduh file resmi, menyimpan hasil, dan mengunggah screenshot.

Sebelum mulai, buka Docker Desktop dan pastikan statusnya berjalan. Buka Ubuntu/WSL lalu periksa dengan perintah: docker --version dan docker compose version. Jika perintah tidak dikenali, selesaikan instalasi/integrasi Docker terlebih dahulu; jangan lanjut ke konfigurasi database sebelum Docker berfungsi.

C. Praktikum 4.1 — Streaming Replication PostgreSQL

C.1 Struktur folder

Buat folder proyek bernama streaming-replication dengan struktur:

streaming-replication/\n├── 00_init.sql\n└── docker-compose.yaml

File env.sh pada modul bersifat opsional karena hanya berisi alias shortcut. Untuk pengguna Windows/WSL pemula, jalankan perintah Docker secara langsung terlebih dahulu.

C.2 Membuat file 00_init.sql

Di VS Code, buat file 00_init.sql lalu isi:

CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');

C.3 Membuat file docker-compose.yaml

Buat docker-compose.yaml di folder yang sama. Isi berikut mengikuti susunan konfigurasi pada modul. Perhatikan indentasi YAML; gunakan spasi, bukan tab.

x-postgres-common: &postgres-common
  image: postgres:18.3-alpine3.23
  user: postgres
  restart: always
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U zuser --dbname=zdb"]
    interval: 10s
    timeout: 5s
    retries: 5

services:
  postgres_primary:
    <<: *postgres-common
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: zuser
      POSTGRES_DB: zdb
      POSTGRES_PASSWORD: zpass
      POSTGRES_HOST_AUTH_METHOD: |-
        scram-sha-256
        host replication replicator 0.0.0.0/0 md5
      POSTGRES_INITDB_ARGS: "--auth-host=scram-sha-256"
    command: >
      postgres
      -c wal_level=replica
      -c hot_standby=on
      -c max_wal_senders=10
      -c max_replication_slots=10
      -c hot_standby_feedback=on
    volumes:
      - ./00_init.sql:/docker-entrypoint-initdb.d/00_init.sql:ro

  postgres_replica:
    <<: *postgres-common
    ports:
      - "5433:5432"
    environment:
      PGUSER: replicator
      PGPASSWORD: replicator_password
      PGDATA: /var/lib/postgresql/18/docker
    command: >
      bash -c "
      until pg_basebackup --pgdata=/var/lib/postgresql/18/docker -R
      --slot=replication_slot --host=postgres_primary --port=5432 -X stream; do
        echo 'pg_basebackup failed. Retrying in 5 seconds ...'
        sleep 5
      done
      echo 'Backup done, starting replica...'
      chmod 0700 /var/lib/postgresql/18/docker
      postgres
      "
    depends_on:
      - postgres_primary


C.4 Menjalankan PostgreSQL

Buka folder proyek di VS Code. Pilih Terminal → New Terminal. Jika menggunakan Windows, terminal harus terhubung ke Ubuntu/WSL yang sudah terintegrasi dengan Docker.

Pindah ke folder proyek: cd streaming-replication

Validasi konfigurasi: docker compose config

Jalankan container: docker compose up -d

Periksa container: docker ps

Jika belum sehat atau gagal berjalan, lihat log: docker compose logs --tail=100 postgres_primary dan docker compose logs --tail=100 postgres_replica.

C.5 Pengujian status replica

Masuk ke primary:

docker exec -it streaming-replication-postgres_primary-1 psql -U zuser -d zdb

Nama container bisa berbeda mengikuti nama folder proyek. Jika perintah di atas tidak cocok, cari nama yang tepat melalui docker ps.

Di prompt psql primary, jalankan:

SELECT application_name, state, sync_state FROM pg_stat_replication;

Keluar dari psql dengan \q. Periksa replica:

docker exec -it streaming-replication-postgres_replica-1 psql -U zuser -d zdb -c "SELECT pg_is_in_recovery();"

Nilai t/true menunjukkan server masih dalam mode recovery/standby, sesuai fungsi replica.

C.6 Menguji replikasi data

Pada primary, jalankan perintah berikut:

docker exec -it streaming-replication-postgres_primary-1 psql -U zuser -d zdb
CREATE TABLE IF NOT EXISTS mahasiswa (id INT PRIMARY KEY, nama VARCHAR(100));
INSERT INTO mahasiswa (id, nama) VALUES (1, 'Rafael') ON CONFLICT (id) DO UPDATE SET nama = EXCLUDED.nama;
SELECT * FROM mahasiswa;
\q

Lalu baca data pada replica:

docker exec -it streaming-replication-postgres_replica-1 psql -U zuser -d zdb -c "SELECT * FROM mahasiswa;"

Hasil yang diharapkan: baris id 1 dan nama Rafael muncul pada primary dan replica. Screenshot harus berasal dari hasil nyata di terminal.

C.7 High Availability (opsional sesuai bagian modul)

Modul menjelaskan bahwa replica dapat dipromosikan menjadi primary jika primary down. Lakukan hanya setelah pengujian replikasi selesai dan jika diminta dosen. Promosi dapat dilakukan dari koneksi ke replica dengan:

SELECT pg_promote();

Setelah promosi, replica lama tidak otomatis kembali menjadi replica primary. Untuk praktikum pemula, jangan menguji failover sebelum menyimpan hasil dan memahami bahwa topologi dapat berubah.

D. Praktikum 4.2 — Master-Master Apache Ignite

D.1 Struktur dan file

Menurut modul, bagian ini membutuhkan docker-compose.yaml untuk tiga node Ignite serta direktori sql yang berisi file SQL. Gunakan file resmi yang ditautkan modul:

Compose: https://ignite.apache.org/docs/ignite3/latest/quick-start/sql-files/docker-compose.yml

SQL ZIP: https://ignite.apache.org/docs/ignite3/latest/quick-start/sql-files/sql.zip

Simpan compose sebagai docker-compose.yaml di folder apache-ignite. Unduh sql.zip, ekstrak menjadi folder sql di folder yang sama. Pastikan file SQL terlihat di dalam folder sql.

D.2 Menjalankan cluster

Buka terminal pada folder apache-ignite.

Jalankan validasi: docker compose config

Jalankan cluster: docker compose up -d

Periksa container: docker ps

Jika ada node yang belum berjalan, periksa log: docker compose logs --tail=100.

Modul menjelaskan tiga node dengan port administratif 10300, 10301, dan 10302 serta port aplikasi 10800–10802.

D.3 Inisialisasi cluster

Jalankan Ignite CLI sesuai versi yang dipakai file compose resmi. Contoh perintah pada modul menggunakan image Apache Ignite CLI:

docker run --rm -it --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 apacheignite/ignite:3.0.0 cli

Di CLI, jalankan:

cluster init --name=ignite3 --metastorage-group=node1,node2,node3

Nama node dan versi image harus cocok dengan compose yang digunakan. Jika image compose menggunakan versi berbeda, gunakan versi CLI yang kompatibel. Setelah inisialisasi berhasil, jangan jalankan ulang kecuali cluster memang belum diinisialisasi.

D.4 Memuat dan menjalankan SQL

Jika perlu mengakses file SQL dari container CLI, gunakan mount direktori lokal sql ke /opt/ignite/sql. Contoh sesuai pola modul:

docker run --rm -it --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -v ./sql:/opt/ignite/sql apacheignite/ignite:3.0.0 cli

Setelah CLI terhubung ke node pada localhost:10300, jalankan perintah SQL yang disediakan dalam file sql. Untuk memeriksa tabel:

sql
SELECT * FROM system.tables WHERE schema = 'PUBLIC';

Ikuti urutan file SQL yang disediakan modul/arsip. Catat output sukses dari setiap file, khususnya pembuatan schema/tabel dan pemuatan data.

D.5 Memeriksa replikasi antar-node

Buka koneksi CLI ke endpoint node lain, misalnya http://localhost:10301 dan http://localhost:10302. Jalankan query pemeriksaan tabel atau query SELECT pada tabel yang sudah dimuat. Hasil yang konsisten di ketiga node menunjukkan data tersedia pada seluruh cluster, sesuai konsep master-master yang dijelaskan modul.

Contoh query analitik dari modul menggunakan tabel Invoice untuk menghitung jumlah invoice, pelanggan, pendapatan bulanan, dan rata-rata nilai transaksi. Jalankan hanya jika tabel Invoice telah berhasil dimuat.

D.6 Mematikan container

Setelah screenshot dan pengujian selesai, matikan layanan dari masing-masing folder proyek:

docker compose down

Jangan gunakan opsi penghapusan volume jika ingin mempertahankan data praktikum.

E. Draft Laporan Praktikum

1. Pendahuluan

Sistem terdistribusi dapat menggunakan replikasi untuk menyediakan salinan data pada lebih dari satu server atau node. Pada Modul 4, praktikum dilakukan dengan dua pendekatan, yaitu streaming replication PostgreSQL dengan primary dan replica, serta replikasi master-master pada cluster Apache Ignite.

2. Tujuan

Praktikum bertujuan memahami konfigurasi replikasi, menjalankan layanan melalui Docker, menguji sinkronisasi data, dan mendokumentasikan hasil pengujian pada repository GitHub.

3. Alat dan Bahan

Laptop/PC, Windows dengan WSL 2/Ubuntu, Docker Desktop, Docker Compose, Visual Studio Code, browser, akun GitHub, image PostgreSQL 18, dan Apache Ignite sesuai konfigurasi modul.

4. Langkah Kerja

Praktikum PostgreSQL dilakukan dengan membuat file 00_init.sql dan docker-compose.yaml, menjalankan dua container, memeriksa status replikasi, lalu membuat tabel dan menguji apakah data yang ditulis di primary dapat dibaca di replica. Praktikum Apache Ignite dilakukan dengan mengunduh compose dan file SQL yang disediakan modul, menjalankan tiga node, menginisialisasi cluster, memuat data SQL, dan memeriksa data melalui endpoint node yang berbeda.

5. Hasil dan Pembahasan

Bagian ini harus diisi berdasarkan hasil aktual. Untuk PostgreSQL, lampirkan hasil docker ps, pg_stat_replication, pg_is_in_recovery(), serta SELECT dari primary dan replica. Untuk Ignite, lampirkan status tiga node, hasil cluster init, hasil query system.tables, dan hasil query dari endpoint node lain. Jika ada error, tuliskan pesan error dan langkah perbaikannya; jangan menuliskan bahwa pengujian berhasil jika belum dijalankan.

6. Kesimpulan

Dari praktikum ini, mahasiswa dapat mempelajari bahwa PostgreSQL streaming replication menggunakan primary sebagai server penulisan utama dan replica sebagai standby yang menerima perubahan data. Apache Ignite menjalankan beberapa node dalam satu cluster sehingga data yang dimuat dapat diakses melalui node lain. Keberhasilan praktikum dibuktikan melalui status container dan hasil query aktual pada masing-masing server/node.

7. Lampiran Screenshot

Docker Desktop berjalan dan versi Docker/Compose.

Struktur folder serta file 00_init.sql dan docker-compose.yaml.

Output docker compose up -d dan docker ps untuk PostgreSQL.

Hasil pg_stat_replication dan pg_is_in_recovery().

Tabel mahasiswa pada primary dan hasil SELECT yang sama pada replica.

Container tiga node Apache Ignite aktif.

Output cluster init berhasil.

Hasil query system.tables pada node 10300.

Hasil query yang sama pada node 10301 dan 10302.

Output docker compose down setelah praktikum.

F. Susunan Repository GitHub yang Disarankan

modul-04-sistem-terdistribusi/
├── README.md
├── streaming-replication/
│   ├── 00_init.sql
│   ├── docker-compose.yaml
│   └── images/
│       ├── 01-docker-ps.png
│       ├── 02-replication-status.png
│       └── 03-data-primary-replica.png
└── apache-ignite/
    ├── docker-compose.yaml
    ├── sql/
    └── images/
        ├── 01-ignite-nodes.png
        ├── 02-cluster-init.png
        └── 03-query-all-nodes.png

Ikuti ketentuan dosen jika nama repository atau struktur folder yang diwajibkan berbeda. Jangan unggah password sungguhan; nilai pada modul adalah contoh praktikum.



