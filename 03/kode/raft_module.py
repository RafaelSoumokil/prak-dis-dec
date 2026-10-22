"""Simulasi pemilihan leader Raft yang disederhanakan untuk pembelajaran.
Bukan implementasi Raft produksi: tidak mencakup log replication atau jaringan nyata.
"""
from dataclasses import dataclass

@dataclass
class Node:
    node_id: str
    role: str = "Follower"
    term: int = 0
    voted_for: str | None = None

class RaftElection:
    def __init__(self, node_ids):
        if len(node_ids) < 1:
            raise ValueError("Minimal satu node diperlukan")
        self.nodes = {node_id: Node(node_id) for node_id in node_ids}

    def elect_leader(self, candidate_id: str, votes: int | None = None) -> str | None:
        if candidate_id not in self.nodes:
            raise ValueError("Candidate tidak ditemukan")
        total = len(self.nodes)
        majority = total // 2 + 1
        votes = majority if votes is None else votes
        candidate = self.nodes[candidate_id]
        candidate.term += 1
        candidate.role = "Candidate"
        print(f"{candidate_id} menjadi Candidate pada term {candidate.term}.")
        print(f"Suara diterima: {votes}; mayoritas yang dibutuhkan: {majority}.")
        if votes >= majority:
            for node in self.nodes.values():
                node.role = "Follower"
                node.voted_for = candidate_id
            candidate.role = "Leader"
            print(f"{candidate_id} terpilih sebagai Leader.")
            return candidate_id
        print("Suara belum mencapai mayoritas; leader belum terpilih.")
        return None

    def show_status(self):
        for node in self.nodes.values():
            print(f"{node.node_id}: {node.role}, term={node.term}, voted_for={node.voted_for}")
