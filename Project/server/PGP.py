import random

from Crypto.Util.number import isPrime


def gen_prime():
    # returns two  different prime numbers between 1 and 100
    primes = [i for i in range(11, 30) if isPrime(i)]
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
    return p, q


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
    co_prime = 2
    while greatest_common_denominator(number, co_prime) != 1:
        co_prime += 1
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
    return n, e, d  # d = private key, n, e = public key


def PublicKey(e, n, data):  # applying public key AKA encryption
    return (data ** e) % n


def encrypt_text(d, n, text):
    return [PublicKey(d, n, ord(each)) for each in text]


def PrivateKey(d, n, encrypted):  # applying private key AKA decryption
    return (encrypted ** d) % n


def decrypt_text(e, n, cipher):
    decrypt = [PrivateKey(e, n, each) for each in cipher]
    return ''.join([chr(each) for each in decrypt])


if __name__ == '__main__':
    #  testing out encryption and decryption by trying it out on a string
    nx, ex, dx = RSA()
    print(nx, ex, dx)
    string = "shit"
    encrypt = encrypt_text(dx, nx, string)

    print(encrypt)

    decrypt = decrypt_text(ex, nx, encrypt)

    altx = encrypt_text(ex, nx, decrypt)

    alt = decrypt_text(dx, nx, altx)
    print(decrypt)
    print(alt)
