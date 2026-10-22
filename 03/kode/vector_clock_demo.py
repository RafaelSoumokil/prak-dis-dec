from vector_clock import VectorClock

p1 = VectorClock(3)
p2 = VectorClock(3)
p3 = VectorClock(3)

print("Event lokal pada P1:", p1.send_event(0))
message = p1.send_event(0)
print("P1 mengirim pesan:", message)
p2.receive_event(1, message)
print("P2 menerima pesan:", p2.snapshot())
p3.send_event(2)
print("Event lokal pada P3:", p3.snapshot())
print("Perbandingan manual: P1 mengubah komponen pertama; P2 mengambil maksimum komponen per komponen, lalu menaikkan komponen P2.")
