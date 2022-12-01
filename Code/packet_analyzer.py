from filter_packets import *
from packet_parser import *
from compute_metrics import *

# List of hardcoded IP addresses
ips = ["192.168.100.1", "192.168.100.2", "192.168.200.1", "192.168.200.2"]

print("Starting packet analysis!")

for i in range(1, 5):
	in_fn = '../Captures/Node' + str(i) + '.txt'
	filter_fn = '../Captures/Node' + str(i) + '_filtered.txt'
	out_fn = '../packet_analysis_output.csv'
	L = []
	D = {}

	#filters nodes 1-4
	filters(in_fn)

	# for each node, format then parse
	hex_formatting(filter_fn, L) 
	hex_parse(L, ips[i-1], D)

	# compute metrics
	if i == 1:
		with open(out_fn, 'w') as f:
			f.write('Node ' + str(i) + '\n\n')
	else:	
		with open(out_fn, 'a') as f:
			f.write('Node ' + str(i) + '\n\n')
	compute(D, out_fn)

print("Done! See output at " + out_fn)

