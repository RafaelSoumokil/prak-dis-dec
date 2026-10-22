"""Contoh race condition yang dibuat lebih mudah diamati dengan jeda."""
import threading
import time

counter = 0
ITERATIONS = 100

def increment():
    global counter
    for _ in range(ITERATIONS):
        current = counter       # baca nilai bersama
        time.sleep(0.00001)     # memberi peluang thread lain menyela
        counter = current + 1   # tulis kembali nilai

threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print("Nilai yang diharapkan:", ITERATIONS * 2)
print("Nilai aktual:", counter)
print("Catatan: besarnya selisih dapat berbeda setiap eksekusi dan pada setiap versi/interpreter Python.")
