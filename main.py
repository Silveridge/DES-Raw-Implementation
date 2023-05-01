from sboxes import *
from tables import *

def performXOR(input1: str, input2: str):
    outputString = [(ord(a) ^ ord(b)) for a, b in zip(input1, input2)] # xor's by pairing each element in input1 and input2, autochange them to int, then xor.
    outputString = "".join(map(str, outputString)) # output of above function is an array of ints, converts to string
    return outputString

def performLeftShift(input: str, roundNumber: int):
    twoShifts = [3,4,5,6,7,8,10,11,12,13,14,15]
    inputA = [*input]
    inputA.append(inputA.pop(0))
    if(roundNumber in twoShifts):
        inputA.append(inputA.pop(0))
    input = "".join(inputA)
    return input

def performRound(inputText: str, inputKey: str, roundNumber: int):
    inLeft = ""
    inRight = ""
    outLeft = ""
    outRight = ""
    keyLeft = ""
    keyRight = ""
    keyOutLeft = ""
    keyOutRight = ""

    ### KEY OPERATIONS
    # split key into 28-bit halves
    keyLeft = inputKey[0:28]
    keyRight = inputKey[28:]

    # left shift the key halves
    keyLeft = performLeftShift(keyLeft, roundNumber)
    keyRight = performLeftShift(keyRight, roundNumber)

    # final key values
    keyOutRight = keyRight
    keyOutLeft = keyLeft
    subKey = keyRight + keyLeft

    # get key to XOR
    keyToXOR = performPermutation(subKey, 6)

    ### TEXT OPERATIONS

    # split text into 32-bit halves
    inLeft = inputText[0:32]
    inRight = inputText[32:]
    outLeft = inRight

    # EXPANSION TABLE
    expandedString = performPermutation(inRight, 3)

    # XOR
    xordString = performXOR(expandedString, keyToXOR)

    # S-BOX
    substitutedString = performSubstitution(xordString)

    # PERMUTATION
    permutatedString = performPermutation(substitutedString, 4)

    # XOR With inLeft
    outRight = performXOR(permutatedString, inLeft)

    return(outLeft, outRight, keyOutLeft, keyOutRight)
    
def encrypt():
    # Step 0: Setup
    rounds = 16
    currentRound = 0

    # Step 1: Input
    inputBinary = "0110000101100010011000110110010001100101011001100110011101101000" #abcdefg
    key = "01101000011010010110101001101011011011000110110101101110" #hijklmn

    # Step 2: Initial Permutation
    newInputBinary = performPermutation(inputBinary, 1)

    # Step 3: Rounds
    newKey = key # for variable's sake
    while currentRound < rounds:
        leftString, rightString, keyLeft, keyRight = performRound(newInputBinary, newKey, currentRound)
        newInputBinary = str(leftString) + str(rightString) # str() is a failsafe just incase it interprets as int or bin
        newKey = str(keyLeft) + str(keyRight)
        currentRound += 1
        
    roundOutput = newInputBinary

    # Step 4: 32-bit swap
    roundOutputLeft = roundOutput[0:32]
    roundOutputRight = roundOutput[32:]

    swapOutput = str(roundOutputRight) + str(roundOutputLeft)

    # Step 5: Inverse Initial Permutation
    finalOutput = performPermutation(swapOutput, 2)

    print(finalOutput)