
import math
import string
import mod
import matrix
import utilities_A4


#-----------------------------------------------------------
# Parameters:   plaintext (str)
#               key (str,int)
# Return:       ciphertext (str)
# Description:  Encryption using Decimation Cipher
#               key is tuple (baseString,k)
#               Does not encrypt characters not in baseString
#               Case of letters should be preserved
# Errors:       if key has no multiplicative inverse -->
#                   print error msg and return empty string
#-----------------------------------------------------------
def e_decimation(plaintext,key):
    ciphertext = ""
    
    sample = []
    text = key[0]
    dec_key = mod.has_mul_inv(key[1],len(key[0]))

    if not dec_key:
        print('Error (e_decimation): Invalid key')
        return 
    else:
        dec_key = mod.mul_inv(key[1], len(text))
        

    val = key[1]

    for i in plaintext:
        if i.lower() in text:
            if i.isupper():
                sample.append([mod.residue(text.index(i.lower())*val,len(key[0])),1])
            else:
                sample.append([mod.residue(text.index(i.lower())*val,len(key[0])),0])
            # if 65<=ord(i)<=90:
            #     sample.append([mod.residue((ord(i)-65)*val,len(key[0])),1])
            # elif 97<=ord(i)<=122:
            #     sample.append([mod.residue((ord(i)-97)*val,len(key[0])),0])  
            # else: 
            #     sample.append([mod.residue((ord(i)-97)*val,len(key[0])),0])        
        else:
            sample.append([ord(i),2])

    for j in sample:
        if j[1] == 1:
            ciphertext+=text[j[0]].upper()
        elif j[1]==0:
            ciphertext+=text[j[0]]
        else:
            ciphertext += chr(j[0])
    
    return ciphertext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (str,int)
# Return:       plaintext (str)
# Description:  Decryption using Decimation Cipher
#               key is tuple (baseString,k)
#               Does not decrypt characters not in baseString
#               Case of letters should be preserved
# Errors:       if key has no multiplicative inverse -->
#                   print error msg and return empty string
#-----------------------------------------------------------
def d_decimation(ciphertext,key):
    plaintext = ""

    sample = []
    
    text = key[0]

    val = key[1]
    if val > len(text):
        val = mod.residue(val, len(text))
    dec_key = mod.has_mul_inv(val,len(text))

    if not dec_key:
        print('Error (d_decimation): Invalid key')
        return 
    else:
        dec_key = mod.mul_inv(key[1], len(text))

    for i in ciphertext:
        if i.lower() in text:
            if i.isupper():
                plaintext+= text[(mod.residue(text.index(i.lower())*dec_key,len(text)))].upper()
            else:
                plaintext+=text[(mod.residue(text.index(i.lower())*dec_key,len(text)))]
            # if 65<=ord(i)<=90:
            #     sample.append([mod.residue((ord(i)-65)*dec_key,26),1])
            # elif 97<=ord(i)<=122:
            #     sample.append([mod.residue((ord(i)-97)*dec_key,26),0])           
        else:
            plaintext+=i

    # for j in sample:
    #     if j[1] == 1:
    #         plaintext+=chr(j[0]+65).upper()
    #     elif j[1]==0:
    #         plaintext+=chr(j[0]+97)
    #     else:
    #         plaintext+= chr(j[0])
    return plaintext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
# Return:       plaintext,key
# Description:  Cryptanalysis of Decimation Cipher
#-----------------------------------------------------------
def cryptanalysis_decimation(ciphertext):

    text = utilities_A4.get_baseString()
    text_len = len(text)
    # num = [3,5,7,9,11,15,17,19,21,23,25]
    # pas = []
    attempts = 0 
    for x in range(26, len(text)):
        testing_text = text[:x]
        testing_len = len(testing_text)
        for y in range(1,testing_len):
            inv = mod.mul_inv(y,testing_len)
            if inv != 'NA':
                check = d_decimation(ciphertext,(testing_text,y))
                attempts+=1 
                is_plain = utilities_A4.is_plaintext(check, utilities_A4.load_dictionary('engmix.txt'), 0.9)
                if is_plain:
                    print("Key found after ", attempts, "attempts")
                    return check, (testing_text,y)
            
    # for i in num:
    #     test = d_decimation(ciphertext, (text,i))
    #     dictList = utilities_A4.load_dictionary('engmix.txt')
    #     check  = utilities_A4.is_plaintext(test, dictList,0.9)
    #     print("Test: ", i, " ans: ", test, " chec: ", check)
    #     if check:
    #         return test, (text,i)
    # i = 0 
    # print(ciphertext)

    # while not check:
    #     key[1]+=1
    #     print("key: ", key)
    #     test = d_decimation(ciphertext, key)
    #     print(test)
    #     check  = utilities_A4.is_plaintext(test, 'engmix.txt',0.9)
    #     i+=1

