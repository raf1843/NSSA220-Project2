from filter_packets import *
from packet_parser import *
from compute_metrics import *

# Hardcoded IP addresses
ip1 = "192.168.100.1"
ip2 = "192.168.100.2"
ip3 = "192.168.200.1" 
ip4 = "192.168.200.2"

print("Starting packet analysis!")

#filters nodes 1-4
filter('../Captures/Node1.txt')
filter('../Captures/Node2.txt')
filter('../Captures/Node3.txt')
filter('../Captures/Node4.txt')


# storage
L1, L2, L3, L4 = [], [], [], []
D1, D2, D3, D4 = {}, {}, {}, {}
# for each node, format then parse
hex_formatting('../Captures/Node1_filtered.txt', L1) 
hex_parse(L1, ip1, D1)
hex_formatting('../Captures/Node2_filtered.txt', L2) 
hex_parse(L2, ip2, D2)
hex_formatting('../Captures/Node3_filtered.txt', L3) 
hex_parse(L3, ip3, D3)
hex_formatting('../Captures/Node4_filtered.txt', L4) 
hex_parse(L4, ip4, D4)

print("\nComputing for Node 1...")
compute(D1)
print("\nComputing for Node 2...")
compute(D2)
print("\nComputing for Node 3...")
compute(D3)
print("\nComputing for Node 4...")
compute(D4)

