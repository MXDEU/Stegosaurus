#-------------------------------------------------------------------------------------------------------------------------
#imports
import os
import sys
import subprocess
#-------------------------------------------------------------------------------------------------------------------------
#input directions
#sys.argv[0]  sys.argv[1]                    sys.argv[2]                                                         sys.argv[3]
#python3      artifical_pcapng_generator.py  /Users/mxdeu/Desktop/_HIWI/_CODE/ recordingsPLC-HMI_13_07_21.pcapng "hidden"
if len(sys.argv) != 4:
    print("")
    print("")
    print("Please call this Program like this: ")
    print("python3.7 artifical_pcapng_generator.py only_filepath filename hidden_message")
    print("ATTENTION: If you have only training filepath, please input same path twice")
    print("In inputfilepath has to be folders with class_names and inside these folders are the image files")
    print("")
    sys.exit()
#-------------------------------------------------------------------------------------------------------------------------
#convert message to bitstream
def messageToBitstream(hiddenmessage):

    result = []
    #c = bits from messageJ
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
#-------------------------------------
#convert list of binaries to message
def binToMessage(binmessage):
    binmessage = "".join(binmessage)
    return ''.join(chr(int(binmessage[i*8:i*8+8], 2)) for i in range(len(binmessage)//8))
#-------------------------------------
#creates string list of message
def listify(message):
    liste = [str(i) for i in message]
    return liste
#-------------------------------------
def patternTest1(pattern):
    if pattern == [0, 0, 1, 1, 1, 0, 1, 1]:
           return [0, 0, 1, 1, 0, 0, 1, 1]
    if pattern == [0, 0, 1, 1, 1, 0, 1, 0]:
           return [0, 0, 1, 1, 0, 0, 1, 0]
    else:
        return pattern     
#-------------------------------------
#get package size from capinfo
#previously "capinfo -c" (Displays the number of packets in the capture file) conversion error: 135k instead of int 

#Capinfos is able to detect and read the same capture files that are supported by Wireshark. 
#The input files don't need a specific filename extension; the file format and an optional gzip compression will be automatically detected. 
#Near the beginning of the DESCRIPTION section of wireshark(1) or https://www.wireshark.org/docs/man-pages/wireshark.html is a detailed description of the way Wireshark handles this, 
#which is the same way Capinfos handles this.
def return_package_size(input_file):
    number_of_packages = subprocess.check_output("capinfos " + input_file, shell=True)
    number_of_packages = str(number_of_packages)
    number_of_packages = [number_of_packages.strip() for number_of_packages in number_of_packages.split(' ')]
    number_of_packages = number_of_packages[len(number_of_packages)-1]
    number_of_packages = [number_of_packages.strip() for number_of_packages in number_of_packages.split('\\n')]
    number_of_packages = int(number_of_packages[0]) # 135k -> 135000
    print(" ")
    print("Number of Packages: " + str(number_of_packages))
    return number_of_packages
#-------------------------------------------------------------------------------------------------------------------------
#variables
input_file = sys.argv[1] + sys.argv[2] + " "
hiddenmessage = sys.argv[3]
msg_bitstream = messageToBitstream(hiddenmessage)

modified_package = sys.argv[1] + "modified_package.pcapng"
output_file = sys.argv[1] + "output.pcapng"
output_temp = sys.argv[1] + "output_temp.pcapng"

package_size = return_package_size(input_file)
os.system("cp " + input_file + " " + output_file)

i = 0
a = 0
counter = 2
#-------------------------------------------------------------------------------------------------------------------------
for a in range (0, len(msg_bitstream), 8):
    #for i in range(0, 3):
        if counter < int(package_size):
            #read single response and save in modified_package.pcapng
            os.system("editcap -r " + output_file + " " + modified_package + " " + str(counter))
            #erase this package from output file
            #input output packagenumber
            os.system("editcap -v " + output_file + " " + output_temp + " " + str(counter) + " >/dev/null 2>&1")

            #extract arrival timestamp
            timestamp_original = subprocess.check_output("tshark -r " + modified_package + " -T fields -e frame.time", shell=True)
            timestamp_original = str(timestamp_original)
            #print (timestamp_original)
            # 'Jul  3, 2020 10:03:00.250946881 CEST\n
            timestamp_original = [timestamp_original.strip() for timestamp_original in timestamp_original.split(' ')]
            # ["b'Jul", '', '3,', '2020', '10:03:00.250546881', "CEST\\n'"]
            timestamp_original = timestamp_original[3]
            # 10:03:00.250546881
            
            # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
            # 1 0 : 0 3 : 0 0 . 2  5  0  5  4  6  8  8  1
            #               x - -  -  -  -  -  -  -  -  x
            timestamp_original = timestamp_original[7:18]
            # 0 1 2 3 4 5 6 7 8 9 10 11
            # 0 . 2 5 0 5 4 6 8 8 1
            
            # 0 . 2 5 0 [5 4 6 8] 8 1
            ##extract digits to change and convert them to bitstream  
            #digit1 = messageToBitstream(timestamp_original[5]) #[0, 0, 1, 1, 0, 1, 0, 1] 5
            #digit2 = messageToBitstream(timestamp_original[6]) #[0, 0, 1, 1, 0, 1, 0, 0] 4
            #digit3 = messageToBitstream(timestamp_original[7]) #[0, 0, 1, 1, 0, 1, 1, 0] 6
            #digit4 = messageToBitstream(timestamp_original[8]) #[0, 0, 1, 1, 1, 0, 0, 0] 8
            ##embed 2 bits each of msg_bitstream into the digits from timestamp
            #digit1[6:8] = msg_bitstream[a:a+2]
            #digit2[6:8] = msg_bitstream[a+2:a+4]
            #digit3[6:8] = msg_bitstream[a+4:a+6]
            #digit4[6:8] = msg_bitstream[a+6:a+8]
            ##test and prevent possible "overflow"
            #digit1 = patternTest1(digit1)
            #digit2 = patternTest1(digit2)
            #digit3 = patternTest1(digit3)
            #digit4 = patternTest1(digit4)
            ##convert modified code back from binary to string  
            #digit1 = int(binToMessage(listify(digit1)))
            #digit2 = int(binToMessage(listify(digit2)))
            #digit3 = int(binToMessage(listify(digit3)))
            #digit4 = int(binToMessage(listify(digit4)))
            ##calculate distance for modifing target 
            #target1 = abs( int(timestamp_original[5]) - digit1)/10000
            #target2 = abs( int(timestamp_original[6]) - digit2)/100000
            #target3 = abs( int(timestamp_original[7]) - digit3)/1000000
            #target4 = abs( int(timestamp_original[8]) - digit4)/10000000
            ##calculate target for editcap
            #target = target1 + target2 + target3 + target4
            

            digit = ['0', '0', '0', '0' ]
            calc = [0.0, 0.0, 0.0, 0.0]

            for b in range(3):
                digit[b] = messageToBitstream(timestamp_original[b+5])
                digit[b][6:8] = msg_bitstream[a+(2*b):a+(2*b)+2] #0-2 2-4 
                digit[b] = patternTest1(digit[b])
                digit[b] = int(binToMessage(listify(digit[b])))
                #calc[b] = abs(int(timestamp_original[b+5]) - digit[b])/(10**(b+4))

            calc[0] = abs( int(timestamp_original[5]) - int(digit[0]))/10000
            calc[1] = abs( int(timestamp_original[6]) - int(digit[1]))/100000
            calc[2]= abs( int(timestamp_original[7]) - int(digit[2]))/1000000
            calc[3] = abs( int(timestamp_original[8]) - int(digit[3]))/10000000
            target = calc[0] + calc[1] + calc[2] + calc[3]


        
            timestamp_modified = format((float(timestamp_original) + float(target)), ".9f")
            print("")
            print("Modifying Package Number: " + str(counter))
            print("Time_Adjustment=    " + str(format(target, ".9f")))
            print("Original Timestamp: " + str(timestamp_original))
            print("Modified Timestamp: " + str(timestamp_modified))

            target = format(target, ".8f")
            #edit selected package
            os.system("editcap -t " + str(target) + " " + modified_package + " " + modified_package)
            #write selected package into output file

            #-t <time adjustment>
            #Sets the time adjustment to use on selected packets. If the -t flag is used to specify a time adjustment, the specified adjustment will be applied to all selected packets in the capture file. 
            #The adjustment is specified as seconds[.fractional seconds]. 
            #For example, -t 3600 advances the timestamp on selected packets by one hour while -t -0.5 reduces the timestamp on selected packets by one-half second.
            #This feature is useful when synchronizing dumps collected on different machines where the time difference between the two machines is known or can be estimated.
            os.remove(output_file)
            os.system("mergecap -w " + output_file + " " + output_temp + " " + modified_package)

            counter += 2

        else:
            print("Bitstream too long to embed in this pcapng file! ")
#-------------------------------------------------------------------------------------------------------------------------
print("Bitstream:  " + str(msg_bitstream) + " for hidden message " + hiddenmessage + " successfully embedded! ")
print("File saved in: " + output_file)
os.remove(modified_package)
os.remove(output_temp)
#-------------------------------------------------------------------------------------------------------------------------