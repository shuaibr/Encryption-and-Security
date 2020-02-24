
#-----------------------------------------------------------
# Parameters:   plaintext (str)
#               key (str)
# Return:       ciphertext (str)
# Description:  Encryption using Hill Cipher, 2x2 (mod 26)
#               key is a string consisting of 4 characters
#                   if key is too short, make it a running key
#                   if key is too long, use first 4 characters
#               Encrypts only alphabet
#               Case of characters can be ignored --> cipher is upper case
#               If necessary pad with 'Q'
# Errors:       if key is not inveritble or if plaintext is empty
#                   print error msg and return empty string
#-----------------------------------------------------------
def e_hill(plaintext,key):
    count = 0 
    ciphertext = ""
    if len(key) < 4:
        while len(key) != 4:
            key+=key[count]
            count+=1
    elif len(key) > 4:
        key = key[0:4]
    
    if plaintext == "":
        print('Error(e_hill): invalid plaintext')
        return ''

    non_alpha = []
    for i in range(len(plaintext)):
        if plaintext[i].isalpha() != True:
            non_alpha.append([i,plaintext[i]])

    text = utilities_A4.remove_nonalpha(plaintext).upper()
    key_matrix = matrix.new_matrix(2,2,0)
    key = key.lower()

    key_matrix[0][0] = ord(key[0])-97
    key_matrix[0][1] = ord(key[1])-97
    key_matrix[1][0] = ord(key[2])-97
    key_matrix[1][1] = ord(key[3])-97

    d = mod.has_mul_inv(matrix.det(key_matrix),26)
    if not d:
        print('Error(e_hill): key is not invertible')
        return ''

    while len(text)%2!=0:
        text+='Q'

    blocks = utilities_A4.text_to_blocks(text,2)

    plain_matrix = matrix.new_matrix(2,len(blocks),0)

    for i in range(len(blocks)):
        plain_matrix[0][i] = ord(blocks[i][0])-65
        plain_matrix[1][i] = ord(blocks[i][1])-65

    cipher_matrix = []

    cipher_matrix = (matrix.matrix_mod(matrix.mul(key_matrix,plain_matrix),26))

    for i in range(matrix.get_columnCount(cipher_matrix)):
            ciphertext+=chr(cipher_matrix[0][i]+65)+chr(cipher_matrix[1][i]+65)
        
    for i in range(len(non_alpha)):
        index = non_alpha[i][0]
        char = non_alpha[i][1]
        ciphertext = ciphertext[:index]+char+ciphertext[index:]

    return ciphertext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (str)
# Return:       plaintext (str)
# Description:  Decryption using Hill Cipher, 2x2 (mod 26)
#               key is a string consisting of 4 characters
#                   if key is too short, make it a running key
#                   if key is too long, use first 4 characters
#               Decrypts only alphabet
#               Case of characters can be ignored --> plain is lower case
#               Remove padding of q's
# Errors:       if key is not inveritble or if ciphertext is empty
#                   print error msg and return empty string
#-----------------------------------------------------------
def d_hill(ciphertext,key):
    
    count = 0 
    plaintext = ""
    if len(key) < 4:
        while len(key) != 4:
            key+=key[count]
            count+=1
    elif len(key) > 4:
        key = key[0:4]
    
    if ciphertext == "" or ciphertext is None:
        print('Error(d_hill): invalid ciphertext')
        return ''

    non_alpha = []
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha() != True:
            non_alpha.append([i,ciphertext[i]])

    text = utilities_A4.remove_nonalpha(ciphertext).upper()
    key_matrix = matrix.new_matrix(2,2,0)
    key = key.lower()

    key_matrix[0][0] = ord(key[0])-97
    key_matrix[0][1] = ord(key[1])-97
    key_matrix[1][0] = ord(key[2])-97
    key_matrix[1][1] = ord(key[3])-97

    d = mod.has_mul_inv(matrix.det(key_matrix),26)
    if not d:
        return 'not invertible'

    A = key_matrix 

    inverse= [[A[1][1],-(A[0][1])],[-(A[1][0]),A[0][0]]]
    # d = abs(det(A))
    d = mod.mul_inv(matrix.det(A),26)
    
    inverse = matrix.scalar_mul(d,inverse)
    inv_matrix = matrix.matrix_mod(inverse,26)

    while len(text)%2!=0:
        text+='Q'

    blocks = utilities_A4.text_to_blocks(text,2)

    cipher_matrix = matrix.new_matrix(2,len(blocks),0)

    for i in range(len(blocks)):
        cipher_matrix[0][i] = ord(blocks[i][0])-65
        cipher_matrix[1][i] = ord(blocks[i][1])-65

    plain_matrix = []

    plain_matrix = (matrix.matrix_mod(matrix.mul(inv_matrix,cipher_matrix),26))

    for i in range(matrix.get_columnCount(plain_matrix)):
        plaintext+=chr(plain_matrix[0][i]+65)+chr(plain_matrix[1][i]+65)
    
    final= plaintext.strip('Q').lower()

    for i in range(len(non_alpha)):
        index = non_alpha[i][0]
        char = non_alpha[i][1]
        final = final[:index]+char+final[index:]

    return final
