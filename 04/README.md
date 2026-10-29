# Modul 4 — Konsistensi dan Replikasi pada Sistem Terdistribusi

Praktikum Sistem Terdistribusi dan Terdesentralisasi, Prodi Informatika, Universitas Teknologi Digital Indonesia.

Repo ini berisi hasil pengerjaan seluruh materi Modul 4:

| Bagian | Topik | Status |
| --- | --- | --- |
| 4.1 | Streaming replication PostgreSQL 18 (primary → standby) | Selesai, termasuk uji failover |
| 4.2 | Replikasi master-master Apache Ignite 3 (3 node) | Selesai, termasuk verifikasi lintas node |

Semua perintah dijalankan dan output yang ditampilkan di bawah adalah hasil eksekusi nyata, bukan kutipan modul.

## Lingkungan pengerjaan

- Windows 11, shell Git Bash
- Docker 29.9.2 (container Linux) dan Docker Compose v5.6.1
- PostgreSQL `postgres:18.3-alpine3.23`
- Apache Ignite `apacheignite/ignite:3.1.0`

Adaptasi dari modul (modul ditulis untuk Linux):

1. Modul memakai `sudo docker-compose`; di Docker Desktop dipakai `docker compose` tanpa `sudo`.
2. Modul memakai opsi `-it` pada Ignite CLI (butuh TTY). Untuk otomasi dipakai bentuk non-interaktif `cli sql --file=...`.
3. Heap Ignite resmi 4 GB per node diturunkan menjadi 512 MB karena Docker Desktop di mesin ini hanya dialokasikan ±3,75 GB untuk 3 node sekaligus.
4. Port host 5432/5433 dan 10300–10302/10800–10802 harus bebas. Pada saat praktikum ada container lama yang menempati 5432 sehingga dihentikan lebih dulu.

## Struktur repo

```
.
├── README.md
├── streaming-replication/
│   ├── 00_init.sql            # user replikasi + physical replication slot
│   ├── docker-compose.yaml    # primary + replica
│   ├── env.sh                 # alias perintah
│   └── README.md              # penjelasan detail bagian 4.1
├── ignite-cluster/
│   ├── docker-compose.yml     # 3 node Ignite 3.1.0
│   ├── env.sh                 # alias perintah
│   ├── sql/                   # 6 skrip SQL Chinook dari dokumentasi Ignite
│   └── README.md              # penjelasan detail bagian 4.2
└── docs/
    └── queries/               # query yang dipakai saat pengujian
```

---

# 4.1 Streaming Replication PostgreSQL 18

## Konsep

Streaming replication adalah replikasi fisik level byte: primary mengirim aliran WAL (Write-Ahead Log) ke standby, lalu standby me-replay WAL tersebut. Standby berada pada mode *hot standby*, yaitu menerima koneksi **read-only** dan menolak operasi tulis.

Komponen yang dipakai:

- `wal_level=replica` — WAL memuat informasi yang cukup untuk standby.
- `max_wal_senders` / `max_replication_slots` — jumlah koneksi WAL sender dan slot.
- **Physical replication slot** (`replication_slot`) — mencegah primary menghapus WAL yang belum dikonsumsi replica, sehingga replica yang tertinggal/offline tetap bisa menyusul.
- `pg_basebackup -R` — mengambil base backup dan otomatis menulis `standby.signal` + `primary_conninfo` (parameter `-R` = `--write-recovery-conf`).
- `hot_standby=on` dan `hot_standby_feedback=on` — standby melayani query baca; feedback mencegah primary melakukan cleanup baris yang masih dibutuhkan query di standby.
- Autentikasi: user `replicator` dengan hak `REPLICATION`, dan baris `host replication all 0.0.0.0/0 md5` di `pg_hba.conf`. Baris ini dibuat lewat trik `POSTGRES_HOST_AUTH_METHOD` berisi dua baris (auth host biasa + auth koneksi replikasi).

## File

`00_init.sql` dijalankan otomatis oleh entrypoint image PostgreSQL saat inisialisasi:

```sql
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');
```

`docker-compose.yaml` mendefinisikan dua service dengan basis yang sama (`x-postgres-common`):

- **postgres_primary** — port host 5432, database `zdb`, user `zuser`/`zpass`, WAL level replica, hot standby aktif, 10 WAL sender & 10 slot. `00_init.sql` di-mount ke `/docker-entrypoint-initdb.d/`.
- **postgres_replica** — port host 5433, `PGDATA=/var/lib/postgresql/18/docker` (lokasi baru data directory PostgreSQL 18 di image Docker), menjalankan `pg_basebackup` berulang sampai berhasil lalu menjalankan `postgres`. Opsi `--slot=replication_slot` memakai slot yang sama sehingga WAL tidak hilang saat replica belum siap.

## Menjalankan

```bash
cd streaming-replication
source env.sh
dcu          # docker compose up -d
dps          # cek status container
```

Hasil setelah kedua container sehat:

```
$ docker ps --filter "name=streaming-replication"
CONTAINER ID   IMAGE                      STATUS                    PORTS
04b800a2a481   postgres:18.3-alpine3.23   Up (healthy)              0.0.0.0:5433->5432/tcp
17fec65046f3   postgres:18.3-alpine3.23   Up (healthy)              0.0.0.0:5432->5432/tcp
```

## Bukti replikasi

**Di primary** — ada satu WAL sender yang sedang streaming ke replica:

```
$ docker exec streaming-replication-postgres_primary-1 \
    psql -U zuser -d zdb -c "SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn, sync_state FROM pg_stat_replication;"

 client_addr |   state   | sent_lsn  | write_lsn | flush_lsn | replay_lsn | sync_state
-------------+-----------+-----------+-----------+-----------+------------+------------
 172.18.0.3  | streaming | 0/3000060 | 0/3000060 | 0/3000060 | 0/3000060  | async
```

`state = streaming` berarti WAL sedang dialirkan. `sync_state = async` berarti commit di primary tidak menunggu replica (replikasi asinkron); konsekuensinya pada saat primary mati mendadak ada kemungkinan beberapa transaksi terakhir belum sampai ke replica.

Slot replikasi aktif dan dimulai dari LSN yang sama:

```
$ ... -c "SELECT slot_name, slot_type, active, restart_lsn FROM pg_replication_slots;"

    slot_name     | slot_type | active | restart_lsn
------------------+-----------+--------+-------------
 replication_slot | physical  | t      | 0/3000060
```

**Di replica** — server berada dalam mode recovery (standby):

```
$ docker exec streaming-replication-postgres_replica-1 \
    psql -U zuser -d zdb -c "SELECT pg_is_in_recovery();"
 pg_is_in_recovery
-------------------
 t

$ ... -c "SELECT status, sender_host, sender_port, slot_name FROM pg_stat_wal_receiver;"
  status   |   sender_host    | sender_port |    slot_name
-----------+------------------+-------------+------------------
 streaming | postgres_primary |        5432 | replication_slot
```

## Uji manipulasi data

Tabel dibuat dan diisi **hanya di primary**:

```
$ ...primary... -c "CREATE TABLE students (id SERIAL PRIMARY KEY, nim VARCHAR(15) UNIQUE NOT NULL, name VARCHAR(100) NOT NULL);" \
                -c "INSERT INTO students (nim, name) VALUES ('225610001','Andi'), ('225610002','Budi'), ('225610003','Citra');"
CREATE TABLE
INSERT 0 3
```

Membaca di primary:

```
 id |    nim    | name
----+-----------+-------
  1 | 225610001 | Andi
  2 | 225610002 | Budi
  3 | 225610003 | Citra
```

Membaca di replica — data sudah otomatis tersinkron tanpa perintah tambahan:

```
$ ...replica... -c "SELECT * FROM students ORDER BY id;"

 id |    nim    | name
----+-----------+-------
  1 | 225610001 | Andi
  2 | 225610002 | Budi
  3 | 225610003 | Citra
```

Percobaan menulis di replica ditolak karena standby bersifat read-only:

```
$ ...replica... -c "INSERT INTO students (nim, name) VALUES ('225610004','Dewi');"
ERROR:  cannot execute INSERT in a read-only transaction
```

## High availability: promosi replica

Skenario: primary dimatikan, lalu replica dipromosikan menjadi primary baru.

```
$ docker stop streaming-replication-postgres_primary-1

$ ...replica... -c "SELECT pg_is_in_recovery();"
 t                          -- masih standby, belum bisa menulis

$ ...replica... -c "SELECT pg_promote();"
 t                          -- permintaan promosi diterima

$ ...replica... -c "SELECT pg_is_in_recovery();"
 f                          -- sudah menjadi primary

$ ...replica... -c "INSERT INTO students (nim, name) VALUES ('225610004','Dewi');" \
                -c "SELECT * FROM students ORDER BY id;"
INSERT 0 1
 id |    nim    | name
----+-----------+-------
  1 | 225610001 | Andi
  2 | 225610002 | Budi
  3 | 225610003 | Citra
 34 | 225610004 | Dewi
```

Setelah promosi, node tersebut menerima read-write. Nilai `id` melompat dari 3 ke 34 karena sequence memakai preallocation/cache dan WAL sequence tidak di-replay per satu nilai; lompatan seperti ini normal pada failover dan tidak melanggar keunikan primary key.

`pg_promote()` mengubah standby menjadi primary: `standby.signal` dihapus, node keluar dari recovery, dan timeline baru dibuat. Proses ini **tidak otomatis** pada konfigurasi modul — perlu dijalankan manual atau diotomasi dengan tool seperti Patroni/repmgr. Replica tidak dapat kembali menjadi standby dari primary baru tanpa `pg_rewind`/base backup ulang.

Mematikan semuanya:

```bash
dcd          # docker compose down
```

Penjelasan langkah lengkap ada di [streaming-replication/README.md](streaming-replication/README.md).

---

# 4.2 Replikasi Master-Master Apache Ignite 3

## Konsep

Cluster Apache Ignite 3 terdiri atas beberapa node dengan metadata cluster (metastorage) yang direplikasi. Data disimpan dalam **distribution zone**; setiap zona menentukan jumlah replika dan jumlah partisi:

- `Chinook` — `replicas=2`, dipakai tabel katalog utama.
- `ChinookReplicated` — `replicas=3`, `partitions=25`, dipakai `Genre` dan `MediaType`.

Semua node menerima operasi **baca dan tulis** (inilah yang disebut master-master), berbeda dengan model primary–standby PostgreSQL. Setiap partisi memiliki replika di node lain sehingga kegagalan satu node tidak menghilangkan data. Secara teknis Ignite 3 menjaga konsistensi metadata dan transaksi dengan konsensus Raft; istilah "master-master" di modul merujuk pada tidak adanya satu node khusus penulis, bukan pada resolusi konflik multi-writer gaya sistem eventual-consistency.

Port yang dipakai:

| Port host | Fungsi |
| --- | --- |
| 10300–10302 | REST API / endpoint administratif (dipakai Ignite CLI) |
| 10800–10802 | Port koneksi aplikasi (thin client) |

## File

- `docker-compose.yml` — tiga service (`node1`, `node2`, `node3`) dari image `apacheignite/ignite:3.1.0`, masing-masing dengan `--node-name`, port 10300/10800 yang dipetakan berbeda per node, dan config bersama yang mendaftarkan node finder `["node1:3344","node2:3344","node3:3344"]`.
- `sql/` — enam skrip Chinook: `schema.sql`, `current_catalog.sql`, `media_and_genre.sql`, `tracks.sql`, `ee_and_cust.sql`, `invoices.sql`.
- `env.sh` — alias `dcu`, `dcd`, `dps`, `dclm`, `dcli`.

Urutan eksekusi penting: `schema.sql` membuat zona dan tabel, baru file data dijalankan. `schema.sql` hanya menghapus 5 tabel (Track, MediaType, Genre, Album, Artist); menjalankannya ulang pada cluster yang sudah berisi tabel lain akan gagal di `DROP ZONE` karena zona masih dipakai (perilaku skrip resmi, bukan bug konfigurasi).

## Menjalankan dan inisialisasi

```bash
cd ignite-cluster
source env.sh
dcu
dps
```

```
NAME              IMAGE                       STATUS    PORTS
ignite3-node1-1   apacheignite/ignite:3.1.0   Up        0.0.0.0:10300->10300/tcp, 0.0.0.0:10800->10800/tcp
ignite3-node2-1   apacheignite/ignite:3.1.0   Up        0.0.0.0:10301->10300/tcp, 0.0.0.0:10801->10800/tcp
ignite3-node3-1   apacheignite/ignite:3.1.0   Up        0.0.0.0:10302->10300/tcp, 0.0.0.0:10802->10800/tcp
```

IP internal container (dicek dengan `docker inspect`):

```
ignite3-node1-1 -> 172.18.0.3
ignite3-node2-1 -> 172.18.0.2
ignite3-node3-1 -> 172.18.0.4
```

Inisialisasi cluster hanya sekali:

```bash
docker run --rm --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 \
  apacheignite/ignite:3.1.0 \
  cli cluster init --name=ignite3 --metastorage-group=node1,node2,node3
# Cluster was initialized successfully
```

Bentuk interaktif (sesuai modul) juga bisa dipakai: jalankan `cli`, lalu di prompt `[node1]>` berikan `cluster init --name=ignite3 --metastorage-group=node1,node2,node3`. Bila CLI dijalankan ulang, inisialisasi tidak perlu dilakukan lagi.

## Eksekusi data Chinook

File SQL dieksekusi lewat CLI dengan direktori `sql/` di-mount ke `/opt/ignite/sql`:

```bash
for f in schema.sql current_catalog.sql media_and_genre.sql tracks.sql ee_and_cust.sql invoices.sql; do
  docker run --rm --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 \
    -v "$PWD/sql:/opt/ignite/sql" apacheignite/ignite:3.1.0 \
    cli sql --file=/opt/ignite/sql/$f
done
```

Hasil:

```
schema.sql           -> 11 tabel dibuat pada zona Chinook/ChinookReplicated
current_catalog.sql  -> Updated 275 rows; Updated 347 rows
media_and_genre.sql  -> Updated 25 rows;  Updated 5 rows
tracks.sql           -> Updated 1000 rows; Updated 503 rows
ee_and_cust.sql      -> Updated 8 rows;   Updated 59 rows
invoices.sql         -> Updated 1000 rows; Updated 715 rows
```

Daftar tabel pada schema `PUBLIC` (query `docs/queries/system_tables.sql`): `Album`, `Artist`, `Customer`, `Employee`, `Genre`, `Invoice`, `InvoiceLine`, `MediaType`, `Playlist`, `PlaylistTrack`, `Track`.

## Verifikasi replikasi ke semua node

Query yang sama dijalankan pada node1 (10300), node2 (10301), dan node3 (10302):

```sql
SELECT (SELECT COUNT(*) FROM Artist) AS artists,
       (SELECT COUNT(*) FROM Album) AS albums,
       (SELECT COUNT(*) FROM Track) AS tracks,
       (SELECT COUNT(*) FROM Customer) AS customers,
       (SELECT COUNT(*) FROM Invoice) AS invoices;
```

Hasil identik di ketiga node:

```
╔═════════╤════════╤════════╤═══════════╤══════════╗
║ ARTISTS │ ALBUMS │ TRACKS │ CUSTOMERS │ INVOICES ║
╠═════════╪════════╪════════╪═══════════╪══════════╣
║ 275     │ 347    │ 3503   │ 59        │ 412      ║
╚═════════╧════════╧════════╧═══════════╧══════════╝
```

Data dimasukkan sekali lewat node1, tetapi terbaca lengkap di node2 dan node3. Ini membuktikan replikasi data antar node dalam satu cluster.

## Bukti master-master (tulis di node mana pun)

Baris uji ditulis **di node2**, lalu dibaca dari node1 dan node3:

```
node2: INSERT INTO Artist (ArtistId, Name) VALUES (9999, 'Master-Master Probe');
       -> Updated 1 rows

node3: SELECT ArtistId, Name FROM Artist WHERE ArtistId = 9999;
       ║ 9999 │ Master-Master Probe ║

node1: SELECT ArtistId, Name FROM Artist WHERE ArtistId = 9999;
       ║ 9999 │ Master-Master Probe ║
```

Baris uji kemudian dihapus dari node1 (`DELETE ... WHERE ArtistId = 9999`) dan jumlah Artist kembali 275 di node3. Semua node dapat menjadi titik masuk tulis, dan perubahan langsung terlihat di node lain.

## Query analytics

Query ringkasan penjualan bulanan dijalankan di node3 (`docs/queries/monthly_sales.sql`):

```
╔═══════════╤══════════════╤═══════════════╤════════════════╤════════════════════╗
║ YEARMONTH │ INVOICECOUNT │ CUSTOMERCOUNT │ MONTHLYREVENUE │ AVERAGEORDERVALUE  ║
╠═══════════╪══════════════╪═══════════════╪════════════════╪════════════════════╣
║ 2024-12   │ 7            │ 7             │ 38.62          │ 5.5171428571428571 ║
║ 2024-11   │ 7            │ 7             │ 49.62          │ 7.0885714285714285 ║
║ 2024-10   │ 7            │ 7             │ 37.62          │ 5.3742857142857142 ║
║ ...       │              │               │                │                    ║
╚═══════════╧══════════════╧═══════════════╧════════════════╧════════════════════╝
```

Query berjalan pada node3 dan membaca data yang dimuat melalui node1, tanpa konfigurasi tambahan.

Mematikan semua node:

```bash
dcd          # docker compose down
```

Penjelasan langkah lengkap ada di [ignite-cluster/README.md](ignite-cluster/README.md).

---

# Menjalankan ulang dari nol

```bash
# 4.1 PostgreSQL
cd streaming-replication
source env.sh
dcu
# tunggu sampai kedua container "healthy" (docker ps)
# uji: SELECT pg_is_in_recovery(); di replica, lalu buat tabel di primary
dcd

# 4.2 Apache Ignite
cd ../ignite-cluster
source env.sh
dcu
docker run --rm --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 \
  apacheignite/ignite:3.1.0 cli cluster init \
  --name=ignite3 --metastorage-group=node1,node2,node3
# eksekusi 6 file SQL (perintah for-loop di atas)
dcd
```

## Kesimpulan

1. PostgreSQL streaming replication mereplikasi WAL secara fisik; standby bersifat read-only dan dapat dipromosikan menjadi primary dengan `pg_promote()`. Replikasi pada konfigurasi ini asinkron, sehingga failover manual berpotensi kehilangan transaksi terakhir yang belum terkirim.
2. Replication slot menjaga WAL tetap tersedia untuk replica yang tertinggal, tetapi slot yang tidak aktif dapat menahan WAL dan menghabiskan disk — perlu dipantau.
3. Apache Ignite 3 membentuk cluster peer-to-peer dengan distribution zone ber-replika; semua node melayani read-write sehingga penulisan melalui node mana pun langsung terlihat di node lain. Ini memberikan ketersediaan dan skalabilitas baca/tulis yang lebih baik, dengan konsistensi yang dijaga oleh mekanisme cluster (Raft untuk metadata/transaksi).
