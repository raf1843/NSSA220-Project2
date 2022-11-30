# Computes a series of metrics for use in packet analysis
# Raina Freeman, November 2022

def size_metrics(packets):
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
		length = p[5] # this will be passed in from data
		data = p[6]

		# request
		if "Request" in p[4]:
			# sent or recv
			if "Sent" in p[4]:
				num_req_sent += 1
				req_bytes_sent += length
				req_data_sent += data
			else: 
				num_req_recv += 1
				req_bytes_recv += length
				req_data_recv += data
		# reply
		else:
			# sent or recv
			if "Sent" in p[4]:
				num_rep_sent += 1
			else:
				num_rep_recv += 1

	
	return [num_req_sent, num_req_recv, num_rep_sent, num_rep_recv, \
		req_bytes_sent, req_bytes_recv, req_data_sent, req_data_recv]
			

def time_metrics(packets, req_bytes_sent, req_data_sent, num_req_sent, num_rep_sent): 
	# ping round trip time
	# time btwn send req and recv rep in ms
	avg_rtt = 0
	sum_rtt = 0
	for i in range(0, len(packets)): 
		if packets[i][1] == 0 and packets[i][2] == 's':
			for j in range (i, len(packets)):
				if packets[i][0] == packets[j][0] and packets[j][1] == 8:
					sum_rtt += (packets[j][4] - packets[i][4])
	avg_rtt = sum_rtt / num_req_sent		

	# throughput in kB/s - frames
	req_tput = req_bytes_sent / sum_rtt
	# goodput in kB/s - data
	req_gput = req_data_sent / sum_rtt
	# avg reply delay in microseconds
	# time between node receiving req and sending rep
	avg_rep_delay = 0
	sum_rep_delay = 0
	for i in range(0, len(packets)): 
		if packets[i][1] == 0 and packets[i][2] == 'r':
			for j in range (i, len(packets)):
				if packets[i][0] == packets[j][0] and packets[j][1] == 8:
					sum_rep_delay += (packets[j][4] - packets[i][4])
	avg_rep_delay = sum_rep_delay / num_rep_sent
	return [avg_rtt, req_tput, req_gput, avg_rep_delay]


def distance_metrics(packets, num_req_sent):
	# avg num hops per request
	avg_hops_req = 0
	sum_hops_req = 0
	for i in range(0, len(packets)): 
		if packets[i][1] == 0 and packets[i][2] == 's':
			for j in range (i, len(packets)):
				if packets[i][0] == packets[j][0] and packets[j][1] == 8:
					ttl_req = packets[i][5]
					ttl_rep = packets[j][5]
					hops = ttl_req - ttl_rep + 1 # need to figure out how this will actually work
					sum_hops_req += hops
	avg_hops_req = sum_hops_req / num_req_sent
	return int(avg_hops_req)


def compute(packet_dict):
	packets = []
	for k in packet_dict.keys():
		packets.append(k)
		packets.append(packet_dict[k])
	size_mets = size_metrics(packets)
	print("Size: ", size_mets)
	# pass through request bytes sent, request data sent, number of requests sent, and number of 	replies sent
	#time_mets = time_metrics(packets, size_mets[4], size_mets[6], size_mets[3], size_mets[4])
	#print("Time: ", time_mets)
	# pass through number of requests sent
	#dist_mets = distance_metrics(packets, size_mets[0])
	#print("Distance: ", dist_mets)


# Dictionary Format:
# Packet Tuple : Response Packet Tuple
# Packet Format (Same for both Packet and Response Packet):
# [(Packet No.), (Time), (Source IP), (Dest. IP), (Msg Type), (Total Packet Size), 
# (Payload Size), (Seq No.), (TTL), (Associated Packet No.)]


if __name__ == '__main__':
	main()


