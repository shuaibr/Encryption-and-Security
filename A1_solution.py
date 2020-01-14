# --------------------------
# Shuaib Reeyaz (150616640)
# CP460 (Fall 2019)
# Assignment 1
# --------------------------


import math
import string

# ---------------------------------
#       Given Functions          #
# ---------------------------------
# -----------------------------------------------------------
# Parameters:   fileName (string)
# Return:       contents (string)
# Description:  Utility function to read contents of a file
#               Can be used to read plaintext or ciphertext
# -----------------------------------------------------------


def file_to_text(fileName):
    inFile = open(fileName, 'r')
    contents = inFile.read()
    inFile.close()
    return contents

# -----------------------------------------------------------
# Parameters:   text (string)
#               filename (string)
# Return:       none
# Description:  Utility function to write any given text to a file
#               If file already exist, previous content will be over-written
# -----------------------------------------------------------


def text_to_file(text, filename):
    outFile = open(filename, 'w')
    outFile.write(text)
    outFile.close()
    return

# -----------------------------------------------------------
# Parameters:   r: #rows (int)
#               c: #columns (int)
#               pad (str,int,double)
# Return:       empty matrix (2D List)
# Description:  Create an empty matrix of size r x c
#               All elements initialized to pad
#               Default row and column size is 2
# -----------------------------------------------------------


def new_matrix(r, c, pad):
    r = r if r >= 2 else 2
    c = c if c >= 2 else 2
    return [[pad] * c for i in range(r)]

# -----------------------------------------------------------
# Parameters:   marix (2D List)
# Return:       None
# Description:  prints a matrix each row in a separate line
#               Assumes given parameter is a valid matrix
# -----------------------------------------------------------


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end='\t')
        print()
    return
# -----------------------------------------------------------
# Parameters:   marix (2D List)
# Return:       text (string)
# Description:  convert a 2D list of characters to a string
#               left to right, then top to bottom
#               Assumes given matrix is a valid 2D character list
# -----------------------------------------------------------


def matrix_to_string(matrix):
    text = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            text += matrix[i][j]
    return text

# --------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (string)
# Return:       ciphertext (string)
# Description:  Encryption using Scytale Cipher
#               Key is the diameter, i.e. # rows
#               Assume infinte length rod (infinte #columns)
# --------------------------------------------------------------


def e_scytale(plaintext, key):
    # By definition, number of rows is key
    r = int(key)
    # number of columns is the length of ciphertext/# rows
    c = int(math.ceil(len(plaintext)/key))
    # create an empty matrix for ciphertext rxc
    cipherMatrix = new_matrix(r, c, "")

    # fill matrix horizontally with characers, pad empty slots with -1
    counter = 0
    for i in range(r):
        for j in range(c):
            cipherMatrix[i][j] = plaintext[counter] if counter < len(
                plaintext) else -1
            counter += 1

    # convert matrix into a string (vertically)
    ciphertext = ""
    for i in range(c):
        for j in range(r):
            if cipherMatrix[j][i] != -1:
                ciphertext += cipherMatrix[j][i]
    return ciphertext


# ---------------------------------
#       Problem 1                #
# ---------------------------------

# ----------------------------------------------------
# Parameters:   ciphertext(string)
#               key (string)
# Return:       plaintext (string)
# Description:  Decryption using Scytale Cipher
#               Assumes key is a valid integer in string format
# ---------------------------------------------------
def d_scytale(ciphertext, key):

    counter = 0
    c = math.ceil(len(ciphertext)/key)
    r = key
    negatives = int(c*r-len(ciphertext))
    filler = c*r-negatives
    
    plainMatrix = new_matrix(r, c, "")

    #print("row: ", r, " col: ", c)
    for i in range(c):
        for j in range(r):
            plainMatrix[j][i] = ciphertext[counter] if counter < len(ciphertext)  else -1
            if j==(r-1) and i==(c-negatives):
                plainMatrix[j][i] = -1
                negatives-=1
                counter -= 1
            counter+=1
            #print(plainMatrix[j][i])
            
        #print("col: ",i, "neg ", negatives)
    plaintext = ""

    for i in range(r):
        for j in range(c):
            if plainMatrix[i][j] != -1:
                plaintext += plainMatrix[i][j]

    return plaintext


# ---------------------------------
#       Problem 2                #
# ---------------------------------

# -----------------------------------------------------------
# Parameters:   dictFile (string): filename
# Return:       list of words (list)
# Description:  Reads a given dictionary file
#               dictionary file is assumed to be formatted: each word in a separate line
#               Returns a list of strings, each pertaining to a dictionary word
# -----------------------------------------------------------
def load_dictionary(dictFile):
    dictList = []

    f = open(dictFile, 'r',encoding="mbcs") 
    line = f.readlines()

    for x in line:
        dictList.append(x.strip())
        
    return dictList

# -------------------------------------------------------------------
# Parameters:   text (string)
# Return:       list of words (list)
# Description:  Reads a given text
#               Each word is saved as an element in a list.
#               Returns a list of strings, each pertaining to a word in file
#               Gets rid of all punctuation at the start and at the end
# -------------------------------------------------------------------


def text_to_words(text):
    wordList = []

    data = text.split()

    for x in data:
            if not x[0].isalnum():
                x = x[1:]
            if len(x)>2 and not x[-1].isalnum():
                #print("old x: ", x) 
                x = x[:-1]
                #print("new x: ", x) 
            wordList.append(x.strip())
        
    return wordList

# -----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
# Return:       (#matches, #mismatches)
# Description:  Reads a given text, checks if each word appears in dictionary
#               Returns a tuple of number of matches and number of mismatches.
#               Words are compared in lowercase.
# -----------------------------------------------------------


def analyze_text(text, dictFile):
    matches = 0
    mismatches = 0

    list = load_dictionary(dictFile)
    text_list = text_to_words(text.lower())

    for i in text_list:
        if i in list:
            matches +=1
        else:
            mismatches+=1
    return(matches, mismatches)

# -----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
#               threshold (float): number between 0 to 1
# Return:       True/False
# Description:  Check if a given file is a plaintext
#               If #matches/#words >= threshold --> True
#                   otherwise --> False
#               If invalid threshold given, default is 0.9
#               An empty string is assumed to be non-plaintext.
# -----------------------------------------------------------


def is_plaintext(text, dictFile, threshold):
    # your code here
    m, miss = analyze_text(text, dictFile)
    total = m+miss
    if threshold < 0 or threshold > 1:
        threshold = 0.9
    if m/total >= threshold:
        return True 
    
    return False

# ---------------------------------
#       Problem 3                #
# ---------------------------------

# ----------------------------------------------------
# Parameters:   cipherFile (string)
#               dictFile (string)
#               startKey (int)
#               endKey (int)
#               threshold (float)
# Return:       key (string)
# Description:  Apply brute-force to break scytale cipher
#               Valid key range: 2-100 (if invalid --> print error msg and return '')
#               Valid threshold: 0-1 (if invalid --> print error msg and return '')
#               If decryption is successful --> print plaintext and return key
#               If decrytpoin fails: print error msg and return ''
# ---------------------------------------------------


def cryptanalysis_scytale(cipherFile, dictFile, startKey, endKey, threshold):
    dictList = load_dictionary(dictFile)
    ciphertext = file_to_text(cipherFile)

    if startKey < 2 or endKey > 100:
        print("Invalid key range. Operation aborted!")
        return ''
    if threshold >1 or threshold <0 :
        print("Invalid threshold value. Operation aborted!")
        return ''
    
    for x in range(startKey, endKey):
        plaintext = d_scytale(ciphertext, x)
        val = is_plaintext(plaintext, dictFile, threshold)
        if val == True:
            print() 
            print("Key Found = ", x)
            print(plaintext)
            
            return x
        print("Key ",x, " failed")

    print("No key was found")
            
    return '' 

# ---------------------------------
#       Problem 4                #
# ---------------------------------

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
