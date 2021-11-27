from DES_encrypt import *

#Generates a file cipher.txt which contains the ciphertext 
cipher = DES_encrypt('plaintext.txt', 'key1.txt', 'cipher.txt')
print('Cipher: ', cipher)

#Generates a file dPlaintext.txt which contains the decrypted plaintext
dplaintext = DES_decrypt('cipher.txt', 'key1.txt', 'dPlaintext.txt')
print('Decrypted Ciphertext: ', dplaintext)
