import hashlib


def jacobi_symbol(a, b):
    """
    Calculates the Jacobi symbol of a with respect to b.
    Assumes that b is an odd positive integer.
    """
    assert b % 2 == 1 and b > 0, "b must be an odd positive integer"

    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if b % 8 in [3, 5]:
                result = -result
        a, b = b, a
        if a % 4 == b % 4 == 3:
            result = -result
        a %= b
    if b == 1:
        return result
    else:
        return 0


def jacobi2(a, b):
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        b8 = b % 8
        if b8 == 3 or b8 == 5:
            return -1
        else:
            return 1
    if a % 2 == 0:
        return jacobi2(2, b)*jacobi2(a//2, b)
    if a >= b:
        return jacobi2(a % b, b)
    if a % 4 == 3 and b % 4 == 3:
        return -jacobi2(b, a)
    else:
        return jacobi2(b, a)


def hashIdentity(identityString, MPK):
    hashNum = int(hashlib.sha256(
        identityString.encode('utf-8')).hexdigest(), 16) % MPK
    jacobiNumber = jacobi_symbol(hashNum % MPK, MPK)
    while (jacobiNumber != 1):
        hashNum = int(hashlib.sha256(
            str(hashNum).encode('utf-8')).hexdigest(), 16) % MPK
        jacobiNumber = jacobi_symbol(hashNum, MPK)
    return hashNum


def mod_inverse(a, m):
    """
    Calculates the modular inverse of a modulo m.

    Parameters:
    a (int): The number to calculate the inverse of.
    m (int): The modulus.

    Returns:
    The modular inverse of a modulo m, or None if it does not exist.
    """
    # Check if gcd(a, m) = 1, otherwise the inverse does not exist
    gcd, x, y = extended_euclidean_algorithm(a, m)
    if gcd != 1:
        return None

    # Calculate the inverse using the extended Euclidean algorithm
    return (x % m + m) % m


def extended_euclidean_algorithm(a, b):
    """
    Calculates the greatest common divisor (gcd) of a and b, as well as the
    Bezout coefficients x and y such that ax + by = gcd(a, b).

    Parameters:
    a (int): The first number.
    b (int): The second number.

    Returns:
    A tuple (gcd, x, y) such that ax + by = gcd(a, b).
    """
    # Base case
    if a == 0:
        return (b, 0, 1)

    # Recursive call
    gcd, x1, y1 = extended_euclidean_algorithm(b % a, a)

    # Calculate the Bezout coefficients
    x = y1 - (b // a) * x1
    y = x1

    return (gcd, x, y)


if __name__ == "__main__":
    P = 4095731
    Q = 5895079
    a = 16999610644564
    b = 19953850441984
    print(jacobi2(a, P))
    print(jacobi2(a, P*Q))
    print(jacobi2(a, Q))
    print(jacobi2(b, P))
    print(jacobi2(b, P*Q))
    print(jacobi2(b, Q))
