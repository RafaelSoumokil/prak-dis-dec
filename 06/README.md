
# Modul 6 – Distributed File System (HDFS)

## 1. Identitas Praktikum

- **Nama:** Rafael Natalino Soumokil
- **Program Studi:** Informatika 1
- **Mata Kuliah:** Sistem Terdistribusi
- **Materi:** Distributed File System – HDFS


## 2. Tujuan Praktikum

Praktikum ini bertujuan untuk:

1. Memahami konsep Distributed File System menggunakan Hadoop Distributed File System (HDFS).
2. Melakukan instalasi dan konfigurasi Hadoop.
3. Menjalankan layanan NameNode dan DataNode.
4. Membuat direktori pada HDFS.
5. Mengunduh dan menyimpan dataset CSV ke HDFS.
6. Melakukan pemeriksaan file yang telah disimpan.

## 3. Lingkungan Praktikum

| Komponen | Keterangan |
|---|---|
| Sistem Operasi | Ubuntu melalui WSL |
| Hadoop | 3.5.0 |
| Java | OpenJDK 17 |
| Username | rafael |
| File System | HDFS |
| Direktori Hadoop | `/home/rafael/software/storage/hadoop` |
| Direktori HDFS | `/user/rafael/datasets` |

## 4. Konfigurasi Hadoop

Beberapa file konfigurasi Hadoop yang digunakan:

### A. core-site.xml

Mengatur alamat NameNode sebagai alamat utama HDFS.

```xml
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
</property>
```

### B. hdfs-site.xml

Mengatur replikasi dan lokasi penyimpanan data NameNode serta DataNode.

```xml
<property>
    <name>dfs.replication</name>
    <value>1</value>
</property>

<property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///home/rafael/hadoopdata/namenode</value>
</property>

<property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///home/rafael/hadoopdata/datanode</value>
</property>
```

### C. mapred-site.xml

Mengatur framework pemrosesan MapReduce menggunakan YARN.

```xml
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
```

### D. yarn-site.xml

Mengatur layanan tambahan untuk menjalankan MapReduce.

```xml
<property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
</property>
```

## 5. Menjalankan Hadoop

Setelah konfigurasi selesai, layanan HDFS dijalankan menggunakan perintah:

```bash
start-dfs.sh
```

Kemudian memeriksa proses Hadoop:

```bash
jps
```

Hasil yang diperoleh menunjukkan proses:

- NameNode
- DataNode
- SecondaryNameNode

Dashboard HDFS dapat diakses melalui browser:

```text
http://localhost:9870
```

## 6. Membuat Direktori HDFS

Membuat direktori untuk menyimpan dataset:

```bash
hdfs dfs -mkdir -p /user/rafael/datasets
```

Memeriksa direktori:

```bash
hdfs dfs -ls /user/rafael
```

Direktori `datasets` berhasil dibuat.

## 7. Mengunduh Dataset CSV

Membuat direktori lokal untuk menyimpan dataset:

```bash
mkdir -p ~/datasets
cd ~/datasets
```

Mengunduh tiga dataset dari GitHub:

```bash
wget https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv

wget https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv

wget https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv
```

Memeriksa file yang telah diunduh:

```bash
ls -lh
```

Dataset yang berhasil diunduh:

| No. | Nama File | Ukuran |
|---|---|---:|
| 1 | iris.csv | 3.8 KB |
| 2 | penguins.csv | 14 KB |
| 3 | tips.csv | 9.6 KB |

## 8. Mengunggah Dataset ke HDFS

Mengunggah file CSV dari direktori lokal ke HDFS:

```bash
hdfs dfs -put ~/datasets/iris.csv /user/rafael/datasets/

hdfs dfs -put ~/datasets/penguins.csv /user/rafael/datasets/

hdfs dfs -put ~/datasets/tips.csv /user/rafael/datasets/
```

Memeriksa file yang telah diunggah:

```bash
hdfs dfs -ls /user/rafael/datasets
```

Hasil pemeriksaan menunjukkan tiga file berhasil tersimpan:

| No. | Nama File | Ukuran (Byte) | Status |
|---|---|---:|---|
| 1 | iris.csv | 3858 | Berhasil |
| 2 | penguins.csv | 13478 | Berhasil |
| 3 | tips.csv | 9729 | Berhasil |

## 9. Verifikasi Isi Dataset

Untuk memastikan file dapat dibaca dari HDFS, digunakan perintah `hdfs dfs -cat`.

### A. Memeriksa iris.csv

```bash
hdfs dfs -cat /user/rafael/datasets/iris.csv | head
```

Dataset berisi informasi ukuran sepal dan petal serta spesies bunga iris.

### B. Memeriksa penguins.csv

```bash
hdfs dfs -cat /user/rafael/datasets/penguins.csv | head
```

Dataset berisi informasi spesies penguin, pulau, ukuran paruh, panjang sirip, berat badan, dan jenis kelamin.

### C. Memeriksa tips.csv

```bash
hdfs dfs -cat /user/rafael/datasets/tips.csv | head
```

Dataset berisi informasi total tagihan, tip, jenis kelamin, perokok, hari, waktu makan, dan jumlah orang.

Ketiga perintah berhasil menampilkan isi file dari HDFS.

## 10. Hasil Praktikum

Berdasarkan praktikum yang telah dilakukan, diperoleh hasil:

1. Hadoop versi 3.5.0 berhasil dipasang dan dikonfigurasi.
2. NameNode, DataNode, dan SecondaryNameNode berhasil dijalankan.
3. Dashboard HDFS dapat diakses melalui browser.
4. Direktori `/user/rafael/datasets` berhasil dibuat.
5. Tiga dataset CSV berhasil diunduh.
6. Ketiga dataset berhasil diunggah ke HDFS.
7. Isi masing-masing dataset berhasil dibaca menggunakan perintah HDFS.

## 11. Kesimpulan

Berdasarkan praktikum Modul 6 tentang Distributed File System menggunakan HDFS, dapat disimpulkan bahwa Hadoop berhasil dikonfigurasi dan dijalankan pada lingkungan Ubuntu WSL.

Proses pembuatan direktori, pengunduhan dataset, pengunggahan file, serta verifikasi data berhasil dilakukan. Ketiga dataset, yaitu `iris.csv`, `penguins.csv`, dan `tips.csv`, telah tersimpan di dalam direktori HDFS `/user/rafael/datasets` dan dapat dibaca dengan baik.

Praktikum ini memberikan pemahaman mengenai pengelolaan penyimpanan file terdistribusi menggunakan Hadoop Distributed File System (HDFS).
