"""Menghindari race condition menggunakan threading.Lock."""
import threading

counter = 0
lock = threading.Lock()
ITERATIONS = 1000

def increment():
    global counter
    for _ in range(ITERATIONS):
        with lock:
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print("Nilai yang diharapkan:", ITERATIONS * 2)
print("Nilai aktual:", counter)
print("Lock melindungi operasi pembaruan agar dilakukan satu thread pada satu waktu.")
