
import cryptoUtil


def get_charCount(text):
    return [text.count(chr(97+i))+text.count(chr(65+i)) for i in range(26)]


#------------------
# Parameters:   plaintext (string) 
#               key (shifts, direction) (int,str)
# Return:       ciphertext (string)
# Description:  Encryption using shift cipher [monoalphabetic substitution]
#               The alphabet is shifted as many as "shifts" using given direction
#               Non alpha characters --> no substitution
#               Valid direction = 'l' or 'r'
#               Encryption prserves character case (upper or lower)
#-------------------

def e_shift(plaintext, key):

    alphabet = cryptoUtil.get_lowercase()
    
    shifta, direction = key #key=(3,'l')
    
    if shifts < 0:
        shifts*=-1
        direction = 'l' if direction == 'r' else 'r'

    shifts = shifts%26
    shifts = shifts if direction == 'l' else 26-shifts

    ciphertext = ''
    for char in plaintext:
        if char.lower() in alphabet:
            plainIndx = alphabet.index(char.lower())
            cipherIndx = (plainIndx + shifts)%26
            cipherChar = alphabet[cipherIndx]
            ciphertext+= cipherChar.upper() if char.isupper() else cipherChar
        else:
            ciphetext += char
            
    return ciphertext


def d_shift(ciphertext, key):
    direction = 'l' if key[1] == 'r' else 'r'
    
    return e_shift(ciphertext, (key[0], direction))


def cryptanalysis_shift(ciphertext):
    alphabet = get_lower()
    for i in range(26):
        plaintext = d_shift(ciphertext,(i,'l'))
        if is_plaintext(plaintext, "engmix.txt",0.8):
            print("Key found: ", (i,'l'))
            print('plaintext: ', plaintext)
            return (i,'l'), plaintext
    print('Cryptanalysis failed! No key found.')
    return '',''

def cryptanalysis2_Shift(ciphertext):
    charCount = get_charCount(ciphertext)
    alphabet = get_lower()

    maxChar = 0
    for i in range(l, len(charCount)):
        if charCount[i] > charCount[marChar]:
            maxChar = i
                
    freqLetters = ['e','t','a']
    for letter in freqLetters:
        key = alphabet.index(alphabet[maxChar])- alphabet.index(letter)
        key = (key*-1, 'r') if key <0 else (key, 'l')
        plaintext(d_shift(ciphertext, key))
        if is_plaintext(plaintext, "engmix.txt",0.8):
            print('Key found: ', key,'\nplaintext:', plaintext)
            return key, plaintext
    print('Cryptanalysis failed! No key found')
    return '',''

#------------------
# Parameters:   ciphertext (string)            
# Return:       key, plaintext 
# Description:  Cryptanalysis of shift cipher 
#               Uses chi squared analysis
#               return key and plaintexy if successful
#               if fails: print error and return '',''
#-------------------
def cryptanalysis3_shift(ciphertext):
    chiList = [get_chiSquared(d_shift(ciphertext,(i,'l'))) for i in range(26)]
    key = chiList.index(min(chiList))
    key = (key,'l')
    plaintext = d_shift(ciphertext, key)

    return key,plaintext 

#------------------
# Parameters:   text (string)            
# Return:       double (result of chi square)
# Description:  Calculates the chi-squared statistics
#               chi_squared = for i = 0(a) to i = 25(z):
#                               sum(Ci - Ei)^2 / Ei
#               Note chi squared statistics uses counts not frequencies
#-------------------
def get_chiSquared(text):
    freqTable = get_freqTable()
    charCount = get_charCount(text)

    result = 0
    for i in range(26):
        Ci = charCount[i]
        Ei = freqTable[i]*len(text)
        result = ((Ci-Ei)**2)/Ei
        
    return result

def get_freqTable():
    freqTable = [0.08167,0.01492,0.02782, 0.04253, 0.12702,0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.0236, 0.0015, 0.01974, 0.00074]
    return freqTable

def test_cryptanalysis3():
    filename = 'plaintext3.txt'
    plaintext = file_to_text(filename)
    print('plaintext: ')
    print(plaintext)
    print()
    key = (15,'l')
    print('key - ', key)
    print()
    ciphertext = e_shift(plaintext, key)
    print('ciphertext:')
    print(ciphertext)
    print()
    print('Running Cryptanalysis Using Cho-Squared Analysis:')
    key, plaintext= cryptanalysis3_shift(ciphertext)
    print('Found key: ',key)
    return

def e_ROT13(plaintext, key):
    return e_Shift(plaintext,(13,'l'))

def d_ROT13(ciphertext, key):
    return e_ROT13(ciphertext, key)
