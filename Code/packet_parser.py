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

def hex_parser(filename, L, ip):
	pData=[]	

	with open(filename, 'r') as f:
		for line in f:
			if (line.isspace() == False):
				pline=re.sub(' +', ' ', line.strip())
				pData.append(pline)
		print(pData)
#main
filename="example2.txt"
L=[]
ip="192.168.100.1"

#parse(filename, L, ip)
hex_parser(filename, L, ip)
	
