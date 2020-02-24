#-----------------------------------------------------------
# Parameters:   plaintext (str)
#               key (str,[int,int])
# Return:       ciphertext (str)
# Description:  Encryption using Affine Cipher
#               key is tuple (baseString,[alpha,beta])
#               Does not encrypt characters not in baseString
#               Case of letters should be preserved
# Errors:       if key can not be used for decryption
#                   print error msg and return empty string
#-----------------------------------------------------------
def e_affine(plaintext,key):
    
    a = key[1][0] 
    b = key[1][1]
    text = key[0]
    ciphertext = ""

    if mod.gcd(a, len(text)) != 1:
        print('Error (e_affine): Invalid key')
        return 
    
    #f(x) = ax + b 

    for i in plaintext: 
        if i.lower() in text:
            if i.isupper():
                ciphertext+= text[mod.residue((text.index(i.lower())*a + b), len(text))].upper()
            else:
                ciphertext+= text[mod.residue((text.index(i)*a + b), len(text))]
        else:
            ciphertext+=i

    return ciphertext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (str,[int,int])
# Return:       plaintext (str)
# Description:  Decryption using Affine Cipher
#               key is tuple (baseString,[alpha,beta])
#               Does not decrypt characters not in baseString
#               Case of letters should be preserved
# Errors:       if key can not be used for decryption
#                   print error msg and return empty string
#-----------------------------------------------------------
def d_affine(ciphertext,key):
    a = key[1][0] 
    b = key[1][1]
    text = key[0]
    plaintext = ""

    if mod.gcd(a, len(text)) != 1:
        print('Error (d_affine): Invalid key')
        return 

    if a > len(text):
        a = mod.residue(a, len(text))
    dec_key = mod.has_mul_inv(a,len(text))

    if not dec_key:
        print('Error (d_decimation): Invalid key')
        return 
    else:
        dec_key = mod.mul_inv(a, len(text))
    
    #(y-b)/a = x 

    for i in ciphertext: 
        if i.lower() in text:
            if i.isupper():
                plaintext+= text[mod.residue(dec_key*(text.index(i.lower())-b),len(text))].upper()
            else:
                plaintext+= text[mod.residue(dec_key*(text.index(i)-b),len(text))]
        else:
            plaintext+=i

    return plaintext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
# Return:       plaintext,key
# Description:  Cryptanalysis of Affine Cipher
#-----------------------------------------------------------
def cryptanalysis_affine(ciphertext):
    # text = 'abcdefghijklmnopqrstuvwxyz'
    # nums = [3,5,7,9,11,15,17,19,21,23,25]
    # char = [] 
    # for i in ciphertext:
    #     char.append(i)
    # char.sort()

    # i = 0 
    # for a in range(12):
    #     for b in range(1, len(text)):
    #         test = d_affine(ciphertext, (text,[nums[a],b]))
    #         dictList = utilities_A4.load_dictionary('engmix.txt')
    #         check  = utilities_A4.is_plaintext(test, dictList,0.9)
    #         # print("Test: ", i, " ans: ", test, " chec: ", check)
    #         if check:
    #             print("key fround afer ", i, " attemps")
    #             return test, (text,[nums[a],b])
    #             break
    #         i+=1
    text = utilities_A4.get_baseString()
    text_len = len(text)

    attempts = 0 

    for x in range(26, len(text)):
        testing_text = text[:x]
        testing_len = len(testing_text)
        for a in range(1,testing_len):
            for b in range(testing_len):
                invA = mod.mul_inv(a,testing_len)

                if invA != 'NA':
                    attempts+=1
                    if invA != 'NA' and mod.gcd(a, len(ciphertext)) == 1 and mod.has_mul_inv(a,len(ciphertext)):
                        check = d_affine(ciphertext,(testing_text,[a,b]))
                        if check != None:
                            
                            is_plain = utilities_A4.is_plaintext(check, utilities_A4.load_dictionary('engmix.txt'), 0.9)
                            if is_plain:
                                print("Key found after ", attempts, "attempts")
                                return check, (testing_text,[a,b])
                
                # print(a,b,invA, mod.gcd(a, len(ciphertext)), mod.has_mul_inv(a,len(ciphertext)))
                # # if invA != 'NA' and mod.gcd(a, len(ciphertext)) == 1 and mod.has_mul_inv(a,len(ciphertext)):
                #     print(a,b)
                #     check = d_affine(ciphertext,(testing_text,[a,b]))
                #     attempts+=1 
                #     # print(check, " key: ", [a,b])
                #     if check != None:
                        
                #         is_plain = utilities_A4.is_plaintext(check, utilities_A4.load_dictionary('engmix.txt'), 0.9)
                #         if is_plain:
                #             print("Key found after ", attempts, "attempts")
                #             return check, (testing_text,[a,b])
                

