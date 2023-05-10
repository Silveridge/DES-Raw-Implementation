from des import *
import time

p = "1010101010101010101010101010101010101010101010101010101010101010"
p1 = "1010101010101010101010101010101010101010101010101010101010101011"
c = "1100011001011111101000110010000110011100101100110010010010011010"
k = "0101010101010101010101010101010101010101010101010101010101010101"
k1 = "0101010101010101000101010101010101010101010101010101010101010101"

def processBinaries(array):
    allBinaries = []
    differences = [[],[],[],[]]
    for des in array:
        allBinaries.append(des.getRoundBinaries())

    for i in range(int(len(allBinaries)/2)): # comparing 0|4, 1|5, 2|6 , 3|7
        for j in range(len(allBinaries[0])):
            differences[i].append(findDifference(allBinaries[i][j], allBinaries[i+4][j]))
    return differences

def findDifference(bin1:str, bin2:str):
    bin1 = [*bin1]
    bin2 = [*bin2]
    totalDiff = 0
    for i in range (len(bin1)):
        if(bin1[i] != bin2[i]):
            totalDiff += 1
    print(totalDiff)
    return totalDiff

start = time.time()

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

# run encryption algorithm on all DES functions
for des in firstDES:
    des.run()

# run encryption algorithm on all DES functions
for des in secondDES:
    des.run()


firstSet = processBinaries(firstDES)
secondSet = processBinaries(secondDES)

end = time.time()

def writeToFile(plaintext1:str, plaintext2:str, key1:str, key2:str, runningTime:str):
    f = open("output.txt","w")
    f.write("Avalance Demonstration\n")
    f.write("Implementation by Sam Fitzpatrick (C3404867) and Corey Silk (C3280997)\n")
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
    for i in range(len(firstSet[0])):
        f.write(f"{i+1}            {firstSet[0][i]}      {firstSet[1][i]}       {firstSet[2][i]}       {firstSet[3][i]}\n")
    f.write("\n")
    f.write("\nP under K and K'\n")
    f.write(f"Ciphertext C: {secondDES[0].getOutputText()}\n")
    f.write(f"Ciphertext C': {secondDES[4].getOutputText()}\n")

    f.write(f"Round      DES0     DES1     DES2     DES3\n")
    f.write("0            1        1        1        1\n")
    for i in range(len(secondSet[0])):
        f.write(f"{i+1}            {secondSet[0][i]}      {secondSet[1][i]}       {secondSet[2][i]}       {secondSet[3][i]}\n")




writeToFile(p, p1, k, k1, end-start)