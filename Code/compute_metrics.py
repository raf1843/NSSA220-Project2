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
			

def time_metrics(packet_dict, req_bytes_sent, req_data_sent, num_req_sent, num_rep_sent): 
	# ping round trip time
	# time btwn send req and recv rep in ms
	avg_rtt = 0
	sum_rtt = 0
	for p in packet_dict.keys():
		if "Request Sent" in p[4]:
			sum_rtt += (float(packet_dict[p][1]) - float(p[1]))
	avg_rtt = sum_rtt / num_req_sent	
	# convert to ms
	avg_rtt *= 1000	

	# throughput in kB/s - frames
	req_tput = req_bytes_sent / sum_rtt
	# convert to kB
	req_tput /= 1000
	# goodput in kB/s - data
	req_gput = req_data_sent / sum_rtt
	# convert to kB
	req_gput /= 1000
	# avg reply delay in microseconds
	# time between node receiving req and sending rep
	avg_rep_delay = 0
	sum_rep_delay = 0
	for p in packet_dict.keys(): 
		if "Request Received" in p[4]:
			sum_rep_delay += (float(packet_dict[p][1]) - float(p[1]))
	avg_rep_delay = sum_rep_delay / num_rep_sent
	# convert to microseconds
	avg_rep_delay *= 1000000
	return [avg_rtt, req_tput, req_gput, avg_rep_delay]


def distance_metrics(packet_dict, num_req_sent):
	# avg num hops per request
	avg_hops_req = 0
	sum_hops_req = 0
	for p in packet_dict.keys(): 
		if "Request Sent" in p[4]:
			ttl_req = p[8]
			ttl_rep = packet_dict[p][8]
			hops = ttl_req - ttl_rep + 1 
			sum_hops_req += hops
	avg_hops_req = sum_hops_req / num_req_sent
	return avg_hops_req


def compute(packet_dict, out_fn):
	packets = []
	for k in packet_dict.keys():
		packets.append(k)
		packets.append(packet_dict[k])
	size_mets = size_metrics(packets)
	'''
	returns [num_req_sent, num_req_recv, num_rep_sent, num_rep_recv, 
			req_bytes_sent, req_bytes_recv, req_data_sent, req_data_recv]
'	'''

	# pass through request bytes sent, request data sent, number of requests sent, and number of replies sent
	time_mets = time_metrics(packet_dict, size_mets[4], size_mets[6], size_mets[0], size_mets[2])
	'''
	returns [avg_rtt, req_tput, req_gput, avg_rep_delay]
'	'''

	# pass through number of requests sent
	dist_mets = distance_metrics(packet_dict, size_mets[0])
	'''
	returns avg_hops_req
	'''
	
	# OUTPUT
	temp = ""
	with open (out_fn, 'a') as f:
		# size
		f.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received\n")
		for i in range(0,4):
			temp += str(size_mets[i])
			if i < 3:
				temp += ','
			else:
				temp += '\n'
		f.write(temp)
		f.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\n")
		temp = str(size_mets[4]) + ',' + str(size_mets[5]) + '\n'
		f.write(temp)
		f.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)\n")
		temp = str(size_mets[6]) + ',' + str(size_mets[7]) + '\n\n'
		f.write(temp)
		
		# time + distance
		timestrs = ["Average RTT (milliseconds)", "Echo Request Throughput (kB/sec)", \
		"Echo Request Goodput (kB/sec)", "Average Reply Delay (microseconds)"]
		for i in range(0,len(timestrs)):
			temp = timestrs[i] + ',' + str(round(time_mets[i], 2)) + '\n'
			f.write(temp)
		f.write('Average Echo Request Hop Count' + ',' + str(round(dist_mets, 2)) + '\n\n')
		

# Dictionary Format:
# Packet Tuple : Response Packet Tuple
# Packet Format (Same for both Packet and Response Packet):
# [(Packet No.), (Time), (Source IP), (Dest. IP), (Msg Type), (Total Packet Size), 
# (Payload Size), (Seq No.), (TTL), (Associated Packet No.)]


if __name__ == '__main__':
	main()


