import os
import sys
import subprocess

if len(sys.argv) != 4:
    print("")
    print("")
    print("Please call this Program like this: ")
    print("python3.7 artifical_pcapng_generator.py only_filepath filename hidden_message")
    print("ATTENTION: If you have only training filepath, please input same path twice")
    print("In inputfilepath has to be folders with class_names and inside these folders are the image files")
    print("")
    sys.exit()

def messageToBitstream(hiddenmessage):

    result = []
    for c in hiddenmessage:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])

    return result

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


input_file = sys.argv[1] + sys.argv[2] + " "
hiddenmessage = sys.argv[3]
print("The hidden message is: " + hiddenmessage)
print("converting the hidden message into bitstream...")
bitstream = messageToBitstream(hiddenmessage)
print("...done! Bitstream: ")
print(bitstream)

modified_package = sys.argv[1] + "modified_package.pcapng"
output_file = sys.argv[1] + "output.pcapng"
output_temp = sys.argv[1] + "output_temp.pcapng"

package_size = return_package_size(input_file)

os.system("cp " + input_file + " " + output_file)

i = 0
counter = 2
for bit in bitstream:
    for i in range(0, 3):
        if counter < int(package_size):
            #read single response and save in modified_package.pcapng
            os.system("editcap -r " + output_file + " " + modified_package + " " + str(counter))
            #erase this package from output file
            # input output packagenumber
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
            timestamp_original = timestamp_original[7:18]
            # 0.250546881
            target = 0.0
            if bit == 0:
                if counter % 6 == 2:
                    print(timestamp_original)
                    timestamp_value = int(timestamp_original[4])
                    print(timestamp_value)
                    target = (timestamp_value - 4) / 1000
                if counter % 6 == 4:
                    timestamp_value = int(timestamp_original[5])
                    target = (timestamp_value - 4) / 10000
                if counter % 6 == 0:
                    timestamp_value = int(timestamp_original[6])
                    target = (timestamp_value - 4) / 100000
                target = target * -1
            if bit == 1:
                if counter % 6 == 2:
                    timestamp_value = int(timestamp_original[4])
                    target = abs(timestamp_value - 9) / 1000
                if counter % 6 == 4:
                    timestamp_value = int(timestamp_original[5])
                    target = abs(timestamp_value - 9) / 10000
                if counter % 6 == 0:
                    timestamp_value = int(timestamp_original[6])
                    target = abs(timestamp_value - 9) / 100000




            timestamp_modified = float(timestamp_original) + float(target)
            print("")
            print("Modifying Package Number: " + str(counter))
            print("Time_Adjustment= " + str(target))
            print("Original Timestamp: " + str(timestamp_original))
            print("Modified Timestamp: " + str(timestamp_modified))

            target = format(target, ".5f")
            #edit selected package
            os.system("editcap -t " + str(target) + " " + modified_package + " " + modified_package)
            #write selected package into output file

            os.remove(output_file)
            os.system("mergecap -w " + output_file + " " + output_temp + " " + modified_package)

            counter += 2

        else:
            print("Bitstream too long to embed in this pcapng file! ")


print("Bitstream:  " + str(bitstream) + " for hidden message " + hiddenmessage + " successfully embedded! ")
print("File saved in: " + output_file)
os.remove(modified_package)
os.remove(output_temp)
