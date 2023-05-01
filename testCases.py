from sboxes import *
from tables import *
from main import performLeftShift, performRound, performXOR

# UNDONE AND INCOMPLETE
def testSBox(testAll: bool, detailed: bool, *listOfTests):
    if not testAll:
        return 
    else:
        for table in sboxes:
            print(performSubstitution("101010101010101010101010101010101010101010101010"))


testSBox(True, False, 1,2,3,4)