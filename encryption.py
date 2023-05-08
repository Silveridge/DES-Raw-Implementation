from sboxes import *
from tables import *

class Encryptor():
    def __init__(self, inputBinary:str, inputKey:str):
        self.rounds = 16
        self.currentRound = 0
        self.fullRoundBinaries = []
        self.permutations = Permutations()
        self.sbox = SubstitutionBoxes()
        self.inputText = inputBinary
        self.inputKey = inputKey

    def changePlaintext(self, newText:str):
        self.inputText = newText
    
    def changeKey(self, newKey:str):
        self.inputKey = newKey

    def performXOR(self, input1: str, input2: str):
        outputString = [(ord(a) ^ ord(b)) for a, b in zip(input1, input2)] # xor's by pairing each element in input1 and input2, autochange them to int, then xor.
        outputString = "".join(map(str, outputString)) # output of above function is an array of ints, converts to string
        return outputString

    def performLeftShift(self, input: str, roundNumber: int):
        twoShifts = [3,4,5,6,7,8,10,11,12,13,14,15]
        inputA = [*input]
        inputA.append(inputA.pop(0))
        if(roundNumber in twoShifts):
            inputA.append(inputA.pop(0))
        input = "".join(inputA)
        return input

    def performRound(self, inputText: str, inputKey: str, roundNumber: int, des:int):
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
        keyLeft = self.performLeftShift(keyLeft, roundNumber)
        keyRight = self.performLeftShift(keyRight, roundNumber)

        # final key values
        keyOutRight = keyRight
        keyOutLeft = keyLeft
        subKey = keyRight + keyLeft

        # get key to XOR
        keyToXOR = self.permutations.performPermutation(subKey, 6)

        ### TEXT OPERATIONS

        # split text into 32-bit halves
        inLeft = inputText[0:32]
        inRight = inputText[32:]
        outLeft = inRight

        # EXPANSION TABLE
        currentString = self.permutations.performPermutation(inRight, 3)

        # XOR
        if(des != 1):
            currentString = self.performXOR(currentString, keyToXOR)

        # S-BOX
        if(des != 2):
            currentString = self.sbox.performSubstitution(currentString)
        else:
            currentString = self.sbox.performSubstitution(currentString)
            #currentString = self.permutations.performPermutation(currentString,7) ## UNFINISHED, SEE tables.py

        # PERMUTATION
        if(des != 3):
            currentString = self.permutations.performPermutation(currentString, 4)

        # XOR With inLeft
        outRight = self.performXOR(currentString, inLeft)

        return(outLeft, outRight, keyOutLeft, keyOutRight)
        
    def encrypt(self, des: int):
        # Step 0: Setup
        self.currentRound = 0
        self.fullRoundBinaries = []

        # Step 1: Input
        binIn = self.inputText
        key = self.inputKey

        # Step 2: Initial Permutation
        newInputBinary = self.permutations.performPermutation(binIn, 1)

        # Step 3: Rounds
        newKey = key # for variable's sake
        self.currentRound = 1
        while self.currentRound <= self.rounds:
            leftString, rightString, keyLeft, keyRight = self.performRound(newInputBinary, newKey, self.currentRound, des)
            newInputBinary = str(leftString) + str(rightString) # str() is a failsafe just incase it interprets as int or bin
            newKey = str(keyLeft) + str(keyRight)
            self.fullRoundBinaries.append(newInputBinary)
            self.currentRound += 1
            
        roundOutput = newInputBinary

        # Step 4: 32-bit swap
        roundOutputLeft = roundOutput[0:32]
        roundOutputRight = roundOutput[32:]

        swapOutput = str(roundOutputRight) + str(roundOutputLeft)

        # Step 5: Inverse Initial Permutation
        finalOutput = self.permutations.performPermutation(swapOutput, 2)

        return finalOutput, self.fullRoundBinaries