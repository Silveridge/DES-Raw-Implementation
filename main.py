# Raw DES Implementation
# This program implements DES encryption and decryption of a single 64 bit plaintext block.
# It also explores the Avalanche effect of the 4 DES encryption algorithms

from des import *
import time

# variable definitions for binaries
p = "1010101010101010101010101010101010101010101010101010101010101010"
p1 = "1010101010101010101010101010101010101010101010101010101010101011"
c = "1100011001011111101000110010000110011100101100110010010010011010"
k = "0101010101010101010101010101010101010101010101010101010101010101"
k1 = "0101010101010101000101010101010101010101010101010101010101010101"

# process round binaries
def processBinaries(array):
    # arrays to store binaries and differences between all 4 DES algorithms
    allBinaries = []
    differences = [[],[],[],[]]
    # add the binary array from all DES's into the allBinaries array, forming two-dimensional array 
    for des in array:
        allBinaries.append(des.getRoundBinaries())

    # compare the DES algorithm round differences based on assignment specs
    for i in range(int(len(allBinaries)/2)): # comparing 0|4, 1|5, 2|6 , 3|7 indexes
        for j in range(len(allBinaries[0])):
            differences[i].append(findDifference(allBinaries[i][j], allBinaries[i+4][j]))
    return differences

# finds differences per bit in a binary string
def findDifference(bin1:str, bin2:str):
    # convert binary string to array
    bin1 = [*bin1]
    bin2 = [*bin2]
    totalDiff = 0

    # compare each value
    for i in range (len(bin1)):
        if(bin1[i] != bin2[i]):
            totalDiff += 1
    return totalDiff

# get start time
start = time.time()

# First requirements, P and P1 under K
firstDES = [
    DES(p, k, "e", 0),
    DES(p, k, "e", 1),
    DES(p, k, "e", 2),
    DES(p, k, "e", 3),
    DES(p1, k, "e", 0),
    DES(p1, k, "e", 1),
    DES(p1, k, "e", 2),
    DES(p1, k, "e", 3)
]

# Second requirements, P under K and K1
secondDES = [
    DES(p, k, "e", 0),
    DES(p, k, "e", 1),
    DES(p, k, "e", 2),
    DES(p, k, "e", 3),
    DES(p, k1, "e", 0),
    DES(p, k1, "e", 1),
    DES(p, k1, "e", 2),
    DES(p, k1, "e", 3)
]

# Decryption requirements
decryptDES = DES(c, k, "d", 0)
decryptDES.run()

# run encryption algorithm on all DES functions
for des in firstDES:
    des.run()

# run encryption algorithm on all DES functions
for des in secondDES:
    des.run()

# process binaries for the first and second set of DES algorithms
firstSet = processBinaries(firstDES)
secondSet = processBinaries(secondDES)

# get finish time
end = time.time()

# write to output.txt file
def writeToFile(plaintext1:str, plaintext2:str, key1:str, key2:str, runningTime:str, ciphertext:str):
    f = open("output.txt","w")
    f.write("Avalanche Demonstration\n")
    f.write(f"Plaintext P: {plaintext1}\n")
    f.write(f"Plaintext P': {plaintext2}\n")
    f.write(f"Key K: {key1}\n")
    f.write(f"Key K': {key2}\n")
    f.write(f"Total running time: {runningTime}\n")
    f.write("\nP and P' under K\n")
    f.write(f"Ciphertext C: {firstDES[0].getOutputText()}\n")
    f.write(f"Ciphertext C': {firstDES[4].getOutputText()}\n")

    f.write(f"Round      DES0     DES1     DES2     DES3\n")
    f.write("0            1        1        1        1\n")
    breaks = ["             ", "         ", "         ", "         "]
    for i in range(len(firstSet[0])):
        f.write(f"{i+1}{breaks[0][len(str(i+1)):]}{firstSet[0][i]}{breaks[1][len(str(firstSet[0][i])):]}{firstSet[1][i]}{breaks[2][len(str(firstSet[1][i])):]}{firstSet[2][i]}{breaks[3][len(str(i+1)):]}{firstSet[3][i]}\n")
    f.write("\n")
    f.write("\nP under K and K'\n")
    f.write(f"Ciphertext C: {secondDES[0].getOutputText()}\n")
    f.write(f"Ciphertext C': {secondDES[4].getOutputText()}\n")

    f.write(f"Round      DES0     DES1     DES2     DES3\n")
    f.write("0            1        1        1        1\n")

    # breaks allows for equally-formatted spaces between all of the difference numbers
    # as extra digits means extra breaks between all of the columns, causing misalignment.
    for i in range(len(secondSet[0])):
        f.write(f"{i+1}{breaks[0][len(str(i+1)):]}{secondSet[0][i]}{breaks[1][len(str(secondSet[0][i])):]}{secondSet[1][i]}{breaks[2][len(str(secondSet[1][i])):]}{secondSet[2][i]}{breaks[3][len(str(i+1)):]}{secondSet[3][i]}\n")

    f.write("\n\n")
    f.write("DECRYPTION\n")
    f.write(f"Ciphertext C: {c}\n")
    f.write(f"Key K: {k}\n")
    f.write(f"Plaintext P: {decryptDES.getOutputText()}\n")

    f.close()




writeToFile(p, p1, k, k1, end-start, c)
