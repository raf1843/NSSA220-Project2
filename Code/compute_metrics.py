# Computes a series of metrics for use in packet analysis
# Raina Freeman, November 2022

def size_metrics(packets):
	# length of headers in bytes
	ETH_HEAD = 14
	IP_HEAD = 20
	ICMP_HEAD = 8
	# counters
	num_req_sent = 0
	num_req_recv = 0
	num_rep_sent = 0
	num_rep_recv = 0
	# bytes based on frame, data based on ICMP
	req_bytes_sent = 0
	req_bytes_recv = 0
	req_data_sent = 0
	req_data_recv = 0
	
	for p in packets:
		# to get data from bytes
		length = 0 # this will be passed in from data
		data = length - (ETH_HEAD + IP_HEAD + ICMP_HEAD)
	
	return [num_req_sent, num_req_recv, num_rep_sent, num_rep_recv, req_bytes_sent, req_bytes_recv, \
			req_data_sent, req_data_recv]
			

def time_metrics(packets, req_bytes_sent, req_data_sent, num_rep_sent): 
	# ping round trip time
	# time btwn send req and recv rep in ms
	avg_rtt = 0
	sum_rtt = 0
	# throughput in kB/s - frames
	req_tput = req_bytes_sent / sum_rtt
	# goodput in kB/s - data
	req_gput = req_data_sent / sum_rtt
	# avg reply delay in microseconds
	# time between node receiving req and sending rep
	avg_rep_delay = 0
	sum_rep_delay = 0
	for p in packets:
		sum_rep_delay += (t_recv_req - t_send_rep)
	avg_rep_delay = sum_rep_delay / num_rep_sent

def distance_metrics(packets, num_req_sent):
	# avg num hops per request
	avg_hops_req = 0
	sum_hops_req = 0
	# fix loop
	for p in packets:
		hops = ttl_req - ttl_rep + 1 # need to figure out how this will actually work
		sum_hops_req += hops
	avg_hops_req = sum_hops_sent / num_req_sent

def compute(packets):
	print('called compute')

	size_mets = size_metrics(packets)
	# pass through request bytes sent, request data sent, and number of replies sent
	time_mets = time_metrics(packets, size_mets[4], size_mets[6], size_mets[3])
	# pass through number of requests sent
	dist_mets = distance_metrics(packets, size_mets[0])
