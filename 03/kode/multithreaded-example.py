"""Menunjukkan bahwa urutan output thread dapat berbeda antar-eksekusi."""
import threading
import time
import random

def worker(name):
    time.sleep(random.uniform(0.01, 0.15))
    print(f"{name}: mulai")
    time.sleep(random.uniform(0.01, 0.15))
    print(f"{name}: selesai")

threads = [threading.Thread(target=worker, args=(f"Thread-{i}",)) for i in range(1, 4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print("Selesai: urutan dapat berubah karena penjadwalan thread dan jeda acak.")
