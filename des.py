try:
    import bitarray
    from bitarray.util import ba2int
except:
    raise Exception("Make sure you have bitarray 2.7.3 or higher installed")


class DES():
    def __init__(self, inputText:str, key:str, mode:str, desType: int):
        self.inputText = inputText
        self.inputKey = key
        self.mode = mode # "e" for encrypt, "d" for decrypt
        self.desVersion = desType
        self.ip = [ #Initial Permutation Function
                        58,50,42,34,26,18,10,2,
                        60,52,44,36,28,20,12,4,
                        62,54,46,38,30,22,14,6,
                        64,56,48,40,32,24,16,8,
                        57,49,41,33,25,17,9,1,
                        59,51,43,35,27,19,11,3,
                        61,53,45,37,29,21,13,5,
                        63,55,47,39,31,23,15,7
                    ]
        self.expansion = [ #self.expansion Table
                        32,1,2,3,4,5,
                        4,5,6,7,8,9,
                        8,9,10,11,12,13,
                        12,13,14,15,16,17,
                        16,17,18,19,20,21,
                        20,21,22,23,24,25,
                        24,25,26,27,28,29,
                        28,29,30,31,32,1
                    ]
        self.pc1 = [ #Permutation Choice 1
                        57,49,41,33,25,17,9,
                        1,58,50,42,34,26,18,
                        10,2,59,51,43,35,27,
                        19,11,3,60,52,44,36,
                        63,55,47,39,31,23,15,
                        7,62,54,46,38,30,22,
                        14,6,61,53,45,37,29,
                        21,13,5,28,20,12,4
                    ]
        self.pc2 = [ #Permutation Choice 2
                        14,17,11,24,1,5,
                        3,28,15,6,21,10,
                        23,19,12,4,26,8,
                        16,7,27,20,13,2,
                        41,52,31,37,47,55,
                        30,40,51,45,33,48,
                        44,49,39,56,34,53,
                        46,42,50,36,29,32
                    ]
        self.leftShifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
        self.sboxes = [[
                        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
                        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
                        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
                        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
                    ],[
                        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
                        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
                        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
                        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
                    ],[
                        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
                        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
                        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
                        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
                    ], [
                        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
                        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
                        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
                        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
                    ], [
                        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
                        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
                        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
                        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
                    ],[
                        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
                        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
                        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
                        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
                    ],[
                        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
                        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
                        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
                        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
                    ], [
                        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
                        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
                        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
                        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
                    ]
                ]
        self.standardPermutation = [ #Standard Permutation Function
                        16,7,20,21,29,12,28,17,
                        1,15,23,26,5,18,31,10,
                        2,8,24,14,32,27,3,9,
                        19,13,30,6,22,11,4,25
                    ]
        self.inverseIP = [ #Inverse Initial Permutation Function
                        40,8,48,16,56,24,64,32,
                        39,7,47,15,55,23,63,31,
                        38,6,46,14,54,22,62,30,
                        37,5,46,13,53,21,61,29,
                        36,4,44,12,52,20,60,28,
                        35,3,43,11,51,19,59,27,
                        34,2,42,10,50,18,58,26,
                        33,1,41,9,49,17,57,25
                    ]
        self.fullRoundBinaries = []
        self.outputText = ""

    def getRoundBinaries(self):
        return self.fullRoundBinaries

    def run(self):
        if(self.mode == "e"):
            ciphertext = self.encrypt()
            self.processRoundBinaries()
            return ciphertext
        elif(self.mode == "d"):
            plaintext = self.decrypt()
            return plaintext
        else:
            raise Exception("ModeError: must be 'e' (encrypt) or 'd' (decrypt)")
        
    def performPermutations(self, block, table):
        if(table == 1):
        # Perform the initial permutation using self.ip table
            permutedText = bitarray.bitarray()
            for i in self.ip:
                permutedText.append(block[i - 1])
            return permutedText
        
        elif(table == 2):
            # Perform the initial permutation using self.ip table
            permutedText = bitarray.bitarray()
            for i in self.ip:
                permutedText.append(block[i - 1])
            return permutedText
        
        elif(table == 3):
            # Perform the self.expansion permutation using self.expansion table
            expandedText = bitarray.bitarray()
            for i in self.expansion:
                expandedText.append(block[i - 1])
            return expandedText
        
        elif(table == 4):
            permutedText = bitarray.bitarray()
            for i in self.standardPermutation:
                permutedText.append(block[i - 1])
            return permutedText
        
        elif(table == 5):
            permutedText = bitarray.bitarray()
            for i in self.inverseIP:
                permutedText.append(block[i - 1])
            return permutedText
        


    def generateRoundKeys(self, key):
        # Perform the permutation choice 1 (self.pc1) on the key
        tempKey = bitarray.bitarray()
        for i in self.pc1:
            tempKey.append(key[i - 1])

        # Split the permuted key into left and right halves
        keyLeft = tempKey[:28]
        keyRight = tempKey[28:]

        roundKeys = []
        for shift in self.leftShifts:
            # Perform left shift on the halves
            keyLeft = keyLeft[shift:] + keyLeft[:shift]
            keyRight = keyRight[shift:] + keyRight[:shift]

            # Perform permutation choice 2 (self.pc2) on the combined halves
            newKey = keyLeft + keyRight
            newRoundKey = bitarray.bitarray()
            for i in self.pc2:
                newRoundKey.append(newKey[i - 1])

            roundKeys.append(newRoundKey)

        return roundKeys

    def performSBox(self, block):
        substitutedText = bitarray.bitarray()

        # Split the block into 6-bit segments
        segments = [block[i:i+6] for i in range(0, len(block), 6)]

        # Apply S-box substitutions to each segment
        for i, segment in enumerate(segments):
            rowNum = segment[0] + segment[5]
            colNum = ba2int(segment[1:5])
            row = int(rowNum)  # Get the row index
            column = int(colNum)  # Get the column index
            newValue = self.sboxes[i][row][column]  # Lookup the S-box value

            substitutedText.extend(format(newValue, '04b'))  # Convert to 4-bit binary and append

        return substitutedText

    def performRounds(self, block, roundKeys):
        left = block[:32]
        right = block[32:]

        for i in range(16):
            currentString = self.performPermutations(right, 3)
            
            # Access the round key for the specific round
            newRoundKey = roundKeys[i]

            # XOR the expanded block with the round key
            if(self.desVersion != 1):
                currentString = currentString ^ newRoundKey

            if(self.desVersion != 2):
                currentString = self.performSBox(currentString)
            else:
                currentString = self.performSBox(currentString)

            if(self.desVersion != 3):
                currentString = self.performPermutations(currentString, 4)
            currentString = currentString ^ left

            left = right
            right = currentString

            self.fullRoundBinaries.append((left,right))

        finalRoundOutput = right + left

        return finalRoundOutput

    def processRoundBinaries(self):
        tempArray = []
        for round in self.fullRoundBinaries:
            fullBinary = str(round[0].to01()) + str(round[1].to01())
            tempArray.append(fullBinary)
        self.fullRoundBinaries = tempArray

    def getOutputText(self):
        return self.outputText

    def encrypt(self):
        # Convert the binary strings to bitarrays
        plaintext = bitarray.bitarray(self.inputText)
        key = bitarray.bitarray(self.inputKey)

        # Perform the initial permutation (self.ip)
        permutedText = self.performPermutations(plaintext, 1)

        # Generate the round keys
        roundKeys = self.generateRoundKeys(key)

        # Perform the rounds
        ciphertext = self.performRounds(permutedText, roundKeys)

        # Perform the final permutation (self.ip-1)
        ciphertext = self.performPermutations(ciphertext, 5)

        # Convert the ciphertext to a binary string and return
        self.outputText = ciphertext.to01()
        return ciphertext.to01()

    def decrypt(self):
        # Convert the binary strings to bitarrays
        ciphertext = bitarray.bitarray(self.inputText)
        key = bitarray.bitarray(self.inputKey)

        # Perform the initial permutation (self.ip)
        permutedText = self.performPermutations(ciphertext, 1)

        # Generate the round keys in reverse order
        roundKeys = self.generateRoundKeys(key)
        roundKeys.reverse()

        # Perform the Feistel network
        plaintext = self.performRounds(permutedText, roundKeys)

        # Perform the final permutation (self.ip-1)
        plaintext = self.performPermutations(plaintext, 5)

        # Convert the plaintext to a binary string and return
        self.outputText = plaintext.to01()
        return plaintext.to01()
