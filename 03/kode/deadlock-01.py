"""Demonstrasi deadlock dengan timeout agar program tidak menggantung selamanya."""
import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_one():
    with lock_a:
        print("Thread A mendapatkan Lock A")
        time.sleep(0.1)
        print("Thread A mencoba mendapatkan Lock B")
        got_b = lock_b.acquire(timeout=0.5)
        if got_b:
            print("Thread A mendapatkan Lock B")
            lock_b.release()
        else:
            print("Thread A timeout: Lock B masih dipegang Thread B (deadlock dihindari agar demo berhenti)")

def thread_two():
    with lock_b:
        print("Thread B mendapatkan Lock B")
        time.sleep(0.1)
        print("Thread B mencoba mendapatkan Lock A")
        got_a = lock_a.acquire(timeout=0.5)
        if got_a:
            print("Thread B mendapatkan Lock A")
            lock_a.release()
        else:
            print("Thread B timeout: Lock A masih dipegang Thread A (deadlock dihindari agar demo berhenti)")

threads = [threading.Thread(target=thread_one), threading.Thread(target=thread_two)]
for t in threads: t.start()
for t in threads: t.join()
print("Demonstrasi selesai. Timeout digunakan supaya contoh aman dijalankan.")
