#filename is the name of the file being filtered
#data is a list that all ICMP echo requests and replies will be stored in

#import regex
#just splitting and .join
def filter(filename, data) :
	#print('called filter function in filter_packets.py')
	infile = open(filename, 'r')
	line = infile.readline().strip().split(" ")

	#used to group the full packet together in order to put it into the data list
	temp_storage = []

	while line:
		#print(line[0])
		if(line[0] == "No."):
			#print(line)
			line = infile.readline().strip().split(" ")
			#print("This is 4: " + line[26]) indices 26 and 37 because of white space but it should be 4 and 6 otherwise
			#print(line)
			if(line[26] == "ICMP" and line[36] == "Echo"):
				#start adding to temp_storage
				temp_storage.append(line)
				for i in range(4):
					line = infile.readline().strip().split(" ")
					temp_storage.append(line)
			data.append(temp_storage)	
		elif(line[0] != "No."):
			line = infile.readline()
	infile.close()


#main
filename = "example.txt"
data = []
filter(filename, data)

#print(data)
#debugging purposes
for i in range(len(data)):
	print(data[i])
	print("\n")
	
