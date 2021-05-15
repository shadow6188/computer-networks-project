import random
import hashlib

from Crypto.Util.number import isPrime


def gen_prime():
    # returns two  different prime numbers between 1 and 100
    primes = [i for i in range(1, 20) if isPrime(i)]
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
    # return p, q
    return 17, 23


def findModInverse(a, m):
    if greatest_common_denominator(a, m) != 1:
        print('error')
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def greatest_common_denominator(first, second):
    # uses euclid algorithm to get greatest common factor
    while second != 0:
        first, second = second, first % second
    return first


def co_prime_of(number):
    co_prime = random.randint(1, number)
    while greatest_common_denominator(number, co_prime) != 1:
        co_prime = random.randint(1, 100)
    return co_prime


def RSA():  # generates a private key and public key
    p, q = gen_prime()
    z = (p - 1) * (q - 1)
    n = p * q
    e = co_prime_of(z)
    d = findModInverse(e, z)
    if e * d % z != 1.0:
        print("something went wrong")
        print('got ', pow(e, d, z))
        return -1
    #print(e, d, z)
    return n, e, d  # d = private key, n, e = public key


def PublicKey(e, n, data):  # applying public key AKA encryption
    return pow(data, e, n)


def PrivateKey(d, n, encrypted):  # applying private key AKA decryption
    return pow(encrypted, d, n)


def PGPClient(data, n_server, e_server):
    secretKey = random
    hashMessage = hashlib.sha1(data)
    encrypted_hash = PublicKey(hashMessage)
    encrypted_key = PublicKey(n_server, e_server, secretKey)
    digital_sig = PrivateKey()
    # send shit here


def PGPServer(clientTransmission, ClientPublicKey):
    all_data = clientTransmission
    data = ClientPublicKey(all_data['digital_sig'])
    secret_key = PrivateKey(n, d, all_data['Encrypted_secret_key'])
    copy = data
    tmp_hashed_message = hash(copy)
    if tmp_hashed_message == hash_message:
        print()
    else:
        return

if __name__ == '__main__':
    #  testing out encryption and decryption by trying it out on a string
    nx, ex, dx = RSA()
    print(nx, ex, dx)
    string = "data"
    num = [ord(each) for each in string]
    print(string, " in unicode is ", num)
    encrypted = [PublicKey(nx, ex, ord(each)) for each in string]
    print("encrypted data is", encrypted)
    decrypt = [PrivateKey(nx, dx, each) for each in encrypted]

    print('decrypted', decrypt)

    print(''.join([chr(each) for each in decrypt]))
