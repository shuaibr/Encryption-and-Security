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
    m, miss = analyze_text(text, dictFile)
    total = m+miss
    if threshold < 0 or threshold > 1:
        threshold = 0.9
    if m/total >= threshold:
        return True 
    
    return False


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