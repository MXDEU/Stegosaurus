# a = [0, 0, 1, 1, 0, 1, 0, 1] = 53
# 546 - y = 53
# y = 493
#          1 0 : 0 3 : 0 0 . 2 5 0 5 4 6 8 8 1
# Result = 1 0 : 0 3 : 0 0 . 2 5 0 0 5 3 8 8 1
# y = timestamp before embedding - timestamp after embedding
# y dann an editcap um diesen wert dann vom timestamp abzuziehen oder draufzuaddieren



#What to do: 

#schleife schreiben
#sonderfälle abfangen
#capedit


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

def binToMessage(binmessage):
    binmessage = "".join(binmessage)
    return ''.join(chr(int(binmessage[i*8:i*8+8], 2)) for i in range(len(binmessage)//8))


def listify(message):
    liste = [str(i) for i in message]
    return liste


timestamp_org = '10:03:00.250546881'
hidden_message = 'hidden'


print(timestamp_org[12:16])

qa = [0, 0, 1, 1, 0, 1, 2, 3]
print(qa[6:8])


bitstream = messageToBitstream(hidden_message)


#10:03:00.250 (5468) 81
# 5 -> [0, 0, 1, 1, 0, 1, 0, 1]
timestamp_bit1 = messageToBitstream(timestamp_org[12]) 
timestamp_bit2 = messageToBitstream(timestamp_org[13])
timestamp_bit3 = messageToBitstream(timestamp_org[14])
timestamp_bit4 = messageToBitstream(timestamp_org[15])

a=0

# "message"-> bitstream
# timestamp[12-15] -> bitstream 

#print(bitstream[a:a+8])
#[0, 1, 1, 0, 1, 0, 0, 0]

#[0, 0, 1, 1, 0, 0, 0, 0] 0 
#[0, 0, 1, 1, 0, 0, 0, 1] 1
#[0, 0, 1, 1, 0, 0, 1, 0] 2
#[0, 0, 1, 1, 0, 0, 1, 1] 3
#[0, 0, 1, 1, 0, 1, 0, 0] 4
#[0, 0, 1, 1, 0, 1, 0, 1] 5
#[0, 0, 1, 1, 0, 1, 1, 0] 6
#[0, 0, 1, 1, 0, 1, 1, 1] 7

#[0, 0, 1, 1, 1, 0, 0, 0] 8
#[0, 0, 1, 1, 1, 0, 0, 1] 9

#[0, 0, 1, 1, 1, 0, 1, 1] 
#[0, 0, 1, 1, 1, 0, 1, 0] 

# 00 01 10 11 
#10 11 

d = [0, 0, 1, 1, 1, 0, 0, 1]
print(binToMessage(listify(d)))


#10:03:00.250 (5468) 81

#convert number to bitstream
# 5 -> [0, 0, 1, 1, 0, 1, 0, 1]
timestamp_bit1 = messageToBitstream(timestamp_org[12]) 
timestamp_bit2 = messageToBitstream(timestamp_org[13])
timestamp_bit3 = messageToBitstream(timestamp_org[14])
timestamp_bit4 = messageToBitstream(timestamp_org[15])

#
timestamp_bit1[6:8] = bitstream[a:a+2]
timestamp_bit2[6:8] = bitstream[a+2:a+4]
timestamp_bit3[6:8] = bitstream[a+4:a+6]
timestamp_bit4[6:8] = bitstream[a+6:a+8]

timestamp_bit1 = int(binToMessage(listify(timestamp_bit1)))
timestamp_bit2 = int(binToMessage(listify(timestamp_bit2)))
timestamp_bit3 = int(binToMessage(listify(timestamp_bit3)))
timestamp_bit4 = int(binToMessage(listify(timestamp_bit4)))

print(timestamp_org[12], timestamp_org[13], timestamp_org[14], timestamp_org[15])
print(timestamp_bit1, timestamp_bit2, timestamp_bit3, timestamp_bit4)

target1 = abs( int(timestamp_org[12]) - timestamp_bit1)
target2 = abs( int(timestamp_org[13]) - timestamp_bit2)
target3 = abs( int(timestamp_org[14]) - timestamp_bit3)
target4 = abs( int(timestamp_org[15]) - timestamp_bit4)

print(target1, target2, target3, target4)

target1 = abs( int(5 - 4))/10000
target2 = abs( int(4 - 6))/100000
target3 = abs( int(6 - 3))/1000000
target4 = abs( int(8 - 4))/10000000

#0.00012340
#0.002260000
#0.250546881



abc =  [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0]

print(binToMessage(listify(abc)))





#calculate target for editcap

target = target1 + target2 + target3 + target4
target = format(target, ".8f")

print(target)

#print(binToMessage(bitstream[a:a+8]))
#12-15
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
# 1 0 : 0 3 : 0 0 . 2  5  0  5  4  6  8  8  1



