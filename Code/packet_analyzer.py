from filter_packets import *
from packet_parser import *
from compute_metrics import *

# Hardcoded IP addresses
ip1 = "192.168.100.1"
ip2 = "192.168.100.2"
ip3 = "192.168.200.1" 
ip4 = "192.168.200.2"

#filters nodes 1-4
filter('Node1.txt')
#filter('Node2.txt')
#filter('Node3.txt')
#filter('Node4.txt')


# storage
L = []
D1, D2, D3, D4 = {}, {}, {}, {}
# for each node, format then parse
hex_formatting('Node1_filtered.txt', L) 
iMet = hex_parse(L, ip1, D1)
#hex_formatting('Node2_filtered.txt', L) 
#hex_parse(L, ip2, D2)
#hex_formatting('Node3_filtered.txt', L) 
#hex_parse(L, ip3, D3)
#hex_formatting('Node4_filtered.txt', L) 
#hex_parse(L, ip4, D4)


compute(D1)
#compute(D2)
#compute(D3)
#compute(D4)

