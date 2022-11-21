#filename is the name of the file being filtered
#data is a list that all ICMP echo requests and replies will be stored in

#look "in" on line and do not split
#skip blank lines and know that file will end with blank line
#take the name of the file to make the name of the outfile
import re

def filter(filename, data):
	infile = open(filename, 'r')
	line = infile.readline()

	outfile = open(filename.split(".")[0] + '_filtered.txt', 'w')
	#used to group the full packet together in order to put it into the data list
	while line:
		if("No." in line):
			outfile.write(line)
			line = infile.readline()
			if("ICMP" and "Echo" in line):
				outfile.write(line)
				for i in range(6):
					line = infile.readline()
					outfile.write(line)
			else:
				line = infile.readline()	

	infile.close()
	outfile.close()


#main
filename = "example.txt"
data = []
filter(filename, data)
