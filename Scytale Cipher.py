import math 
import string 

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