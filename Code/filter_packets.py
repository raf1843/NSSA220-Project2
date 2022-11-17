#filename is the name of the file being filtered
#data is a list that all ICMP echo requests and replies will be stored in

#look "in" on line and do not split
#skip blank lines and know that file will end with blank line
import re
#just splitting and .join
def filter(filename, data) :
	#print('called filter function in filter_packets.py')
	infile = open(filename, 'r')
	line = re.sub(' +', ' ', infile.readline())
	line = line.split(" ")
	#used to group the full packet together in order to put it into the data list
	temp_storage = []
	while line:
		if(line[0] == "No."):
			line = line = re.sub(' +', ' ', infile.readline())
			line = line.split(" ")
			if(line[5] == "ICMP" and line[7] == "Echo"):
				#start adding to temp_storage
				temp_storage.append(line)
				for i in range(6):
					line = re.sub(' +', ' ', infile.readline())
					line = line.split(" ")
					temp_storage.append(line)
				data.append(temp_storage)
				line = re.sub(' +', ' ', infile.readline())
				line = line.split(" ")	
		#WILL NOT GO TO THE NEXT PACKET
			elif not(line[5] == "ICMP") and not (line[7] == "Echo"):
				line = re.sub(' +', ' ', infile.readline())
				print(line)
	infile.close()


#main
filename = "example.txt"
data = []
filter(filename, data)

#print(data)
#debugging purposes
print(data)
