#-------------------------------------------------------------------------------------------------------------------------
#imports
import os
import sys
#-------------------------------------------------------------------------------------------------------------------------
#convert message to bitstream
def messageToBitstream(hiddenmessage):
    result = []
    #c = bits from message
    for c in hiddenmessage:
        #cut the 0b from the start of binary 
        #0b111000 -> 111000 len8 -> len6 
        bits = bin(ord(c))[2:]
        #add the 6bit onto a empty 8 bit bin
        #00000000 + 111000 = 00111000
        bits = '00000000'[len(bits):] + bits
        #write the rseult into a list
        result.extend([int(b) for b in bits])

    return result
#-------------------------------------------------------------------------------------------------------------------------
#processing input file
#python3 decode_stego_pcapng.py output.pcapng    
input_file = sys.argv[1]

os.system('tshark -r ' + input_file + ' -T fields -e frame.time -E separator=, > ' + input_file + '.csv')

print('')
print('Processing File...')

with open(input_file + '.csv') as csv_file:
    all_Timestamps_fromFile = csv_file.readlines()
    num_lines = len(all_Timestamps_fromFile)

#-------------------------------------------------------------------------------------------------------------------------

timestamp_list = []
counter = 1
for i in all_Timestamps_fromFile:

    timestamp_fromFile = i
    timestamp_fromFile = [timestamp_fromFile.strip() for timestamp_fromFile in timestamp_fromFile.split(' ')]
    # ["b'Jul", '', '3,', '2020', '10:03:00.250546881', "CEST\\n'"]
    timestamp_fromFile = timestamp_fromFile[3]
    if counter % 2 == 0:
        timestamp_fromFile = timestamp_fromFile[12:16]
        timestamp_list.append(timestamp_fromFile)

    counter += 1
#-------------------------------------
bitstream = []
n = 0
while n < len(timestamp_list)-1:
    x = timestamp_list[n] #'0.250546881'   
    
    for i in range(3):
        y = messageToBitstream(x[i])
        bitstream.append(y[6:8])



if len(bitstream) == 0:
    print('')
    print('No Hidden Message found! ')

else:
    print('')
    print('Hidden Bitstream found! ')

    print("this is a test")
    print(bitstream)
    bitstream = "".join(bitstream)
    bitstream = "011010000110100101100100011001000110010101101110"
    print('Bitstream: ' + str(bitstream))
    ascii_string = ''.join(chr(int(bitstream[i*8:i*8+8], 2)) for i in range(len(bitstream)//8))
    print("Hidden Message: " + ascii_string)

os.remove(input_file + '.csv')        
    



