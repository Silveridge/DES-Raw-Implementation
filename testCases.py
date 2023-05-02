from sboxes import *
from tables import *
from main import performLeftShift, performRound, performXOR
from des import DesKey

# UNDONE AND INCOMPLETE
def testSBox(testAll: bool, detailed: bool, *listOfTests):
    if not testAll:
        return 
    else:
        for table in sboxes:
            print(performSubstitution("101010101010101010101010101010101010101010101010"))


key = DesKey(b'hijklm')
key.is_single()

key.encrypt("abcdefgh")