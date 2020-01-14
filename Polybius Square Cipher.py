import string 
import math 

# ----------------------------------------------------
# Parameters:   None
# Return:       polybius_square (string)
# Description:  Returns the following polybius square
#               as a sequential string:
#               [1] [2]  [3] [4] [5] [6] [7] [8]
#           [1]      !    "   #   $   %   &   '
#           [2]  (   )    *   +   '   -   .   /
#           [3]  0   1    2   3   4   5   6   7
#           [4]  8   9    :   ;   <   =   >   ?
#           [5]  @   A    B   C   D   E   F   G
#           [6]  H   I    J   K   L   M   N   O
#           [7]  P   Q    R   S   T   U   V   W
#           [8]  X   Y    Z   [   \   ]   ^   _
# ---------------------------------------------------


def get_polybius_square():
    polybius_square = ''

    for i in range (32,96):
        char = str(chr(int(i)))
        polybius_square+= char 
        
    return polybius_square

# --------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (none)
# Return:       ciphertext (string)
# Description:  Encryption using Polybius Square
# --------------------------------------------------------------


def e_polybius(plaintext, key):
    ciphertext = ''

    sqr = get_polybius_square()
    p = plaintext.split('\n')
    for plain in p: 
        for i in plain:
            j = sqr.find(i.upper())
            num = str(j+11+2*(j//8))
            ciphertext+=str(num)
            
            if '8567' in ciphertext:
                print("newline found") 
                ciphertext.replace('8567', '\n')
        ciphertext+='\n'

    
    return ciphertext

# ---------------------------------
#       Problem 5                #
# ---------------------------------

# -------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (none)
# Return:       plaintext (string)
# Description:  Decryption using Polybius Square Cipher
#               Detects invalid ciphertext --> print error msg and return ''
#               Case 1: #of chars (other than \n) is not even
#               Case 2: the ciphertext contains non-numerical chars (except \n')
# -------------------------------------------------------


def d_polybius(ciphertext, key):
    plaintext = ''

    sqr = get_polybius_square()

    text = ciphertext.split("\n")

    for x in text:
        x = x.strip()

        if len(x)%2!=0:
            print("Invalid ciphertext! Decryption Failed!")
            return ''
        if x.isdigit() or x==0:
            for i in range(0, len(x),2):
                s = int(x[i:i+2])
                if s< 19:
                    a = 0
                elif s%10 > 5:
                    a = 2*round((s-11)/11)
                else:
                    a = 2*round((s-11)/10)
                asky = s-11-a

                char = sqr[asky] 
                plaintext +=char
            plaintext += '\n'
        elif len(x)==0:
            plaintext+='\n'
        else:
            print("Invalid ciphertext! Decryption Failed!")

        
    return plaintext
