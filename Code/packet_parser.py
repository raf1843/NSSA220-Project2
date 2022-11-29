"""
AHHHHHHHH Packet Parsing!!
-------------------------------------------------------------------------------------------------------------------------
3 Functions
1) parse = NOT COMPLETE and will most likely be deleted

2) hex_formatting = Reads Filtered Files and formats the data into data lists that can be more easily parsed

3) hex_parse = Takes the data list from (2)hex_formatting and through a bunch of magic generates a dictionary
   of which pairs Packet to the Response Packet as seen from the Host PC. hex_parse will generate the dictionary 
   via pass through and then it will return the 4 initial metrics we need.
-------------------------------------------------------------------------------------------------------------------------
D is our output Dictionary
Dictionary Format:
Packet Tuple : Response Packet Tuple

Packet Format (Same for both Packet and Response Packet):
[(Packet No.), (Time), (Source IP), (Dest. IP), (Msg Type), (Total Packet Size), (Payload Size), (Seq No.), (TTL), (Associated Packet No.)]
-------------------------------------------------------------------------------------------------------------------------
Some Notes!
1) There is no need for any cutting of header lengths from the Payload Size, the math is already done! Payload Size
   is strictly the ICMP Payload Size!

2) Associated Packet No. This is the packet that is either the response packet or the packet that this current 
   packet is responding to!
-------------------------------------------------------------------------------------------------------------------------
"""

import re

def parse(filename, L, ip):
	pingData=[]
	eReqSent=0
	eReqRec=0
	eRepSent=0
	eRepRec=0

	with open(filename, 'r') as f:
		for line in f:
			if("Echo (ping) request" in line) or ("Echo (ping) reply" in line):
				pline=line.split()				
				pingData.append(pline)
	
	for line in pingData:
		sip=line[2]
		dip=line[3]
		etype=line[8]
		if(etype=="request") and (sip==ip):
			eReqSent+=1
		elif(etype=="request") and (dip==ip):
			eReqRec+=1
		elif(etype=="reply") and (sip==ip):
			eRepSent+=1
		else:
			eRepRec+=1
		 
	print(eReqSent, eReqRec, eRepSent, eRepRec)

def hex_formatting(filename, dataList):
	pingData=[]

	with open(filename, 'r') as f:
		for line in f:
			if (line.isspace() == False):
				pline=re.sub(' +', ' ', line.strip())
				pingData.append(line.strip())

	for i in range(len(pingData)):
		if "ICMP" in pingData[i]:
			start=True
			packet=[]
		if start:
			packet.append(pingData[i])
		if ((i+2) > len(pingData)):
			start=False
			dataList.append(packet)
			break
		elif ("ICMP" in pingData[i+1]):
			start=False
			dataList.append(packet)

			
	for pack in dataList:
		hexp=[]
		pack[0]=re.sub(' +', ' ', pack[0])
		for i in range(1, len(pack)):
			x=re.search("\s{2}(.*?)\s{2,}", pack[i])
			hexp.extend(x.group(1).split(" "))
		del pack[1:len(pack)]
		pack.append(hexp)

def hex_parse(L, ip, D):
	eReqSent=0
	eReqRec=0
	eRepSent=0
	eRepRec=0
	tlist=[]
	
	for packet in L:
		sip="{}.{}.{}.{}".format(int(packet[1][26], 16),int(packet[1][27], 16), int(packet[1][28], 16),int(packet[1][29], 16))
		dip="{}.{}.{}.{}".format(int(packet[1][30], 16),int(packet[1][31], 16), int(packet[1][32], 16),int(packet[1][33], 16))
		etype=int(packet[1][34], 16)
		
		if(etype==8) and (sip==ip):
			eReqSent+=1
			eString="Echo Request Sent"
		elif(etype==8) and (dip==ip):
			eReqRec+=1
			eString="Echo Request Received"
		elif(etype==0) and (sip==ip):
			eRepSent+=1
			eString="Echo Reply Sent"
		elif(etype==0) and (dip==ip):
			eRepRec+=1
			eString="Echo Reply Received"	

		ipSize=int(packet[1][16], 16) + int(packet[1][17], 16)		
	
		temp=packet[0].split(" ")
		tlist.append((temp[0], temp[1], sip, dip, eString, (ipSize-28), temp[10], (ipSize+14), int(packet[1][22], 16), int(re.search(r'(\d+)', temp[14]).group())))

	for item in tlist:
		for item2 in tlist:
			if(item2[9]==int(item[0])) and item not in D.values():
				D[item]=item2

	return (eReqSent, eReqRec, eRepSent,eRepRec)
#main
filename="Node1_filtered.txt"
L=[]
D={}
ip="192.168.100.1"

#parse(filename, L, ip)
hex_formatting(filename, L)
iMet=hex_parse(L, ip, D)

#Test Prints (This is also your warning to not uncomment and print the dictionary!!!)
print(iMet)
print(iMet, "\n", D)
