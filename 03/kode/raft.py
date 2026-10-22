"""Contoh simulasi pemilihan leader menggunakan modul raft_module."""
from raft_module import RaftElection

cluster = RaftElection(["Node-A", "Node-B", "Node-C", "Node-D", "Node-E"])
leader = cluster.elect_leader("Node-C", votes=3)
print("Leader terpilih:", leader)
print("Status node:")
cluster.show_status()
