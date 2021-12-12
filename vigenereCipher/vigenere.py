import string
import base64

def vigenere_encrypt(message, key):
    table = list(string.printable)
    keyString = extendKey(message, key)
    encrypted = ""
    for i in range(0, len(message)):
        mLetter = message[i]
        kLetter = keyString[i]
        mIndex = table.index(mLetter)
        kIndex = table.index(kLetter)
        index = (mIndex + kIndex) % len(table)
        encrypted += table[index]
    return encrypted


def vigenere_decrypt(message, key):
    table = list(string.printable)
    keyString = extendKey(message, key)
    decrypted = ""
    for i in range(0, len(message)):
        mLetter = message[i]
        kLetter = keyString[i]
        mIndex = table.index(mLetter)
        kIndex = table.index(kLetter)
        index = (mIndex - kIndex) % len(table)
        decrypted += table[index]
    return decrypted


def extendKey(message, key):
    keyString = ""
    for i in range(0, len(message)):
        keyString += key[i % len(key)]

    return keyString


def vigenere_encrypt_file_inputted(key):
    file_path = 'vigenereCipher/encrypted.txt'
    try:
        file = open(file_path, 'r+')
        file2 = open("encrypted.txt", 'w')
        data = file.read()
        encrypted = vigenere_encrypt(data, key)
        file2.write(encrypted)
        return encrypted
    except Exception as e:
        print("CANNOT READ THE FILE AT GIVEN PATH")
        print(e)


def vigenere_encrypt_file(key, file_path):
    try:
        file = open(file_path, 'r+')
        file2 = open("encrypted.txt", 'w')
        data = file.read()
        encrypted = vigenere_encrypt(data, key)
        file2.write(encrypted)
        return encrypted
    except Exception as e:
        print("CANNOT READ THE FILE AT GIVEN PATH")
        print(e)


def vigenere_decrypt_to_file(key, message):
    file = open("decrypted.txt", 'w')
    decrypted = vigenere_decrypt(message, key)
    file.write(decrypted)
    return decrypted


def vigenere_decrypt_from_file(key):
    file_e = open("encrypted.txt", 'r+')
    file_d = open("decrypted.txt", 'w')
    message = file_e.read()
    decrypted = vigenere_decrypt(message, key)
    file_d.write(decrypted)
    return decrypted

#print(vigenere_decrypt(vigenere_encrypt('message', 'testkey'), 'testkey'))


def encrypt_jpg(img_string, key):
    #image = open(path, 'rb')
    #raw = image.read()

    #to_64 = base64.encodebytes(raw)
    #print(to_64)
    #img_string = to_64.decode("ascii")

    #file_image = open("img.txt", 'w')
    #file_image.write(img_string)

    encrypted = vigenere_encrypt(img_string, key)

   # file_encrypted = open("vigenereCipher/encrypted.txt", 'w')
   # file_encrypted.write(encrypted)
    return encrypted


def decrypt_to_jpg_from_file(key):
    decrypted = vigenere_decrypt_from_file(key)
    string_to_64 = decrypted.encode("ascii")
    decode = base64.decodebytes(string_to_64)

    decrypted_image = open('decrypted_from_file.jpg', 'wb')
    decrypted_image.write(decode)
    return decode


def decrypt_to_jpg(message, key):
    decrypted = vigenere_decrypt(message, key)
    #print(decrypted)
    string_to_64 = decrypted.encode("ascii")
    decode = base64.decodebytes(string_to_64)

    decrypted_image = open('vigenereCipher/decrypted.jpg', 'wb')
    decrypted_image.write(decode)
    decrypted_image.close()
    return decode


#message = encrypt_jpg('/home/thomas/Documents/Projects/csds344/vigenereCipher/example.jpg', 'testkey')
#decrypt_to_jpg(message, 'testkey')