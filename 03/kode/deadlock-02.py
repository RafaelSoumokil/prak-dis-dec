"""Mengurangi risiko deadlock dengan mengambil lock dalam urutan konsisten."""
import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def worker(name):
    # Semua thread mengambil Lock A dahulu, kemudian Lock B.
    with lock_a:
        print(name, "mendapatkan Lock A")
        time.sleep(0.05)
        with lock_b:
            print(name, "mendapatkan Lock B dan menjalankan bagian kritis")
    print(name, "selesai")

threads = [threading.Thread(target=worker, args=(f"Thread-{i}",)) for i in (1, 2)]
for t in threads: t.start()
for t in threads: t.join()
print("Selesai tanpa deadlock karena urutan pengambilan lock konsisten.")
