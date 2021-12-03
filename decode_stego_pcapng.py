import os
import sys

input_file = sys.argv[2 ]

os.system('tshark -r ' + input_file + ' -T fields -e frame.time -E separator=, > ' + input_file + '.csv')

print('')
print('Processing File...')

with open(input_file + '.csv') as csv_file:
    all_Timestamps_fromFile = csv_file.readlines()
    num_lines = len(all_Timestamps_fromFile)

timestamp_list = []
counter = 1
for i in all_Timestamps_fromFile:

    timestamp_fromFile = i
    timestamp_fromFile = [timestamp_fromFile.strip() for timestamp_fromFile in timestamp_fromFile.split(' ')]
    # ["b'Jul", '', '3,', '2020', '10:03:00.250546881', "CEST\\n'"]
    timestamp_fromFile = timestamp_fromFile[3]
    if counter % 2 == 0:
        timestamp_fromFile = timestamp_fromFile[7:18]
        timestamp_list.append(timestamp_fromFile)

    # 10:03:00.250546881
    counter += 1

# print(timestamp_list)

bitstream = []
n = 3
while n < len(timestamp_list)-1:
    x = timestamp_list[n]
    y = timestamp_list[n-2]
    z = timestamp_list[n-4]

    if x[4] == '4' and y[5] == '4' and z[6] == '4':
        bitstream.append('0')

    if x[4] == '9' and y[5] == '9' and z[6] == '9':
        bitstream.append('1')

    n += 3

if len(bitstream) == 0:
    print('')
    print('No Hidden Message found! ')

else:
    print('')
    print('Hidden Bitstream found! ')

    bitstream = "".join(bitstream)
    bitstream = "011010000110100101100100011001000110010101101110"
    print('Bitstream: ' + str(bitstream))
    ascii_string = ''.join(chr(int(bitstream[i*8:i*8+8], 2)) for i in range(len(bitstream)//8))
    print("Hidden Message: " + ascii_string)

os.remove(input_file + '.csv')
