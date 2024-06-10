# Using readlines()
import os

cwd = os.getcwd()

file1 = open('stocks.txt', 'r')
Lines = file1.readlines()
 
count = 0
file_count = 0

def write():
    global file_count, current_file, count
    f = open(f"{cwd}/nifty500/Nifty 500 - {file_count+1}.txt", "w")
    f.write("\n".join(current_file))
    f.close()

    count = 0
    current_file = []
    file_count += 1

current_file = []
# Strips the newline character
for line in Lines:
    count += 1

    data = line.strip()
    data = data[:-1]
    data = data + '-EQ'
    current_file.append(data)
    if count == 52:
        write()
        
write()