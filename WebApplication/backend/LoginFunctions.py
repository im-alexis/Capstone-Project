#AWPS: Backend
# Home of Login related Operations:
#   1) /(login)
#   2) /create_user
#   3) /forgot_password
#   4) Encryption


# USER VALIDATION
def encrypt(passw):
    encrypt = ""
    for char in passw:
        newC = char
        if ord(newC) - 13 < 34:
            newC = chr(127 - (34 - (ord(newC) - 13)))
        else:
            newC = chr(ord(char) - 13)
        encrypt += newC
    return encrypt[::-1]


def decrypt(passw):
    decrypt = ""
    for char in passw:
        newC = char
        if ord(newC) + 13 > 126:
            newC = chr(33 + ord(newC) - 126 + 13)
        else:
            newC = chr(ord(char) + 13)
        decrypt += newC
    return decrypt[::-1]
