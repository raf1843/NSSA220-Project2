# NSSA220-Project2
Packet Capture Analysis Tool

The packet capture analysis tool will
consist of three main phases
– Packet Filtering: keep only the packets
we want to analyze
– Packet Parsing: read relevant packet
fields into memory for processing
– Compute Metrics: using packet fields to
compute metrics

Task is to filter select ICMP packets
out of packet captures containing ~8000
packets collected across 4 nodes and
compute 13 metrics from them

Given one .pcap and one raw .txt file derived from pcap per node
Capture files contain anywhere from 1300-1800 packets

1. Filter packets to only echo requests and replies - Gavin
2. Parse relevant fields out of filtered packets - Ivan
3. Calculate metrics from relevant fields - Raina

Metrics:

Data size (8):
  1. number of echo requests sent
  2. number of echo requests recv
  3. number of echo replies sent
  4. number of echo replies recv
  5. total echo request bytes sent
  6. total echo request bytes recv
  7. total echo request data sent in bytes (based on amount of data in ICMP payload)
  8. total echo request data recv in bytes (based on amount of data in ICMP payload)
  
  
Time based (4):
  1. avg ping round trip time in ms
     (time btwn node sending echo req and recieving echo reply)
  2. echo request throughput in kB/s
     (sum of all sent echo req frame sizes / sum of all ping RTTs)
  3. echo request goodput in kB/s
     (sum of all sent echo req data sizes / sum of all ping RTTs)
  4. avg reply delay in μs
     (time btwn node receiving echo req and sending echo reply)
     
 Distance (1):
  1. number of hops per echo req
