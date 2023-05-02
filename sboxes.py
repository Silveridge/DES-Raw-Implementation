# Right-hand 32-bit input
# Expansion box turns into 48-bit bit string
# 48 bit key
# Key/String XOR'd together.
# 6 bit inputs get split in numerical order among the sboxes
# result in 4 bit outputs to form 32-bit output which becomes left-half of next round

sboxes = [
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],

    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],

    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],

    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],

    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],

    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],

    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],

    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]

# Expected Input: XOR'd 48-bit long string 
def performSubstitution(inputString: str):
    # splits input string into Array of 6-char-long subarrays
    # example of one of these sub arrays: [1,2,3,4,5,6]
    sboxSplit = [*inputString]
    sboxSplit = [sboxSplit[n:n+6] for n in range(0, len([*inputString]), 6)]

    # runs sbox subsitution and concats the final output binary string
    index = 0
    outputBinary = ""
    while index < len(sboxSplit):
        outputBinary += runSBox(sboxSplit[index], index)
        index += 1
    
    return outputBinary

# expected input: 6-char string
# converts the binary string into a row and column number, performs necessary s box and returns 4-char-long string of binary

def runSBox(inputString: str, index: int):
    row = int(inputString[0] + inputString[5], 2) # the ,2 indicates to the int() that it's converting from base 2
    column = int(inputString[1] + inputString[2] + inputString[3] + inputString[4], 2)

    substitution = sboxes[index][row][column]
    substitution = bin(substitution)[2:] # [2:] removes the 0b that python adds to the end of binary strings

    # pads any strings less than 4 chars long with 0's
    while(len([*substitution]) < 4):
        substitution = "0" + substitution
    return substitution