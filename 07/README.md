

UNIVERSITAS TEKNOLOGI DIGITAL INDONESIA
PROGRAM STUDI INFORMATIKA · FAKULTAS TEKNOLOGI INFORMASI



LAPORAN PRAKTIKUM
MODUL 7
CLOUD COMPUTING
Containerized App: Flaskr dengan Docker dan Podman


“Membangun, Mengemas, dan Menjalankan Aplikasi sebagai Layanan”


Nama	Rafael N Soumokil
NIM	255410022
Kelas	Informatika 1
Mata Kuliah	Praktikum Sistem Terdistribusi dan Terdesentralisasi
Dosen Pengampu	Dr. Bambang Purnomosidi D. P.




PROGRAM STUDI INFORMATIKA
FAKULTAS TEKNOLOGI INFORMASI
UNIVERSITAS TEKNOLOGI DIGITAL INDONESIA
YOGYAKARTA · 2026
BAB 1  PENDAHULUAN
1.1  Latar Belakang
Cloud computing mengubah cara sumber daya komputasi dikonsumsi. Jika sebelumnya organisasi harus membeli server, merakit ruang data, dan merawat sistem operasi sendiri, kini sumber daya tersebut dapat disewa sebagai layanan. Pendekatan ini dikenal sebagai XaaS (Everything as a Service) dan secara umum dibagi menjadi tiga tingkat: Software as a Service (SaaS), Platform as a Service (PaaS), dan Infrastructure as a Service (IaaS). Penyedia cloud bertanggung jawab atas sebagian besar lapisan di bawah aplikasi, sedangkan konsumen fokus pada data, konfigurasi, atau kode yang menjadi tanggung jawabnya.
Salah satu blok bangunan yang memungkinkan layanan-layanan tersebut adalah containerized app (CA). Container mengemas aplikasi bersama dependensi, konfigurasi, dan runtime ke dalam sebuah image yang konsisten. Image dapat dijalankan oleh container engine seperti Docker atau Podman di laptop, server, maupun cloud tanpa perubahan berarti. Pada praktikum ini, aplikasi blog Flaskr dari tutorial resmi Flask diubah menjadi CA, dibangun menjadi image, lalu dijalankan sebagai container dengan pemetaan port. Praktik ini memperlihatkan bagaimana sebuah aplikasi yang semula dijalankan langsung di host dapat dikemas menjadi unit deployment yang portabel.
1.2  Tujuan Praktikum
1.  Menjelaskan konsep XaaS dan memberikan contoh vendor SaaS, PaaS, serta IaaS beserta layanannya.
2.  Menjelaskan arsitektur XaaS dalam bentuk visualisasi gambar.
3.  Menyiapkan aplikasi Flaskr dengan Python 3.14.4 dan menjalankannya secara lokal.
4.  Membuat Dockerfile, membangun image, dan menjalankan aplikasi sebagai container Docker dengan pemetaan port 5001:5000.
5.  Menjelaskan langkah padanan untuk membangun dan menjalankan aplikasi dengan Podman.
6.  Menganalisis hasil, keterbatasan lingkungan, serta hubungan container dengan model XaaS.
1.3  Lingkungan Praktikum
Praktikum dikerjakan pada lingkungan Windows 11 dengan terminal Git Bash yang terintegrasi di Visual Studio Code. Server Flask dijalankan di host, sedangkan container dijalankan oleh Docker Desktop yang menyediakan VM Linux. Podman tidak tersedia secara native pada host ini; bagian Podman dijelaskan pada Bab 5 dengan keterangan sumber keluarannya. Ringkasan lingkungan disajikan pada Tabel 1.
Tabel 1. Lingkungan praktikum dan versi perkakas yang digunakan.
Komponen	Versi / Keterangan
Sistem operasi	Windows 11 build 10.0.22631 (x64)
Terminal	Git Bash di Visual Studio Code 1.146.0
Git	2.52.0.windows.1
uv	0.13.1 (x86_64-pc-windows-msvc)
Python	3.14.4 (dikelola oleh uv)
Flask / flaskr	Flask 3.1.3; flaskr 1.0.0 (editable install)
Docker	29.9.2 (Docker Desktop, container Linux)
Podman	Tidak tersedia native; referensi keluaran modul
Browser	Google Chrome (tangkapan layar 1280 × 760 @2x)
Direktori kerja	C:\Users\Admin\src\flask-app

Catatan tentang gambar
Seluruh gambar terminal dalam laporan ini merupakan render gaya terminal Visual Studio Code dari keluaran sesi nyata pada mesin praktikum (Windows 11 + Git Bash). Gambar browser adalah tangkapan layar nyata aplikasi Flaskr. Gambar Podman pada Bab 5 dikutip dari modul sebagai referensi dan diberi keterangan sumber secara eksplisit.

1.4  Sistematika Laporan
Laporan ini disusun mengikuti urutan pengerjaan praktikum. Bab 1 memaparkan latar belakang, tujuan, dan lingkungan kerja. Bab 2 menjawab Tugas 0, yaitu konsep XaaS beserta contoh vendor dan visualisasi arsitekturnya. Bab 3 mendokumentasikan persiapan aplikasi Flaskr mulai dari clone repositori, pembuatan environment Python 3.14.4, instalasi paket, inisialisasi basis data, hingga verifikasi melalui browser.
Bab 4 membahas containerization dengan Docker: penulisan Dockerfile, pembangunan image, verifikasi image, menjalankan container dengan pemetaan port, serta pembersihan container. Bab 5 menjelaskan padanan perintah dengan Podman beserta keterbatasan lingkungan praktikum. Bab 6 menyajikan pembahasan keterkaitan hasil praktikum dengan konsep cloud dan XaaS, sedangkan Bab 7 merangkum kesimpulan. Seluruh perintah, berkas konfigurasi, dan ringkasan pengujian ditempatkan pada lampiran agar laporan mudah direproduksi.
BAB 2  TUGAS 0 — KONSEP XaaS
2.1  Definisi XaaS
XaaS adalah singkatan dari Everything as a Service, yaitu model penyediaan sumber daya komputasi dalam bentuk layanan melalui jaringan. Konsumen tidak perlu memiliki atau merawat seluruh tumpukan teknologi; ia memilih tingkat abstraksi yang sesuai dengan kebutuhannya. NIST mendefinisikan cloud computing sebagai model yang memungkinkan akses jaringan yang mudah, on-demand, dan luas ke kumpulan sumber daya komputasi yang dapat dikonfigurasi dan dibagikan [5]. Tiga model layanan yang paling umum adalah:
•  SaaS (Software as a Service): penyedia menjalankan aplikasi lengkap dan konsumen mengakesnya melalui browser atau aplikasi klien. Konsumen hanya mengelola akun dan data.
•  PaaS (Platform as a Service): penyedia menyediakan runtime, middleware, basis data, dan alat deployment. Konsumen fokus pada kode aplikasi dan data.
•  IaaS (Infrastructure as a Service): penyedia menyediakan sumber daya komputasi virtual seperti VM, storage, dan jaringan. Konsumen mengelola sistem operasi dan seluruh lapisan di atasnya.
2.2  Contoh Vendor dan Layanan
Tabel 2 merangkum satu contoh vendor untuk setiap kategori XaaS beserta layanan utama dan bagian yang tetap menjadi tanggung jawab konsumen. Ketiga contoh dipilih karena banyak digunakan di industri dan dokumentasinya terbuka.
Tabel 2. Contoh vendor, layanan utama, dan tanggung jawab konsumen per kategori XaaS.
Kategori	Vendor	Layanan Utama	Dikelola Konsumen
SaaS	Google Workspace	Gmail, Drive, Docs, Sheets, Slides, Meet, Calendar, Chat	Akun, data, kebijakan berbagi, dan konfigurasi organisasi
PaaS	Google App Engine	Runtime terkelola, auto-scaling, Datastore/Firestore, versioning, traffic splitting, logging, Cloud Build	Kode aplikasi, dependensi, dan data
IaaS	Amazon EC2	Instance VM, EBS, VPC, Elastic Load Balancing, security group, snapshot, EC2 Auto Scaling	Sistem operasi, runtime, middleware, aplikasi, dan patch keamanan

2.2.1  SaaS — Google Workspace
Google Workspace adalah kumpulan aplikasi produktivitas berbasis cloud: Gmail untuk surel, Drive untuk penyimpanan, Docs/Sheets/Slides untuk dokumen kolaboratif, Meet untuk konferensi video, serta Calendar dan Chat. Konsumen berlangganan per akun dan mengakses aplikasi melalui browser atau aplikasi mobile. Penyedia mengelola aplikasi, server, sistem operasi, jaringan, dan patch keamanan; konsumen mengelola identitas pengguna, data, serta kebijakan berbagi. Model ini menghilangkan kebutuhan menyiapkan server surel atau kolaborasi sendiri.
2.2.2  PaaS — Google App Engine
Google App Engine menyediakan platform terkelola untuk menjalankan aplikasi web. Pengembang mengunggah kode (Python, Java, Node.js, Go, PHP, atau Ruby) dan mendeklarasikan konfigurasi pada app.yaml; App Engine menangani provisioning instance, load balancing, auto-scaling, serta integrasi dengan layanan data dan monitoring. Fitur versioning dan traffic splitting memungkinkan pengujian versi baru sebelum memindahkan seluruh trafik. Konsumen tidak mengelola sistem operasi maupun runtime secara langsung.
2.2.3  IaaS — Amazon EC2
Amazon Elastic Compute Cloud (EC2) menyediakan mesin virtual yang dapat dikonfigurasi sesuai kebutuhan. Pengguna memilih tipe instance, image sistem operasi, storage EBS, dan konfigurasi jaringan VPC. Layanan pendukung seperti Elastic Load Balancing, security group, snapshot, dan Auto Scaling memudahkan operasional. Pada IaaS, konsumen tetap bertanggung jawab atas sistem operasi, runtime, middleware, aplikasi, dan patch keamanan; penyedia bertanggung jawab atas virtualisasi, perangkat keras, data center, dan jaringan dasar.
2.3  Arsitektur XaaS
Gambar 1 memvisualisasikan arsitektur XaaS. Konsumen berada di lapisan paling atas dan mengakses layanan melalui Internet. Di bawahnya terdapat tiga tingkat layanan: SaaS sebagai aplikasi siap pakai, PaaS sebagai platform deployment, dan IaaS sebagai infrastruktur virtual. Seluruh lapisan berdiri di atas infrastruktur fisik penyedia yang mencakup data center, server, jaringan, penyimpanan, dan virtualisasi.
 
Gambar 1. Arsitektur XaaS: SaaS, PaaS, dan IaaS di atas infrastruktur fisik penyedia.
Sumber: diolah penulis (2026), mengacu pada konsep NIST SP 800-145.
Matriks pada sisi kanan Gambar 1 menunjukkan pembagian tanggung jawab. Pada On-Premises, konsumen mengelola seluruh komponen. Pada IaaS, penyedia mengambil alih infrastruktur, tetapi konsumen masih mengelola OS ke atas. Pada PaaS, runtime dan OS dikelola penyedia, sedangkan aplikasi dan data tetap menjadi tanggung jawab konsumen. Pada SaaS, hampir seluruh lapisan dikelola penyedia; konsumen hanya mengelola akun, data, dan kebijakan penggunaan. Prinsipnya sederhana: semakin tinggi tingkat layanan, semakin sedikit komponen yang perlu dikelola konsumen.
2.4  Posisi Containerized App dalam XaaS
Containerized app berada pada lapisan pengemasan dan deployment aplikasi. Image container berisi aplikasi dan dependensinya, sehingga dapat dijalankan secara konsisten di berbagai lingkungan. Container dapat berjalan di atas VM IaaS, di runtime container milik PaaS, atau menjadi bagian internal dari layanan SaaS. Dengan demikian, container bukan pengganti model XaaS, melainkan unit yang mempermudah aplikasi dipindahkan antar-lapisan layanan.
Pada praktikum ini, Docker Desktop menyediakan VM Linux yang berperan seperti IaaS sederhana, sedangkan Flaskr dikemas menjadi image dan dijalankan sebagai container. Alur kerja yang dilakukan—menulis Dockerfile, membangun image, lalu menjalankan container—menyerupai alur deployment pada PaaS, tetapi seluruh kendali atas image dan konfigurasi berada di tangan praktikan.
Hubungan tersebut dapat dipetakan langsung ke komponen yang digunakan pada praktikum, seperti dirangkum pada Tabel 3.
Tabel 3. Pemetaan lapisan XaaS terhadap komponen yang digunakan pada praktikum.
Lapisan XaaS	Peran Penyedia	Padanan pada Praktikum
IaaS	Menyediakan VM, jaringan, dan penyimpanan	Docker Desktop menyediakan VM Linux tempat container berjalan
PaaS	Menyediakan runtime dan mekanisme deployment	Image container dan perintah docker run berperan sebagai unit deployment
SaaS	Menjalankan aplikasi lengkap untuk pengguna akhir	Flaskr yang diakses melalui browser pada http://127.0.0.1:5001

BAB 3  PERSIAPAN APLIKASI FLASKR
3.1  Clone Repositori dan Penyalinan Tutorial
Aplikasi yang digunakan adalah contoh tutorial resmi Flask, yaitu aplikasi blog Flaskr. Repositori di-clone ke direktori $HOME/src, lalu direktori examples/tutorial disalin menjadi flask-app agar dapat dimodifikasi tanpa mengubah repositori asli. Clone dilakukan pada tag 3.1.3 agar sesuai dengan versi yang dirujuk modul; opsi --depth 1 mempercepat unduhan karena hanya mengambil satu commit.
Perintah:
cd $HOME/src
git clone --depth 1 --branch 3.1.3 https://github.com/pallets/flask
cp -R ~/src/flask/examples/tutorial flask-app
ls -la
cd flask-app

Keluaran perintah tersebut ditunjukkan pada Gambar 2. Git menampilkan peringatan bahwa tag 3.1.3 bukan sebuah commit dan berpindah ke commit 22d9247, sehingga repositori berada pada kondisi detached HEAD. Kondisi ini normal untuk clone berbasis tag dan tidak memengaruhi praktikum karena kita tidak akan membuat commit baru di repositori tersebut.
 
Gambar 2. Clone repositori Flask dan penyalinan direktori tutorial ke flask-app.
Sumber: hasil praktikum (render terminal VS Code).
3.2  Membuat Environment Python 3.14.4
Environment dibuat menggunakan uv agar versi Python dapat ditentukan secara eksplisit dan instalasi paket berlangsung cepat. Perintah uv venv --python 3.14.4 akan mengunduh CPython 3.14.4 bila belum tersedia, membuat direktori .venv, dan menyiapkan interpreter yang terisolasi dari Python sistem. Pada Windows, skrip aktivasi berada di .venv/Scripts; pada Linux/macOS berada di .venv/bin. File .python-version ditulis agar versi Python yang digunakan konsisten ketika proyek dibuka kembali.
Perintah:
uv venv --python 3.14.4
source .venv/Scripts/activate      # Linux/macOS: source .venv/bin/activate
echo "3.14.4" > .python-version
python --version

Gambar 3 memperlihatkan proses pembuatan environment dan verifikasi versi. Prompt terminal berubah menjadi (flask-app) setelah venv diaktifkan, menandakan bahwa perintah python dan flask akan memakai interpreter di dalam .venv.
 
Gambar 3. Pembuatan environment Python 3.14.4 dengan uv dan aktivasi venv.
Sumber: hasil praktikum (render terminal VS Code).
3.3  Instalasi Paket yang Diperlukan
Paket aplikasi didefinisikan pada pyproject.toml. Perintah uv pip install -e . melakukan editable install: paket flaskr dipasang sehingga perubahan pada kode sumber langsung terbaca tanpa perlu membangun ulang paket. Dependensi yang terpasang adalah Flask 3.1.3, Jinja2, Werkzeug, Click, ItsDangerous, Blinker, dan MarkupSafe.
Perintah:
uv pip install -e .

Hasil instalasi pada Gambar 4 menunjukkan delapan paket berhasil dipasang, termasuk flaskr 1.0.0 yang menunjuk ke direktori proyek. Dengan editable install, paket flaskr tidak disalin ke site-packages, tetapi dipasang sebagai tautan ke sumber proyek.
 
Gambar 4. Instalasi paket flaskr secara editable dengan uv pip install -e .
Sumber: hasil praktikum (render terminal VS Code).
3.4  Inisialisasi Database dan Menjalankan Aplikasi
Flaskr menggunakan SQLite. Perintah flask --app flaskr init-db menjalankan skrip flaskr/schema.sql untuk membuat tabel user dan post, lalu menyimpannya pada instance/flaskr.sqlite. Setelah database siap, server pengembangan dijalankan pada port 5000. Server Flask yang digunakan adalah development server; pesan peringatan pada keluaran menegaskan bahwa server ini tidak boleh dipakai untuk produksi.
Perintah:
flask --app flaskr init-db
flask --app flaskr run

Gambar 5 menunjukkan database berhasil diinisialisasi dan server melayani permintaan di http://127.0.0.1:5000. Baris Press CTRL+C to quit menandakan server berjalan di foreground; terminal tersebut harus tetap terbuka selama pengujian.
 
Gambar 5. Inisialisasi database dan menjalankan server Flask pada port 5000.
Sumber: hasil praktikum (render terminal VS Code).
3.5  Verifikasi melalui Browser
Aplikasi diakses melalui http://127.0.0.1:5000. Halaman awal menampilkan judul Posts, tautan Register, dan Log In (Gambar 6). Untuk mencoba alur autentikasi, halaman Register menyediakan formulir username dan password (Gambar 7), sedangkan halaman Log In digunakan untuk masuk dengan akun yang telah dibuat (Gambar 8). Rute ini ditangani oleh blueprint auth pada flaskr/auth.py, sedangkan halaman posting ditangani oleh blueprint blog.
 
Gambar 6. Halaman Posts aplikasi Flaskr pada http://127.0.0.1:5000.
Sumber: tangkapan layar aplikasi (Chrome headless, 2026).
 
Gambar 7. Halaman Register pada http://127.0.0.1:5000/auth/register.
Sumber: tangkapan layar aplikasi (Chrome headless, 2026).
 
Gambar 8. Halaman Log In pada http://127.0.0.1:5000/auth/login.
Sumber: tangkapan layar aplikasi (Chrome headless, 2026).
Pada praktikum ini halaman-halaman tersebut berhasil dimuat. Formulir Register dan Log In menggunakan session Flask serta penyimpanan password yang di-hash dengan Werkzeug, sehingga password tidak disimpan dalam bentuk teks biasa.
Ketiga halaman memakai template Jinja2 yang sama, yaitu base.html, melalui mekanisme template inheritance. Template turunan hanya mendefinisikan blok konten, sedangkan header, navigasi Register/Log In, dan pesan flash didefinisikan sekali pada template induk. Pola ini memisahkan tampilan dari logika aplikasi dan memudahkan perubahan antarmuka. Berkas statis seperti style.css dilayani dari direktori static, sedangkan instance/flaskr.sqlite menyimpan data pengguna dan post. Struktur inilah yang nantinya ikut tersalin ke dalam image container pada Bab 4.
BAB 4  CONTAINERIZATION DENGAN DOCKER
4.1  Menulis Dockerfile
Dockerfile diletakkan di direktori root aplikasi, sejajar dengan pyproject.toml. File ini mendefinisikan base image, direktori kerja, cara menyalin kode, instalasi dependensi, inisialisasi database, serta perintah yang dijalankan saat container dimulai. Isi Dockerfile ditunjukkan pada Gambar 9 dan Kode 1.
 
Gambar 9. Dockerfile aplikasi Flaskr di editor Visual Studio Code.
Sumber: berkas proyek flask-app/Dockerfile (2026).
Kode 1 — Dockerfile
FROM python:3.14
 
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -e .
RUN flask --app flaskr init-db
 
EXPOSE 5000
CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0", "--port=5000"]

Setiap instruksi memiliki peran yang spesifik. Tabel 4 merangkum fungsi dan alasan penggunaannya.
Tabel 4. Peran setiap instruksi dalam Dockerfile aplikasi Flaskr.
Instruksi	Fungsi dan Alasan
FROM python:3.14	Menentukan base image resmi Python 3.14 yang sudah berisi interpreter dan pip.
RUN mkdir /app; WORKDIR /app	Membuat dan menetapkan direktori kerja di dalam image agar seluruh perintah berikutnya berjalan pada lokasi yang konsisten.
ADD . /app/	Menyalin konteks build (kode aplikasi, pyproject.toml, Dockerfile) ke dalam image. File yang tidak diperlukan dikecualikan melalui .dockerignore.
RUN pip install -e .	Memasang aplikasi dan dependensinya di dalam image. Editable install dipakai karena kode sudah berada di /app.
RUN flask --app flaskr init-db	Membuat database SQLite awal di dalam image saat build. Pada produksi, inisialisasi sebaiknya dilakukan saat runtime dengan volume.
EXPOSE 5000	Mendokumentasikan port yang dipakai aplikasi di dalam container. EXPOSE tidak otomatis memublikasikan port ke host.
CMD [...]	Menjalankan Flask dengan host 0.0.0.0 agar dapat diakses dari luar container, pada port 5000.

Selain Dockerfile, dibuat file .dockerignore untuk mencegah direktori .venv, __pycache__, file .pyc, instance, dan .pytest_cache ikut masuk ke dalam image. Tanpa .dockerignore, venv Windows yang berisi berkas platform-specific akan memperbesar konteks build dan tidak berguna di dalam container Linux. Direktori instance juga dikecualikan agar database lokal tidak ikut tersalin; database di dalam image dibuat ulang oleh perintah init-db.
Kode 2 — .dockerignore
.venv
__pycache__
*.pyc
instance
.pytest_cache

4.2  Membangun Image Docker
Image dibangun dengan perintah docker build. Opsi -f menunjuk Dockerfile, -t memberi nama dan tag image (flaskr:1.0.0), dan titik di akhir perintah menunjuk direktori konteks build, yaitu direktori saat ini. Opsi --progress=plain dipakai agar keluaran build mudah dibaca dan didokumentasikan.
Perintah:
docker build --progress=plain -f Dockerfile -t flaskr:1.0.0 .

Gambar 10 menampilkan awal proses build. Docker memuat Dockerfile, mengambil metadata base image python:3.14, dan mengekstrak layer. Base image diunduh sekali dan disimpan di cache lokal, sehingga build berikutnya tidak perlu mengunduh ulang. Layer yang tidak berubah juga dipakai kembali dari cache.
 
Gambar 10. Awal proses docker build: pemuatan Dockerfile dan base image python:3.14.
Sumber: hasil praktikum (render terminal VS Code).
Gambar 11 menampilkan akhir proses build. Paket Flask dan dependensinya berhasil dipasang, database diinisialisasi, dan image diberi tag flaskr:1.0.0. Baris Successfully tagged menandakan image siap dijalankan.
 
Gambar 11. Akhir proses docker build: image flaskr:1.0.0 berhasil dibuat.
Sumber: hasil praktikum (render terminal VS Code).
4.3  Verifikasi Image
Image yang telah dibuat diverifikasi dengan docker image ls. Gambar 12 menunjukkan image flaskr:1.0.0 dengan ID a95c036735f3, disk usage 1.64 GB, dan content size 423 MB. Selisih antara disk usage dan content size terjadi karena layer base image dan metadata image ikut terhitung pada disk usage. Ukuran tersebut wajar untuk base image python:3.14 yang lengkap; optimasi dapat dilakukan dengan base image slim atau multi-stage build.
 
Gambar 12. Verifikasi image dan container dengan docker image ls serta docker ps.
Sumber: hasil praktikum (render terminal VS Code).
4.4  Menjalankan Container
Container dijalankan dengan memetakan port 5000 di dalam container ke port 5001 di host. Format -p 5001:5000 berarti host:container. Aplikasi tetap mendengarkan port 5000 di dalam container, tetapi dari sisi host dapat diakses melalui http://127.0.0.1:5001. Pemetaan ini memungkinkan beberapa container berjalan bersamaan tanpa bentrok port.
Perintah:
docker run -p 5001:5000 flaskr:1.0.0

Gambar 13 menampilkan log container. Flask melaporkan berjalan pada 0.0.0.0:5000 di dalam container, dengan alamat 172.17.0.2 yang merupakan alamat container pada network bridge Docker. Pesan peringatan development server kembali muncul; untuk produksi, aplikasi perlu dijalankan dengan WSGI server seperti Gunicorn atau Waitress.
 
Gambar 13. Menjalankan container dengan pemetaan port 5001:5000.
Sumber: hasil praktikum (render terminal VS Code).
Akses browser ke http://127.0.0.1:5001 menampilkan aplikasi Flaskr yang sama (Gambar 14). Dengan demikian, aplikasi telah berhasil dijalankan sebagai containerized app dan dapat diakses dari host melalui port yang dipetakan.
 
Gambar 14. Aplikasi Flaskr diakses dari container melalui http://127.0.0.1:5001.
Sumber: tangkapan layar aplikasi (Chrome headless, 2026).
4.5  Menghentikan dan Membersihkan Container
Container yang dijalankan di foreground dapat dihentikan dengan Ctrl+C. Untuk container yang berjalan di background, gunakan docker ps untuk melihat ID atau nama container, lalu docker stop. Setelah tidak diperlukan, container dapat dihapus dengan docker rm. Image yang sudah tidak dipakai dapat dihapus dengan docker rmi, tetapi pada praktikum ini image lain tidak dihapus agar tidak mengganggu pekerjaan lain.
Perintah:
docker ps
docker stop <container-id>
docker rm <container-id>
docker rmi <image-id>        # opsional, hanya jika image tidak dipakai

4.6  Catatan untuk Produksi
Konfigurasi pada modul ditujukan untuk pembelajaran, bukan produksi. Beberapa hal yang perlu diperhatikan ketika aplikasi hendak dipakai di lingkungan nyata:
•  Jangan memakai Flask development server di produksi. Gunakan WSGI server seperti Gunicorn (Linux) atau Waitress (Windows), lalu letakkan reverse proxy di depannya.
•  Jangan menginisialisasi database hanya saat build. Gunakan volume untuk menyimpan data dan jalankan migrasi/inisialisasi saat container mulai, agar data tidak hilang ketika container diganti.
•  Jalankan container sebagai pengguna non-root dan batasi kapabilitasnya.
•  Sematkan versi base image (misalnya dengan digest) agar build reprodusibel.
BAB 5  CONTAINERIZATION DENGAN PODMAN
5.1  Gambaran Podman
Podman adalah container engine yang kompatibel dengan OCI dan menyediakan antarmuka baris perintah yang mirip Docker. Perbedaan utamanya adalah Podman tidak memerlukan daemon: perintah podman menjalankan proses container secara langsung (fork/exec), sehingga tidak ada layanan latar belakang yang harus aktif. Podman juga mendukung mode rootless secara default, yang mengurangi risiko keamanan karena container tidak harus berjalan dengan hak root.
Karena kompatibel dengan OCI dan Dockerfile, image yang dibangun dengan Docker dapat dijalankan dengan Podman, dan sebaliknya. Podman juga menyediakan podman-compose serta integrasi Quadlet/systemd untuk menjalankan container sebagai layanan sistem.
5.2  Lingkungan dan Keterbatasan
Podman tidak terpasang secara native pada host Windows yang digunakan untuk praktikum ini. Di Windows dan macOS, Podman biasanya dijalankan melalui podman machine, yaitu VM Linux ringan berbasis WSL2 atau Hyper-V. Docker Desktop yang tersedia di host hanya menyediakan engine Docker, bukan Podman. Percobaan menjalankan Podman di dalam container resmi memerlukan mode privileged dan tidak diizinkan oleh kebijakan keamanan lingkungan praktikum.
Keterangan sumber gambar
Gambar 15–17 pada bab ini dikutip dari modul praktikum (lingkungan Linux) sebagai referensi keluaran Podman. Perintah dan hasilnya dapat direproduksi pada Linux atau pada Windows/macOS yang telah memasang Podman machine. Implementasi yang diverifikasi langsung pada laporan ini adalah Docker (Bab 4).

5.3  Build, Verifikasi, dan Run dengan Podman
Podman memakai Dockerfile yang sama. Perintah build, daftar image, dan run memiliki bentuk yang identik dengan Docker, sehingga migrasi dari Docker ke Podman tidak memerlukan perubahan pada artefak aplikasi.
Perintah (Linux):
podman build -f Dockerfile -t flaskr:1.0.0 .
podman image ls
podman run -p 5001:5000 flaskr:1.0.0

Gambar 15 menampilkan proses podman build. Podman mengambil base image python:3.14, menjalankan setiap instruksi Dockerfile, lalu memberi tag localhost/flaskr:1.0.0. Perhatikan bahwa nama image diakhiri dengan localhost/ karena Podman menyimpan image pada registry lokal secara default.
 
Gambar 15. Contoh keluaran podman build (referensi modul, Linux).
Sumber: modul praktikum Modul 7, halaman 7–9 (dikutip sebagai referensi).
Gambar 16 menunjukkan daftar image hasil build. Image localhost/flaskr:1.0.0 memiliki ukuran sekitar 1.16 GB, sedangkan base image python:3.14 sekitar 1.14 GB. Selisih kecil ini menunjukkan bahwa sebagian besar ukuran berasal dari base image.
 
Gambar 16. Contoh keluaran podman image ls (referensi modul, Linux).
Sumber: modul praktikum Modul 7, halaman 10 (dikutip sebagai referensi).
Gambar 17 menampilkan container yang berjalan dengan pemetaan port 5001:5000. Sama seperti Docker, aplikasi di dalam container tetap mendengarkan port 5000 dan dapat diakses dari host melalui port 5001.
 
Gambar 17. Contoh keluaran podman run (referensi modul, Linux).
Sumber: modul praktikum Modul 7, halaman 10 (dikutip sebagai referensi).
Jika Podman hendak digunakan di Windows, langkah umumnya adalah memasang Podman Desktop, menjalankan podman machine init, lalu podman machine start. Setelah VM aktif, perintah podman build dan podman run dapat dijalankan dari terminal Windows. Pada Linux, Podman dapat langsung dipakai tanpa VM karena berjalan di atas kernel yang sama.
5.4  Perbandingan Docker dan Podman
Aspek	Docker	Podman
Arsitektur	Client-server dengan daemon dockerd	Daemonless; proses container dijalankan langsung
Hak akses	Daemon umumnya berjalan sebagai root; rootless tersedia	Rootless secara default
Kompatibilitas	Standar de facto container	OCI-compatible; CLI dan Dockerfile kompatibel
Compose	docker compose	podman-compose atau Quadlet
Integrasi systemd	Perlu konfigurasi tambahan	Quadlet/systemd tersedia
Windows/macOS	Docker Desktop dengan VM Linux	Podman machine (WSL2/Hyper-V)
Pada praktikum ini	Dijalankan dan diverifikasi langsung	Tidak tersedia native; keluaran mengacu pada modul

BAB 6  PEMBAHASAN
6.1  Mengapa Aplikasi Cocok Dijadikan Containerized App
Flaskr adalah aplikasi web dengan dependensi yang jelas: Flask, Jinja2, Werkzeug, dan beberapa pustaka pendukung. Seluruh dependensi tersebut dideklarasikan pada pyproject.toml, sehingga dapat dipasang ulang secara konsisten. Container membungkus aplikasi, dependensi, dan konfigurasi runtime ke dalam satu image. Hasilnya, aplikasi tidak bergantung pada kondisi Python di host dan dapat dijalankan dengan cara yang sama di mesin lain.
Dengan container, perbedaan lingkungan seperti versi Python, lokasi venv, atau paket sistem tidak lagi menjadi sumber masalah. Image menjadi artefak yang dapat diuji, diberi versi, dan dipromosikan dari lingkungan pengembangan ke staging maupun produksi.
6.2  Layer, Cache, dan Ukuran Image
Setiap instruksi pada Dockerfile menghasilkan layer. Layer yang tidak berubah akan dipakai kembali dari cache, sehingga build berikutnya lebih cepat. Urutan instruksi memengaruhi efektivitas cache: menyalin seluruh kode sebelum instalasi dependensi menyebabkan layer instalasi ikut dibangun ulang setiap kali kode berubah. Praktik yang lebih baik adalah menyalin file dependensi terlebih dahulu, memasang dependensi, lalu menyalin sisa kode.
Ukuran image flaskr:1.0.0 sekitar 1.64 GB (423 MB content) karena base image python:3.14 bersifat lengkap. Untuk produksi, base image slim, multi-stage build, dan pembersihan cache pip dapat menurunkan ukuran secara signifikan. Meskipun demikian, untuk tujuan pembelajaran, image tersebut sudah memadai karena seluruh dependensi dan database awal tersedia.
6.3  Port Mapping dan Isolasi Container
Container memiliki network namespace sendiri, sehingga port 5000 di dalam container tidak otomatis terlihat dari host. Opsi -p 5001:5000 membuat Docker meneruskan koneksi dari port 5001 di host ke port 5000 di container. Aplikasi harus mendengarkan 0.0.0.0, bukan 127.0.0.1, agar dapat diakses dari luar container. Itulah sebabnya CMD menggunakan opsi --host=0.0.0.0. Isolasi ini memungkinkan beberapa container berjalan bersamaan dengan pemetaan port yang berbeda.
6.4  Database di Dalam Image
Dockerfile menjalankan init-db saat build. Pendekatan ini praktis untuk demonstrasi karena container langsung memiliki database yang siap dipakai. Namun, untuk aplikasi nyata, data yang ditulis saat container berjalan bersifat sementara: ketika container dihapus dan dijalankan ulang dari image, data kembali ke kondisi awal. Solusi yang tepat adalah menyimpan database pada volume atau layanan basis data terkelola, serta menjalankan migrasi saat container mulai. Praktikum ini memberi gambaran penting bahwa container bersifat ephemeral dan data harus dipisahkan dari lifecycle container.
6.5  Hubungan dengan XaaS
Praktikum memperlihatkan rantai yang menghubungkan konsep XaaS dengan implementasi teknis. Docker Desktop menyediakan infrastruktur virtual (IaaS) berupa VM Linux. Di atasnya, container engine menjalankan image aplikasi. Alur build–run ini mirip dengan layanan PaaS yang menerima kode atau image lalu menjalankannya, meskipun pada praktikum seluruh kendali berada di tangan praktikan. Jika aplikasi yang sama dijalankan pada layanan container terkelola, konsumen tidak perlu mengelola VM, runtime, atau patch sistem operasi; cukup menyerahkan image dan konfigurasi. Dengan demikian, container menjadi unit yang memungkinkan aplikasi berpindah antar-lapisan XaaS tanpa perubahan besar.
6.6  Kendala Lingkungan
•  Windows menggunakan path .venv/Scripts untuk aktivasi, sedangkan modul (Linux) menggunakan .venv/bin. Perbedaan ini hanya pada perintah aktivasi dan tidak memengaruhi isi aplikasi.
•  Perintah sudo systemctl start docker dan sudo dinitctl start dockerd tidak berlaku di Windows; Docker Desktop mengelola daemon melalui aplikasi desktop.
•  Podman tidak tersedia native di Windows. Menjalankannya di dalam container memerlukan mode privileged yang tidak diizinkan pada lingkungan ini, sehingga keluarannya dikutip dari modul.
•  Path Windows yang panjang dan perbedaan line ending dapat memengaruhi Git dan Docker; penggunaan .dockerignore membantu menjaga konteks build tetap bersih.
6.7  Keamanan dan Praktik Terbaik
Beberapa praktik terbaik yang dapat diterapkan pada pengembangan selanjutnya:
•  Gunakan base image resmi dengan tag versi yang spesifik atau digest, lalu perbarui secara berkala untuk mendapatkan patch keamanan.
•  Jalankan proses container sebagai non-root dan terapkan read-only filesystem bila memungkinkan.
•  Jangan menyimpan kredensial di Dockerfile atau image; gunakan secret manager atau environment variable yang disuntikkan saat runtime.
•  Pisahkan data dari container dengan volume, dan lakukan backup secara teratur.
•  Gunakan WSGI server produksi, health check, serta logging terpusat.
•  Scan image dengan alat seperti Trivy atau Docker Scout sebelum dipublikasikan.
BAB 7  KESIMPULAN
1.  XaaS membagi layanan cloud menjadi SaaS, PaaS, dan IaaS. Contoh yang dibahas adalah Google Workspace (SaaS), Google App Engine (PaaS), dan Amazon EC2 (IaaS). Setiap kategori memiliki pembagian tanggung jawab yang berbeda antara konsumen dan penyedia.
2.  Arsitektur XaaS dapat divisualisasikan sebagai tiga lapisan layanan di atas infrastruktur fisik penyedia. Semakin tinggi lapisan, semakin sedikit komponen yang dikelola konsumen.
3.  Aplikasi Flaskr berhasil disiapkan dengan Python 3.14.4, dependensi terpasang secara editable, database SQLite diinisialisasi, dan aplikasi berjalan pada port 5000.
4.  Dockerfile berhasil mengubah Flaskr menjadi image flaskr:1.0.0. Container dijalankan dengan pemetaan port 5001:5000 dan aplikasi dapat diakses dari browser pada http://127.0.0.1:5001.
5.  Podman menggunakan Dockerfile dan perintah yang kompatibel dengan Docker. Pada lingkungan Windows ini Podman tidak tersedia secara native, sehingga keluarannya dikutip dari modul sebagai referensi; implementasi yang diverifikasi langsung adalah Docker.
6.  Container membuat aplikasi lebih portabel dan reprodusibel, tetapi data harus dipisahkan dari image dan server pengembangan tidak boleh dipakai di produksi.
Praktikum ini menunjukkan bahwa satu Dockerfile yang sama dapat menghasilkan image yang konsisten di mesin mana pun selama container engine tersedia. Untuk pengembangan berikutnya, image dapat dipublikasikan ke registry, dijalankan dengan WSGI server produksi, dan diorkestrasi bersama basis data eksternal. Penambahan health check, volume, serta pipeline build otomatis akan melengkapi alur yang telah dicoba pada praktikum ini.
DAFTAR PUSTAKA
[1]  Pallets Projects. (2026). Flask Tutorial. https://flask.palletsprojects.com/en/stable/tutorial/
[2]  Pallets Projects. (2025). Flask 3.1.3 — examples/tutorial. GitHub. https://github.com/pallets/flask/tree/3.1.3/examples/tutorial
[3]  Docker Inc. (2026). Dockerfile reference. https://docs.docker.com/reference/dockerfile/
[4]  Docker Inc. (2026). Docker overview. https://docs.docker.com/get-started/docker-overview/
[5]  Podman. (2026). Podman Documentation. https://docs.podman.io/
[6]  Mell, P., & Grance, T. (2011). The NIST Definition of Cloud Computing (NIST Special Publication 800-145). National Institute of Standards and Technology.
[7]  Google Cloud. (2026). App Engine documentation. https://cloud.google.com/appengine/docs
[8]  Amazon Web Services. (2026). Amazon EC2 User Guide. https://docs.aws.amazon.com/ec2/
[9]  Google Workspace. (2026). Google Workspace Admin Help. https://support.google.com/a
LAMPIRAN
Lampiran A  Struktur Proyek
Struktur direktori flask-app setelah proses praktikum:
flask-app/
+-- flaskr/
|   +-- __init__.py          # application factory
|   +-- auth.py              # blueprint autentikasi (register, login, logout)
|   +-- blog.py              # blueprint posting (CRUD)
|   +-- db.py                # koneksi SQLite dan CLI init-db
|   +-- schema.sql           # skema tabel user dan post
|   +-- static/style.css     # gaya tampilan
|   +-- templates/           # template Jinja2
+-- tests/                   # pengujian pytest
+-- Dockerfile               # definisi image
+-- .dockerignore            # berkas yang tidak masuk konteks build
+-- pyproject.toml           # metadata dan dependensi
+-- .python-version          # pin Python 3.14.4
+-- README.rst
+-- LICENSE.txt
+-- instance/flaskr.sqlite   # database lokal (tidak ikut image)

Lampiran B  Dockerfile
FROM python:3.14
 
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -e .
RUN flask --app flaskr init-db
 
EXPOSE 5000
CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0", "--port=5000"]

Lampiran C  pyproject.toml
[project]
name = "flaskr"
version = "1.0.0"
description = "The basic blog app built in the Flask tutorial."
readme = "README.rst"
license = {file = "LICENSE.txt"}
maintainers = [{name = "Pallets", email = "contact@palletsprojects.com"}]
classifiers = ["Private :: Do Not Upload"]
dependencies = [
    "flask",
]
 
[project.urls]
Documentation = "https://flask.palletsprojects.com/tutorial/"
 
[project.optional-dependencies]
test = ["pytest"]
 
[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
 
[tool.flit.module]
name = "flaskr"
 
[tool.flit.sdist]
include = [
    "tests/",
]
 
[tool.pytest.ini_options]
testpaths = ["tests"]
filterwarnings = ["error"]

Lampiran D  Perintah Lengkap
# 1. Clone dan salin tutorial
cd $HOME/src
git clone --depth 1 --branch 3.1.3 https://github.com/pallets/flask
cp -R ~/src/flask/examples/tutorial flask-app
cd flask-app
 
# 2. Environment Python 3.14.4
uv venv --python 3.14.4
source .venv/Scripts/activate        # Linux/macOS: source .venv/bin/activate
echo "3.14.4" > .python-version
uv pip install -e .
 
# 3. Inisialisasi dan jalankan aplikasi
flask --app flaskr init-db
flask --app flaskr run
 
# 4. Docker
docker build --progress=plain -f Dockerfile -t flaskr:1.0.0 .
docker image ls flaskr
docker run -p 5001:5000 flaskr:1.0.0
 
# 5. Verifikasi dari terminal lain
curl -I http://127.0.0.1:5001
docker ps
docker stop <container-id>
 
# 6. Podman (Linux)
podman build -f Dockerfile -t flaskr:1.0.0 .
podman image ls
podman run -p 5001:5000 flaskr:1.0.0

Lampiran E  Ringkasan Hasil Pengujian
No	Pengujian	Perintah / URL	Hasil
1	Aplikasi lokal	flask --app flaskr run; http://127.0.0.1:5000	HTTP 200; halaman Posts tampil
2	Halaman Register	http://127.0.0.1:5000/auth/register	Form register tampil
3	Halaman Log In	http://127.0.0.1:5000/auth/login	Form login tampil
4	Build image	docker build -t flaskr:1.0.0 .	Image flaskr:1.0.0 (ID a95c036735f3)
5	Daftar image	docker image ls flaskr	1.64 GB (423 MB content)
6	Run container	docker run -p 5001:5000 flaskr:1.0.0	HTTP 200 pada http://127.0.0.1:5001
7	Podman	podman build / podman run	Referensi modul; tidak tersedia native

Lampiran F  Catatan Gambar dan Reproduksibilitas
Gambar terminal dibuat dengan merender keluaran sesi nyata ke dalam tampilan terminal Visual Studio Code (tema gelap, prompt Git Bash, status bar). Konten perintah dan keluaran dipertahankan sesuai sesi; beberapa baris panjang dibungkus oleh terminal. Gambar browser merupakan tangkapan layar nyata halaman Flaskr pada 1280 × 760 piksel dengan skala 2×.
Gambar 15–17 (Podman) merupakan kutipan keluaran dari modul praktikum karena Podman tidak tersedia secara native pada host Windows yang dipakai. Pembaca yang ingin mereproduksinya dapat menjalankan perintah pada Linux, atau memasang Podman machine pada Windows/macOS. Seluruh perintah dan berkas konfigurasi tersedia pada Lampiran B–D sehingga praktikum dapat diulang.
Identitas pada halaman sampul sengaja dikosongkan agar dapat diisi sesuai data mahasiswa sebelum laporan dikumpulkan.
