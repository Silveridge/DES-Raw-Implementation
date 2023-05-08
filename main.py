from encryption import *
import time

def writeToFile(plaintext1:str, plaintext2:str, key1:str, key2:str, runningTime:str, processedOut):
    f = open("output.txt","w")
    f.write("Avalance Demonstration\n")
    f.write("Implementation by Sam Fitzpatrick (C3404867) and Corey Silk (C3280997)\n")
    f.write(f"Plaintext P: {plaintext1}\n")
    f.write(f"Plaintext P': {plaintext2}\n")
    f.write(f"Key K: {key1}\n")
    f.write(f"Key K': {key2}\n")
    f.write(f"Total running time: {runningTime}\n")
    f.write("\nP and P' under K\n")
    f.write(f"Ciphertext C DES0: {processedOut[2][0]}\n")
    f.write(f"Ciphertext C DES1: {processedOut[2][1]}\n")
    f.write(f"Ciphertext C DES2: {processedOut[2][2]}\n")
    f.write(f"Ciphertext C DES3: {processedOut[2][3]}\n")
    f.write(f"Ciphertext C' DES0: {processedOut[2][4]}\n")
    f.write(f"Ciphertext C' DES1: {processedOut[2][5]}\n")
    f.write(f"Ciphertext C' DES2: {processedOut[2][6]}\n")
    f.write(f"Ciphertext C' DES3: {processedOut[2][7]}\n")

    f.write(f"Round      DES0     DES1     DES2     DES3\n")
    for i in range(len(processedOut[0][0])):
        f.write(f"{processedOut[0][0][i]}       {processedOut[0][1][i]}         {processedOut[0][2][i]}         {processedOut[0][3][i]}           {processedOut[0][4][i]}\n")
    

def execute(plaintext1:str, plaintext2:str, key1:str, key2:str):
    start = time.time()
    outputs = []
    encrypt = Encryptor(plaintext1, key1)
    outputs.append(encrypt.encrypt(0))
    outputs.append(encrypt.encrypt(1))
    outputs.append(encrypt.encrypt(2))
    outputs.append(encrypt.encrypt(3)) #DES 3 NOT WORKING YET, SEE tables.py FOR MORE

    encrypt.changePlaintext(plaintext2)
    
    outputs.append(encrypt.encrypt(0))
    outputs.append(encrypt.encrypt(1))
    outputs.append(encrypt.encrypt(2))
    outputs.append(encrypt.encrypt(3)) #DES 3 NOT WORKING YET, SEE tables.py FOR MORE

    end = time.time()
    total = end-start
    processedOut = processOutputs(plaintext1, plaintext2, outputs)
    writeToFile(plaintext1, plaintext2, key1, key2, total, processedOut)

def execute1(a,b,c,d):
    return

def processOutputs(p1, p2, outputArray):
    initialInputs = [p1, p2]
    finalOutputs = []
    roundOutputs = [] # Comparing indexes 0,4 | 1,5 | 2,6 | 3,7
    returnedArray = [[],[],[],[],[]] # Round | DES0 | DES1 | DES2 | DES3
    for i in range(len(outputArray)):
        finalOutputs.append(outputArray[i][0])
        roundOutputs.append(outputArray[i][1])

    returnedArray[0].append(0)
    returnedArray[1].append(findDifference(p1, p2))
    returnedArray[2].append(findDifference(p1, p2))
    returnedArray[3].append(findDifference(p1, p2))
    returnedArray[4].append(findDifference(p1, p2))


    for i in range(0,16):
        returnedArray[0].append(i+1)
        returnedArray[1].append(findDifference(roundOutputs[0][i], roundOutputs[4][i]))
        returnedArray[2].append(findDifference(roundOutputs[1][i], roundOutputs[5][i]))
        returnedArray[3].append(findDifference(roundOutputs[2][i], roundOutputs[6][i]))
        returnedArray[4].append(findDifference(roundOutputs[3][i], roundOutputs[7][i]))
    
    print(finalOutputs)
    return returnedArray, initialInputs, finalOutputs


def findDifference(bin1:str, bin2:str):
    bin1 = [*bin1]
    bin2 = [*bin2]
    totalDiff = 0
    for i in range (len(bin1)):
        if(bin1[i] != bin2[i]):
            totalDiff += 1
    return totalDiff

# inputBinary = "0110000101100010011000110110010001100101011001100110011101101000" #abcdefgh
    #key = "01101001011010100110101101101100011011010110111001101111" #ijklmno


execute(
    "0110000101100010011000110110010001100101011001100110011101101000", 
    "0110000101100010011000110110010001100101011001100110011101101001",
    "01101001011010100110101101101100011011010110111001101111", #ijklmno
    "01101001011010100110101101101100011011010110111001101110" #xyzABCD
)