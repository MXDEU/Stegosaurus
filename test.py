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


def bitstreamToMessage(bitstream):
     bitstream = *bitstream, sep = ""
     bitstream = int(bitstream)
     return bitstream


def convertBin(list):
# using join() + list comprehension
# converting binary list to integer 
    return int("".join(str(x) for x in list), 2)

# Python3 program to convert a list
# of integers into a single integer
def convertList(list):
      
    # Converting integer list to string list
    s = [str(i) for i in list]
      
    # Join list items using join()
    res = int("".join(s))
      
    return(res)     

#index = 0
#while index < 10:
#    p = str(index)
#    print(p)
#    print(messageToBitstream(p))
#    index += 1

timestamp_org = '10:03:00.250546881'
timestamp_mod0 = timestamp_org[14:18]
print(timestamp_mod0)
hidden_message = 'hidden'
bitstream = messageToBitstream(hidden_message)


# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
# 1 0 : 0 3 : 0 0 . 2  5  0  5  4  6  8  8  1
#                                  x  x  x  x
#                                  2  2  2  2    1 Byte pro Timestamp
#timestamp_mod = timestamp_org[14:18]

# step.1 convert message to bitstream *
# step.2 convert number to bitstream
# step.3 embed 2 bits of message in the last to bits of the last 4 numbers of the timestamp
# step.4 convert bitstream back to number 
# step.5 write new timestamp to output


timestamp_bit1 = messageToBitstream(timestamp_org[14])     
timestamp_bit2 = messageToBitstream(timestamp_org[15])
timestamp_bit3 = messageToBitstream(timestamp_org[16])
timestamp_bit4 = messageToBitstream(timestamp_org[17])
                         
#print(timestamp_org[14])
#print(timestamp_org[15])
#print(timestamp_org[16])
#print(timestamp_org[17]) 

# 0 1 2 3 4 5 6 7
#print(bitstream[a])
#print(len(timestamp_bit1))
#print(timestamp_bit1[6])
print("\ntimestamps before embeding:")
print(timestamp_bit1)
print(timestamp_bit2)
print(timestamp_bit3)
print(timestamp_bit4)


#a[start:stop]  items start through stop-1
#a[start:]      items start through the rest of the array
#a[:stop]       items from the beginning through stop-1
#a[:]           a copy of the whole array
a=0

timestamp_bit1[6:8] = bitstream[a:a+2] 
timestamp_bit2[6:8] = bitstream[a+2:a+4]
timestamp_bit3[6:8] = bitstream[a+4:a+6]
timestamp_bit4[6:8] = bitstream[a+6:a+8]

a+=8
#timestamp_bit1[6] = bitstream[a]
#timestamp_bit1[7] = bitstream[a+1]
#timestamp_bit2[6] = bitstream[a+2] 
#timestamp_bit2[7] = bitstream[a+3]
#timestamp_bit3[6] = bitstream[a+4] 
#timestamp_bit3[7] = bitstream[a+5]
#timestamp_bit4[6] = bitstream[a+6] 
#timestamp_bit4[7] = bitstream[a+7]

print("\ntimestamps after embeding:")                
print(timestamp_bit1)
print(timestamp_bit2)
print(timestamp_bit3)
print(timestamp_bit4)

print("\nmessage as bin:")
print(bitstream[0:8])

print(type(timestamp_bit1))

convertList(timestamp_bit1)





#make bit versions 
#timestamp_mod0 = messageToBitstream(timestamp_mod0)
#message_bit = messageToBitstream(hidden_message)


#print(timestamp_mod0)
#print("hello")
#print(message_bit)

#i = 0
#timestamp_mod0[4:8] = message_bit[i : i+4]
#timestamp_original = [timestamp_original.strip() for timestamp_original in timestamp_original.split(' ')]
#timestamp_mod0 = bitstreamToMessage(timestamp_mod0)


#result = *timestamp_bit1, sep = ""
print(*timestamp_bit1, sep = "")


#for i in range (len(timestamp_mod0)):
#    result = ""
#    result = result + str(timestamp_mod0[i])
#    print(timestamp_mod0[i])

#print(result)


result = str(timestamp_mod0)
result = result.replace(",","")
result = result.replace(" ", "")
result = result.replace("[", "")
result = result.replace("]", "")
#result = "0b"+result
#result = binascii.a2b_uu(result)

#result = result.decode('utf-8', 'ignore')

