import math
import string
import mod
import utilities

configFile = 'SDES_config.txt'
sbox1File = 'sbox1.txt'
sbox2File = 'sbox2.txt'
primeFile = 'primes.txt'

#-----------------------------------------------------------
# Parameters:   c (str): a character
#               codeType (str)
# Return:       b (str): corresponding binary number
# Description:  Generic function for encoding
#               Current implementation supports only ASCII and B6 encoding
# Error:        If c is not a single character:
#                   print('Error(encode): invalid input'), return ''
#               If unsupported encoding type:
#                   print('Error(encode): Unsupported Coding Type'), return '' 
#-----------------------------------------------------------
def encode(c,codeType):
    if not isinstance(c, str) or len(c) != 1:
        print('Error(encode): invalid input')
        return ''
    if codeType == 'ASCII': #represents each character in 7 bits 
        b = utilities.dec_to_bin(ord(c),8)
    elif codeType == 'B6': #B6 is lower, upper and ten numerical works in 6 bits 
        b = encode_B6(c)
    else:
        print('Error(encode): Unsupported Coding Type')
        return ''
    return b

#-----------------------------------------------------------
# Parameters:   b (str): a binary number
#               codeType (str)
# Return:       c (str): corresponding character
# Description:  Generic function for decoding
#               Current implementation supports only ASCII and B6 encoding
# Error:        If c is not a binary number:
#                   print('Error(decode): invalid input',end =''), return ''
#               If unsupported encoding type:
#                   print('Error(decode): Unsupported Coding Type',end =''), return '' 
#-----------------------------------------------------------
def decode(b,codeType):
    if not utilities.is_binary(b):
        print('Error(decode): invalid input',end ='')
        return ''
    if codeType == 'ASCII':
        c = chr(utilities.bin_to_dec(b))
    elif codeType == 'B6':
        b6 = utilities.get_B6Code()
        c = b6[utilities.bin_to_dec(b)]
    else:
        print('Error(decode): Unsupported Coding Type',end ='')
        return ''
    return c

#-----------------------------------------------------------
# Parameters:   c (str): a character
# Return:       b (str): 6-digit binary code
# Description:  Encodes any given symbol in the B6 Encoding scheme
#               If given symbol is one of the 64 symbols, the function returns
#               the binary representation, which is the equivalent binary number
#               of the decimal value representing the position of the symbol in the B6Code
#               If the given symbol is not part of the B6Code --> return empty string (no error msg)
# Error:        If given input is not a single character -->
#                   print('Error(encode_B6): invalid input',end =''), return ''
#-----------------------------------------------------------
def encode_B6(c):
    b6 = utilities.get_B6Code()
    if not isinstance(c, str) or len(c)!=1:
        print('Error(encode_B6): invalid input')
        return ''
    else:
        b = utilities.dec_to_bin(b6.index(c),6)
    return b

#-----------------------------------------------------------
# Parameters:   b (str): binary number
# Return:       c (str): a character
# Description:  Decodes any given binary code in the B6 Coding scheme
#               Converts the binary number into integer, then get the
#               B6 code at that position
# Error:        If given input is not a valid 6-bit binary number -->
#                   print('Error(decode_B6): invalid input',end =''), return ''
#-----------------------------------------------------------
def decode_B6(b):
    b6 = utilities.get_B6Code()
    if not isinstance(b, str) or len(b)!=6:
        print('Error(decode_B6): Invalid input')
        return ''
    else:
        c = b6[utilities.bin_to_dec(b)]
    return c

#-----------------------
# SDES Configuration
#-----------------------
#-----------------------------------------------------------
# Parameters:   None
# Return:       paramList (list)
# Description:  Returns a list of parameter names which are used in
#               Configuration of SDES
# Error:        None
#-----------------------------------------------------------
def get_SDES_parameters():
    return ['encoding_type','block_size','key_size','rounds','p','q']

#-----------------------------------------------------------
# Parameters:   None
# Return:       configList (2D List)
# Description:  Returns the current configuraiton of SDES
#               configuration list is formatted as the following:
#               [[parameter1,value],[parameter2,value2],...]
#               The configurations are read from the configuration file
#               If configuration file is empty --> return []
# Error:        None
#-----------------------------------------------------------
def get_SDES_config():
    configFile = 'SDES_config.txt'
    conf = ['encoding_type','block_size','key_size','rounds','p','q']
    f = open(configFile, "r")
    if f.mode == 'r':
        contents = f.readline()
        configList = []
        while contents.split(" ")[0] in conf:
            configList.append([contents.split(" ")[0],contents.split(" ")[1]])
            contents = f.readline()
        f.close()
    return configList

#-----------------------------------------------------------
# Parameters:   parameter (str)
# Return:       value (str)
# Description:  Returns the value of the parameter based on the current
# Error:        If the parameter is undefined in get_SDES_parameters() -->
#                   print('Error(get_SDES_value): invalid parameter',end =''), return ''
#-----------------------------------------------------------
def get_SDES_value(parameter):
    conf = ['encoding_type','block_size','key_size','rounds','p','q']
    configList = get_SDES_config()
    if parameter in conf:
        for i in range(len(configList)):
            if configList[i][0] == parameter:
                return configList[i][1]
        return ''
    else:
        print('Error(get_SDES_value): invalid parameter',end ='')
        return ''
    return value

#-----------------------------------------------------------
# Parameters:   parameter (str)
#               value (str)
# Return:       True/False
# Description:  Sets an SDES parameter to the given value and stores
#               the output in the configuration file
#               if the configuration file contains previous value for the parameter
#               the function overrides it with the new value
#               otherwise, the new value is appended to the configuration file
#               Function returns True if set value is successful and False otherwise
# Error:        If the parameter is undefined in get_SDES_parameters() -->
#                   print('Error(cofig_SDES): invalid parameter',end =''), return False
#               If given value is not a string or is an empty string:
#                   print('Error(config_SDES): invalid value',end =''), return 'False
#-----------------------------------------------------------
def config_SDES(parameter,value):
    conf = ['encoding_type','block_size','key_size','rounds','p','q']
    configList = get_SDES_config()
    if parameter in conf and isinstance(value, str): 
        f = open(configFile, 'w+')
        rep = False 
        for i in range(len(configList)):
            if configList[i][0] == parameter:
                configList[i][1] = value
                rep = True 
            f.write(configList[i][0]+ " " +configList[i][1] + " \n")
        if not rep:
            f.write(parameter+ " " + value + " \n")
        f.close()
        return True 
    elif parameter not in conf:
        print('Error(cofig_SDES): invalid parameter',end ='')
    elif not isinstance(value,str) or value == "":
        print('Error(config_SDES): invalid value',end ='')
    return False

#-----------------------
# Key Generation
#-----------------------
#-----------------------------------------------------------
# Parameters:   p (int)
#               q (int)
#               m (int): number of bits
# Return:       bitStream (str)
# Description:  Uses Blum Blum Shub Random Generation Algorithm to generates
#               a random stream of bits of size m
#               The seed is the nth prime number, where n = p*q
#               If the nth prime number is not relatively prime with n,
#               the next prime number is selected until a valid one is found
#               The prime numbers are read from the file primeFile (starting n=1)
# Error:        If number of bits is not a positive integer -->
#                   print('Error(blum): Invalid value of m',end =''), return ''
#               If p or q is not an integer that is congruent to 3 mod 4:
#                   print('Error(blum): Invalid values of p,q',end =''), return ''
#-----------------------------------------------------------
def blum(p,q,m):
    if m <= 0:
        print('Error(blum): Invalid value of m',end ='')
        return ''
    elif not isinstance(p, int) or not isinstance(q, int) or not mod.is_congruent(p,3,4) or not mod.is_congruent(q,3,4):
        print('Error(blum): Invalid values of p,q',end ='')
        return ''
    else:
        n = p*q 
        prime = open(primeFile, 'r')
        lines = prime.readlines()
        pn = lines[n-1]
        while not mod.is_relatively_prime(pn,n):
            # print(n, pn)
            pn = lines[n-1]
            n+=1 
            # print(n, pn)

        seed = int(pn)
        bitStream = ""
        for x in range(m):            
            seed = (seed**2)%n
            bitStream+= str(mod.residue((seed**2),n)%2)
        prime.close()

        return bitStream

#-----------------------------------------------------------
# Parameters:   None
# Return:       key (str)
# Description:  Generates an SDES key based on preconfigured values
#               The key size is fetched from the SDES configuration
#               If no key size is available, an error message is printed
#               Also, the values of p and q are fetched as per SDES configuration
#               If no values are found, the default values p = 383 and q = 503 are used
#               These values should be updated in the configuration file
#               The function calls the blum function to generate the key
# Error:        if key size is not defined -->
#                           print('Error(generate_key_SDES):Unknown Key Size',end=''), return ''
#-----------------------------------------------------------
def generate_key_SDES():
    key_size = get_SDES_value('key_size')
    p = get_SDES_value('p')
    q = get_SDES_value('q')
    if key_size == '':
        print('Error(generate_key_SDES):Unknown Key Size',end='')
        return ''
    else: 
        if p =='': p = 383 ; config_SDES('p','383')
        if q =='': q = 503 ; config_SDES('q','503')
        p = int(p)
        q = int(q)
        key = blum(p,q,int(key_size))
    return key

#-----------------------------------------------------------
# Parameters:   key (str)
#               i (int)
# Return:       key (str)
# Description:  Generates a subkey for the ith round in SDES
#               The sub-key is one character shorter than original key size
#               Sub-key is generated by circular shift of key with value 1,
#               where i=1 means no shift
#               The least significant bit is dropped after the shift
# Errors:       if key is not a valid binary number or its length does not match key_size: -->
#                   print('Error(get_subKey): Invalid key',end='')
#               if i is not a positive integer:
#                   print('Error(get_subKey): invalid i',end=''), return ''
#-----------------------------------------------------------
def get_subKey(key,i):
    key_size = int(get_SDES_value('key_size'))
    if not utilities.is_binary(key) or len(key) != key_size:
        print('Error(get_subKey): Invalid key',end='')
        return '' 
    elif not isinstance(i, int) or i <= 0: 
        print('Error(get_subKey): invalid i',end='')
        return ''
    else: 
        i-=1
        leftA = key[0:i]
        leftB = key[i:]
        subKey = leftB+leftA
        subKey = subKey[:len(subKey)-1]
    return subKey

#-----------------------
# Fiestel Network
#-----------------------
#-----------------------------------------------------------
# Parameters:   R (str): binary number of size (block_size/2)
# Return:       output (str): expanded binary
# Description:  Expand the input binary number by adding two digits
#               The input binary number should be an even number >= 6
#               Expansion works as the following:
#               If the index of the two middle elements is i and i+1
#               From indices 0 up to i-1: same order
#               middle becomes: R(i+1)R(i)R(i+1)R(i)
#               From incides R(i+2) to the end: same order
# Error:        if R not a valid binary number or if it has an odd length
#               or is of length smaller than 6
#                   print('Error(expand): invalid input',end=''), return ''
#-----------------------------------------------------------
def expand(R):
    if not utilities.is_binary(R) or len(R)%2 != 0 or utilities.bin_to_dec(R)<6:
        print('Error(expand): invalid input',end='')
        return ''
    else: 
        mid = int(len(R)/2)-1
        i = mid 
        start = R[0:i]
        middle = R[i+1]+R[i]+R[i+1]+R[i]
        end = R[i+2:]
        output = start+middle+end
    
    return output

#-----------------------------------------------------------
# Parameters:   R (str): binary number of size (block_size//4)
# Return:       output (str): binary number
# Description:  Validates that R is of size block_size//4 + 1
#               Retrieves relevant structure of sbox1 from sbox1File
#               Most significant bit of R is row number, other bits are column number
# Error:        if undefined block_size:
#                   print('Error(sbox1): undefined block size',end=''), return ''
#               if invalid R:
#                   print('Error(sbox1): invalid input',end=''),return ''
#               if no sbox1 structure exist:
#                   print('Error(sbox1): undefined sbox1',end=''),return ''
#-----------------------------------------------------------       
def sbox1(R):
    block_size = int(get_SDES_value('block_size'))
    sbox = open(sbox1File, 'r')
    bi_bs = utilities.dec_to_bin(block_size, 10)
    lines = sbox.readlines()
    check =lines[0]
    if R != '' and len(R) == int(get_SDES_value('block_size'))//4 +1 and isinstance(int(check[0]),int):
        
        # print("Block size: ", len(R))
        struc = lines[len(R)-2]
        inf = struc[2:].strip('\n').split(',')
        row = 2
        col = int(len(inf)/2)
        array = []
        x = 0
        for r in range(row):
            array.append([])
            for c in range(col):
                array[r].append(inf[x])
                x+=1
        output = array[int(R[0])][utilities.bin_to_dec(R[1:])]
        sbox.close()
        return output
    elif len(R) != int(get_SDES_value('block_size'))//4 +1:
        print('Error(sbox1): invalid input',end='')
        return ''
    elif not isinstance(int(check[0]),int):
        print('Error(sbox1): undefined sbox1',end='')
        return ''
    else:
        print('Error(sbox1): undefined block size',end='')
        return ''

#-----------------------------------------------------------
# Parameters:   R (str): binary number of size (block_size//4)
# Return:       output (str): binary
# Description:  Validates that R is of size block_size//4 + 1
#               Retrieves relevant structure of sbox2 from sbox2File
#               Most significant bit of R is row number, other bits are column number
# Error:        if undefined block_size:
#                   print('Error(sbox2): undefined block size',end=''), return ''
#               if invalid R:
#                   print('Error(sbox2): invalid input',end=''),return ''
#               if no sbox1 structure exist:
#                   print('Error(sbox2): undefined sbox1',end=''),return ''
#-----------------------------------------------------------
def sbox2(R):
    block_size = int(get_SDES_value('block_size'))
    sbox = open(sbox2File, 'r')
    bi_bs = utilities.dec_to_bin(block_size, 10)
    check =lines[0]
    if R != '' and len(R) == int(get_SDES_value('block_size'))//4 +1 and isinstance(int(check[0]),int):
        lines = sbox.readlines()
        struc = lines[len(R)-2]
        inf = struc[2:].strip('\n').split(',')
        row = 2
        col = int(len(inf)/2)
        array = []
        x = 0
        for r in range(row):
            array.append([])
            for c in range(col):
                array[r].append(inf[x])
                x+=1
        output = array[int(R[0])][utilities.bin_to_dec(R[1:])]
        sbox.close()
        return output
    elif len(R) != int(get_SDES_value('block_size'))//4 +1:
        print('Error(sbox2): invalid input',end='')
        return ''
    elif not isinstance(int(check[0]),int):
        print('Error(sbox2): undefined sbox2',end='')
        return ''
    else:
        print('Error(sbox2): undefined block size',end='')
        return ''

#-----------------------------------------------------------
# Parameters:   Ri (str): block of binary numbers
#               ki (str): binary number representing subkey
# Return:       Ri2 (str): block of binary numbers
# Description:  Performs the following five tasks:
#               1- Pass the Ri block to the expander function
#               2- Xor the output of [1] with ki
#               3- Divide the output of [2] into two equal sub-blocks
#               4- Pass the most significant bits of [3] to Sbox1
#                  and least significant bits to sbox2
#               5- Conactenate the output of [4] as [sbox1][sbox2]
# Error:        if ki is an invalid binary number:
#                   print('Error(F): invalid key',end=''), return ''
#               if invalid Ri:
#                   print('Error(F): invalid input',end=''),return ''
#-----------------------------------------------------------   
def F(Ri,ki):
    if utilities.is_binary(ki) and len(Ri)%2 == 0 and len(ki)%2== 0:
        expander = expand(Ri)
        xor_output = utilities.xor(expander,ki)
        mid = len(xor_output)//2
        bx1 = xor_output[:mid]
        bx2 = xor_output[mid:]
        sx1 = sbox1(bx1)
        sx2 = sbox2(bx2)
        Ri2 = sx1+sx2
        return Ri2
    elif not utilities.is_binary(ki) or len(ki)%2!= 0:
        print('Error(F): invalid key',end='')
        return ''
    elif len(Ri)%2 != 0:
        print('Error(F): invalid input',end='')
        return ''
    

#-----------------------------------------------------------
# Parameters:   bi (str): block of binary numbers
#               ki (str): binary number representing subkey
# Return:       bi2 (str): block of binary numbers
# Description:  Applies Fiestel Cipher on a block of binary numbers
#               L(current) = R(previous)
#               R(current) = L(previous)xor F(R(previous), subkey)
# Error:        if ki is an invalid binary number or of invalid size
#                   print('Error(feistel): Invalid key',end=''), return ''
#               if invalid Ri:
#                   print('Error(feistel): Invalid block',end=''),return ''
#----------------------------------------------------------- 
def feistel(bi,ki):
    if len(bi)%2!= 0:
        print('Error(feistel): Invalid block',end='')
        return ''
    elif not utilities.is_binary(ki) or len(ki)%2!= 0:
        print('Error(feistel): Invalid key',end='')
        return ''
    else:
        # print(bi, ki)
        m = int(len(bi)//2)
        Li = bi[:m]
        Ri = bi[m:]
        Li1 = Ri 
        Ri1 = utilities.xor(Li, F(Ri,ki))
        bi2 = Li1 + Ri1
    return bi2

#----------------------------------
# SDES Encryption/Decryption
#----------------------------------
#-----------------------------------------------------------
# Parameters:   plaintext (str)
#               key (str)
# Return:       ciphertext (str)
# Description:  Encryption using Simple DES
#----------------------------------------------------------- 
def e_SDES(plaintext,key):

    ciphertext = ''

    if isinstance(plaintext, str) and plaintext != '':
        conf = get_SDES_config()
        k = get_SDES_value('key_size')
        r = get_SDES_value('rounds')
        e = get_SDES_value('encoding_type')
        b = get_SDES_value('block_size')
        p = get_SDES_value('p')
        q = get_SDES_value('q')
        if k!= '' and r != '' and e != '' and b !='':
            if key == '' and p!= '' and q !='':
                key = generate_key_SDES()
            if key!='' and int(k) == len(key):
                k = int(k)
                r = int(r)
                b = int(b)
                b6_base = utilities.get_B6Code()
                sv_undef = utilities.get_undefined(plaintext, b6_base)
                text = utilities.remove_undefined(plaintext, b6_base)
                blk_text = []
                while len(text)%2 != 0:
                    text+='Q'
                for i in range(0,len(text),2):
                    blk_text.append(text[i]+text[i+1])
                round = 0 
                enc_text = []
                for x in blk_text:
                    enc_text.append(encode(x[0],e)+encode(x[1],e))
                stream = ''

                for blocks in enc_text:
                    for rounds in range(r):
                        if rounds == 0:
                            rnd_text = blocks 
                        ki = get_subKey(key,rounds+1)
                        rnd_text = feistel(rnd_text, ki)
                        if rounds == r-1:
                            m = int(len(rnd_text)//2)
                            Li = rnd_text[:m]
                            Ri = rnd_text[m:]
                            rnd_text = Ri+Li    
                    stream += rnd_text
                ciphertext = ''
                for s in range(0, len(stream), b//2):
                    ciphertext+=decode(stream[s:s+b//2], e)
                ciphertext = utilities.insert_undefinedList(ciphertext, sv_undef)

            elif key!= '' and int(k) != len(key):
                print('Error(e_SDES): Invalid key')
                return ''
            elif key=='' and p == '' or q == '':
                print('Error(e_SDES): Invalid key')
                return ''
        else:
            print("Error(e_SDES): Invalid configuration")
            return ''
    else:
        print("Error(e_SDES): Invalid input")
        return ''
    return ciphertext

#-----------------------------------------------------------
# Parameters:   ciphertext (str)
#               key (str)
# Return:       plaintext (str)
# Description:  Decryption using Simple DES
#----------------------------------------------------------- 
def d_SDES(ciphertext,key):
    plaintexttext = ''

    if isinstance(ciphertext, str) and ciphertext != '':
        conf = get_SDES_config()
        k = get_SDES_value('key_size')
        r = get_SDES_value('rounds')
        e = get_SDES_value('encoding_type')
        b = get_SDES_value('block_size')
        p = get_SDES_value('p')
        q = get_SDES_value('q')
        if k!= '' and r != '' and e != '' and b !='':
            if key == '' and p!= '' and q !='':
                key = generate_key_SDES()
            if key!='' and int(k) == len(key):
                k = int(k)
                r = int(r)
                b = int(b)
                b6_base = utilities.get_B6Code()
                sv_undef = utilities.get_undefined(ciphertext, b6_base)
                text = utilities.remove_undefined(ciphertext, b6_base)
                blk_text = []
                while len(text)%2 != 0:
                    text+='Q'
                for i in range(0,len(text),2):
                    blk_text.append(text[i]+text[i+1])
                round = 0 
                enc_text = []
                for x in blk_text:
                    enc_text.append(encode(x[0],e)+encode(x[1],e))
                stream = ''

                for blocks in enc_text:
                    for rounds in range(r):
                        if rounds == 0:
                            rnd_text = blocks
                        ki = get_subKey(key,r-rounds)
                        rnd_text = feistel(rnd_text, ki)
                        if rounds == r-1:
                            m = int(len(rnd_text)//2)
                            Li = rnd_text[:m]
                            Ri = rnd_text[m:]
                            rnd_text = Ri+Li    
                    stream += rnd_text
                plaintext = ''
                for s in range(0, len(stream), b//2):
                    plaintext+=decode(stream[s:s+b//2], e)
                plaintext = utilities.insert_undefinedList(plaintext, sv_undef)
                plaintext = plaintext.strip('Q')

            elif key!= '' and int(k) != len(key):
                print('Error(d_SDES): Invalid key')
                return ''
            elif key=='' and p == '' or q == '':
                print('Error(d_SDES): Invalid key')
                return ''
        else:
            print("Error(d_SDES): Invalid configuration")
            return ''
    else:
        print("Error(d_SDES): Invalid input")
        return ''
    return plaintext
