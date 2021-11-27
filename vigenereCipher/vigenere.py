import string


def vigenere_encrypt(message, key):
    table = list(string.printable)
    # print("KEY:", key)
    # print(message)
    keyString = extendKey(message, key)
    # print(keyString)

    encrypted = ""
    for i in range(0, len(message)):
        mLetter = message[i]
        kLetter = keyString[i]
        mIndex = table.index(mLetter)
        kIndex = table.index(kLetter)
        index = (mIndex + kIndex) % len(table)
        encrypted += table[index]

   # print(encrypted)
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

    # print(decrypted)
    return decrypted


def extendKey(message, key):
    keyString = ""
    for i in range(0, len(message)):
        keyString += key[i % len(key)]

    return keyString


def vigenere_encrypt_file_inputted(key):
    file_path = input("File path to txt file: ")
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


if __name__ == '__main__':
    msg = "Reed is cool"
    k = "asf12e34224vssavs"
    encrypted_message = vigenere_encrypt_file_inputted(k)
    decrypted = vigenere_decrypt_from_file(k)
