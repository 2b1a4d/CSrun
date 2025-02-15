import random


# 无第三方库的RSA算法的实现


# 欧几里得算法，取最大公约数
def gcd(a: int, b: int) -> int:
    if a < b:
        a, b = b, a
    while b:
        a, b = b, a % b
    return a


# Miller-Rabin素性测试，判断是否为质数
def is_prime(n: int) -> bool:
    d = n - 1
    r = 0
    while not (d & 1):
        r += 1
        d >>= 1

    for _ in range(5):
        a = random.randint(2, n - 2)

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False

    return True


# 扩展欧几里得算法，计算模逆元
def extended_euclid(a: int, m: int) -> int:
    x = 0
    y = 1
    om = m
    while m != 0:
        q = a // m
        (a, m) = (m, a % m)
        (x, y) = ((y - (q * x)), x)
    if y < 0:
        y += om
    return y


# 生成一个多少比特的质数
def prime_generate(key_size: int) -> int:
    size = key_size // 2
    # 密钥大小的一半，两个质数乘起来为密钥大小
    key_min = pow(2, size - 1)
    key_max = pow(2, size)
    while True:
        num = random.randrange(key_min, key_max)
        # 取为偶数
        num = num | 1
        if is_prime(num):
            return num


# 生成公钥和私钥
def key_generate(p: int, q: int):
    t = (p - 1) * (q - 1)
    # 一般为65537，这里随机
    e = random.randint(1, t)
    while gcd(e, t) != 1:
        e = random.randint(1, t)
    n = p * q
    d = extended_euclid(e, t)
    return n, e, d


# 加密
def encrypt(message: int, e: int, n: int) -> int:
    ciphertext = pow(message, e, n)
    return ciphertext


# 解密
def decrypt(ciphertext: int, d: int, n: int) -> int:
    plaintext = pow(ciphertext, d, n)
    return plaintext
