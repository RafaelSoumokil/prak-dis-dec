"""Modul VectorClock sederhana untuk demonstrasi logical clock."""

class VectorClock:
    def __init__(self, process_count: int):
        if process_count < 1:
            raise ValueError("process_count harus minimal 1")
        self.clock = [0] * process_count

    def tick(self, process_id: int) -> None:
        """Naikkan komponen untuk proses lokal (process_id dimulai dari 0)."""
        self.clock[process_id] += 1

    def send_event(self, process_id: int) -> list[int]:
        self.tick(process_id)
        return self.clock.copy()

    def receive_event(self, process_id: int, received_clock: list[int]) -> None:
        """Gabungkan clock pesan dan lokal, lalu catat event penerimaan."""
        if len(received_clock) != len(self.clock):
            raise ValueError("Panjang vector clock harus sama")
        self.clock = [max(a, b) for a, b in zip(self.clock, received_clock)]
        self.tick(process_id)

    def snapshot(self) -> list[int]:
        return self.clock.copy()

    def __repr__(self) -> str:
        return f"VectorClock({self.clock})"
